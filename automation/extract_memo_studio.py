import sys
import os
import time
from playwright.sync_api import sync_playwright

def run_extraction():
    profile_dir = "/Users/byeongtaekkim/Documents/multi-AI agents/automation/google_profile"
    notebook_url = "https://notebooklm.google.com/notebook/a53f2273-c0f7-45f3-bcf8-437740d3af32"

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            headless=False,
            args=["--start-maximized", "--disable-blink-features=AutomationControlled"]
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.set_default_timeout(60000)

        print("[1/5] 고2 모의고사 연구실 진입...")
        page.goto(notebook_url)
        time.sleep(10)
        
        print("[2/5] 전체 소스 선택 해제...")
        page.evaluate('''() => {
            const checkboxes = document.querySelectorAll('div[role="checkbox"], input[type="checkbox"]');
            checkboxes.forEach(cb => {
                if (cb.getAttribute('aria-checked') === 'true' || cb.checked) {
                    cb.click();
                }
            });
        }''')
        time.sleep(2)

        print("[3/5] 타겟 소스 검색 (2025, 3, PDF 문제/답 포함)...")
        try:
            page.locator('text="모든 소스 선택"').first.click(force=True)
            time.sleep(1)
            page.evaluate('''() => {
                const cb = Array.from(document.querySelectorAll('div[role="checkbox"], input[type="checkbox"]')).find(cb => cb.parentElement.textContent.includes("모든 소스 선택"));
                if(cb && (cb.getAttribute('aria-checked') === 'true' || cb.checked)) cb.click();
            }''')
        except:
            pass

        clicked_sources = page.evaluate('''() => {
            const getScrollable = () => {
                const els = Array.from(document.querySelectorAll('*'));
                return els.find(el => {
                    const style = window.getComputedStyle(el);
                    return el.scrollHeight > el.clientHeight + 10 && 
                           el.textContent.includes('모든 소스 선택') &&
                           (style.overflowY === 'auto' || style.overflowY === 'scroll');
                }) || document.querySelector('aside') || document.querySelector('nav');
            };
            
            let clicked = [];
            let scrollable = getScrollable();
            
            for (let retry = 0; retry < 30; retry++) {
                const items = Array.from(document.querySelectorAll('div[role="listitem"], div[role="row"]'));
                const listItems = items.length > 0 ? items : Array.from(document.querySelectorAll('div')).filter(el => {
                    const cb = el.querySelector('div[role="checkbox"], input[type="checkbox"]');
                    return cb && el.textContent.trim().length > 0;
                });
                
                for (let el of listItems) {
                    let txt = el.textContent.toLowerCase();
                    if (txt.includes('2025') && txt.includes('3') && !txt.includes('.md') && (txt.includes('문제') || txt.includes('답'))) {
                        let name = el.textContent.trim();
                        if (!clicked.includes(name)) {
                            const cb = el.querySelector('div[role="checkbox"], input[type="checkbox"]');
                            if (cb) {
                                if (cb.getAttribute('aria-checked') !== 'true' && !cb.checked) {
                                    cb.scrollIntoView({block: "center"});
                                    cb.click();
                                }
                                clicked.push(name);
                            }
                        }
                    }
                }
                
                if (clicked.length >= 2) break;
                
                if (scrollable) {
                    scrollable.scrollBy(0, 400);
                }
            }
            return clicked;
        }''')

        print(f"소스 선택 완료: {clicked_sources}")
        time.sleep(2)
        
        # We will do 23, 24 as requested
        questions = [23, 24]
        
        for q in questions:
            print(f"[{q}번 문제] 1. 질문 및 추출 시작...")
            prompt = f"{q}번 문제를 톤앤매너를 유지하면서 세련되고 모던한 느낌으로 추출해 줘. 이 지문의 원문과 해설을 상세요구사항에 맞춰 정리해 줘."
            
            try:
                page.locator('textarea:not([disabled])').last.wait_for(state="visible", timeout=30000)
                textarea = page.locator('textarea:not([disabled])').last
                textarea.click()
                textarea.fill(prompt)
                textarea.press("Enter")
            except Exception as e:
                print(f"[{q}번 문제] 입력창 오류:", e)
                continue

            print(f"[{q}번 문제] 2. 답변 대기 중...")
            for i in range(12):
                time.sleep(10)
                print(f"기다리는 중 ({i*10}s)...")
            
            print(f"[{q}번 문제] 3. 메모에 저장 클릭...")
            try:
                page.evaluate('''() => {
                    const btns = Array.from(document.querySelectorAll('button'));
                    const noteBtns = btns.filter(b => b.getAttribute('aria-label') && (b.getAttribute('aria-label').includes('메모에 저장') || b.getAttribute('aria-label').includes('노트에 저장')));
                    if (noteBtns.length > 0) {
                        noteBtns[noteBtns.length - 1].click();
                    }
                }''')
            except Exception as e:
                print(f"[{q}번 문제] 메모 저장 아이콘 찾기 실패: {e}")

            time.sleep(5)
            
            # Now we must convert the newly pinned note to a source. 
            print(f"[{q}번 문제] 4. 가장 최근 메모를 소스로 변환 시도...")
            source_title = f"2025-03-{q}번"
            
            # Select the latest note on the board to trigger toolbar
            try:
                page.evaluate('''() => {
                    // find latest pinned note check box
                    const noteCbs = Array.from(document.querySelectorAll('pfe-card input[type="checkbox"], .note-card input[type="checkbox"], .artifact-card input[type="checkbox"]'));
                    if(noteCbs.length > 0) {
                        noteCbs[0].click(); // Click the top-left (latest) note
                    }
                }''')
                time.sleep(2)
                
                convert_btn = page.locator('button:has-text("소스로 전환"), button[aria-label*="소스로 전환"]').last
                if convert_btn.count() > 0:
                    convert_btn.click()
                else:
                    # fallback
                    page.evaluate('''() => {
                        const cb = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('소스로 전환') || b.getAttribute('aria-label')?.includes('소스로 전환'));
                        if(cb) cb.click();
                    }''')
                    
                print(f"✅ 소스로 변환 버튼 클릭 완료")
            except Exception as e:
                print(f"⚠️ 소스 전환 버튼 클릭 실패: {e}")
                
            time.sleep(8)
            
            # 5. 소스 이름 변경
            print(f"[{q}번 문제] 5. 생성된 소스의 이름을 '{source_title}'로 변경 중...")
            try:
                for attempt in range(3):
                    clicked = page.evaluate('''() => {
                        let buttons = Array.from(document.querySelectorAll('button.source-item-more-button'));
                        if(buttons.length > 0) {
                            buttons[0].click(); // recently added source is at the top
                            return true;
                        }
                        return false;
                    }''')
                    
                    time.sleep(2)
                    rename_opt = page.locator('[role="menuitem"]:has-text("이름 바꾸기"), [role="menuitem"]:has-text("소스 이름 바꾸기"), [role="menuitem"]:has-text("Rename")')
                    if rename_opt.count() > 0:
                        rename_opt.last.click()
                        time.sleep(2)
                        inputs = page.locator('input[type="text"]:visible, textarea:visible, input.title-input:visible')
                        if inputs.count() > 0:
                            t_input = inputs.last
                            t_input.fill(source_title)
                            time.sleep(0.5)
                            t_input.press("Enter")
                        print("✅ 소스 이름 변경 완료.")
                        break
                    time.sleep(2)
            except Exception as e:
                print(f"⚠️ 소스 이름 변경 실패: {e}")
                
            time.sleep(3)
            
            # 6. 소스 단독 선택 및 슬라이드 파이프라인
            print(f"[{q}번 문제] 6. (단일 대상) 스튜디오 모던 슬라이드 생성 작업 시작...")
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
                
                # 2) 방금 생성한 소스 클릭
                page.evaluate(f'''(title) => {{
                    let cbs = Array.from(document.querySelectorAll('input[type="checkbox"]'));
                    let target = cbs.find(c => c.getAttribute('aria-label') && c.getAttribute('aria-label').includes(title));
                    if(target && !target.checked) {{
                        target.click();
                    }}
                }}''', source_title)
                time.sleep(1)
                
                # 3) 슬라이드 자료 버튼 클릭
                slide_txt = page.locator('text="슬라이드 자료"')
                if slide_txt.count() > 0:
                    slide_txt.first.click(force=True)
                else:
                    page.evaluate('''() => {
                        let els = Array.from(document.querySelectorAll('*')).filter(el => 
                            el.childNodes.length === 1 && 
                            el.childNodes[0].nodeType === 3 && 
                            el.textContent.trim() === '슬라이드 자료'
                        );
                        if (els.length > 0) {
                            let clickable = els[0].closest('button, [role="button"], .create-artifact-button-container, .ng-star-inserted') || els[0];
                            clickable.click();
                        }
                    }''')
                    
                print("✅ 톤앤매너 유지 슬라이드 생성을 스튜디오에 요청했습니다.")
                time.sleep(20) # 슬라이드 생성 대기
                
                # 7. 슬라이드 이름 변경
                print(f"[{q}번 문제] 7. 슬라이드 이름을 '{source_title}'로 동기화 중...")
                page.evaluate(f'''() => {{
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
                    let opts = Array.from(document.querySelectorAll('[role="menuitem"]'));
                    let r_opt = opts.find(o => o.textContent && (o.textContent.includes("이름 바꾸기") || o.textContent.includes("Rename")));
                    if (r_opt) r_opt.click();
                }}''')
                time.sleep(2)
                
                s_inputs = page.locator('input[type="text"]:visible, textarea:visible, input.title-input:visible')
                if s_inputs.count() > 0:
                    s_input = s_inputs.last
                    s_input.fill(source_title)
                    time.sleep(0.5)
                    s_input.press("Enter")
                    print("✅ 슬라이드 이름 변경 처리를 완료했습니다.")
                    
                time.sleep(2)
                
                # 다음 문제를 위해 슬라이드 보기 같은 뷰 닫기 (우측 상단 닫기 등)
                close_view = page.locator('button[aria-label="보기 닫기"], button[aria-label="Close view"]').last
                if close_view.count() > 0:
                    close_view.click()
                    time.sleep(1)
                    
            except Exception as e:
                print(f"⚠️ 슬라이드 생성 작업 실패: {e}")

            time.sleep(5)
            
            # 다음 작업을 위해 다시 PDF 파일들만 선택된 상태로 복구해야 함.
            print(f"[{q}번 문제] 추출 파이프라인 완료. 다음 문제를 위해 소스 선택 상태를 갱신합니다.")
            
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
            time.sleep(2)
            
            page.evaluate(f'''(targets) => {{
                for (let t of targets) {{
                    let cbs = Array.from(document.querySelectorAll('input[type="checkbox"]'));
                    let target = cbs.find(c => c.getAttribute('aria-label') && c.getAttribute('aria-label').includes(t));
                    if(target && !target.checked) {{
                        target.click();
                    }}
                }}
            }}''', clicked_sources)
            time.sleep(2)

        print("🎉 모든 프로세스 완료!")
        browser.close()

if __name__ == "__main__":
    run_extraction()
