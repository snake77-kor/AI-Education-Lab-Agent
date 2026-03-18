import os
import time
from playwright.sync_api import sync_playwright

def run_extraction(notebook_url, grade_name):
    profile_dir = "/Users/byeongtaekkim/Documents/multi-AI agents/automation/google_profile"
    questions = [20, 21, 22, 23, 24, 29, 30]

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            headless=False,
            args=["--start-maximized", "--disable-blink-features=AutomationControlled"]
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.set_default_timeout(60000)

        print(f"[{grade_name}] 1. 페이지 접속...")
        page.goto(notebook_url)
        time.sleep(10)
        
        print(f"[{grade_name}] 2. '모든 출처(소스)' 전체 선택 확인...")
        try:
            page.evaluate('''() => {
                // '모든 소스 선택' 체크박스 요소를 찾아 무조건 활성화(체크) 되도록 합니다.
                const labels = Array.from(document.querySelectorAll('span, div, label')).filter(e => e.textContent.trim() === '모든 소스 선택' || e.textContent.trim() === '모든 출처 선택' || e.textContent.trim() === 'Select all sources');
                if (labels.length > 0) {
                    const cbContainer = labels[0].closest('label') || labels[0].parentElement;
                    const cb = cbContainer.querySelector('input[type="checkbox"], div[role="checkbox"], md-checkbox');
                    if (cb && cb.getAttribute('aria-checked') !== 'true' && !cb.checked) {
                        cb.click();
                    }
                }
            }''')
        except Exception as e:
            print(f"소스 선택 중 오류 발생: {e}")
            
        time.sleep(3)
        
        for q in questions:
            print(f"[{grade_name} - {q}번 문제] 3. 추출 질문 전송...")
            if q == questions[0]:
                prompt = "20, 21, 22, 23, 24, 29, 30번"
            else:
                prompt = "."

            try:
                page.locator('textarea:not([disabled])').last.wait_for(state="visible", timeout=30000)
                textarea = page.locator('textarea:not([disabled])').last
                textarea.click()
                textarea.fill(prompt)
                textarea.press("Enter")
            except Exception as e:
                print(f"[{grade_name} - {q}번 문제] 입력창 오류 발생: {e}")
                time.sleep(10)
                try:
                    textarea = page.locator('textarea:not([disabled])').last
                    textarea.click()
                    textarea.fill(prompt)
                    textarea.press("Enter")
                except:
                    print("재시도 실패, 다음 문항으로 넘어갑니다.")
                    continue
                
            print(f"[{grade_name} - {q}번 문제] 4. AI 답변 출력 대기 중...")
            time.sleep(15) 
            
            # 텍스트 입력창이 다시 활성화(disabled가 풀릴 때까지)될 때까지 대기
            for i in range(24):
                try:
                    disabled = page.evaluate('() => { const t = document.querySelectorAll("textarea"); return t.length > 0 && t[t.length-1].disabled; }')
                    if not disabled:
                        break
                except:
                    pass
                time.sleep(5)
                print(f"[{grade_name} - {q}번 문제] 답변 기다리는 중... ({i*5}s 경과)")
                
            time.sleep(5) # 출력 완료 후 애니메이션 대기
            
            print(f"[{grade_name} - {q}번 문제] 5. 우측 상단 '메모에 저장(핀 꽂기)' 클릭...")
            try:
                page.evaluate('''() => {
                    const btns = Array.from(document.querySelectorAll('button'));
                    const noteBtns = btns.filter(b => b.getAttribute('aria-label') && (b.getAttribute('aria-label').includes('메모에 저장') || b.getAttribute('aria-label').includes('노트에 저장') || b.getAttribute('aria-label').includes('Save to note')));
                    if (noteBtns.length > 0) noteBtns[noteBtns.length - 1].click();
                }''')
            except Exception as e:
                print(f"메모 저장 버튼 클릭 오류: {e}")
                
            time.sleep(5)
            print(f"✅ [{grade_name} - {q}번 문제] 메모 보드 저장 완료!")

        browser.close()

if __name__ == "__main__":
    g1_url = "https://notebooklm.google.com/notebook/9e355ce4-0b87-4789-94ba-66a931558438"
    g2_url = "https://notebooklm.google.com/notebook/a53f2273-c0f7-45f3-bcf8-437740d3af32"
    
    print("============ 고2 모의고사 연구실 1일차 파트 시작 ============")
    run_extraction(g2_url, "고2 학평")
    
    print("============ 고1 모의고사 연구실 1일차 파트 시작 ============")
    run_extraction(g1_url, "고1 학평")
