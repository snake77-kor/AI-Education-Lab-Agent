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
    
    # Try to rename the generated slide
    html = page.evaluate('''() => {
        let results = [];
        const titles = Array.from(document.querySelectorAll('span, div')).filter(el => 
            el.textContent.includes('슬라이드 자료') || el.classList.contains('title')
        );
        if(titles.length > 0) {
            let container = titles[0].closest('[role="complementary"]') || titles[0].parentElement.parentElement;
            if(container) {
                let btn = container.querySelector('button[aria-label="이름 바꾸기"], button[aria-label="편집"], button[aria-haspopup="menu"]');
                if(btn) {
                     btn.click();
                     return "Rename menu opened";
                }
            }
        }
        return "Rename button not found";
    }''')
    print("Rename Step 1:", html)
    time.sleep(2)
    
    html = page.evaluate(f'''() => {{
        let titleInput = document.querySelector('input[type="text"], textarea');
        if(titleInput) {{
            titleInput.value = "2026-03-03_중학 영문법 강의안: Point 09. 현재완료 1 (기본 형태 have p.p. 와 계속, 경험 용법 구분)";
            titleInput.dispatchEvent(new Event("input", {{bubbles: true}}));
            titleInput.blur();
            return "Title Input Set";
        }}
        return "Title Input not found";
    }}''')
    print("Rename Step 2:", html)
    
    time.sleep(2)
    page.screenshot(path="debug_rename_slide.png")
    
    browser.close()
