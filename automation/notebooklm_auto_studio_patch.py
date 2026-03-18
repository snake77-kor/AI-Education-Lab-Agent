import subprocess

with open('notebooklm_auto_studio.py', 'r', encoding='utf-8') as f:
    orig = f.read()

# Replace slide click logic
old_slide = """                    # 1) 전체 소스 선택 해제
                    page.evaluate('''() => {
                        const clearBtn = Array.from(document.querySelectorAll('*')).find(el => 
                            (el.textContent === '선택 해제' || el.textContent === '모두 선택 해제' || el.textContent === 'Clear selection') && 
                            (el.tagName === 'BUTTON' || el.tagName === 'SPAN' || el.tagName === 'DIV')
                        );
                        if (clearBtn) clearBtn.click();
                        
                        const checkboxes = document.querySelectorAll('div[role="checkbox"], input[type="checkbox"]');
                        checkboxes.forEach(cb => {
                            if (cb.getAttribute('aria-checked') === 'true' || cb.checked) {
                                cb.click();
                            }
                        });
                    }''')
                    time.sleep(1)
                    
                    # 2) 방금 업로드한 소스 단독 체크
                    # UI 한계로 제목 매칭이 완벽하지 않을 수 있으나, 가장 최근 추가된 소스가 상단/하단에 위치
                    # 여기서는 그냥 첫번째 체크박스를 다이렉트로 선택하도록 시도 (또는 title 기반 선택 유지)
                    page.evaluate(f'''(title) => {{
                        const els = Array.from(document.querySelectorAll('*'));
                        const target = els.find(el => el.textContent && el.textContent.includes(title));
                        if (target) {{
                            const container = target.closest('div[role="listitem"]') || target.closest('div[role="row"]') || target.parentElement;
                            if (container) {{
                                const checkbox = container.querySelector('div[role="checkbox"], input[type="checkbox"]');
                                if (checkbox) checkbox.click();
                            }}
                        }}
                    }}''', title)
                    time.sleep(1)
                    
                    # 3) 슬라이드 자료 버튼 클릭
                    try:
                        slide_btn = page.locator('div[role="button"]:has-text("슬라이드 자료"), button:has-text("슬라이드 자료"), div[role="button"][aria-label="슬라이드 자료"]').last
                        if slide_btn.count() > 0:
                            slide_btn.click(timeout=10000, force=True)
                            print("✅ [단일 대상] 스튜디오 슬라이드 생성을 요청했습니다.")
                        else:
                            page.evaluate('''() => {
                                const els = Array.from(document.querySelectorAll('div, button, span'));
                                const slideEl = els.reverse().find(el => el.textContent && (el.textContent.includes('슬라이드 자료') || el.textContent.includes('슬라이드 가이드')));
                                if(slideEl) slideEl.click();
                            }''')
                            print("✅ [단일 대상] 스튜디오 슬라이드 생성을 요청했습니다 (JS fallback).")"""

new_slide = """                    # 1) 전체 소스 선택 해제
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
                        // Extract just Point 00 pattern
                        const m = title.match(/(Point \\d+)/);
                        const matchText = m ? m[1] : title;
                        
                        let cbs = Array.from(document.querySelectorAll('input[type="checkbox"]'));
                        let target = cbs.find(c => c.getAttribute('aria-label') && c.getAttribute('aria-label').includes(matchText));
                        if(target && !target.checked) {{
                            target.click();
                        }}
                    }}''', title)
                    time.sleep(1)
                    
                    # 3) 슬라이드 자료 버튼 클릭
                    try:
                        container_locator = page.locator('.create-artifact-button-container', has_text='슬라이드 자료')
                        if container_locator.count() > 0:
                            container_locator.first.click(force=True)
                            print("✅ [단일 대상] 스튜디오 슬라이드 생성을 요청했습니다.")
                        else:
                            page.evaluate('''() => {
                                const slideBtn = Array.from(document.querySelectorAll('.create-artifact-button-container')).find(el => 
                                    el.textContent && el.textContent.includes('슬라이드 자료')
                                );
                                if (slideBtn) {
                                    slideBtn.click();
                                }
                            }''')
                            print("✅ [단일 대상] 스튜디오 슬라이드 생성을 요청했습니다 (JS fallback).")"""

if old_slide in orig:
    fixed = orig.replace(old_slide, new_slide)
    with open('notebooklm_auto_studio.py', 'w', encoding='utf-8') as f:
        f.write(fixed)
    print("PATCH APPLIED")
else:
    print("NOT FOUND")
