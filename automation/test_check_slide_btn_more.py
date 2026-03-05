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
    
    # 1. uncheck all
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
    
    # 2. check point 09 target
    page.evaluate('''() => {
        let cbs = Array.from(document.querySelectorAll('input[type="checkbox"]'));
        let target = cbs.find(c => c.getAttribute('aria-label') && c.getAttribute('aria-label').includes('Point 09'));
        if(target && !target.checked) {
            target.click();
        }
    }''')
    time.sleep(2)
    
    # 3. Simulate natural click instead of programmatic click
    err = page.evaluate('''() => {
        try {
            const slideBtnContainer = Array.from(document.querySelectorAll('.create-artifact-button-container')).find(el => 
                el.textContent && el.textContent.includes('슬라이드 자료')
            );
            return slideBtnContainer ? "Found container" : "Not found";
        } catch(e) { return e.toString(); }
    }''')
    print("Find container:", err)
    
    # Do normal click with playwright locator instead of python evaluate JS
    try:
        container_locator = page.locator('.create-artifact-button-container', has_text='슬라이드 자료')
        container_locator.click(force=True)
        print("Locator Click Triggered")
    except Exception as e:
        print("Locator Error:", e)

    time.sleep(20)
        
    browser.close()
