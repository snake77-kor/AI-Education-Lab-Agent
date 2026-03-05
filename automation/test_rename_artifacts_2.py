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
        // Find saved artifacts (studio panel)
        // Usually there is a "Saved items" text or they are in artifact-list
        let cards = Array.from(document.querySelectorAll('mat-card, [role="listitem"]'));
        
        let targetMenu = null;
        // Let's find menus just for artifacts 
        // Typically, artifacts have a "소스 X개" text.
        let mBtns = Array.from(document.querySelectorAll('button[aria-haspopup="menu"], button[aria-label*="더보기"]')).filter(b => {
             return b.parentElement && b.parentElement.textContent.includes("소스 1개");
        });
        
        if(mBtns.length > 0) {
            targetMenu = mBtns[0];
            targetMenu.click();
            return "Clicked first artifact menu: " + mBtns[0].parentElement.textContent;
        }
        return "Not found";
    }''')
    print("Step 1:", html)
    time.sleep(2)
    
    html = page.evaluate(f'''() => {{
        let opts = Array.from(document.querySelectorAll('[role="menuitem"]'));
        let r_opt = opts.find(o => o.textContent.includes("이름 바꾸기") || o.textContent.includes("Rename"));
        if (r_opt) {{
             r_opt.click();
             return "Rename Opt clicked";
        }}
        return "Rename Opt not found";
    }}''')
    print("Step 2:", html)
    time.sleep(2)
    
    html = page.evaluate(f'''() => {{
        let titleInput = Array.from(document.querySelectorAll('input[type="text"], textarea')).pop();
        if(titleInput) {{
            titleInput.value = "TEST TITLE SYNC";
            titleInput.dispatchEvent(new Event("input", {{bubbles: true}}));
            titleInput.blur();
            
            let save = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes("저장") || b.textContent.includes("Save"));
            if(save) save.click();
            return "Saved!";
        }}
        return "Input not found";
    }}''')
    print("Step 3:", html)
    
    time.sleep(2)
    browser.close()
