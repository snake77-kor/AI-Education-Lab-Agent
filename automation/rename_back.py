import os
import time
from playwright.sync_api import sync_playwright

def rename_back():
    profile_dir = "/Users/byeongtaekkim/Documents/multi-AI agents/automation/google_profile"
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            headless=False,
            args=["--start-maximized"]
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.set_default_timeout(60000)
        page.goto("https://notebooklm.google.com/notebook/a53f2273-c0f7-45f3-bcf8-437740d3af32")
        time.sleep(10)

        # Scroll to bottom
        page.evaluate('''() => {
            const getScrollable = () => {
                const els = Array.from(document.querySelectorAll('*'));
                return els.find(el => {
                    const style = window.getComputedStyle(el);
                    return el.scrollHeight > el.clientHeight + 10 && el.textContent.includes('모든 소스 선택') && (style.overflowY === 'auto' || style.overflowY === 'scroll');
                }) || document.querySelector('aside') || document.querySelector('nav');
            };
            let scrollable = getScrollable();
            if(scrollable) scrollable.scrollBy(0, 5000);
        }''')
        time.sleep(2)
        
        for old, new_name in [("2025-03-23번", "2024년_11월 고2 영어문제지.pdf"), ("2025-03-24번", "2024년_11월 고2 정답해설.pdf")]:
            try:
                page.evaluate(f'''(t) => {{
                    let items = Array.from(document.querySelectorAll('div[role="listitem"]'));
                    for(let el of items) {{
                        if(el.textContent.includes(t)) {{
                            let btn = el.querySelector('button[aria-haspopup="menu"], button.source-item-more-button, button[aria-label*="옵션"], button[aria-label*="more"]');
                            if(btn) btn.click();
                            return;
                        }}
                    }}
                }}''', old)
                time.sleep(2)
                
                # Check for menu items
                page.evaluate('''() => {
                    let items = Array.from(document.querySelectorAll('[role="menuitem"]'));
                    let rename = items.find(el => el.textContent.includes("이름 바꾸기") || el.textContent.includes("Rename"));
                    if(rename) rename.click();
                }''')
                time.sleep(2)
                
                inputs = page.locator('input[type="text"]:visible, textarea:visible')
                if inputs.count() > 0:
                    inputs.last.fill(new_name)
                    inputs.last.press("Enter")
                    print(f"Renamed {old} to {new_name}")
                time.sleep(2)
            except Exception as e:
                print(e)

        browser.close()

if __name__ == "__main__":
    rename_back()
