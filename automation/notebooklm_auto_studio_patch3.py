import sys

with open('notebooklm_auto_studio.py', 'r', encoding='utf-8') as f:
    orig = f.read()

old_rename = """                        # 생성된 슬라이드 파일 이름도 소스와 동일하게 변경 시도
                        print(f"[6/6] 🎬 슬라이드 이름을 '{title}'(으)로 동기화 변경 시도 중...")
                        page.evaluate(f'''() => {{
                            // Open menu on the specific slide item. We find the first artifact that contains "소스 1개" as it'll be the newly generated slide (NotebookLM generates an arbitrary creative title).
                            let mBtns = Array.from(document.querySelectorAll('button[aria-haspopup="menu"], button[aria-label*="더보기"]')).filter(b => {{
                                return b.parentElement && b.parentElement.textContent.includes("소스 1개");
                            }});
                            if(mBtns.length > 0) {{
                                mBtns[0].click();
                            }}
                        }}''')"""
                        
new_rename = """                        # 생성된 슬라이드 파일 이름도 소스와 동일하게 변경 시도
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
                        }}''')"""

if old_rename in orig:
    fixed = orig.replace(old_rename, new_rename)
    with open('notebooklm_auto_studio.py', 'w', encoding='utf-8') as f:
        f.write(fixed)
    print("PATCH3 APPLIED")
else:
    print("NOT FOUND3")
