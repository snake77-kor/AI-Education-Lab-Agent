import os
import time
from playwright.sync_api import sync_playwright

def verify():
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
        
        sources = page.evaluate('''() => {
            const getScrollable = () => {
                const els = Array.from(document.querySelectorAll('*'));
                return els.find(el => {
                    const style = window.getComputedStyle(el);
                    return el.scrollHeight > el.clientHeight + 10 && el.textContent.includes('모든 소스 선택') && (style.overflowY === 'auto' || style.overflowY === 'scroll');
                }) || document.querySelector('aside') || document.querySelector('nav');
            };
            let scrollable = getScrollable();
            if(scrollable) scrollable.scrollBy(0, 5000);
            
            return new Promise(r => setTimeout(() => {
                const els = Array.from(document.querySelectorAll('div[role="listitem"]'));
                r(els.map(e => e.textContent.trim()));
            }, 2000));
        }''')
        
        print("SOURCES:")
        for s in sources:
            if '2025' in s or '2024' in s:
                print(" ->", s)
        browser.close()

if __name__ == "__main__":
    verify()
