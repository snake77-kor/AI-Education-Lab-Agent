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
    
    try:
        # 1. Choose unselect all
        page.evaluate('''() => {
            const clearBtn = Array.from(document.querySelectorAll('*')).find(el => 
                (el.textContent === '선택 해제' || el.textContent === '모두 선택 해제' || el.textContent === 'Clear selection') && 
                (el.tagName === 'BUTTON' || el.tagName === 'SPAN' || el.tagName === 'DIV')
            );
            if (clearBtn) clearBtn.click();
            
            const checkboxes = document.querySelectorAll('div[role="checkbox"], input[type="checkbox"]');
            checkboxes.forEach(cb => {
                if (cb.getAttribute('aria-checked') === 'true' || cb.checked) {
                    cb.click();
                }
            });
        }''')
        time.sleep(1)
        
        # 2. Select only point 09 lecture
        title = "Point 09"
        page.evaluate(f'''(title) => {{
            const els = Array.from(document.querySelectorAll('*'));
            const target = els.find(el => el.textContent && el.textContent.includes(title));
            if (target) {{
                const container = target.closest('div[role="listitem"]') || target.closest('div[role="row"]') || target.parentElement;
                if (container) {{
                    const checkbox = container.querySelector('div[role="checkbox"], input[type="checkbox"]');
                    if (checkbox) checkbox.click();
                }}
            }}
        }}''', title)
        time.sleep(1)
        
        # 3. Request slide generation
        print("Clicking slide button with Locator...")
        slide_btn = page.locator('div[role="button"][aria-label="슬라이드 자료"], button[aria-label="슬라이드 자료"]').last
        if slide_btn.count() > 0:
            slide_btn.click(force=True)
            print("Slide requested.")
        else:
            print("Could not find button")
            
        time.sleep(15)
        page.screenshot(path="debug_action_slide2.png")
    except Exception as e:
        print(e)
        
    browser.close()
