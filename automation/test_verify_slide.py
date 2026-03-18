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
    
    with open("debug_slide_verify2.txt", "w", encoding="utf-8") as f:
        html = page.evaluate("""() => {
            const btns = Array.from(document.querySelectorAll('div, span, button'));
            return btns
                .filter(b => b.textContent && (b.textContent.includes("슬라이드") || b.textContent.includes("자료") || b.textContent.includes("가이드")))
                .map(b => b.outerHTML)
                .join('\\n\\n');
        }""")
        f.write(html)
        
    browser.close()
