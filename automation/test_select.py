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
    
    # 1. Uncheck all
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
    time.sleep(1)
    
    # 2. Check Point 09 only
    page.evaluate('''() => {
        let input = document.querySelector('input[aria-label*="Point 09. 현재완료 1 (기본 형태 have p.p."]');
        if (input && !input.checked) {
            input.click();
            return "Found and clicked from exact title";
        }
        
        let cbs = Array.from(document.querySelectorAll('input[type="checkbox"]'));
        let target = cbs.find(c => c.getAttribute('aria-label') && c.getAttribute('aria-label').includes('Point 09'));
        if(target && !target.checked) {
            target.click();
            return "Found and clicked from partial title";
        }
        return "Not found";
    }''')
    time.sleep(1)
    
    # 3. Request slide
    page.locator('div[aria-label="슬라이드 자료"][role="button"], button[aria-label="슬라이드 자료"], button:has-text("슬라이드 자료")').first.click(force=True)
    time.sleep(15)
    page.screenshot(path="debug_after_select.png")
    
    with open("debug_selected_result.txt", "w", encoding="utf-8") as f:
        html = page.evaluate('''() => {
            return document.body.innerHTML;
        }''')
        f.write(html)
        
    browser.close()
