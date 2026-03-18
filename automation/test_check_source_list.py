import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir="./google_profile",
        headless=True,
        args=["--start-maximized", "--disable-blink-features=AutomationControlled", "--lang=ko-KR"]
    )
    page = browser.pages[0] if browser.pages else browser.new_page()
    page.goto("https://notebooklm.google.com/notebook/3fa36817-1786-4833-8908-dff1a7f28ec7")
    
    page.wait_for_selector('button[aria-label="출처 추가"]', timeout=15000)
    time.sleep(5)
    
    html = page.evaluate('''() => {
        let text = [];
        // The left panel is usually <source-list> or similar, let's grab the list items.
        // Let's find source rows and their titles.
        let sources = Array.from(document.querySelectorAll('div[role="listitem"]')).slice(0, 5);
        sources.forEach((s, idx) => {
            let titleNode = s.querySelector('.title, [title], .name, span');
            let txt = s.textContent.trim().substring(0, 100);
            text.push("Source " + idx + ": " + txt);
        });
        return text.join("\\n");
    }''')
    print("Sources:\n" + html)
    
    browser.close()
