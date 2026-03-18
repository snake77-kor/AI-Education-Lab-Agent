#!/bin/bash
set -e

cd "/Users/byeongtaekkim/Documents/multi-AI agents/automation"

echo "🚀 [1/2] 중학교 문법 연구실 (문 실장) - 퀴즈 14 개정판 자동화 시작..."
python3 notebooklm_auto_studio.py "output/2026-03-12/ms_quiz_14_v2.md" "https://notebooklm.google.com/notebook/3fa36817-1786-4833-8908-dff1a7f28ec7"

echo "🚀 [2/2] 중학교 문법 연구실 (문 실장) - 퀴즈 15 개정판 자동화 시작..."
python3 notebooklm_auto_studio.py "output/2026-03-12/ms_quiz_15_v2.md" "https://notebooklm.google.com/notebook/3fa36817-1786-4833-8908-dff1a7f28ec7"

echo "📢 블로그 포스팅 시작..."
python3 naver_blog_poster.py "output/2026-03-12/ms_quiz_14_v2.md"
python3 naver_blog_poster.py "output/2026-03-12/ms_quiz_15_v2.md"

echo "🧹 로컬 원본 삭제..."
rm "output/2026-03-12/ms_quiz_14_v2.md"
rm "output/2026-03-12/ms_quiz_15_v2.md"

echo "🎉 재작업 완료!"
