#!/bin/bash

echo "🚀 [1/4] 수능 영어 연구실 (수 실장) 자동화 시작..."
python3 notebooklm_auto_studio.py "output/2026-02-27/2026-02-27_수능 영어 연구실: Point 06 어법 및 Day 05 어휘.md" "https://notebooklm.google.com/notebook/e336e724-5781-4f52-84c0-929c276b0b20"

echo "🚀 [2/4] 중학교 문법 연구실 (문 실장) - 퀴즈 자동화 시작..."
python3 notebooklm_auto_studio.py "output/2026-02-27/2026-02-27_중학 영문법 퀴즈: Point 07. 진행시제.md" "https://notebooklm.google.com/notebook/3fa36817-1786-4833-8908-dff1a7f28ec7"

echo "🚀 [3/4] 중학교 문법 연구실 (문 실장) - 강의안 자동화 시작..."
python3 notebooklm_auto_studio.py "output/2026-02-27/2026-02-27_Point 07. 진행시제와 상태동사.md" "https://notebooklm.google.com/notebook/3fa36817-1786-4833-8908-dff1a7f28ec7"

echo "🚀 [4/4] 고등 영어 연구실 (고 실장) 자동화 시작..."
python3 notebooklm_auto_studio.py "output/2026-02-27/2026-02-27_3강. 주어-동사 수 일치 II.md" "https://notebooklm.google.com/notebook/1e21d971-3d7a-4ab4-b6d5-ff717af6becb"

echo "✅ 모든 자동화 작업이 완료되었습니다!"
