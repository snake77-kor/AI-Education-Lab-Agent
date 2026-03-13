#!/bin/bash
set -e

cd "/Users/byeongtaekkim/Documents/multi-AI agents/automation"

echo "🚀 [1/4] 수능 영어 연구실 (수 실장) - 어법 13, 어휘 12 자동화 시작..."
python3 notebooklm_auto_studio.py "output/2026-03-13/csat_quiz_13_12.md" "https://notebooklm.google.com/notebook/e336e724-5781-4f52-84c0-929c276b0b20"

echo "🚀 [2/4] 중학교 문법 연구실 (문 실장) - 퀴즈 16 자동화 시작..."
python3 notebooklm_auto_studio.py "output/2026-03-13/ms_quiz_16.md" "https://notebooklm.google.com/notebook/3fa36817-1786-4833-8908-dff1a7f28ec7"

echo "🚀 [3/4] 중학교 문법 연구실 (문 실장) - 강의안 16 자동화 시작..."
python3 notebooklm_auto_studio.py "output/2026-03-13/ms_lecture_16.md" "https://notebooklm.google.com/notebook/3fa36817-1786-4833-8908-dff1a7f28ec7"

echo "🚀 [4/4] 고등학교 문법 연구실 (고 실장) - 강의안 11강 자동화 시작..."
python3 notebooklm_auto_studio.py "output/2026-03-13/hs_lecture_11.md" "https://notebooklm.google.com/notebook/1e21d971-3d7a-4ab4-b6d5-ff717af6becb"

echo "📢 블로그 포스팅 시작..."
python3 naver_blog_poster.py "output/2026-03-13/csat_quiz_13_12.md"
python3 naver_blog_poster.py "output/2026-03-13/ms_quiz_16.md"

echo "🧹 로컬 원본 파일은 남겨둡니다. (원하시면 rm으로 삭제하세요)"

echo "🎉 2026-03-13 AI 연구소 루틴 자동화 완료!"
