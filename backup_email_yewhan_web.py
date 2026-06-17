#!/usr/bin/env python3
"""
QQ企业邮箱 + me@yewhan.com 往来邮件抓取
扫码登录版（用户扫企业微信二维码）
"""

import asyncio
import os, re, json, time
from datetime import datetime
from playwright.async_api import async_playwright

ACCOUNT = "hongliang@kongzhong.com"
PASSWORD = "DkaK4yzZcrMfJxT2"
TARGET = "me@yewhan.com"

OUTPUT_BASE = os.path.expanduser("~/.openclaw/workspace/email_backups/yewhan_com")
os.makedirs(OUTPUT_BASE, exist_ok=True)
SCREENSHOT_DIR = os.path.join(OUTPUT_BASE, "_debug_screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def clean_filename(s, max_len=50):
    s = re.sub(r'[<>:"/\\|?*]', '_', s)
    s = re.sub(r'\s+', '_', s)
    return s[:max_len]

async def screenshot(page, name):
    await page.screenshot(path=os.path.join(SCREENSHOT_DIR, f"{name}.png"))

async def wait_for_login(page, timeout=120):
    """等待用户扫码登录完成"""
    print("=" * 50)
    print("📱 请用企业微信扫码登录！")
    print("   （在打开的浏览器窗口中扫码）")
    print("=" * 50)

    start = time.time()
    last_check = 0

    while time.time() - start < timeout:
        await asyncio.sleep(2)
        url = page.url

        # 检测登录成功 - URL 变了，不再是 login 页面
        if "login" not in url.lower():
            elapsed = time.time() - start
            print(f"\n✅ 登录成功！({elapsed:.0f}秒)")
            print(f"   URL: {url}")
            return True

        # 每10秒报告一次等待状态
        if time.time() - last_check >= 10:
            last_check = time.time()
            elapsed = int(time.time() - start)
            print(f"   ⏳ 等待中... ({elapsed}秒)")

    print("\n❌ 扫码登录超时")
    return False


async def get_search_count(page):
    body = await page.inner_text("body")
    for pat in [r'查找到[^0-9]*(\d+)[^0-9]*封', r'找到[^0-9]*(\d+)[^0-9]*封']:
        m = re.search(pat, body)
        if m:
            return int(m.group(1))
    return 0


async def get_email_links(page):
    links = []
    for sel in ["tr[class*='mailitem']", "tr[class*='mail_list']",
                "div[class*='mail_item']"]:
        items = await page.query_selector_all(sel)
        for item in items:
            try:
                a = await item.query_selector("a[href*='read']")
                if not a:
                    a = await item.query_selector("a")
                if a:
                    href = await a.get_attribute("href")
                    if href:
                        links.append(href)
            except:
                pass

    if not links:
        all_a = await page.query_selector_all("a")
        for a in all_a:
            href = await a.get_attribute("href") or ""
            if "read" in href and "exmail" in href:
                links.append(href)

    seen = set()
    return [l for l in links if l not in seen and not seen.add(l)]


async def extract_email(page):
    data = {}
    for sel, key in [("[class*='from']", 'from'), ("[class*='subject']", 'subject'),
                      ("[class*='date']", 'date'), ("[class*='to']", 'to'),
                      ("[class*='cc']", 'cc')]:
        try:
            el = await page.wait_for_selector(sel, timeout=3000)
            data[key] = (await el.inner_text()).strip()
        except:
            data[key] = ''

    for sel in ["[class*='content']", "#content"]:
        try:
            el = await page.wait_for_selector(sel, timeout=3000)
            data['body'] = (await el.inner_text()).strip()
            break
        except:
            data['body'] = ''

    atts = await page.query_selector_all("a[href*='attach'], a[href*='download']")
    data['attachments'] = []
    for a in atts:
        name = (await a.inner_text()).strip()
        href = await a.get_attribute("href")
        if name and href:
            data['attachments'].append({'name': name, 'href': href})

    return data


async def main():
    print("=" * 60)
    print("📧 QQ企业邮箱 + me@yewhan.com 邮件抓取")
    print("   方式: 扫码登录（企业微信）")
    print("=" * 60)

    async with async_playwright() as p:
        # 可见浏览器，这样才能扫码
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={"width": 900, "height": 700},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        # 打开登录页
        await page.goto("https://exmail.qq.com/login", timeout=20000)
        await page.wait_for_load_state("domcontentloaded", timeout=15000)
        await asyncio.sleep(2)

        print("\n🔐 等待扫码...")

        # 等待用户扫码
        ok = await wait_for_login(page, timeout=180)
        if not ok:
            print("❌ 登录超时，请重试")
            await browser.close()
            return

        await screenshot(page, "00_logged_in")

        # 保存 cookies 方便以后复用
        cookies = await context.cookies()
        with open(os.path.join(OUTPUT_BASE, "_cookies.json"), 'w') as f:
            json.dump(cookies, f, ensure_ascii=False)
        print("  💾 Cookies 已保存")

        # 前往搜索
        print("\n🔍 打开搜索页面...")
        await page.goto(
            f"https://exmail.qq.com/cgi-bin/search?action=advanced&t=search_index.html&keyword={TARGET}",
            timeout=20000
        )
        await asyncio.sleep(3)
        await screenshot(page, "01_search_page")

        total = await get_search_count(page)
        print(f"\n📊 搜索结果: {total} 封")

        if total == 0:
            body = await page.inner_text("body")
            print(f"  页面内容前300字: {body[:300]}")
            await browser.close()
            return

        all_email_data = []
        processed = set()
        page_num = 1

        while True:
            print(f"\n--- 第 {page_num} 页 ---")
            links = await get_email_links(page)
            new_links = [l for l in links if l not in processed]
            print(f"  {len(new_links)} 个新邮件")

            for i, link in enumerate(new_links):
                print(f"  [{i+1}/{len(new_links)}] ", end="", flush=True)
                processed.add(link)

                try:
                    url = link if link.startswith('http') else "https://exmail.qq.com" + link
                    await page.goto(url, timeout=20000)
                    await page.wait_for_load_state("domcontentloaded", timeout=10000)
                    await asyncio.sleep(1)

                    data = await extract_email(page)
                    subject = data.get('subject', '无主题') or '无主题'
                    print(f"✅ {subject[:50]}")

                    date_str = data.get('date', '')
                    try:
                        from email.utils import parsedate_to_datetime
                        dt = parsedate_to_datetime(date_str) if date_str else datetime.now()
                        date_key = dt.strftime("%Y-%m-%d")
                    except:
                        date_key = datetime.now().strftime("%Y-%m-%d")

                    ddir = os.path.join(OUTPUT_BASE, date_key)
                    os.makedirs(ddir, exist_ok=True)

                    # 下载附件
                    att_names = []
                    for att in data.get('attachments', []):
                        fn = clean_filename(att['name'])
                        if not fn:
                            continue
                        href = att['href']
                        if href.startswith('/'):
                            href = "https://exmail.qq.com" + href
                        try:
                            async with context.request.fetch(href) as resp:
                                if resp.status == 200:
                                    with open(os.path.join(ddir, fn), 'wb') as f:
                                        f.write(await resp.body())
                                    att_names.append(fn)
                        except:
                            pass

                    # 写 md
                    counter = len(all_email_data) + 1
                    with open(os.path.join(ddir, f"{counter:04d}_{clean_filename(subject[:50])}.md"), 'w', encoding='utf-8') as f:
                        f.write(f"# {subject}\n\n")
                        f.write(f"**发件人:** {data.get('from', '')}\n")
                        f.write(f"**收件人:** {data.get('to', '')}\n")
                        if data.get('cc'):
                            f.write(f"**抄送:** {data.get('cc', '')}\n")
                        f.write(f"**日期:** {date_str}\n\n")
                        f.write("---\n\n")
                        f.write(data.get('body', '*（正文为空）*'))
                        if att_names:
                            f.write("\n\n---\n\n## 附件\n")
                            for a in att_names:
                                f.write(f"- {a}\n")

                    all_email_data.append(data)

                except Exception as e:
                    print(f"❌ {e}")

            # 下一页
            next_btn = None
            for sel in ["a[class*='next']", "#nextPage"]:
                try:
                    btn = await page.query_selector(sel)
                    if btn and await btn.get_attribute("disabled") is None:
                        next_btn = btn
                        break
                except:
                    pass

            if next_btn:
                print(f"  → 下一页")
                await next_btn.click()
                await asyncio.sleep(2)
                page_num += 1
            else:
                print("  📭 没有更多页面")
                break

        elapsed = time.time()
        index = {"target_email": TARGET, "total": len(all_email_data),
                 "account": ACCOUNT, "backup_time": datetime.now().isoformat()}
        with open(os.path.join(OUTPUT_BASE, "_index.json"), 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)

        print(f"\n🎉 完成！{len(all_email_data)} 封 → {OUTPUT_BASE}")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())