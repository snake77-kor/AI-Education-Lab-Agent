#!/bin/bash
# 매일 아침 9시에 실행되어 오늘의 퀴즈 및 강의 생성 과제를 남깁니다.
DATE=$(date +%Y-%m-%d)
WORKSPACE_DIR="/Users/byeongtaekkim/Documents/multi-AI agents"
TARGET_FILE="$WORKSPACE_DIR/automation/TODO_${DATE}.md"

echo "# 📅 오늘의 AI 교육 연구소 업무 ($DATE)" > "$TARGET_FILE"
echo "" >> "$TARGET_FILE"
echo "## 1. 📝 Daily Quiz Generation" >> "$TARGET_FILE"
echo "- [ ] 중학교 문법 퀴즈 (문 실장) - 3문제 + 어휘 5개" >> "$TARGET_FILE"
echo "- [ ] 수능 실전 퀴즈 (수 실장) - 3문제 + 어휘 5개" >> "$TARGET_FILE"
echo "" >> "$TARGET_FILE"
echo "## 2. 📢 Daily Lecture Generation" >> "$TARGET_FILE"
echo "- [ ] 중학 영문법 마스터 클래스 (문 실장)" >> "$TARGET_FILE"
echo "- [ ] 고등 영문법 완성 프로젝트 (고 실장)" >> "$TARGET_FILE"
echo "" >> "$TARGET_FILE"
echo "## 3. 📝 Writing Lab" >> "$TARGET_FILE"
echo "- [ ] 중등 서술형 연구실 (중 실장) - 서술형 연습문제 10문제 생성" >> "$TARGET_FILE"
echo "- [ ] 고등 서술형 연구실 (서 실장) - 서술형 연습문제 10문제 생성" >> "$TARGET_FILE"

echo "✅ 오늘의 업무 리스트가 생성되었습니다: $TARGET_FILE"
echo "👉 다음 명령어로 모든 연구실의 업무를 자동으로 시작하세요: /daily_lab_routine"
