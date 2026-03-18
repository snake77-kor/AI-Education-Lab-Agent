import os
import time
from playwright.sync_api import sync_playwright

def debug_notebooklm():
    profile_dir = os.path.join(os.getcwd(), "google_profile")
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            headless=False,
            args=["--start-maximized"]
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto("https://notebooklm.google.com/notebook/3fa36817-1786-4833-8908-dff1a7f28ec7")
        page.wait_for_timeout(15000)
        
        # 1. Take a screenshot of the main screen
        page.screenshot(path="debug_main.png")
        
        with open("main_dom.html", "w", encoding="utf-8") as f:
            f.write(page.content())
        
        # 2. Open source options
        page.evaluate('''() => {
            let btns = Array.from(document.querySelectorAll('button[aria-label="더보기"], button[aria-label*="옵션"], button[aria-haspopup="menu"]'));
            let target = btns.find(b => b.closest('div[role="listitem"]'));
            if(target) target.click();
        }''')
        page.wait_for_timeout(3000)
        page.screenshot(path="debug_menu.png")
        
        # 3. Click Rename
        page.evaluate('''() => {
            let r_opt = Array.from(document.querySelectorAll('[role="menuitem"]')).find(o => o.textContent && o.textContent.includes("이름 바꾸기"));
            if(r_opt) r_opt.click();
        }''')
        page.wait_for_timeout(3000)
        
        page.screenshot(path="debug_rename_popup.png")
        html = page.content()
        with open("rename_popup_dom.html", "w", encoding="utf-8") as f:
            f.write(html)
            
        browser.close()

if __name__ == "__main__":
    debug_notebooklm()
