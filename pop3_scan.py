#!/usr/bin/env python3
"""Scan all POP3 messages for yewhan emails"""
import poplib, socket, email as email_module, time
from email.header import decode_header

def ds(s):
    if not s: return ''
    parts = decode_header(s)
    r = []
    for p, c in parts:
        if isinstance(p, bytes): r.append(p.decode(c or 'utf-8', errors='replace'))
        else: r.append(p)
    return ''.join(r)

socket.setdefaulttimeout(20)
mail = poplib.POP3_SSL('pop.exmail.qq.com', 995)
mail.user('hongliang@kongzhong.com')
mail.pass_('DkaK4yzZcrMfJxT2')

stat = mail.stat()
print(f'POP3 total: {stat[0]} messages', flush=True)

yewhan = []
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
            yewhan.append((i, frm, subj))
            print(f'  msg {i}: From={frm[:60]}, Subject={subj[:50]}', flush=True)
    except Exception as e:
        print(f'  msg {i}: error {e}', flush=True)
    if i % 20 == 0:
        elapsed = time.time() - start
        per_msg = elapsed / i
        print(f'  ... scanned {i}/{stat[0]}, found {len(yewhan)}, elapsed {elapsed:.1f}s, ETA {per_msg*(stat[0]-i):.0f}s', flush=True)

print(f'\nTotal POP3: {stat[0]}, yewhan: {len(yewhan)}, time: {time.time()-start:.1f}s')
mail.quit()
print('Done')