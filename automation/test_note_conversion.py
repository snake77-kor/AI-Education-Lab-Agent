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
        
        # 1. Click Add Note button
        add_note_btn = page.locator('.add-note-button, button:has-text("새 메모")').last
        print("Add note button found:", add_note_btn.count())
        add_note_btn.click()
        page.wait_for_timeout(2000)
        
        with open('note_popup_dom.html', 'w') as f:
            f.write(page.content())
            
        print("Note popup opened.")
        browser.close()

if __name__ == "__main__":
    test()
