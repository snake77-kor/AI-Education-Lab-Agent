#!/bin/bash
set -e

echo "🚀 [1/4] 수능 영어 연구실 - Point 08 어법 NotebookLM 업로드..."
python3 notebooklm_auto_studio.py "output/2026-03-05/2026-03-05_수능 영어 연구실: Point 08 어법.md" "https://notebooklm.google.com/notebook/e336e724-5781-4f52-84c0-929c276b0b20"

echo "🚀 [2/4] 수능 영어 연구실 - Point 11 어법 NotebookLM 업로드..."
python3 notebooklm_auto_studio.py "output/2026-03-05/2026-03-05_수능 영어 연구실: Point 11 어법.md" "https://notebooklm.google.com/notebook/e336e724-5781-4f52-84c0-929c276b0b20"

echo "📢 [3/4] 수능 영어 연구실 - Point 08 어법 네이버 블로그 포스팅..."
python3 naver_blog_poster.py "output/2026-03-05/2026-03-05_수능 영어 연구실: Point 08 어법.md"

echo "📢 [4/4] 수능 영어 연구실 - Point 11 어법 네이버 블로그 포스팅..."
python3 naver_blog_poster.py "output/2026-03-05/2026-03-05_수능 영어 연구실: Point 11 어법.md"

echo "🧹 SOP 준수: 마크다운 파일 원본 영구 삭제 진행..."
rm "output/2026-03-05/2026-03-05_수능 영어 연구실: Point 08 어법.md"
rm "output/2026-03-05/2026-03-05_수능 영어 연구실: Point 11 어법.md"

echo "🎉 Point 08, 11 추가 작업 완료!"
