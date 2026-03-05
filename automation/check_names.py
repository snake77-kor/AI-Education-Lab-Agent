import os
import time
from playwright.sync_api import sync_playwright

def list_sources():
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

        sources2 = page.evaluate('''() => {
            const cbs = document.querySelectorAll('div[role="checkbox"], input[type="checkbox"]');
            return Array.from(cbs).map(cb => {
                let p = cb.parentElement;
                while(p && !p.textContent.trim()) { p = p.parentElement; }
                return p ? p.textContent.trim() : "";
            });
        }''')
        print("SOURCE TITLES:")
        for i, s in enumerate(sources2):
            print(f"[{i}] -> {s}")

        browser.close()

if __name__ == "__main__":
    list_sources()
