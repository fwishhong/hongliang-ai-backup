#!/usr/bin/env python3
"""
备份 hongliang@kongzhong.com 中与 me@yewhan.com 的往来邮件
"""

import imaplib
import email as email_module
from email.header import decode_header
import html2text
import os, sys, re, json
from datetime import datetime
from dateutil import parser as dateutil_parser
import time, signal

# ============ 配置 ============
IMAP_HOST = "imap.exmail.qq.com"
IMAP_PORT = 993
USERNAME  = "hongliang@kongzhong.com"
PASSWORD  = "DkaK4yzZcrMfJxT2"
TARGET    = "me@yewhan.com"

OUTPUT_BASE = os.path.expanduser("~/.openclaw/workspace/email_backups/yewhan_com")
os.makedirs(OUTPUT_BASE, exist_ok=True)

# ============ 工具 ============

def decode_str(s):
    if s is None: return ""
    if hasattr(s, 'encode') and not isinstance(s, str): s = str(s)
    if not isinstance(s, str): return ""
    parts = decode_header(s)
    result = []
    for part, charset in parts:
        if isinstance(part, bytes):
            try: result.append(part.decode(charset or "utf-8", errors="replace"))
            except: result.append(part.decode("utf-8", errors="replace"))
        else: result.append(part)
    return "".join(result)

def get_date(msg):
    try: return dateutil_parser.parse(msg.get("Date",""))
    except: return datetime.now()

def extract_emails(hdr):
    if not hdr: return []
    return [e.lower() for e in re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', str(hdr))]

def is_relevant(msg):
    for h in ["From","To","Cc","Bcc"]:
        if TARGET.lower() in extract_emails(msg.get(h,"")): return True
    return False

def get_body(msg):
    body, html = "", ""
    if msg.is_multipart():
        for p in msg.walk():
            ct,pisp = p.get_content_type(), str(p.get("Content-Disposition",""))
            if "attachment" in pisp: continue
            cs = p.get_content_charset() or "utf-8"
            pl = p.get_payload(decode=True)
            if not pl: continue
            try: text = pl.decode(cs, errors="replace")
            except: continue
            if ct=="text/plain" and not body: body = text
            elif ct=="text/html" and not html: html = text
    else:
        ct,cs,pl = msg.get_content_type(), msg.get_content_charset() or "utf-8", msg.get_payload(decode=True)
        if pl:
            try: text = pl.decode(cs, errors="replace")
            except: pass
            else:
                if ct=="text/html": html = text
                else: body = text
    if body.strip(): return body.strip(), "text"
    if html:
        h = html2text.HTML2Text(); h.ignore_links=False; h.body_width=0
        return h.handle(html).strip(), "html"
    return "", "none"

def save_attachments(msg, ddir):
    atts, seen = [], {}
    for p in msg.walk():
        disp = str(p.get("Content-Disposition",""))
        if "attachment" not in disp: continue
        fn = decode_str(p.get_filename())
        if not fn: continue
        if fn in seen: seen[fn]+=1; name,ext=os.path.splitext(fn); fn=f"{name}_{seen[fn]}{ext}"
        else: seen[fn]=0
        fn = re.sub(r'[<>:"/\\|?*]','_', fn)
        with open(os.path.join(ddir,fn),"wb") as f: f.write(p.get_payload(decode=True))
        atts.append(fn)
    return atts

def make_md(msg, body, btype, atts):
    lines=[f"# {decode_str(msg.get('Subject','(无主题)'))}","",
           f"**发件人:** {decode_str(msg.get('From',''))}",
           f"**收件人:** {decode_str(msg.get('To',''))}"]
    cc=msg.get("Cc","")
    if cc and str(cc).strip(): lines.append(f"**抄送:** {decode_str(cc)}")
    bcc=msg.get("Bcc","")
    if bcc and str(bcc).strip(): lines.append(f"**密送:** {decode_str(bcc)}")
    lines += [f"**日期:** {msg.get('Date','')}"]
    mid=msg.get("Message-ID","")
    if mid: lines.append(f"**Message-ID:** {mid}")
    lines += ["","---",""]
    if body: lines += [f"**正文类型:** {btype}","", body]
    else: lines.append("*（正文为空）*")
    if atts:
        lines += ["","---","","## 附件"]
        for a in atts: lines.append(f"- {a}")
    return "\n".join(line for line in lines if line)

def parse_folder_name(line):
    """从 LIST response 行提取文件夹名"""
    m = re.search(r'"([^"]+)"\s*$', line)
    if m: return m.group(1)
    parts = line.strip().split()
    return parts[-1].strip('"') if parts else None

# ============ 主流程 ============

def main():
    print(f"📧 连接 {IMAP_HOST}:{IMAP_PORT} ...")
    # 忽略 SIGPIPE
    signal.signal(signal.SIGPIPE, signal.SIG_IGN)

    try:
        mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, timeout=30)
        mail.login(USERNAME, PASSWORD)
        print("✅ 登录成功")
    except Exception as e:
        print(f"❌ 登录失败: {e}"); sys.exit(1)

    # 解析所有文件夹
    status, raw_folders = mail.list()
    folder_names = []
    for f in raw_folders:
        line = f.decode("utf-8", errors="replace")
        name = parse_folder_name(line)
        if name: folder_names.append(name)
    print(f"📂 文件夹: {folder_names}\n")

    # 文件夹别名（处理带空格的文件名需要加引号）
    folder_select_name = {
        "Sent Messages": '"Sent Messages"',
        "Deleted Messages": '"Deleted Messages"',
    }

    all_msgs = []
    start_time = time.time()

    for fname in folder_names:
        # 选择要 select 的名称
        select_name = folder_select_name.get(fname, fname)

        print(f"📂 {fname}", end="", flush=True)
        try:
            st, dat = mail.select(select_name, readonly=True)
            if st != "OK" or not dat:
                print(" ⚠️ 无法访问"); continue
            count = int(dat[0])
            if count == 0: print(" (0 封)"); continue
        except Exception as e:
            print(f" ⚠️ {e}"); continue

        st, mids = mail.search(None, "ALL")
        if st != "OK" or not mids[0]: print(" (无邮件)"); continue
        ids = mids[0].split()
        print(f"  {count} 封...", end="", flush=True)

        prev_relevant_count = len(all_msgs)
        batch_progress = max(1, len(ids) // 10)

        for i, uid in enumerate(ids):
            try:
                typ, data = mail.fetch(uid, '(RFC822)')
                if typ != 'OK' or not isinstance(data[0], tuple):
                    time.sleep(0.3)
                    typ, data = mail.fetch(uid, '(RFC822)')
                if typ == 'OK' and isinstance(data[0], tuple):
                    msg = email_module.message_from_bytes(data[0][1])
                    if is_relevant(msg):
                        all_msgs.append((fname, msg))
            except imaplib.IMAP4.abort as e:
                time.sleep(1)  # 服务器异常，暂停1秒后继续
            except Exception:
                pass

            if (i+1) % batch_progress == 0:
                pct = int((i+1)/len(ids)*100)
                print(f" {pct}%", end="", flush=True)

        new_relevant = len(all_msgs) - prev_relevant_count
        print(f" ✅ (找到 {new_relevant} 相关 / 共 {len(all_msgs)})")

    print(f"\n🎯 共找到 {len(all_msgs)} 封相关邮件\n")
    elapsed = time.time() - start_time
    print(f"⏱️  邮件抓取耗时: {elapsed:.0f}s ({len(all_msgs)/elapsed:.1f} 封/s)\n")

    if not all_msgs:
        print("无相关邮件，退出。"); mail.logout(); sys.exit(0)

    # 按日期分组
    by_date = {}
    for fname, msg in all_msgs:
        dk = get_date(msg).strftime("%Y-%m-%d")
        by_date.setdefault(dk, []).append((fname, msg))

    for dk in sorted(by_date):
        ddir = os.path.join(OUTPUT_BASE, dk)
        os.makedirs(ddir, exist_ok=True)
        print(f"📅 {dk} ({len(by_date[dk])} 封)")
        for i, (fname, msg) in enumerate(by_date[dk]):
            i += 1
            atts = save_attachments(msg, ddir)
            body, btype = get_body(msg)
            subj = decode_str(msg.get("Subject","无主题"))
            safe = re.sub(r'[<>:"/\\|?*]','_', subj)[:50]
            with open(os.path.join(ddir, f"{i:03d}_{safe}.md"), "w", encoding="utf-8") as f:
                f.write(make_md(msg, body, btype, atts))
            print(f"  [{i}/{len(by_date[dk])}] ✅ {subj[:60]}")

    total_elapsed = time.time() - start_time
    index = {"target_email":TARGET,"total":len(all_msgs),"days":len(by_date),
             "account":USERNAME,"date_ranges":sorted(by_date.keys()),
             "backup_time":datetime.now().isoformat(),
             "elapsed_seconds": round(total_elapsed, 1)}
    with open(os.path.join(OUTPUT_BASE,"_index.json"),"w",encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 完成！{len(all_msgs)} 封邮件 → {OUTPUT_BASE}")
    print(f"⏱️  总耗时: {total_elapsed:.0f}s")
    mail.logout()

if __name__ == "__main__":
    main()