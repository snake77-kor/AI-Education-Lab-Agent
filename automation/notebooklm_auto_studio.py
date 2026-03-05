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
            print(f"[3/5] 📝 새 메모(Note)를 추가하고 내용을 입력합니다...")
            
            # 1. 새 메모 버튼 클릭
            try:
                add_note_btn = page.locator('.add-note-button, button:has-text("새 메모")').last
                add_note_btn.wait_for(state="visible", timeout=15000)
                add_note_btn.click()
            except Exception as e:
                raise Exception(f"새 메모 버튼을 찾을 수 없습니다: {e}")
            
            time.sleep(2)
            
            # 2. 제목 입력
            try:
                title_in = page.locator('input.note-header__editable-title').last
                title_in.fill(title)
                title_in.press("Enter")
            except Exception as e:
                print(f"⚠️ 메모 제목 입력 오류: {e}")

            time.sleep(1)
            
            # 3. 텍스트 입력창 찾고 타이핑
            try:
                content_in = page.locator('div.ql-editor').last
                content_in.click()
                content_in.fill(content)
                time.sleep(2)
            except Exception as e:
                print(f"⚠️ 메모 내용 입력 오류: {e}")
            
            print(f"[4/5] ✨ 작성된 메모를 '{title}' 소스로 변환 시도 중...")
            
            # 4. 소스로 전환 버튼 클릭
            try:
                convert_btn = page.locator('button:has-text("소스로 전환"), button[aria-label*="소스로 전환"]').last
                convert_btn.wait_for(state="visible", timeout=10000)
                convert_btn.click()
                print("✅ [소스로 전환] 버튼을 성공적으로 클릭하여 소스로 추가했습니다.")
            except Exception as e:
                print(f"⚠️ 소스로 전환 버튼 클릭 실패 (수동 버튼 클릭 필요할 수 있음): {e}")
                
            time.sleep(4) 
            
            # 5. 메모 보기 닫기 (팝업이 열려있으면 닫아주어 배경 UI와 스튜디오가 클릭되도록 함)
            try:
                close_note_btn = page.locator('button[aria-label="메모 보기 닫기"], button[aria-label="Close note view"]').last
                if close_note_btn.count() > 0:
                    close_note_btn.click()
                    print("✅ 메모 보기 팝업을 닫았습니다.")
            except Exception as e:
                pass
                
            time.sleep(4) # 소스 변환 및 동기화 대기 시간
            
            # 5. 슬라이드 자료 생성 클릭 (특정 소스 단독 지정 및 서술형 연구실은 생략)
            if "서술형" in title or "수능 영어" in title:
                print(f"[5/5] ⏭️ 서술형/수능 영어 연구실 파일이므로 '슬라이드 자료' 생성을 생략합니다.")
            else:
                print(f"[5/5] 🎉 특정 소스 단독 선택 및 스튜디오 '슬라이드 자료' 생성을 시작합니다...")
                try:
                    # 1) 전체 소스 선택 해제
                    page.evaluate('''() => {
                        let allCheck = document.querySelector('input[aria-label="모든 출처 선택"]');
                        if (allCheck && allCheck.checked) {
                            allCheck.click();
                        } else {
                            const clearBtn = Array.from(document.querySelectorAll('*')).find(el => 
                                (el.textContent === '선택 해제' || el.textContent === '모두 선택 해제' || el.textContent === 'Clear selection') && 
                                (el.tagName === 'BUTTON' || el.tagName === 'SPAN' || el.tagName === 'DIV')
                            );
                            if (clearBtn) clearBtn.click();
                        }
                    }''')
                    time.sleep(1)
                    
                    # 2) 방금 업로드한 소스 단독 체크
                    # UI 한계로 제목 매칭이 완벽하지 않을 수 있으나, 가장 최근 추가된 소스가 상단/하단에 위치
                    # 여기서는 그냥 title 기반으로 aria-label 체크 시도
                    page.evaluate(f'''(title) => {{
                        // Exact match required because '퀴즈: Point 07' and '강의안: Point 07' are different
                        let cbs = Array.from(document.querySelectorAll('input[type="checkbox"]'));
                        let target = cbs.find(c => c.getAttribute('aria-label') && c.getAttribute('aria-label').includes(title));
                        if(target && !target.checked) {{
                            target.click();
                        }}
                    }}''', title)
                    time.sleep(1)
                    
                    # 3) 슬라이드 자료 버튼 클릭
                    try:
                        # Try pure locator first
                        slide_txt = page.locator('text="슬라이드 자료"')
                        if slide_txt.count() > 0:
                            slide_txt.first.click(force=True)
                            print("✅ [단일 대상] 스튜디오 슬라이드 생성을 요청했습니다 (Playwright native).")
                        else:
                            page.evaluate('''() => {
                                // Find element containing "슬라이드 자료" Text and is a clickable container
                                let els = Array.from(document.querySelectorAll('*')).filter(el => 
                                    el.childNodes.length === 1 && 
                                    el.childNodes[0].nodeType === 3 && 
                                    el.textContent.trim() === '슬라이드 자료'
                                );
                                
                                if (els.length > 0) {
                                    // Usually it's a span inside a button or div, clicking the element or its parent
                                    let clickable = els[0].closest('button, [role="button"], .create-artifact-button-container, .ng-star-inserted') || els[0];
                                    clickable.click();
                                } else {
                                    throw new Error("슬라이드 자료 버튼을 찾을 수 없습니다.");
                                }
                            }''')
                            print("✅ [단일 대상] 스튜디오 슬라이드 생성을 요청했습니다 (JS execution).")
                        
                        time.sleep(20) # 슬라이드 생성 대기시간 증가 (15초 -> 20초)
                        
                        # 생성된 슬라이드 파일 이름도 소스와 동일하게 변경 시도
                        print(f"[6/6] 🎬 슬라이드 이름을 '{title}'(으)로 동기화 변경 시도 중...")
                        page.evaluate(f'''() => {{
                            // 스튜디오 결과물 영역에서 "소스 1개"가 포함된 것을 찾아 더보기 옵션 열기
                            // 기존에는 pfe-card, article 내에 있었으나 class나 구성이 달라질 수 있으므로 강건하게 작성
                            let container = Array.from(document.querySelectorAll('*')).find(el => 
                                el.textContent && el.textContent.includes("소스 1개") && 
                                (el.tagName === 'PFE-CARD' || el.tagName === 'ARTICLE' || el.getAttribute('role') === 'listitem' || el.classList.contains('artifact-card'))
                            );
                            
                            if (container) {{
                                let btn = container.querySelector('button[aria-haspopup="menu"], button[aria-label*="더보기"], button[aria-label*="옵션"]');
                                if (btn) btn.click();
                            }} else {{
                                let mBtns = Array.from(document.querySelectorAll('button[aria-haspopup="menu"], button[aria-label*="더보기"]')).filter(b => {{
                                    return b.parentElement && b.parentElement.textContent.includes("소스 1개");
                                }});
                                if(mBtns.length > 0) mBtns[0].click();
                            }}
                        }}''')
                        time.sleep(2)
                        
                        page.evaluate(f'''() => {{
                            // Click the rename option
                            let opts = Array.from(document.querySelectorAll('[role="menuitem"]'));
                            let r_opt = opts.find(o => o.textContent && (o.textContent.includes("이름 바꾸기") || o.textContent.includes("Rename")));
                            if (r_opt) {{
                                 r_opt.click();
                            }}
                        }}''')
                        time.sleep(2)

                        # 새 이름 입력 후 저장
                        try:
                            # Use .last on visible inputs to avoid modifying the Lab Title
                            s_inputs = page.locator('input[type="text"]:visible, textarea:visible, input.title-input:visible')
                            if s_inputs.count() > 0:
                                st_input = s_inputs.last
                                st_input.fill(title)
                                time.sleep(0.5)
                                st_input.press("Enter")
                        except Exception as err:
                            print(f"⚠️ 슬라이드 이름 입력 중 오류: {err}")
                    except Exception as e:
                        print(f"⚠️ 슬라이드 생성 / 수정 오류: {e}")
                except Exception as e:
                    print(f"⚠️ 슬라이드 연계 기능 전반 중 오류 발생: {e}")
                 
            print("\n--------------------------------------------------------------")
            print("🎉 [작업 완료] NotebookLM 소스 업로드 및 자동화 파이프라인이 종료되었습니다.")
            print(f"👉 브라우저를 확인하시어 이름 변경이나 슬라이드 생성이 잘 적용되었는지 최종 체크해 주세요.")
            print("--------------------------------------------------------------")
            
            time.sleep(5)
            
        except Exception as e:
            print(f"❌ 스크립트 실행 중 치명적인 오류 발생: {e}")
            if 'page' in locals():
                page.screenshot(path="debug_timeout.png")
            time.sleep(5)
            sys.exit(1)  # 에러가 발생한 경우 무조건 비정상 종료
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
