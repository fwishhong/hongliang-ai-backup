#!/usr/bin/env python3
"""QQ Enterprise Email browser automation - QR scan + export"""
from playwright.sync_api import sync_playwright
import time, json, os

OUT_DIR = '/Users/hongliang/.openclaw/workspace/email_backups/yewhan_com'
COOKIES_FILE = f'{OUT_DIR}/_cookies_wechat.json'
SID_FILE = f'{OUT_DIR}/_sid.json'

def save_cookies(context):
    with open(COOKIES_FILE, 'w') as f:
        json.dump(context.cookies(), f)
    print(f"Saved {len(context.cookies())} cookies to {COOKIES_FILE}")

def save_sid(page):
    for frame in page.frames:
        url = frame.url
        if 'sid=' in url:
            import re
            m = re.search(r'sid=([^,&]+)', url)
            if m:
                sid = m.group(1)
                with open(SID_FILE, 'w') as f:
                    json.dump({'sid': sid}, f)
                print(f"Saved SID: {sid}")
                return sid
    return None

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        args=['--disable-blink-features=AutomationControlled']
    )
    context = browser.new_context(
        viewport={'width': 1280, 'height': 900},
        locale='zh-CN',
        timezone_id='Asia/Shanghai',
        extra_http_headers={'Accept-Language': 'zh-CN,zh;q=0.9'}
    )
    
    page = context.new_page()
    page.goto('https://exmail.qq.com/', timeout=20000)
    time.sleep(2)
    
    print("=" * 50)
    print("扫码登录 QQ 企业邮箱")
    print("=" * 50)
    print("请用企业微信扫码登录...")
    print("Waiting for QR scan...")
    
    # Wait for the page to load and show QR code
    # Try to detect when user scans
    for attempt in range(60):  # 60 * 2s = 2 minutes
        time.sleep(2)
        # Check if logged in by looking at URL or page content
        url = page.url
        title = page.title()
        body_text = page.inner_text('body')[:200] if page.inner_text('body') else ''
        
        if 'mail_list' in url or 'today' in url or 'folderlist' in url:
            print(f"\n✓ Logged in! URL: {url[:80]}")
            save_cookies(context)
            save_sid(page)
            
            # Print frame structure
            print("\nFrame structure:")
            for fr in page.frames:
                print(f"  [{fr.name}] {fr.url[:80]}")
            
            break
        
        # Check for "验证" or login error
        if '验证' in body_text or '异常' in body_text:
            print(f"Page shows verification: {body_text[:100]}")
        
        if attempt % 10 == 0:
            print(f"  ... waiting for scan (attempt {attempt}/60), URL: {url[:60]}")
    
    else:
        print("Timeout waiting for QR scan!")
    
    print("\nDone - browser will stay open. Close manually.")
    print("Press Ctrl+C to stop")
    
    # Keep browser open
    import time
    while True:
        time.sleep(1)