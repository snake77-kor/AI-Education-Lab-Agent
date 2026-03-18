import os
import time
from playwright.sync_api import sync_playwright

def get_screenshot():
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

        page.evaluate('''() => {
            let allCheck = document.querySelector('input[aria-label="모든 출처 선택"]');
            if (allCheck && allCheck.checked) allCheck.click();
            else {
                const clearBtn = Array.from(document.querySelectorAll('button, span, div')).find(el => el.textContent === '선택 해제');
                if (clearBtn) clearBtn.click();
            }
        }''')
        time.sleep(2)

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

        page.evaluate('''() => {
            const listItems = Array.from(document.querySelectorAll('div[role="listitem"], div[role="row"]'));
            for (let el of listItems) {
                let txt = el.textContent.toLowerCase();
                if (txt.includes('2025') && txt.includes('3') && !txt.includes('.md') && (txt.includes('문제') || txt.includes('답'))) {
                    const cb = el.querySelector('div[role="checkbox"], input[type="checkbox"]');
                    if (cb && !cb.checked && cb.getAttribute('aria-checked') !== 'true') {
                        cb.click();
                    }
                }
            }
        }''')
        time.sleep(2)

        page.screenshot(path="debug_chat.png")
        browser.close()

if __name__ == "__main__":
    get_screenshot()
