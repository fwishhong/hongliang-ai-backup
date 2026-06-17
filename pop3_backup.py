#!/usr/bin/env python3
"""Download all emails involving yewhan via POP3"""
import poplib, socket, email as email_module, os, json, time, re
from email.header import decode_header
from email.utils import parsedate_to_datetime

HOST = 'pop.exmail.qq.com'
PORT = 995
ACCOUNT = 'hongliang@kongzhong.com'
PASSWORD = 'DkaK4yzZcrMfJxT2'
TARGET = 'me@yewhan.com'
OUT_DIR = '/Users/hongliang/.openclaw/workspace/email_backups/yewhan_com/mail_pop3'
INDEX_FILE = '/Users/hongliang/.openclaw/workspace/email_backups/yewhan_com/_index_pop3.json'

def ds(s):
    if not s: return ''
    parts = decode_header(s)
    r = []
    for p, c in parts:
        if isinstance(p, bytes): r.append(p.decode(c or 'utf-8', errors='replace'))
        else: r.append(p)
    return ''.join(r)

def make_fn(date_str, subject, seq):
    safe = re.sub(r'[^\w\u4e00-\u9fff,-. ]', '', subject)[:40].strip().replace(' ', '-')
    return f"{date_str}_{seq}_{safe}.md"

socket.setdefaulttimeout(20)
mail = poplib.POP3_SSL(HOST, PORT)
mail.user(ACCOUNT)
mail.pass_(PASSWORD)
print(f'POP3 connected: {mail.stat()[0]} messages')

stat = mail.stat()
yewhan_msgs = []
print('Scanning all messages...')
start = time.time()
for i in range(1, stat[0]+1):
    try:
        _, lines, _ = mail.retr(i)
        raw = b'\n'.join(lines)
        msg = email_module.message_from_bytes(raw)
        frm = ds(msg.get('From', ''))
        to = ds(msg.get('To', ''))
        if 'yewhan' in frm.lower() or 'yewhan' in to.lower():
            subj = ds(msg.get('Subject', ''))
            date_hdr = msg.get('Date', '')
            try: dt = parsedate_to_datetime(date_hdr)
            except: dt = None
            date_str = dt.strftime('%Y-%m-%d') if dt else 'unknown-date'
            yewhan_msgs.append({'seq': i, 'from': frm, 'to': to, 'subject': subj, 'date': date_hdr, 'date_str': date_str})
            print(f'  msg {i}: {frm[:50]} → {subj[:50]}')
    except Exception as e:
        pass
    if i % 40 == 0: print(f'  ... {i}/{stat[0]}')

print(f'\nFound {len(yewhan_msgs)} yewhan emails in POP3 ({stat[0]} total)')

print('\nDownloading and saving...')
saved = []
for m in yewhan_msgs:
    try:
        _, lines, _ = mail.retr(m['seq'])
        raw = b'\n'.join(lines)
        msg = email_module.message_from_bytes(raw)
        frm = ds(msg.get('From', ''))
        to = ds(msg.get('To', ''))
        subj = ds(msg.get('Subject', ''))
        date_hdr = msg.get('Date', '')
        try: dt = parsedate_to_datetime(date_hdr)
        except: dt = None
        date_str = dt.strftime('%Y-%m-%d') if dt else 'unknown-date'
        
        out_dir = os.path.join(OUT_DIR, date_str)
        os.makedirs(out_dir, exist_ok=True)
        filepath = os.path.join(out_dir, make_fn(date_str, subj, m['seq']))
        
        body = ''
        if msg.is_multipart():
            for part in msg.walk():
                ct = part.get_content_type()
                disp = str(part.get('Content-Disposition') or '')
                if ct == 'text/plain' and 'attachment' not in disp:
                    try:
                        cs = part.get_content_charset() or 'utf-8'
                        body = part.get_payload(decode=True).decode(cs, errors='replace')
                        break
                    except: pass
        else:
            try:
                cs = msg.get_content_charset() or 'utf-8'
                body = msg.get_payload(decode=True).decode(cs, errors='replace')
            except: pass
        
        atts = []
        for part in msg.walk():
            disp = str(part.get('Content-Disposition') or '')
            if 'attachment' in disp:
                fn = ds(part.get_filename() or '')
                if fn:
                    att_dir = os.path.join(out_dir, '_atts', os.path.splitext(make_fn(date_str, subj, m['seq']))[0])
                    os.makedirs(att_dir, exist_ok=True)
                    with open(os.path.join(att_dir, fn), 'wb') as f: f.write(part.get_payload(decode=True))
                    atts.append(fn)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {subj}\n\n**From:** {frm}\n**To:** {to}\n**Date:** {date_hdr}\n**Msg#:** {m['seq']}\n")
            if atts: f.write(f"**Attachments:** {', '.join(atts)}\n")
            f.write(f"\n---\n\n{body}")
        
        saved.append({'seq': m['seq'], 'file': filepath, 'atts': atts, 'date': date_str})
        print(f'  ✓ msg {m["seq"]}: {subj[:50]}')
    except Exception as e:
        print(f'  ✗ msg {m["seq"]}: {e}')

print(f'\n✓ Saved {len(saved)} emails')

idx = {'account': ACCOUNT, 'target': TARGET, 'found': len(yewhan_msgs), 'saved': len(saved), 'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'), 'emails': saved}
with open(INDEX_FILE, 'w') as f: json.dump(idx, f, indent=2, ensure_ascii=False)

from collections import Counter
dates = Counter(e['date'] for e in saved)
for d, c in sorted(dates.items()): print(f'  {d}: {c}')

mail.quit()
print('✓ Done!')