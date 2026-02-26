import os
import sys
import time
import pyperclip
from playwright.sync_api import sync_playwright

def post_to_naver_blog(file_path):
    if not os.path.exists(file_path):
        print(f"파일을 찾을 수 없습니다: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 내용 분석 (첫 줄을 제목으로 파악)
    lines = content.split('\n')
    if lines and lines[0].startswith('#'):
        title = lines[0].replace('#', '').strip()
        body = '\n'.join(lines[1:]).strip()
    else:
        title = "AI 교육 연구소 일일 자료"
        body = content

    WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
    # 보안: .env 파일에서 아이디/비밀번호 정보 로드
    env_path = os.path.join(WORKSPACE_DIR, ".env")
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as env_f:
            for line in env_f:
                if '=' in line and not line.startswith('#'):
                    key, val = line.strip().split('=', 1)
                    os.environ[key] = val
                    
    naver_id = os.environ.get("NAVER_ID", "default_id")
    naver_pw = os.environ.get("NAVER_PW", "")

    # 이 디렉토리에 브라우저 쿠키(로그인 세션)가 암호화되어 저장됩니다.
    USER_DATA_DIR = os.path.join(WORKSPACE_DIR, "naver_profile")

    print(f"[1/4] 🚀 네이버 블로그 오토-포스팅 플러그인을 시작합니다...")
    
    # 미리 본문을 클립보드에 복사해 둡니다.
    pyperclip.copy(body)
    print(f"[2/4] 마크다운 본문을 클립보드에 복사했습니다. (자동 추출 제목: {title})")

    with sync_playwright() as p:
        # 로그인 세션을 기억하기 위해 persistent context를 사용.
        # Automation 플래그를 꺼서 최대한 봇 감지를 우회합니다.
        browser = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ],
            viewport={'width': 1280, 'height': 800}
        )
        
        page = browser.pages[0] if browser.pages else browser.new_page()

        print("[3/4] 🌐 네이버 블로그로 이동하여 세션을 확인합니다...")
        page.goto("https://section.blog.naver.com/BlogHome.naver")
        time.sleep(3)
        page.bring_to_front() # 브라우저를 맨 앞으로 가져오기 시도
        
        # '로그인' 버튼(.btn_login)이 보이거나, 현재 URL이 로그인 페이지(nid.naver.com)로 이동되었다면 세션이 풀린 것입니다.
        if page.locator("a.btn_login").is_visible() or "nid.naver.com" in page.url:
            print("\n❗ [주의] 네이버 로그인이 되어있지 않거나 세션이 만료되었습니다.")
            print(f"❗ 캡차를 우회하기 위해 본인 계정 정보({naver_id})를 클립보드로 붙여넣어 자동 로그인을 시도합니다...")
            page.goto("https://nid.naver.com/nidlogin.login")
            time.sleep(2)
            
            # 아이디 붙여넣기
            page.click('#id')
            pyperclip.copy(naver_id)
            page.keyboard.press("Meta+v")
            time.sleep(1)
            
            # 비밀번호 붙여넣기
            page.click('#pw')
            pyperclip.copy(naver_pw)
            page.keyboard.press("Meta+v")
            time.sleep(1)
            
            # 로그인 클릭
            page.click('.btn_login')
            time.sleep(4) # 로그인 대기
            
            # 기기등록 여부 묻는 창 확인 (등록 안 함)
            try:
                if page.locator("text='등록 안 함'").is_visible():
                     page.locator("text='등록 안 함'").click()
                elif page.locator("text='등록안함'").is_visible():
                     page.locator("text='등록안함'").click()
                elif page.locator("a#new\\.btn_cancel").is_visible():
                     page.click("a#new\\.btn_cancel")
            except:
                pass
            
            # 본문 다시 클립보드로 복사 유지
            pyperclip.copy(body)
            page.goto("https://section.blog.naver.com/BlogHome.naver")
            time.sleep(2)
        else:
            print("✅ 네이버 로그인 세션 확인 완료! (자동 통과)")

        print("[4/4] 📝 글쓰기 에디터 창으로 진입합니다...")
        
        # '내 블로그' ID 파악 (기본값 설정)
        user_id = "kbt0326"
        try:
            my_blog_btn = page.locator("a.btn_myblog").nth(0)
            if my_blog_btn.is_visible(timeout=5000):
                nav_url = my_blog_btn.get_attribute("href")
                user_id = nav_url.split('/')[-1]
        except:
            pass
            
        # 스마트 에디터 ONE 글쓰기 URL 
        write_url = f"https://blog.naver.com/{user_id}?Redirect=Write"
        page.goto(write_url)
        time.sleep(4) # 에디터 로딩 대기
        
        # 만약 여기서도 로그인 창으로 튕겼다면 잡아줍니다
        if "nid.naver.com" in page.url or page.locator("#ac_uid").is_visible() or page.locator("input#id").is_visible():
            print("\n❗ 글쓰기 권한 접근 중 로그인이 한 번 더 요구되었습니다.")
            print(f"❗ 캡차를 우회하기 위해 본인 계정 정보({naver_id})를 클립보드로 붙여넣어 자동 로그인을 시도합니다...")
            page.goto("https://nid.naver.com/nidlogin.login")
            time.sleep(2)
            
            page.click('#id')
            pyperclip.copy(naver_id)
            page.keyboard.press('Meta+v')
            time.sleep(1)
            
            page.click('#pw')
            pyperclip.copy(naver_pw)
            page.keyboard.press('Meta+v')
            time.sleep(1)
            
            page.click('.btn_login')
            time.sleep(4)
            
            try:
                if page.locator("text='등록 안 함'").is_visible():
                     page.locator("text='등록 안 함'").click()
                elif page.locator("a#new\\.btn_cancel").is_visible():
                     page.click("a#new\\.btn_cancel")
            except:
                pass
            
            pyperclip.copy(body)
            page.goto(write_url)
            time.sleep(4)
        
        print("[5/5] ✨ 에디터 자동 입력을 시작합니다...")
        
        # 디버깅을 위한 스크린샷 캡쳐
        page.screenshot(path="debug_editor_load.png")
        
        # 네이버 블로그 스마트 에디터는 iframe 'mainFrame' 내부에 존재합니다.
        try:
            frame = page.frame_locator("iframe#mainFrame")
            
            # 먼저 에디터 영역 자체가 로드되었는지 확인합니다
            if not frame.locator(".se-component").first.is_visible(timeout=5000):
                 print("❗ 에디터 컴포넌트를 찾을 수 없습니다. 로그인이 풀렸거나 페이지 로딩 오류일 수 있습니다.")
                 page.screenshot(path="debug_error.png")
                 print("❗ 디버그용 스크린샷이 debug_error.png에 저장되었습니다.")
            
            # 팝업 닫기 시도 (추천 템플릿 등)
            try:
                cancel_btn = frame.locator(".se-popup-button-cancel").first
                if cancel_btn.is_visible(timeout=2000):
                    cancel_btn.click()
            except:
                pass
            
            # 1. 제목 영역 클릭 후 제목 타이핑
            title_area = frame.locator(".se-documentTitle").first
            if title_area.is_visible(timeout=5000):
                title_area.click()
                title_input = title_area.locator("textarea, input").first
                if title_input.is_visible():
                    title_input.fill(title)
                else:
                    page.keyboard.type(title)
                time.sleep(1)
            else:
                print("❗ 제목 영역(.se-documentTitle)을 찾을 수 없습니다.")
            
            # 2. 본문 영역 클릭 후 클립보드 붙여넣기 (마크다운 양식 유지)
            content_area = frame.locator(".se-content").first
            if content_area.is_visible(timeout=5000):
                content_area.click()
                time.sleep(1)
                page.keyboard.press("Meta+v")
                time.sleep(3) # 렌더링 대기
            else:
                print("❗ 본문 영역(.se-content)을 찾을 수 없습니다.")
            
            # 3. 임시 '저장' 버튼 클릭 (발행 전 초안 저장)
            try:
                save_btn = frame.locator("button:has-text('선택 안됨'), button.btn_save").first
                if not save_btn.is_visible():
                    save_btn = frame.locator("button").filter(has_text="저장").last
                
                if save_btn.is_visible(timeout=3000):
                    save_btn.click()
                    time.sleep(2)
                    print("✅ 초안(임시) 저장을 완료했습니다.")
                else:
                    print("❗ 저장 버튼을 찾을 수 없습니다.")
            except:
                pass
            
            print("\n--------------------------------------------------------------")
            print("🎉 [작업 완료] 스마트에디터 입력 루틴이 종료되었습니다.")
            print(f"👉 방금 작성된 제목: {title}")
            print("👉 브라우저를 확인하시어 우측 상단의 [발행] 버튼만 직접 클릭해 주세요.")
            print("--------------------------------------------------------------")
        except Exception as e:
            print(f"❗ 에디터 프레임을 자동 조작할 수 없습니다: {e}")
            page.screenshot(path="debug_exception.png")

        print("⚠️ 마무리가 모두 끝난 후 이 창에서 [Enter] 키를 누르면 반 팀장의 에이전트가 종료됩니다.")
        
        input() # 사용자가 작업을 끝내고 종료할 때 가지 대기
        browser.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python3 naver_blog_poster.py <마크다운_파일_경로>")
        sys.exit(1)
    
    post_to_naver_blog(sys.argv[1])
