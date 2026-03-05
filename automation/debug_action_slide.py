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
    
    # Check if there is already a slide running or an unfinished overlay
    try:
        # We need to test the fallback clicking behavior from notebooklm_auto_studio.py
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
        
        # Click the slide button
        print("Clicking slide button with JS...")
        page.evaluate('''() => {
            const els = Array.from(document.querySelectorAll('div, button, span'));
            const slideEl = els.reverse().find(el => el.textContent && (el.textContent.trim() === '슬라이드 자료' || el.textContent.includes('슬라이드 가이드')));
            // Go to the closest button or role="button" parent
            if(slideEl) {
                let p = slideEl.closest('[role="button"]') || slideEl.closest('button') || slideEl;
                p.click();
                return "Clicked " + slideEl.textContent;
            }
            return "Not found";
        }''')
        time.sleep(10)
        
        with open("after_slide_click.txt", "w", encoding="utf-8") as f:
            html = page.evaluate('''() => {
                return Array.from(document.querySelectorAll('span, div')).filter(el => el.textContent.includes('슬라이드 자료')).map(e => e.outerHTML).join('\\n');
            }''')
            f.write(html)
            
    except Exception as e:
        print(e)
        
    page.screenshot(path="debug_action_slide.png")
    browser.close()
