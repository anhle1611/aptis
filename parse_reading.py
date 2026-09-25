import docx
import json
import glob
import re
import os

def parse_doc(filepath):
    doc = docx.Document(filepath)
    lines = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    
    ans_idx = -1
    for i, line in enumerate(lines):
        if line.upper() == "ANSWER":
            ans_idx = i
            break
            
    if ans_idx == -1: return None
    
    test_data = {
        "test_name": os.path.basename(filepath).replace(".docx", ""),
        "part1": [],
        "part2": {},
        "part3": {},
        "part4": [],
        "part5": []
    }
    
    current_part = None
    p1_answers = []
    
    i = ans_idx + 1
    while i < len(lines):
        line = lines[i]
        upper = line.upper()
        
        if "PART 1" in upper:
            current_part = 1
        elif "PART 2" in upper:
            current_part = 2
        elif "PART 3" in upper:
            current_part = 3
        elif "PART 4" in upper:
            current_part = 4
        elif "PART 5" in upper:
            current_part = 5
            
        elif current_part == 1:
            # parse options like (market/window/shoe)
            match = re.search(r'\((.*?/.*?/.*?)\)', line)
            if match:
                opts = [o.strip() for o in match.group(1).split('/')]
                ans_word = ""
                # try to guess answer from p1_answers or context
                test_data["part1"].append({
                    "qnum": len(test_data["part1"]) + 1,
                    "question": line.replace(match.group(0), "___"),
                    "options": opts,
                    "answer": "" # will fill if we can parse it from line 62
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
        elif current_part == 4:
            if re.match(r'^(Person )?[A-D]:', line):
                person = line.split(":")[0].strip()
                statement = line.split(":", 1)[1].strip()
                # next line is usually paragraph
                if i+1 < len(lines):
                    test_data["part4"].append({
                        "person": person,
                        "statement": statement,
                        "paragraph": lines[i+1]
                    })
        elif current_part == 5:
            # Paragraphs and headers. A heuristic: Short lines are headers.
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
for file in glob.glob("/Users/anhlee/Downloads/source/data/reading/*.docx"):
    res = parse_doc(file)
    if res: out.append(res)
    
out.sort(key=lambda x: x["test_name"])
with open("/Users/anhlee/Downloads/source/data/reading/reading_tests.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print("Saved to reading_tests.json")
