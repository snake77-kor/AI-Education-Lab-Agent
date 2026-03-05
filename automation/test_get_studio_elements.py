import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir="./google_profile",
        headless=True,
        args=["--start-maximized", "--disable-blink-features=AutomationControlled", "--lang=ko-KR"]
    )
    page = browser.pages[0] if browser.pages else browser.new_page()
    page.goto("https://notebooklm.google.com/notebook/3fa36817-1786-4833-8908-dff1a7f28ec7")
    
    page.wait_for_selector('button[aria-label="출처 추가"]', timeout=15000)
    time.sleep(3)
    
    # After sliding logic executed
    with open("studio_elements_after.txt", "w", encoding="utf-8") as f:
        html = page.evaluate('''() => {
            return document.querySelector('notebook-audio-overview-artifact, artifact-list, model-artifact') ? document.querySelector('notebook-audio-overview-artifact, artifact-list, model-artifact').outerHTML : "Not found";
        }''')
        f.write(html)
        
    with open("studio_elements_after_all.txt", "w", encoding="utf-8") as f:
         html = page.evaluate('''() => {
            return document.querySelector('[role="main"]') ? document.querySelector('[role="main"]').outerHTML : "Not found main";
        }''')
         f.write(html)
         
    browser.close()
