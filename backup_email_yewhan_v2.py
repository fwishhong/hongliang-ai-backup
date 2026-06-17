#!/usr/bin/env python3
"""Download emails involving me@yewhan.com from QQ Enterprise Email"""
import imaplib, email as email_module, os, json, re, time
from email.header import decode_header
from email.utils import parsedate_to_datetime

IMAP_HOST = 'imap.exmail.qq.com'
IMAP_PORT = 993
ACCOUNT   = 'hongliang@kongzhong.com'
PASSWORD  = 'DkaK4yzZcrMfJxT2'
TARGET    = 'me@yewhan.com'
OUT_DIR   = '/Users/hongliang/.openclaw/workspace/email_backups/yewhan_com/mail'
INDEX_FILE= '/Users/hongliang/.openclaw/workspace/email_backups/yewhan_com/_index.json'

def decode_str(s):
    if not s: return ''
    parts = decode_header(s)
    result = []
    for part, charset in parts:
        if isinstance(part, bytes):
            result.append(part.decode(charset or 'utf-8', errors='replace'))
        else:
            result.append(part)
    return ''.join(result)

def make_filename(date_str, subject, uid):
    safe_subj = re.sub(r'[^\w\u4e00-\u9fff,-. ]', '', subject)[:40].strip().replace(' ', '-')
    return f"{date_str}_{uid}_{safe_subj}.md"

print("=" * 50)
print("QQ Enterprise Email Backup - me@yewhan.com")
print("=" * 50)

mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
mail.login(ACCOUNT, PASSWORD)
print("✓ Logged in")

mail.select('INBOX', readonly=True)
print("✓ INBOX selected")

# Phase 1: Find all yewhan emails via ENVELOPE scan
yewhan_uids = []
print("\nPhase 1: Scanning INBOX for emails involving me@yewhan.com...")
for seq in range(1, 176):
    typ, data = mail.fetch(str(seq), '(UID ENVELOPE)')
    if typ != 'OK' or not data or not data[0]: continue
    raw = str(data[0])
    m_uid = re.search(r'UID (\d+)', raw)
    uid = int(m_uid.group(1)) if m_uid else None
    addrs = re.findall(r'\(\"([^\"]*)\"\s+NIL\s+"([^"]+)"\s+"([^"]+)"\)', raw)
    emails_in_msg = [f"{a[1]}@{a[2]}" for a in addrs]
    if any(TARGET in e.lower() for e in emails_in_msg):
        yewhan_uids.append(uid)
        print(f"  ✓ UID {uid}: matches")

print(f"\nFound {len(yewhan_uids)} emails involving {TARGET}")

# Phase 2: Download each email
print(f"\nPhase 2: Downloading {len(yewhan_uids)} emails...")
saved = []
for uid in yewhan_uids:
    typ, data = mail.uid('FETCH', str(uid), '(RFC822)')
    if typ != 'OK' or not data or not data[0]:
        print(f"  ✗ UID {uid}: fetch failed")
        continue
    msg = email_module.message_from_bytes(data[0][1])
    subject = decode_str(msg.get('Subject', '(no subject)'))
    date_hdr = msg.get('Date', '')
    try:
        dt = parsedate_to_datetime(date_hdr)
        date_str = dt.strftime('%Y-%m-%d')
    except:
        date_str = 'unknown-date'
    
    out_dir = os.path.join(OUT_DIR, date_str)
    os.makedirs(out_dir, exist_ok=True)
    filepath = os.path.join(out_dir, make_filename(date_str, subject, uid))
    
    # Extract body
    body = ''
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            disp = str(part.get('Content-Disposition') or '')
            if ct == 'text/plain' and 'attachment' not in disp:
                try:
                    charset = part.get_content_charset() or 'utf-8'
                    body = part.get_payload(decode=True).decode(charset, errors='replace')
                    break
                except: pass
    else:
        try:
            charset = msg.get_content_charset() or 'utf-8'
            body = msg.get_payload(decode=True).decode(charset, errors='replace')
        except: pass
    
    # Extract attachments
    attachments = []
    for part in msg.walk():
        disp = str(part.get('Content-Disposition') or '')
        if 'attachment' in disp:
            fn = decode_str(part.get_filename() or '')
            if fn:
                att_subdir = os.path.splitext(make_filename(date_str, subject, uid))[0]
                att_dir = os.path.join(out_dir, '_attachments', att_subdir)
                os.makedirs(att_dir, exist_ok=True)
                with open(os.path.join(att_dir, fn), 'wb') as f:
                    f.write(part.get_payload(decode=True))
                attachments.append(fn)
    
    from_hdr = decode_str(msg.get('From', ''))
    to_hdr = decode_str(msg.get('To', ''))
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# {subject}\n\n")
        f.write(f"**From:** {from_hdr}\n")
        f.write(f"**To:** {to_hdr}\n")
        f.write(f"**Date:** {date_hdr}\n")
        f.write(f"**UID:** {uid}\n")
        if attachments:
            f.write(f"**Attachments:** {', '.join(attachments)}\n")
        f.write(f"\n---\n\n{body}")
    
    saved.append({'uid': uid, 'file': filepath, 'attachments': attachments})
    print(f"  ✓ UID {uid}: {subject[:50]}")
    if attachments:
        print(f"    + {attachments}")

print(f"\n✓ Saved {len(saved)} emails")

# Save index
index = {
    'account': ACCOUNT,
    'target': TARGET,
    'found': len(yewhan_uids),
    'saved': len(saved),
    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'emails': saved
}
with open(INDEX_FILE, 'w') as f:
    json.dump(index, f, indent=2, ensure_ascii=False)

from collections import Counter
dates = Counter(os.path.basename(os.path.dirname(e['file'])) for e in saved)
print("\nBy date:")
for d, c in sorted(dates.items()):
    print(f"  {d}: {c}")

mail.logout()
print("\n✓ Done!")