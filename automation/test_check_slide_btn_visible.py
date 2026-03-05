import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir="./google_profile",
        headless=False, # visible mode
        args=["--start-maximized", "--disable-blink-features=AutomationControlled", "--lang=ko-KR"]
    )
    page = browser.pages[0] if browser.pages else browser.new_page()
    page.goto("https://notebooklm.google.com/notebook/3fa36817-1786-4833-8908-dff1a7f28ec7")
    
    page.wait_for_selector('button[aria-label="출처 추가"]', timeout=15000)
    time.sleep(3)
    
    # Check Point 09 only
    page.evaluate('''() => {
        let allCheck = document.querySelector('input[aria-label="모든 출처 선택"]');
        if (allCheck && allCheck.checked) {
            allCheck.click();
        } else {
            const clearBtn = Array.from(document.querySelectorAll('*')).find(el => 
                (el.textContent === '선택 해제' || el.textContent === '모두 선택 해제' || el.textContent === 'Clear selection') && 
                (el.tagName === 'BUTTON' || el.tagName === 'SPAN' || el.tagName === 'DIV')
            );
            if (clearBtn) clearBtn.click();
        }
    }''')
    time.sleep(2)
    
    page.evaluate('''() => {
        let cbs = Array.from(document.querySelectorAll('input[type="checkbox"]'));
        let target = cbs.find(c => c.getAttribute('aria-label') && c.getAttribute('aria-label').includes('Point 09'));
        if(target && !target.checked) {
            target.click();
        }
    }''')
    time.sleep(2)
    
    # Click slide button
    err = page.evaluate('''() => {
        try {
            const slideBtn = Array.from(document.querySelectorAll('.create-artifact-button-container')).find(el => 
                el.textContent && el.textContent.includes('슬라이드 자료')
            );
            if (slideBtn) {
                slideBtn.click();
                return "Clicked slide button in Studio by JS: " + slideBtn.outerHTML;
            }
            return "Slide button not found in .create-artifact-button-container";
        } catch(e) { return e.toString(); }
    }''')
    print("Click Slide result:", err)
    
    time.sleep(25)
    page.screenshot(path="debug_after_slide_click_visible.png")
    
    # Try capturing artifact items
    html = page.evaluate('''() => {
        let cards = Array.from(document.querySelectorAll('artifact-card, pfe-card, .artifact-card'));
        return "Found " + cards.length + " cards. HTML: " + cards.map(c => c.outerHTML.substring(0, 100)).join(", ");
    }''')
    print("Artifact cards:", html)
    
    browser.close()
