import os
import time
from playwright.sync_api import sync_playwright

def restore_and_extract():
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

        print("[1/5] 소스 이름 원상복구 체크...")
        # Check if 2025-03-23번 still exists
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
        
        for wrong_name, orig_name in [("2025-03-23번", "2024년_11월 고2 문항지.pdf"), ("2025-03-24번", "2024년_11월 고2 정답해설.pdf")]:
            try:
                clicked = page.evaluate(f'''(t) => {{
                    let cbs = Array.from(document.querySelectorAll('div[role="checkbox"], input[type="checkbox"]'));
                    let targetCb = cbs.find(cb => cb.parentElement && cb.parentElement.textContent.includes(t));
                    if(targetCb) {{
                        let btn = targetCb.closest('div[role="listitem"], .source-item').querySelector('button.source-item-more-button');
                        if(btn) {{ btn.click(); return true; }}
                    }}
                    return false;
                }}''', wrong_name)
                
                if clicked:
                    time.sleep(1)
                    rename_opt = page.locator('[role="menuitem"]:has-text("이름 바꾸기"), [role="menuitem"]:has-text("Rename")')
                    if rename_opt.count() > 0:
                        rename_opt.last.click()
                        time.sleep(1)
                        inputs = page.locator('input[type="text"]:visible, textarea:visible')
                        if inputs.count() > 0:
                            inputs.last.fill(orig_name)
                            inputs.last.press("Enter")
                        print(f"복원 완료: {wrong_name} -> {orig_name}")
                time.sleep(2)
            except Exception as e:
                pass

        print("[2/5] 문제 추출을 위해 2025년 3월 PDF 소스 단독 선택...")
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

        questions = [23, 24]
        for q in questions:
            print(f"[{q}번 문제] 질문 입력 및 추출 요청...")
            prompt = f"{q}번 문제를 톤앤매너를 유지하면서 세련되고 모던한 느낌으로 추출해 줘. 이 지문의 원문과 해설을 상세요구사항에 맞춰 정리해 줘."
            try:
                page.locator('textarea:not([disabled])').last.wait_for(state="visible", timeout=30000)
                textarea = page.locator('textarea:not([disabled])').last
                textarea.click()
                textarea.fill(prompt)
                textarea.press("Enter")
            except Exception as e:
                print("Textarea error", e)
                continue

            for i in range(12):
                time.sleep(10)
                print(f"[{q}번] 대기 중...")
            
            print(f"[{q}번 문제] 메모에 저장 클릭...")
            page.evaluate('''() => {
                const btns = Array.from(document.querySelectorAll('button'));
                const noteBtns = btns.filter(b => b.getAttribute('aria-label') && (b.getAttribute('aria-label').includes('메모에 저장') || b.getAttribute('aria-label').includes('노트에 저장')));
                if (noteBtns.length > 0) noteBtns[noteBtns.length - 1].click();
            }''')
            time.sleep(5)

            source_title = f"2025-03-{q}번"
            print(f"[{q}번 문제] 메모 열기 및 '{source_title}'로 이름 변경 후 소스로 변환...")
            try:
                # click latest board note
                page.evaluate('''() => {
                    const cards = Array.from(document.querySelectorAll('pfe-card, article[role="listitem"], .note-card'));
                    if(cards.length > 0) cards[0].click();
                }''')
                time.sleep(2)
                
                title_in = page.locator('input.note-header__editable-title').last
                if title_in.count() > 0:
                    title_in.fill(source_title)
                    title_in.press("Enter")
                    time.sleep(2)

                convert_btn = page.locator('button:has-text("소스로 전환"), button[aria-label*="소스로 전환"]').last
                if convert_btn.count() > 0:
                    convert_btn.click()
                else:
                    page.evaluate('''() => {
                        const cb = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('소스로 전환') || b.getAttribute('aria-label')?.includes('소스로 전환'));
                        if(cb) cb.click();
                    }''')
                
                print("✅ 소스로 변환 완료.")
                time.sleep(5)
                
                close_note_btn = page.locator('button[aria-label="메모 보기 닫기"], button[aria-label="Close note view"]').last
                if close_note_btn.count() > 0:
                    close_note_btn.click()
            except Exception as e:
                print(f"[{q}번] 노트 처리 오류: {e}")
            
            time.sleep(4)

            print(f"[{q}번 문제] 스튜디오 슬라이드 생성 파이프라인 시작...")
            page.evaluate('''() => {
                let allCheck = document.querySelector('input[aria-label="모든 출처 선택"]');
                if (allCheck && allCheck.checked) allCheck.click();
                else {
                    const clearBtn = Array.from(document.querySelectorAll('button, span, div')).find(el => el.textContent === '선택 해제');
                    if (clearBtn) clearBtn.click();
                }
            }''')
            time.sleep(2)

            page.evaluate(f'''(t) => {{
                let cbs = Array.from(document.querySelectorAll('div[role="checkbox"], input[type="checkbox"]'));
                let target = cbs.find(c => c.parentElement && c.parentElement.textContent.includes(t));
                if(target && !target.checked && target.getAttribute('aria-checked') !== 'true') {{
                    target.click();
                }}
            }}''', source_title)
            time.sleep(2)

            slide_txt = page.locator('text="슬라이드 문서"').last
            if slide_txt.count() == 0:
                slide_txt = page.locator('text="슬라이드 자료"').last
                if slide_txt.count() == 0:
                    slide_txt = page.locator('text="슬라이드"').last
            if slide_txt.count() > 0:
                slide_txt.click(force=True)
            else:
                page.evaluate('''() => {
                    let els = Array.from(document.querySelectorAll('*')).filter(el => 
                        el.childNodes.length === 1 && 
                        el.childNodes[0].nodeType === 3 && 
                        (el.textContent.trim().includes('슬라이드'))
                    );
                    if (els.length > 0) {
                        let clickable = els[0].closest('button, [role="button"]') || els[0];
                        clickable.click();
                    }
                }''')

            time.sleep(25)

            try:
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
                time.sleep(1)
                rename_opt = page.locator('[role="menuitem"]:has-text("이름 바꾸기"), [role="menuitem"]:has-text("Rename")')
                if rename_opt.count() > 0:
                    rename_opt.last.click()
                    time.sleep(1)
                    s_inputs = page.locator('input[type="text"]:visible, textarea:visible')
                    if s_inputs.count() > 0:
                        s_inputs.last.fill(source_title)
                        s_inputs.last.press("Enter")
                time.sleep(1)
                close_view = page.locator('button[aria-label="보기 닫기"], button[aria-label="Close view"]').last
                if close_view.count() > 0:
                    close_view.click()
            except Exception as e:
                pass
                
            time.sleep(2)
            print("✅ 슬라이드 이름 동기화 완료.")

            # Re-select original PDFs for next loop
            page.evaluate('''() => {
                let allCheck = document.querySelector('input[aria-label="모든 출처 선택"]');
                if (allCheck && allCheck.checked) allCheck.click();
                else {
                    const clearBtn = Array.from(document.querySelectorAll('button, span, div')).find(el => el.textContent === '선택 해제');
                    if (clearBtn) clearBtn.click();
                }
            }''')
            time.sleep(1)
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

        browser.close()

if __name__ == "__main__":
    restore_and_extract()
