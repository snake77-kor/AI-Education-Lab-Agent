import sys
import os
import time
from playwright.sync_api import sync_playwright

def post_to_notebooklm(filepath, notebook_url):
    print(f"\n[1/5] 🚀 NotebookLM 오토-스튜디오 플러그인을 시작합니다...")
    
    if not os.path.exists(filepath):
        print(f"❌ 오류: 파일을 찾을 수 없습니다 -> {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 추출할 소스 이름
    filename = os.path.basename(filepath)
    title = os.path.splitext(filename)[0]
    
    # 구글 프로필 유지를 위한 크롬 세션 저장소
    profile_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "google_profile")
    os.makedirs(profile_dir, exist_ok=True)

    with sync_playwright() as p:
        try:
            # 브라우저 실행 (화면 노출 모드)
            browser = p.chromium.launch_persistent_context(
                user_data_dir=profile_dir,
                headless=False,
                args=["--start-maximized", "--disable-blink-features=AutomationControlled"]
            )
            page = browser.pages[0] if browser.pages else browser.new_page()
            
            # 타임아웃 넉넉하게 설정
            page.set_default_timeout(60000)

            print(f"[2/5] 🌐 지정된 NotebookLM 연구실로 진입합니다...")
            page.goto(notebook_url)
            
            # ----- 구글 로그인 대기 로직 -----
            if "accounts.google.com" in page.url or "signin" in page.url:
                print("❗ 구글 로그인이 필요합니다. 창에서 로그인을 완료해 주세요.")
                print("❗ 로그인이 완료되면 자동으로 다음 단계로 넘어갑니다...")
                # notebooklm 주소로 넘어갈 때까지 무제한 대기
                page.wait_for_url("https://notebooklm.google.com/**", timeout=0)
                print("✅ 구글 로그인 세션 확인 완료! (자동 통과)")
            
            # 노트북 로딩 대기
            print(f"[3/5] 📝 소스 추가를 진행합니다...")
            
            # '소스 추가' 버튼이 보일 때까지 대기
            page.wait_for_selector('text="소스 추가" | text="출처 추가" | text="Add Source" | text="Add source"', timeout=60000)
            time.sleep(2) # 안정화
            
            # 1. 소스 추가 클릭
            page.evaluate('''(texts) => {
                const elements = Array.from(document.querySelectorAll("*"));
                const target = elements.find(el => texts.includes(el.textContent.trim()));
                if(target) target.click();
            }''', ["소스 추가", "출처 추가", "Add Source", "Add source"])
            
            time.sleep(1)
            
            # 2. 복사된 텍스트 선택
            page.evaluate('''(texts) => {
                const elements = Array.from(document.querySelectorAll("*"));
                const target = elements.find(el => texts.includes(el.textContent.trim()));
                if(target) target.click();
            }''', ["복사된 텍스트", "복사한 텍스트", "Copied text", "Pasted text"])
            
            time.sleep(1)
            
            # 3. 텍스트 입력창 찾고 타이핑
            textarea = page.locator('textarea').first
            textarea.fill(content)
            
            time.sleep(1)
            
            # 4. 삽입 클릭
            # NotebookLM의 다이얼로그 안의 삽입 버튼
            insert_btns = page.locator('button:has-text("삽입"), button:has-text("Insert")')
            if insert_btns.count() > 0:
                insert_btns.last.click() # 보통 팝업 창의 삽입 버튼이 마지막에 렌더링됨
            
            print(f"[4/5] ✨ 소스 이름을 '{title}'(으)로 변경 시도 중...")
            time.sleep(5) # 소스 분석 및 UI 업데이트 대기
            
            # 이름 변경 시도 (UI가 복잡하므로 실패해도 진행)
            try:
                # 점 3개 메뉴 버튼 찾기
                more_btns = page.locator('button[aria-label="소스 옵션"], button[aria-label="옵션"], button[aria-label="더보기"], button[aria-label="Options"], button[aria-label="Source options"]')
                if more_btns.count() > 0:
                    more_btns.first.click()
                    time.sleep(1)
                    
                    rename_opt = page.locator('text="이름 바꾸기" | text="소스 이름 바꾸기" | text="Rename"')
                    if rename_opt.count() > 0:
                        rename_opt.first.click()
                        time.sleep(1)
                        
                        rename_input = page.locator('input[type="text"]').first
                        if rename_input.count() > 0:
                            rename_input.fill(title)
                            rename_input.press('Enter')
            except Exception as e:
                print(f"⚠️ 이름 변경 시도 실패 (수동 변경 권장). 사유: {e}")
                
            time.sleep(2)
            
            # 5. 슬라이드 자료 생성 클릭
            print(f"[5/5] 🎉 스튜디오 '슬라이드 자료' 생성을 시작합니다...")
            try:
                # 슬라이드 자료 찾기 (div, span 등 다양하게 매핑)
                slide_btn = page.evaluate('''(texts) => {
                    const elements = Array.from(document.querySelectorAll("*"));
                    const target = elements.find(el => texts.includes(el.textContent.trim()) && el.tagName !== 'SCRIPT' && el.tagName !== 'STYLE');
                    if(target) target.click();
                }''', ["슬라이드 자료", "Slide material"])
                print("✅ [슬라이드 자료] 스튜디오 생성을 요청했습니다.")
            except Exception as e:
                 print(f"⚠️ 슬라이드 버튼 클릭 중 오류 발생: {e}")
                 
            print("\n--------------------------------------------------------------")
            print("🎉 [작업 완료] NotebookLM 소스 업로드 및 자동화 파이프라인이 종료되었습니다.")
            print(f"👉 브라우저를 확인하시어 이름 변경이나 슬라이드 생성이 잘 적용되었는지 체크해 주세요.")
            print("--------------------------------------------------------------")
            
            # 브라우저가 바로 닫히지 않고 결과를 눈으로 볼 수 있게 대기
            input("⚠️ 마무리가 모두 끝난 후 이 창에서 [Enter] 키를 누르면 반 팀장의 에이전트가 종료됩니다.\n")
            
        except Exception as e:
            print(f"❌ 스크립트 실행 중 치명적인 오류 발생: {e}")
            input("오류를 확인 후 [Enter]를 눌러 종료하세요.\n")
        finally:
            if 'browser' in locals():
                browser.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("사용법: python3 notebooklm_auto_studio.py <마크다운파일경로> <NotebookLM URL>")
        sys.exit(1)
    
    file_arg = sys.argv[1]
    url_arg = sys.argv[2]
    post_to_notebooklm(file_arg, url_arg)
