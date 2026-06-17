#!/usr/bin/env python3
"""
QQ Enterprise Email backup script for me@yewhan.com
Uses IMAP with ENVELOPE-based filtering (IMAP search is broken on this server)
"""
import imaplib, email as email_module, os, json, re, time
from email.header import decode_header
from email.utils import parsedate_to_datetime

# ── Config ──────────────────────────────────────────────────
IMAP_HOST = 'imap.exmail.qq.com'
IMAP_PORT = 993
ACCOUNT   = 'hongliang@kongzhong.com'
PASSWORD  = 'DkaK4yzZcrMfJxT2'
TARGET    = 'me@yewhan.com'
OUT_DIR   = '/Users/hongliang/.openclaw/workspace/email_backups/yewhan_com/mail'
INDEX_FILE= '/Users/hongliang/.openclaw/workspace/email_backups/yewhan_com/_index.json'

# ── Helpers ─────────────────────────────────────────────────
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
    """Make a safe filename from date/subject"""
    safe_subj = re.sub(r'[^\w\u4e00-\u9fff,-. ]', '', subject)[:40]
    safe_subj = safe_subj.strip().replace(' ', '-')
    return f"{date_str}_{uid}_{safe_subj}.md"

def save_email(msg, uid, date_str, out_dir):
    """Save email as .md file"""
    os.makedirs(out_dir, exist_ok=True)

    subject = decode_str(msg.get('Subject', ''))
    from_hdr = decode_str(msg.get('From', ''))
    to_hdr = decode_str(msg.get('To', ''))
    date_hdr = msg.get('Date', '')

    # Parse date
    try:
        dt = parsedate_to_datetime(date_hdr)
        date_str = dt.strftime('%Y-%m-%d')
    except:
        pass

    filename = make_filename(date_str, subject, uid)
    filepath = os.path.join(out_dir, filename)

    # Get body
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
                except:
                    pass
    else:
        try:
            charset = msg.get_content_charset() or 'utf-8'
            body = msg.get_payload(decode=True).decode(charset, errors='replace')
        except:
            pass

    # Get attachments
    attachments = []
    for part in msg.walk():
        disp = str(part.get('Content-Disposition') or '')
        if 'attachment' in disp:
            filename_att = decode_str(part.get_filename() or '')
            if filename_att:
                att_subdir = os.path.splitext(filename)[0]
                att_dir = os.path.join(out_dir, '_attachments', att_subdir)
                os.makedirs(att_dir, exist_ok=True)
                att_path = os.path.join(att_dir, filename_att)
                with open(att_path, 'wb') as f:
                    f.write(part.get_payload(decode=True))
                attachments.append(filename_att)

    # Write .md file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# {subject}\n\n")
        f.write(f"**From:** {from_hdr}\n")
        f.write(f"**To:** {to_hdr}\n")
        f.write(f"**Date:** {date_hdr}\n")
        f.write(f"**UID:** {uid}\n")
        if attachments:
            f.write(f"**Attachments:** {', '.join(attachments)}\n")
        f.write(f"\n---\n\n")
        f.write(body)

    return filepath, attachments

# ── Main ───────────────────────────────────────────────────
print("=" * 50)
print("QQ Enterprise Email Backup - me@yewhan.com")
print("=" * 50)

mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
mail.login(ACCOUNT, PASSWORD)
print("✓ Logged in")

mail.select('INBOX', readonly=True)
typ, data = mail.status('INBOX', '(UIDVALIDITY UIDNEXT MESSAGES)')
print(f"INBOX status: {data}")

# Get all message UIDs
typ, data = mail.search(None, 'ALL')
all_seq_ids = data[0].split()
print(f"Total messages in INBOX: {len(all_seq_ids)}")

# Get UIDs using sequence numbers
typ, data = mail.fetch('1:*', '(UID)')
uid_map = {}
if typ == 'OK':
    for item in data:
        if item and isinstance(item, tuple):
            raw_str = str(item[0])
            m_uid = re.search(r'UID (\d+)', raw_str)
            m_seq = re.search(r'^(\d+)', raw_str)
            if m_uid and m_seq:
                uid = int(m_uid.group(1))
                seq_id = int(m_seq.group(1))
                uid_map[seq_id] = uid

print(f"UIDs collected: {len(uid_map)}")

# Now scan ENVELOPE for each message to find yewhan emails
print("\nScanning for emails from/to me@yewhan.com...")
yewhan_uids = []
processed = 0

for seq_id in sorted(uid_map.keys()):
    uid = uid_map[seq_id]
    typ, msg_data = mail.fetch(str(seq_id), '(ENVELOPE)')
    if typ != 'OK' or not msg_data or not msg_data[0]:
        continue

    raw_str = str(msg_data[0])

    # ENVELOPE format: (date subject (from_name from_email) (to_name to_email) ...)
    # Extract all email addresses: find patterns like ("name" NIL "local" "domain")
    from_addrs = re.findall(r'\(\"([^\"]*)\"\s+NIL\s+"([^"]+)"\s+"([^"]+)"\)', raw_str)
    from_emails = [f"{local}@{domain}" for _, local, domain in from_addrs]

    # The ENVELOPE structure: first parenthesized group is FROM, second is TO
    # Split by '))(('' to separate from/to groups
    is_yewhan = any(TARGET in e.lower() for e in from_emails)

    if is_yewhan:
        yewhan_uids.append(uid)
        print(f"  ✓ UID {uid}: {' | '.join(from_emails)}")

    processed += 1
    if processed % 20 == 0:
        print(f"  ... scanned {processed}/{len(uid_map)} messages, found {len(yewhan_uids)} matching...")

print(f"\nTotal emails from me@yewhan.com: {len(yewhan_uids)}")

# Now download each matching email
print(f"\nDownloading {len(yewhan_uids)} emails...")
saved = []
for uid in yewhan_uids:
    typ, msg_data = mail.uid('FETCH', str(uid), '(RFC822)')
    if typ != 'OK' or not msg_data or not msg_data[0]:
        print(f"  ✗ UID {uid}: failed to fetch")
        continue

    raw = msg_data[0][1]
    msg = email_module.message_from_bytes(raw)

    date_hdr = msg.get('Date', '')
    try:
        dt = parsedate_to_datetime(date_hdr)
        date_str = dt.strftime('%Y-%m-%d')
    except:
        date_str = 'unknown-date'

    subject = decode_str(msg.get('Subject', '(no subject)'))

    out_dir = os.path.join(OUT_DIR, date_str)

    try:
        filepath, attachments = save_email(msg, uid, date_str, out_dir)
        saved.append({'uid': uid, 'file': filepath, 'attachments': attachments})
        print(f"  ✓ UID {uid}: {subject[:50]} → {os.path.basename(filepath)}")
        if attachments:
            print(f"    Attachments: {attachments}")
    except Exception as e:
        print(f"  ✗ UID {uid}: error saving - {e}")

print(f"\n✓ Saved {len(saved)} emails")

# Save index
index = {
    'account': ACCOUNT,
    'target': TARGET,
    'total_found': len(yewhan_uids),
    'total_saved': len(saved),
    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'emails': [{'uid': e['uid'], 'file': e['file']} for e in saved]
}

with open(INDEX_FILE, 'w') as f:
    json.dump(index, f, indent=2, ensure_ascii=False)

print(f"✓ Index saved to {INDEX_FILE}")

# Summary by date
from collections import Counter
dates = Counter(os.path.dirname(e['file']) for e in saved)
print("\nEmails by date:")
for d, c in sorted(dates.items()):
    print(f"  {os.path.basename(d)}: {c} emails")

mail.logout()
print("\n✓ Done!")