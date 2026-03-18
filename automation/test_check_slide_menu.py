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
    
    html = page.evaluate('''() => {
        let text = [];
        let r_btn = Array.from(document.querySelectorAll('button[aria-haspopup="menu"]')).find(b => 
            b.parentElement && b.parentElement.textContent.includes("2026-03-03_중학 영문법 강의안: Point 09")
        );
        if(r_btn) {
            r_btn.click();
            return "Menu Opened";
        }
        return "Menu btn not found";
    }''')
    print("Menu Click:", html)
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
    print("Rename Opt:", html)
    time.sleep(2)
    
    html = page.evaluate(f'''() => {{
        let titleInput = Array.from(document.querySelectorAll('input[type="text"], textarea')).pop();
        if(titleInput) {{
            titleInput.value = "2026-03-03_중학 영문법 강의안: Point 09. 현재완료 1 (기본 형태 have p.p. 와 계속, 경험 용법 구분)";
            titleInput.dispatchEvent(new Event("input", {{bubbles: true}}));
            titleInput.blur();
            // find save
            let save = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes("저장") || b.textContent.includes("Save"));
            if(save) save.click();
            
            return "Title Input Set & Saved";
        }}
        return "Title Input not found";
    }}''')
    print("Set & Save:", html)
    
    time.sleep(2)
    
    browser.close()
