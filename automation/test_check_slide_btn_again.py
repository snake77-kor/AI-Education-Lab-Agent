import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir="./google_profile",
        headless=False, # Make it visible for a moment
        args=["--start-maximized", "--disable-blink-features=AutomationControlled", "--lang=ko-KR"]
    )
    page = browser.pages[0] if browser.pages else browser.new_page()
    page.goto("https://notebooklm.google.com/notebook/3fa36817-1786-4833-8908-dff1a7f28ec7")
    
    page.wait_for_selector('button[aria-label="출처 추가"]', timeout=15000)
    time.sleep(3)
    
    # Check what buttons are in Studio
    html = page.evaluate('''() => {
        let text = [];
        let studioBtns = Array.from(document.querySelectorAll('.create-artifact-button-container'));
        studioBtns.forEach(b => {
            text.push(b.textContent.trim());
        });
        return text.join(", ");
    }''')
    print("Studio Buttons:", html)
    
    time.sleep(10)
    page.screenshot(path="debug_studio_visible.png")
    browser.close()
