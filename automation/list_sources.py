import sys
import os
import time
from playwright.sync_api import sync_playwright

def list_sources():
    profile_dir = "/Users/byeongtaekkim/Documents/multi-AI agents/automation/google_profile"
    notebook_url = "https://notebooklm.google.com/"

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            headless=False,
            args=["--start-maximized", "--disable-blink-features=AutomationControlled"]
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.set_default_timeout(60000)

        page.goto(notebook_url)
        time.sleep(5)
        
        notebook_href = page.evaluate('''() => {
            const els = Array.from(document.querySelectorAll('*'));
            const target = els.find(el => el.textContent && el.textContent.trim() === '고2 모의고사 연구실' && el.children.length === 0);
            if (target) {
                const aTag = target.closest('a');
                if (aTag) return aTag.href;
                let parent = target.parentElement;
                while (parent) {
                    if (parent.tagName === 'A') return parent.href;
                    if (parent.getAttribute('data-href')) return parent.getAttribute('data-href');
                    parent = parent.parentElement;
                }
            }
            return null;
        }''')
        
        if notebook_href:
            page.goto(notebook_href)
        else:
            page.locator('text="고2 모의고사 연구실"').last.click(force=True)
            
        time.sleep(10)
        
        sources = page.evaluate('''async () => {
            let names = new Set();
            const scrollContainer = Array.from(document.querySelectorAll('*')).find(el => {
                return el.scrollHeight > el.clientHeight + 10 && el.textContent.includes('모든 소스 선택');
            }) || document.querySelector('aside') || document.querySelector('nav');
            
            for (let i = 0; i < 30; i++) {
                const textNodes = Array.from(document.querySelectorAll('*'))
                    .filter(el => el.children.length === 0 && el.textContent && el.textContent.trim() !== '')
                    .map(el => el.textContent.trim());
                    
                textNodes.forEach(t => {
                    if (t.includes('모의고사') || t.includes('년_') || t.includes('문제') || t.includes('해설')) {
                        names.add(t);
                    }
                });
                
                if (scrollContainer) {
                    scrollContainer.scrollTop += 800;
                    const event = new Event('scroll');
                    scrollContainer.dispatchEvent(event);
                }
                await new Promise(r => setTimeout(r, 1000));
            }
            return Array.from(names);
        }''')
        print("결과:", sources)
        browser.close()

if __name__ == "__main__":
    list_sources()
