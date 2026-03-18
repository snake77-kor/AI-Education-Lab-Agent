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
        let containers = Array.from(document.querySelectorAll('div[role="listitem"], .single-source-container'));
        if(containers.length === 0) return "No containers found";
        
        let target = containers[0];
        let name = target.textContent.trim().substring(0, 30);
        let b = target.querySelector('button[aria-label="더보기"], button[aria-label*="옵션"], button[aria-haspopup="menu"]');
        if(b) {
            b.click();
            return "Clicked menu: " + name;
        }
        return "Not found button inside container";
    }''')
    print("Step 1:", html)
    time.sleep(2)
    
    html = page.evaluate('''() => {
        let opts = Array.from(document.querySelectorAll('[role="menuitem"]'));
        let r_opt = opts.find(o => o.textContent.includes("이름 바꾸기") || o.textContent.includes("Rename"));
        if (r_opt) {
             r_opt.click();
             return "Rename clicked";
        }
        return "Rename not found";
    }''')
    print("Step 2:", html)
    time.sleep(2)
    
    page.screenshot(path="debug_source_rename.png")
    
    # Can we cancel?
    page.keyboard.press("Escape")
    
    browser.close()
