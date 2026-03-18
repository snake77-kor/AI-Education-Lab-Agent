import os
import time
from playwright.sync_api import sync_playwright

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
profile_dir = os.path.join(WORKSPACE_DIR, "google_profile")

def cancel_generation():
    print("🚀 슬라이드 생성 중지 스크립트 시작...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=profile_dir,
                headless=False,
                args=["--start-maximized", "--disable-blink-features=AutomationControlled"]
            )
            page = browser.pages[0] if browser.pages else browser.new_page()
            
            # 중학교 문법 연구실 URL 
            print("🌐 중학교 문법 연구실 진입...")
            page.goto("https://notebooklm.google.com/notebook/3fa36817-1786-4833-8908-dff1a7f28ec7")
            time.sleep(6) # 노트북 로딩 대기
            
            # 생성 중지 버튼 찾아서 클릭 시도
            print("🛑 중지 버튼 탐색 및 클릭 시도 중...")
            clicked = page.evaluate('''() => {
                let clicked = false;
                const els = Array.from(document.querySelectorAll('button, span, div'));
                const stopBtn = els.find(el => 
                    el.textContent && 
                    (el.textContent.trim() === '중지' || el.textContent.trim() === 'Stop' || el.textContent.trim() === '생성 중지' || el.textContent.trim() === 'Cancel' || el.textContent.trim() === '중단')
                );
                
                if (stopBtn) {
                    stopBtn.click();
                    clicked = true;
                }
                
                const iconBtns = Array.from(document.querySelectorAll('button[aria-label*="중지"], button[aria-label*="취소"], button[aria-label*="Stop"], button[aria-label*="Cancel"]'));
                if (iconBtns.length > 0) {
                    iconBtns[0].click();
                    clicked = true;
                }
                return clicked;
            }''')
            
            if clicked:
                print("✅ 슬라이드 생성 중지 버튼을 성공적으로 클릭했습니다!")
            else:
                print("⚠️ 중지 버튼을 찾지 못했습니다. (이미 생성이 완료되었거나 버튼 UI가 다를 수 있습니다.)")
                
            time.sleep(3)
        except Exception as e:
            print(f"❌ 스크립트 오류: {e}")
        finally:
            if 'browser' in locals():
                browser.close()

if __name__ == "__main__":
    cancel_generation()
