import sys
import os
import time
from playwright.sync_api import sync_playwright

def run_extraction():
    profile_dir = "/Users/byeongtaekkim/Documents/multi-AI agents/automation/google_profile"
    profile_dir = "/Users/byeongtaekkim/Documents/multi-AI agents/automation/google_profile"
    # 바로 고2 모의고사 연구실로 직행 (팀장님 제공 URL)
    notebook_url = "https://notebooklm.google.com/notebook/a53f2273-c0f7-45f3-bcf8-437740d3af32"

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            headless=False,
            args=["--start-maximized", "--disable-blink-features=AutomationControlled"]
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.set_default_timeout(60000)

        print("[1/5] 25년 고2 모의고사 변형실 진입...")
        page.goto(notebook_url)
        
        # 페이지 로딩을 충분히 대기
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

        print("[3/5] 타겟 소스 검색 (2025, 3월, md 포함)...")
        # Ensure we focus the sources panel
        try:
            page.locator('text="모든 소스 선택"').first.click(force=True)
            time.sleep(1)
            page.evaluate('''() => {
                const cb = Array.from(document.querySelectorAll('div[role="checkbox"], input[type="checkbox"]')).find(cb => cb.parentElement.textContent.includes("모든 소스 선택"));
                if(cb && (cb.getAttribute('aria-checked') === 'true' || cb.checked)) cb.click();
            }''')
        except:
            pass

        # Select MD sources for 2025 3월
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
        
        questions = [23, 24]
        
        for q in questions:
            print(f"[{q}번 문제] 질문 시작...")
            prompt = f"{q}번 문제를 추출해 줘. 이 지문의 원문과 해설을 상세요구사항에 맞춰 정리해 줘."
            if q in [29, 30]:
                prompt = f"{q}번 문제를 정답을 반영해서 본문을 추출해 줘. 이 지문의 원문과 해설을 상세요구사항에 맞춰 정리해 줘."

            try:
                page.locator('textarea:not([disabled])').last.wait_for(state="visible", timeout=30000)
                textarea = page.locator('textarea:not([disabled])').last
                textarea.click()
                textarea.fill(prompt)
                textarea.press("Enter")
            except Exception as e:
                print(f"[{q}번 문제] 입력창 오류:", e)
                continue

            print(f"[{q}번 문제] 답변 기다리는 중...")
            for i in range(12):
                time.sleep(10)
                print(f"기다리는 중 ({i*10}s)...")
            
            print(f"[{q}번 문제] 메모에 저장 클릭...")
            try:
                page.evaluate('''() => {
                    const btns = Array.from(document.querySelectorAll('button'));
                    const noteBtns = btns.filter(b => b.getAttribute('aria-label') && (b.getAttribute('aria-label').includes('메모에 저장') || b.getAttribute('aria-label').includes('노트에 저장')));
                    if (noteBtns.length > 0) {
                        noteBtns[noteBtns.length - 1].click();
                    }
                }''')
            except Exception as e:
                print(f"[{q}번 문제] 저장 버튼 오류:", e)

            time.sleep(5)
            
            # Change the note title
            note_title = f"2025-03-{q}번"
            print(f"[{q}번 문제] 메모 이름 변경 시도 중: {note_title}")
            try:
                # 1. Open the last generic note. The note board should show it.
                # Actually, NotebookLM selects the memo card on the board. We can find the note card with the exact text or just click the last note on the board.
                page.evaluate('''() => {
                    const cards = Array.from(document.querySelectorAll('pfe-card, .note-card, article[role="listitem"]'));
                    // The pinned note is typically the last one added, which appears first or last.
                    // Usually it's the first one in the "Saved notes" list if sorted by recent?
                    // Let's click the latest one (first on top or whichever has default title "저장된 답변" or similar).
                    // Or we just find the last card in the DOM.
                    if(cards.length > 0) {
                        // try to click the first card assuming newest is top left
                        let clickable = cards[0];
                        clickable.click();
                    }
                }''')
                time.sleep(3)
                
                title_in = page.locator('input.note-header__editable-title').last
                if title_in.count() > 0:
                    title_in.fill(note_title)
                    time.sleep(0.5)
                    title_in.press("Enter")
                    print(f"✅ 메모 제목 변경 완료: {note_title}")
                else:
                    print(f"⚠️ 메모 제목을 입력할 필드를 찾지 못했습니다.")
                    
                time.sleep(1)
                
                close_note_btn = page.locator('button[aria-label="메모 보기 닫기"], button[aria-label="Close note view"]').last
                if close_note_btn.count() > 0:
                    close_note_btn.click()
                
            except Exception as e:
                print(f"[{q}번 문제] 메모 이름 변경 오류:", e)
                
            time.sleep(3)
            
        print("모든 문제 추출 완료")
        browser.close()

if __name__ == "__main__":
    run_extraction()
