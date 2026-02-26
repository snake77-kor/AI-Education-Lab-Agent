import json
import os

files_to_parse = {
    "443": "2026-02-26_Point 06. 4형식 문장 (수여동사의 3형식 전환).md",
    "450": "2026-02-26_중학 영문법 퀴즈: Point 06. 4형식 문장.md",
    "451": "2026-02-26_수능 어휘 마스터: Day 04.md",
    "452": "2026-02-26_수능 실전 어법: Point 05.md",
    "462": "2026-02-26_2강. [Killer] 주어-동사 수 일치 I.md"
}

base_path = "/Users/byeongtaekkim/.gemini/antigravity/brain/503700be-c77f-4778-91bd-dc0196ac4fae/.system_generated/steps/{}/output.txt"
out_dir = "/Users/byeongtaekkim/Documents/multi-AI agents/automation/"

for step_id, filename in files_to_parse.items():
    filepath = base_path.format(step_id)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        content = data.get("data", {}).get("answer", "")
        # Remove the system prompt if present
        prompt_suffix = "EXTREMELY IMPORTANT: Is that ALL you need to know"
        if prompt_suffix in content:
            content = content.split(prompt_suffix)[0].strip()
            
        out_filepath = os.path.join(out_dir, filename)
        with open(out_filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Saved: {filename}")
    else:
        print(f"File not found: {filepath}")
