#!/bin/bash
set -e

cd "/Users/byeongtaekkim/Documents/multi-AI agents/automation"

echo "🚀 [1/3] 중학교 문법 연구실 (문 실장) - 퀴즈 자동화 시작..."
python3 notebooklm_auto_studio.py "output/2026-03-12/ms_quiz_15.md" "https://notebooklm.google.com/notebook/3fa36817-1786-4833-8908-dff1a7f28ec7"

echo "🚀 [2/3] 중학교 문법 연구실 (문 실장) - 강의안 자동화 시작..."
python3 notebooklm_auto_studio.py "output/2026-03-12/ms_lecture_15.md" "https://notebooklm.google.com/notebook/3fa36817-1786-4833-8908-dff1a7f28ec7"

echo "📢 블로그 포스팅 시작..."
python3 naver_blog_poster.py "output/2026-03-12/ms_quiz_15.md"

echo "🧹 로컬 원본 삭제..."
rm "output/2026-03-12/ms_quiz_15.md"
rm "output/2026-03-12/ms_lecture_15.md"

echo "🎉 MS Grammar 작업 완료!"
