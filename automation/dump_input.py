import os
import time
from playwright.sync_api import sync_playwright

def get_input_selector():
    profile_dir = "/Users/byeongtaekkim/Documents/multi-AI agents/automation/google_profile"
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            headless=False,
            args=["--start-maximized"]
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto("https://notebooklm.google.com/notebook/a53f2273-c0f7-45f3-bcf8-437740d3af32")
        time.sleep(10)

        html = page.evaluate('''() => {
            const inputs = Array.from(document.querySelectorAll('input[type="text"], textarea, [contenteditable="true"]'));
            return inputs.map(i => i.outerHTML);
        }''')
        for h in html:
            if '입력을 시작하세요' in h or 'chat' in h.lower() or 'placeholder' in h:
                print("-------------------")
                print(h[:300] + "...")

        browser.close()

if __name__ == "__main__":
    get_input_selector()
