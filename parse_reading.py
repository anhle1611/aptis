import docx
import json
import glob
import re
import os
from difflib import SequenceMatcher

def clean(s):
    s = s.lower()
    s = re.sub(r'^(who\s+|now\s+i\s+)', '', s)
    s = re.sub(r'[^\w\s]', ' ', s)
    return ' '.join(s.split())

def match_ratio(q, s):
    cq = clean(q)
    cs = clean(s)
    if cq in cs or cs in cq:
        return 1.0
    wq = set(cq.split())
    ws = set(cs.split())
    if not wq or not ws: return 0.0
    jaccard = len(wq & ws) / len(wq | ws)
    seq = SequenceMatcher(None, cq, cs).ratio()
    return max(jaccard, seq)

def parse_part4_from_doc(raw_lines, ans_idx):
    test_lines = raw_lines[:ans_idx]
    ans_lines = raw_lines[ans_idx:]
    
    title = "Part 4: Choose the answer according to each person's opinion."
    topic = ""
    questions = []
    paragraphs = {}
    
    in_p4 = False
    in_paragraphs = False
    curr_person = None
    
    for line in test_lines:
        lower = line.lower()
        if 'part 4' in lower:
            in_p4 = True
            title = line
            m_top = re.search(r'topic[\s:\-]+([^\.\n]+)', line, re.I)
            if m_top: topic = m_top.group(1).strip()
            continue
        if in_p4 and ('part 5' in lower or 'matching headings' in lower):
            in_p4 = False
            break
        if in_p4:
            if 'topic' in lower and not topic:
                m_top = re.search(r'topic[\s:\-]+([^\.\n]+)', line, re.I)
                if m_top: topic = m_top.group(1).strip()
                else: topic = line.split(':', 1)[-1].strip()
                continue
            if 'đoạn văn' in lower or 'doan van' in lower:
                in_paragraphs = True
                continue
            if lower.startswith('questions:'):
                continue
            if not in_paragraphs:
                if lower.startswith('who') or re.match(r'^\d+[\.\)]\s*who', lower):
                    questions.append(re.sub(r'^\d+[\.\)]\s*', '', line).strip())
            else:
                m = re.match(r'^(?:person\s+)?([A-D])[\s:\.]*(.*)', line, re.I)
                if m and len(m.group(1)) == 1:
                    curr_person = m.group(1).upper()
                    rest = m.group(2).strip()
                    paragraphs[curr_person] = rest
                elif curr_person:
                    if paragraphs[curr_person]:
                        paragraphs[curr_person] += ' ' + line
                    else:
                        paragraphs[curr_person] = line

    in_ans_p4 = False
    statements = []
    for line in ans_lines:
        lower = line.lower()
        if 'part 4' in lower:
            in_ans_p4 = True
            if not topic:
                m_top = re.search(r'topic[\s:\-]+([^\.\n]+)', line, re.I)
                if m_top: topic = m_top.group(1).strip()
            continue
        if in_ans_p4 and ('part 5' in lower or 'part 3' in lower or 'part 1' in lower or 'part 2' in lower):
            in_ans_p4 = False
            break
        if in_ans_p4:
            m = re.match(r'^(?:person\s+)?([A-D])[\s:\.]+(.+)', line, re.I)
            if m:
                p = m.group(1).upper()
                content = m.group(2).strip()
                if len(content) < 200 or '/' in content or '–' in content or '-' in content:
                    parts = re.split(r'\s*[/–—]\s*|\s+-\s+', content)
                    for part in parts:
                        part = part.strip()
                        if part and len(part) < 120 and not part.lower().startswith('in the past'):
                            statements.append((p, part))

    q_objects = []
    for idx, q in enumerate(questions):
        best_match = None
        best_score = -1
        for p, s in statements:
            score = match_ratio(q, s)
            if score > best_score:
                best_score = score
                best_match = (p, s, score)
        q_objects.append({
            'qnum': idx + 1,
            'question': q,
            'answer': best_match[0] if best_match else '',
            'statement': best_match[1] if best_match else ''
        })

    return {
        'title': "Part 4: Choose the answer according to each person's opinion.",
        'topic': topic,
        'paragraphs': paragraphs,
        'questions': q_objects
    }

def parse_doc(filepath):
    doc = docx.Document(filepath)
    raw_lines = []
    for p in doc.paragraphs:
        for l in p.text.split('\n'):
            l = l.strip().replace('\xa0', ' ')
            if l: raw_lines.append(l)
            
    ans_idx = len(raw_lines)
    for i, line in enumerate(raw_lines):
        if re.match(r'^ANSWER\b', line, re.I):
            ans_idx = i
            break
            
    if ans_idx == len(raw_lines): return None
    
    test_data = {
        "test_name": os.path.basename(filepath).replace(".docx", ""),
        "part1": [],
        "part2": {},
        "part3": {},
        "part4": parse_part4_from_doc(raw_lines, ans_idx),
        "part5": []
    }
    
    # Parse other parts from ANSWER section
    lines = raw_lines
    current_part = None
    i = ans_idx + 1
    p1_answers = []
    
    while i < len(lines):
        line = lines[i]
        upper = line.upper()
        
        if "PART 1" in upper:
            current_part = 1
            ans_match = re.search(r'part\s*1[\.:\s]+(.*)', line, re.I)
            if ans_match:
                p1_answers = [a.strip() for a in re.split(r'[/–—\-\s]+', ans_match.group(1)) if a.strip()]
        elif "PART 2" in upper:
            current_part = 2
        elif "PART 3" in upper:
            current_part = 3
        elif "PART 4" in upper:
            current_part = 4
        elif "PART 5" in upper:
            current_part = 5
            
        elif current_part == 1:
            match = re.search(r'\((.*?/.*?/.*?)\)', line)
            if match:
                opts = [o.strip() for o in match.group(1).split('/')]
                qnum = len(test_data["part1"])
                ans_word = p1_answers[qnum] if qnum < len(p1_answers) else ""
                test_data["part1"].append({
                    "qnum": qnum + 1,
                    "question": line.replace(match.group(0), "___"),
                    "options": opts,
                    "answer": ans_word
                })
        elif current_part == 2:
            if line.startswith("0."):
                test_data["part2"]["fixed"] = line[2:].strip()
            elif "-" in line and len(line) > 50:
                test_data["part2"]["sentences"] = [s.strip() for s in line.split("-") if s.strip()]
        elif current_part == 3:
            if line.startswith("0."):
                test_data["part3"]["fixed"] = line[2:].strip()
            elif "-" in line and len(line) > 50:
                test_data["part3"]["sentences"] = [s.strip() for s in line.split("-") if s.strip()]
        elif current_part == 5:
            if len(line) < 100 and i+1 < len(lines) and len(lines[i+1]) > 50:
                header = line
                if header.startswith(tuple("ABCDEFG.")):
                    header = header.split(".", 1)[-1].strip()
                test_data["part5"].append({
                    "header": header,
                    "paragraph": lines[i+1]
                })
        i += 1
        
    return test_data

out = []
for file in sorted(glob.glob("/Users/anhlee/Downloads/source/data/reading/*.docx")):
    res = parse_doc(file)
    if res: out.append(res)
    
out.sort(key=lambda x: x["test_name"])
with open("/Users/anhlee/Downloads/source/data/reading/reading_tests.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print("Saved to reading_tests.json successfully!")
