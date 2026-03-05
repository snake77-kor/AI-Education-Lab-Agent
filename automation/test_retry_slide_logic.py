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
    
    # 5. 슬라이드 자료 생성 클릭 로직
    # 1) 전체 소스 선택 해제
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
        } catch (e) { return e.toString(); }
    }''')
    print("Uncheck All:", err)
    time.sleep(2)
    
    # 2) 방금 업로드한 소스 단독 체크
    title = "Point 09"
    err = page.evaluate(f'''(title) => {{
        try {{
            let cbs = Array.from(document.querySelectorAll('input[type="checkbox"]'));
            let target = cbs.find(c => c.getAttribute('aria-label') && c.getAttribute('aria-label').includes(title));
            if(target && !target.checked) {{
                target.click();
                return "Checked by JS: " + target.getAttribute('aria-label');
            }}
            return "Target not found";
        }} catch(e) {{ return e.toString(); }}
    }}''', title)
    print("Check One:", err)
    time.sleep(2)
    
    # 3) 슬라이드 자료 버튼 클릭
    err = page.evaluate('''() => {
        try {
            const slideBtn = Array.from(document.querySelectorAll('div[role="button"]')).find(el => 
                el.getAttribute('aria-label') === '슬라이드 자료' || 
                (el.textContent && el.textContent.includes('슬라이드 자료'))
            );
            if (slideBtn) {
                slideBtn.click();
                return "Clicked slide button in Studio by JS";
            }
            return "Slide button not found";
        } catch(e) { return e.toString(); }
    }''')
    print("Click Slide:", err)
    
    time.sleep(15) # 슬라이드 생성 대기
    
    # 생성된 슬라이드 파일 이름 변경
    err = page.evaluate('''() => {
        try {
            let opts = Array.from(document.querySelectorAll('*')).filter(el => 
                el.getAttribute('aria-label') === '이름 일괄 변경' || 
                (el.textContent && el.textContent.includes('이름 바꾸기'))
            );
            return "Rename Option Length: " + opts.length;
        } catch(e) { return e.toString(); }
    }''')
    print("Rename attempt:", err)

    browser.close()
