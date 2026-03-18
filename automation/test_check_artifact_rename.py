import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir="./google_profile",
        headless=False,
        args=["--start-maximized", "--disable-blink-features=AutomationControlled", "--lang=ko-KR"]
    )
    page = browser.pages[0] if browser.pages else browser.new_page()
    page.goto("https://notebooklm.google.com/notebook/3fa36817-1786-4833-8908-dff1a7f28ec7")
    
    page.wait_for_selector('button[aria-label="출처 추가"]', timeout=15000)
    time.sleep(5)
    
    html = page.evaluate('''() => {
        let text = [];
        let artifacts = Array.from(document.querySelectorAll('artifact-card, pfe-card, .artifact-card, [role="listitem"]'));
        
        // Find menus
        let menus = Array.from(document.querySelectorAll('button[aria-haspopup="menu"], button[aria-label*="옵션"], button[aria-label*="더보기"], button[aria-label*="맞춤설정"]'));
        menus.forEach(m => {
            text.push({
                label: m.getAttribute('aria-label'),
                parentText: m.parentElement ? m.parentElement.textContent.trim().substring(0, 30) : ""
            });
        });
        
        let slideTextNode = Array.from(document.querySelectorAll('*')).find(el => el.textContent === '슬라이드 자료' && el.children.length === 0);
        let parentDetails = slideTextNode ? slideTextNode.closest('div').innerHTML.substring(0, 200) : "Not found";
        
        return {
            menus: text,
            slideNode: parentDetails
        };
    }''')
    print("Found info:", html)
    
    page.screenshot(path="debug_artifact_rename.png")
    
    browser.close()
