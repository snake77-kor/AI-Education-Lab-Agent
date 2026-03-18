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
    
    # 1. Uncheck all sources
    err = page.evaluate('''() => {
        try {
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
            return "Cleared";
        } catch (e) {
            return e.toString();
        }
    }''')
    print("Clear Step:", err)
    time.sleep(2)
    
    # 2. Check Point 09 target
    err = page.evaluate('''() => {
        try {
            let cbs = Array.from(document.querySelectorAll('input[type="checkbox"]'));
            let target = cbs.find(c => c.getAttribute('aria-label') && c.getAttribute('aria-label').includes('Point 09'));
            if(target && !target.checked) {
                target.click();
                return "Checked: " + target.getAttribute('aria-label');
            }
            return "Target not found";
        } catch (e) {
            return e.toString();
        }
    }''')
    print("Check Step:", err)
    time.sleep(2)
    
    # Wait for the Studio panel to update and click Slide
    err = page.evaluate('''() => {
        try {
            // Find the slide button correctly based on role and text
            const slideBtn = Array.from(document.querySelectorAll('div[role="button"]')).find(el => 
                el.getAttribute('aria-label') === '슬라이드 자료' || 
                (el.textContent && el.textContent.includes('슬라이드 자료'))
            );
            
            if (slideBtn) {
                slideBtn.click();
                return "Clicked slide button in Studio";
            }
            return "Slide button not found";
        } catch (e) {
            return e.toString();
        }
    }''')
    print("Click Step:", err)
    
    # Wait for generation
    time.sleep(15)
    page.screenshot(path="debug_studio_result.png")
    
    browser.close()
