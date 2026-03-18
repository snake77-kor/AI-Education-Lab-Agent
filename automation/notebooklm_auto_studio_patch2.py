import sys

with open('notebooklm_auto_studio.py', 'r', encoding='utf-8') as f:
    orig = f.read()

old_rename = """                        # 생성된 슬라이드 파일 이름도 소스와 동일하게 변경 시도
                        print(f"[6/6] 🎬 슬라이드 이름을 '{title}'(으)로 동기화 변경 시도 중...")
                        page.evaluate(f'''() => {{
                            let titleInput = document.querySelector('textarea, input[aria-label="제목"], input[placeholder="제목 추가"]');
                            if(!titleInput) {{
                                let els = Array.from(document.querySelectorAll('span, div')).filter(el => el.textContent.includes('슬라이드 자료') || el.classList.contains('title'));
                                if(els.length > 0) {{
                                    let btn = els[0].parentElement.querySelector('button[aria-label="이름 바꾸기"], button[aria-label="편집"], button[aria-label="더보기"]');
                                    if(btn) btn.click();
                                }}
                            }}
                        }}''')
                        time.sleep(2)
                        
                        # 만약 제목을 수정할 수 있는 상태라면 값 삽입
                        page.evaluate(f'''() => {{
                            let titleInput = document.querySelector('input[type="text"], textarea');
                            if(titleInput) {{
                                titleInput.value = "{title}";
                                titleInput.dispatchEvent(new Event("input", {{bubbles: true}}));
                                titleInput.blur();
                            }}
                        }}''')"""
                        
new_rename = """                        # 생성된 슬라이드 파일 이름도 소스와 동일하게 변경 시도
                        print(f"[6/6] 🎬 슬라이드 이름을 '{title}'(으)로 동기화 변경 시도 중...")
                        page.evaluate(f'''() => {{
                            // Open menu on the specific slide item
                            let menuBtn = Array.from(document.querySelectorAll('button[aria-haspopup="menu"]')).find(b => 
                                b.parentElement && b.parentElement.textContent.includes("슬라이드 자료")
                            );
                            if(menuBtn) {{
                                menuBtn.click();
                            }}
                        }}''')
                        time.sleep(2)
                        
                        page.evaluate(f'''() => {{
                            // Click the rename option
                            let opts = Array.from(document.querySelectorAll('[role="menuitem"]'));
                            let r_opt = opts.find(o => o.textContent.includes("이름 바꾸기") || o.textContent.includes("Rename"));
                            if (r_opt) {{
                                 r_opt.click();
                            }}
                        }}''')
                        time.sleep(2)

                        # 새 이름 입력 후 저장
                        page.evaluate(f'''() => {{
                            let titleInput = Array.from(document.querySelectorAll('input[type="text"], textarea')).pop();
                            if(titleInput) {{
                                titleInput.value = "{title}";
                                titleInput.dispatchEvent(new Event("input", {{bubbles: true}}));
                                titleInput.blur();
                                
                                let save = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes("저장") || b.textContent.includes("Save"));
                                if(save) save.click();
                            }}
                        }}''')"""

if old_rename in orig:
    fixed = orig.replace(old_rename, new_rename)
    with open('notebooklm_auto_studio.py', 'w', encoding='utf-8') as f:
        f.write(fixed)
    print("PATCH2 APPLIED")
else:
    print("NOT FOUND2")
