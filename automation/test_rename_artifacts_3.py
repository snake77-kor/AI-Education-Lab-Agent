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
        let artifacts = Array.from(document.querySelectorAll('.artifact-card, pfe-card, [role="listitem"]')).filter(el => {
             return el.textContent.includes("소스 1개");
        });
        
        for (let art of artifacts) {
            let btn = art.querySelector('button[aria-haspopup="menu"], button[aria-label*="더보기"]');
            if (btn) {
                btn.click();
                return "Clicked first artifact menu: " + art.textContent.substring(0, 30);
            }
        }
        return "Not found menu button in artifacts";
    }''')
    print("Step 1:", html)
    time.sleep(2)
    
    html = page.evaluate('''() => {
        let opts = Array.from(document.querySelectorAll('[role="menuitem"]'));
        let r_opt = opts.find(o => o.textContent.includes("이름 바꾸기") || o.textContent.includes("Rename"));
        if (r_opt) {
             r_opt.click();
             return "Rename Opt clicked";
        }
        return "Rename Opt not found";
    }''')
    print("Step 2:", html)
    time.sleep(2)
    
    html = page.evaluate('''() => {
        let titleInputs = Array.from(document.querySelectorAll('input[type="text"], textarea'));
        let targetInput = titleInputs.pop();
        if(targetInput) {
            targetInput.value = "2026-03-03_중학 영문법 강의안: Point 09. 현재완료 1 (기본 형태 have p.p. 와 계속, 경험 용법 구분)";
            targetInput.dispatchEvent(new Event("input", {bubbles: true}));
            targetInput.blur();
            
            let save = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes("저장") || b.textContent.includes("Save"));
            if(save) save.click();
            return "Saved!";
        }
        return "Input not found";
    }''')
    print("Step 3:", html)
    
    time.sleep(2)
    
    # 2nd run to rename another 
    page.evaluate('''() => {
        let artifacts = Array.from(document.querySelectorAll('.artifact-card, pfe-card, [role="listitem"]')).filter(el => {
             return el.textContent.includes("소스 1개") && !el.textContent.includes("2026-03-03"); // skip renamed
        });
        for (let art of artifacts) {
            let btn = art.querySelector('button[aria-haspopup="menu"], button[aria-label*="더보기"]');
            if (btn) {
                btn.click();
                return "Clicked 2nd artifact menu";
            }
        }
    }''')
    time.sleep(1)
    
    page.evaluate('''() => {
        let opts = Array.from(document.querySelectorAll('[role="menuitem"]'));
        let r_opt = opts.find(o => o.textContent.includes("지우기") || o.textContent.includes("삭제") || o.textContent.includes("Delete"));
        if (r_opt) {
             r_opt.click();
        }
    }''')
    time.sleep(1)
    
    page.evaluate('''() => {
         let confirm = Array.from(document.querySelectorAll('button')).find(o => o.textContent.includes("삭제") || o.textContent.includes("Delete"));
         if(confirm) confirm.click();
    }''')
    time.sleep(2)
    browser.close()
