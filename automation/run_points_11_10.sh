#!/bin/bash
set -e

echo "🚀 [1/3] 수능 영어 연구실 - Point 11 어법 및 Day 10 어휘 NotebookLM 업로드..."
python3 notebooklm_auto_studio.py "output/2026-03-05/2026-03-05_수능 영어 연구실: Point 11 어법 및 Day 10 어휘.md" "https://notebooklm.google.com/notebook/e336e724-5781-4f52-84c0-929c276b0b20"

echo "📢 [2/3] 수능 영어 연구실 - Point 11 어법 및 Day 10 어휘 네이버 블로그 포스팅..."
python3 naver_blog_poster.py "output/2026-03-05/2026-03-05_수능 영어 연구실: Point 11 어법 및 Day 10 어휘.md"

echo "🧹 [3/3] SOP 준수: 마크다운 파일 원본 영구 삭제 진행..."
rm "output/2026-03-05/2026-03-05_수능 영어 연구실: Point 11 어법 및 Day 10 어휘.md"

echo "🎉 누락된 수능 영어 업무(어법 Point 11, 어휘 Day 10) 모두 완료!"
