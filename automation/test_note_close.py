import os
import time
from playwright.sync_api import sync_playwright

def test():
    profile_dir = os.path.join(os.getcwd(), "google_profile")
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            headless=False,
            args=["--start-maximized"]
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto("https://notebooklm.google.com/notebook/3fa36817-1786-4833-8908-dff1a7f28ec7")
        page.wait_for_timeout(5000)
        
        # Test finding and checking a source by name
        cb = page.locator('input[type="checkbox"][aria-label*="진행시제"]').last
        cb_info = cb.get_attribute('aria-label') if cb.count() > 0 else "None found"
        print("Test checkbox find:", cb_info)
        
        # Check if the note panel is still open
        close_btn = page.locator('button[aria-label="메모 보기 닫기"]')
        if close_btn.count() > 0:
            print("Note view was still open! Clicking close.")
            close_btn.last.click()
            page.wait_for_timeout(1000)
            
        print("Trying to find 슬라이드 자료...")
        res = page.evaluate('''() => {
             return Array.from(document.querySelectorAll('*')).filter(el => 
                                     el.childNodes.length === 1 && 
                                     el.childNodes[0].nodeType === 3 && 
                                     el.textContent.trim() === '슬라이드 자료'
                                 ).length;
        }''')
        print("Found 슬라이드 자료:", res)
        browser.close()

if __name__ == "__main__":
    test()
