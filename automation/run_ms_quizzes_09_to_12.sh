#!/bin/bash
set -e
cd "/Users/byeongtaekkim/Documents/multi-AI agents/automation"

echo "🚀 Point 09 업로드 시작..."
python3 notebooklm_auto_studio.py "output/2026-03-13/ms_quiz_09.md" "https://notebooklm.google.com/notebook/3fa36817-1786-4833-8908-dff1a7f28ec7"

echo "🚀 Point 10 업로드 시작..."
python3 notebooklm_auto_studio.py "output/2026-03-13/ms_quiz_10.md" "https://notebooklm.google.com/notebook/3fa36817-1786-4833-8908-dff1a7f28ec7"

echo "🚀 Point 11 업로드 시작..."
python3 notebooklm_auto_studio.py "output/2026-03-13/ms_quiz_11.md" "https://notebooklm.google.com/notebook/3fa36817-1786-4833-8908-dff1a7f28ec7"

echo "🚀 Point 12 업로드 시작..."
python3 notebooklm_auto_studio.py "output/2026-03-13/ms_quiz_12.md" "https://notebooklm.google.com/notebook/3fa36817-1786-4833-8908-dff1a7f28ec7"

echo "🎉 모든 업로드 완료"
