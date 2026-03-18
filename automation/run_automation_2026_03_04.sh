#!/bin/bash
set -e

# 2026-03-04 일일 자동화 순차 실행 스크립트

echo "🚀 [1/6] 수능 영어 연구실 (수 실장) 자동화 시작..."
python3 notebooklm_auto_studio.py "output/2026-03-04/2026-03-04_수능 영어 연구실: Point 12 어법 및 Day 11 어휘.md" "https://notebooklm.google.com/notebook/e336e724-5781-4f52-84c0-929c276b0b20"

echo "🚀 [2/6] 중학교 문법 연구실 (문 실장) - 퀴즈 자동화 시작..."
python3 notebooklm_auto_studio.py "output/2026-03-04/2026-03-04_중학 영문법 퀴즈: Point 10. 현재완료 2.md" "https://notebooklm.google.com/notebook/3fa36817-1786-4833-8908-dff1a7f28ec7"

echo "🚀 [3/6] 중학교 문법 연구실 (문 실장) - 강의안 자동화 시작..."
python3 notebooklm_auto_studio.py "output/2026-03-04/2026-03-04_중학 영문법 강의안: Point 10. 현재완료 2.md" "https://notebooklm.google.com/notebook/3fa36817-1786-4833-8908-dff1a7f28ec7"

echo "🚀 [4/6] 고등학교 문법 연구실 (고 실장) - 8강 강의안 자동화 시작..."
python3 notebooklm_auto_studio.py "output/2026-03-04/2026-03-04_고등 영문법 강의안: 8강. to부정사의 부사적 용법과 관용구.md" "https://notebooklm.google.com/notebook/1e21d971-3d7a-4ab4-b6d5-ff717af6becb"

echo "🚀 [5/6] 중등 서술형 연구실 (중 실장) - 연습문제 자동화 시작..."
python3 notebooklm_auto_studio.py "output/2026-03-04/2026-03-04_중등 서술형 연습문제: 현재완료 결과 용법과 명백한 과거 부사.md" "https://notebooklm.google.com/notebook/afd5f65f-98c8-4fae-a468-d23cb5c2682e"

echo "🚀 [6/6] 고등 서술형 연구실 (서 실장) - 연습문제 자동화 시작..."
python3 notebooklm_auto_studio.py "output/2026-03-04/2026-03-04_고등 서술형 연습문제: 8강. to부정사 목적과 결과.md" "https://notebooklm.google.com/notebook/14d8e2b4-9cba-4a56-b2bc-ff5e7d6b6d57"

echo "✅ 모든 NotebookLM 자동화 업로드 완료!"

echo "📢 블로그 포스팅 순차 시작..."
python3 naver_blog_poster.py "output/2026-03-04/2026-03-04_수능 영어 연구실: Point 12 어법 및 Day 11 어휘.md"
python3 naver_blog_poster.py "output/2026-03-04/2026-03-04_중학 영문법 퀴즈: Point 10. 현재완료 2.md"

echo "🎉 금일 모든 작업 완료!"

echo "🧹 SOP 준수: 작업 성공에 따른 로컬 마크다운 파일 원본 영구 삭제 진행..."
rm -rf output/2026-03-04/*.md

python3 update_progress.py
