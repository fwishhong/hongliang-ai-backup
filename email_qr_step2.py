#!/usr/bin/env python3
"""QQ Enterprise Email - step2: use correct SID and navigate to search"""
from playwright.sync_api import sync_playwright
import time, json, re, os

OUT_DIR = '/Users/hongliang/.openclaw/workspace/email_backups/yewhan_com'
COOKIES_FILE = f'{OUT_DIR}/_cookies.json'
SID_FILE = f'{OUT_DIR}/_sid.json'
DEBUG_DIR = f'{OUT_DIR}/_debug_screenshots'
os.makedirs(DEBUG_DIR, exist_ok=True)

with open(COOKIES_FILE) as f:
    cookies = json.load(f)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(viewport={'width': 1280, 'height': 900})
    context.add_cookies(cookies)
    
    page = context.new_page()
    page.goto('https://exmail.qq.com/', timeout=20000)
    time.sleep(5)
    
    print(f"URL: {page.url}")
    
    # Get current SID from frame URLs (these are fresh from the page)
    current_sid = None
    for fr in page.frames:
        if 'sid=' in fr.url:
            m = re.search(r'sid=([^,&]+)', fr.url)
            if m and 'YORvJ33gFyUmnFgy' in m.group(1):
                current_sid = m.group(1)
                print(f"Current SID: {current_sid}")
                break
    
    page.screenshot(path=f'{DEBUG_DIR}/step2_initial.png')
    print("Screenshot: step2_initial.png")
    
    if not current_sid:
        print("Could not find valid SID")
        while True: time.sleep(1)
    
    # Find mainFrame
    mainfr = None
    for fr in page.frames:
        print(f"  Frame [{fr.name}]: {fr.url[:80]}")
        if fr.name == 'mainFrame' or ('today' in fr.url):
            mainfr = fr
    
    if mainfr:
        print(f"\nUsing mainFrame: {mainfr.url[:80]}")
        # Navigate to search URL using the CURRENT SID from the page
        search_url = f'https://exmail.qq.com/cgi-bin/mail_list?sid={current_sid}&folderid=1&page=0&s=search&keyword=me%40yewhan.com'
        print(f"Navigating to search: {search_url[:100]}")
        
        try:
            mainfr.goto(search_url, timeout=15000)
            time.sleep(6)
            body = mainfr.inner_text('body')[:1000]
            print(f"\nSearch result:\n{body}")
            mainfr.screenshot(path=f'{DEBUG_DIR}/step2_search.png')
            print("Screenshot: step2_search.png")
        except Exception as e:
            print(f"Error: {e}")
            # Try clicking the search input in leftFrame instead
            print("\nTrying leftFrame search input...")
            for fr in page.frames:
                if 'folderlist' in fr.url:
                    # Type in the search box
                    fr.click('body')
                    fr.keyboard.press('/')
                    time.sleep(2)
                    fr.keyboard.type('me@yewhan.com')
                    fr.keyboard.press('Enter')
                    time.sleep(5)
                    body = fr.inner_text('body')[:500]
                    print(f"leftFrame after search: {body}")
                    break
    
    print("\nDone - browser stays open")
    while True:
        time.sleep(1)