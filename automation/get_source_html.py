import os
import time
from playwright.sync_api import sync_playwright

def inspect_sources():
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

        # Get outer html of the div having the text
        htmls = page.evaluate('''() => {
            const getScrollable = () => {
                const els = Array.from(document.querySelectorAll('*'));
                return els.find(el => {
                    const style = window.getComputedStyle(el);
                    return el.scrollHeight > el.clientHeight + 10 && 
                           el.textContent.includes('모든 소스 선택') &&
                           (style.overflowY === 'auto' || style.overflowY === 'scroll');
                }) || document.querySelector('aside') || document.querySelector('nav');
            };
            let scrollable = getScrollable();
            if(scrollable) scrollable.scrollBy(0, 5000); // scroll down to render all
            
            return new Promise(r => setTimeout(() => {
                const els = Array.from(document.querySelectorAll('div[role="listitem"]'));
                const targetEls = els.filter(el => el.textContent.includes("2025-03-23") || el.textContent.includes("2025-03-24"));
                r(targetEls.map(el => el.outerHTML));
            }, 2000));
        }''')
        
        for h in htmls:
            print("-----------------------")
            print(h)

        browser.close()

if __name__ == "__main__":
    inspect_sources()
