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
        page.goto("https://notebooklm.google.com/notebook/26ca1051-5183-42e7-8b06-44435ce82df2")
        time.sleep(10)
        
        # Click to go "고2 모의고사 연구실" if not already there, just try to get all source titles
        page.evaluate('''() => {
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
            if(scrollable) {
                scrollable.scrollBy(0, 1000);
            }
        }''')
        time.sleep(2)
        
        sources = page.evaluate('''() => {
            const cbs = document.querySelectorAll('div[role="checkbox"], input[type="checkbox"]');
            return Array.from(cbs).map(cb => cb.parentElement.textContent.trim());
        }''')
        print("ALL SOURCES ON SCREEN:")
        for s in sources:
            print(" ->", s)
        browser.close()

if __name__ == "__main__":
    list_sources()
