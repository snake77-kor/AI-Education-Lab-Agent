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
        let menus = Array.from(document.querySelectorAll('button[aria-haspopup="menu"], button[aria-label*="옵션"], button[aria-label*="더보기"]'));
        menus.forEach(m => {
            text.push({
                label: m.getAttribute('aria-label'),
                parentInfo: m.parentElement ? m.parentElement.textContent.trim().substring(0, 50) : ""
            });
        });
        
        let slideTextNode = Array.from(document.querySelectorAll('*')).find(el => el.textContent === '슬라이드 자료' && el.children.length === 0);
        let parentDetails = slideTextNode ? slideTextNode.closest('div').innerHTML.substring(0, 1000) : "Not found";
        
        // Let's also look for generated artifacts 
        let generatedCards = Array.from(document.querySelectorAll('[role="complementary"], pfe-card, article'));
        let cardInfo = generatedCards.map(c => c.textContent.trim().substring(0, 50));
        
        return JSON.stringify({
            menus: text,
            slideNode: parentDetails,
            cards: cardInfo
        });
    }''')
    print("Found info:", html)
    
    page.screenshot(path="debug_artifact_rename.png")
    
    browser.close()
