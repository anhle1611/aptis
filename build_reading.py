import json

with open('/Users/anhlee/Downloads/source/data/reading/reading_tests.json', 'r', encoding='utf-8') as f:
    json_data = f.read()

html_template = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>APTIS Reading Practice</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<script src="https://unpkg.com/jszip/dist/jszip.min.js"></script>
<script src="https://unpkg.com/docx-preview/dist/docx-preview.min.js"></script>
<style>
  :root {{
    --bg: #0f1117; --bg2: #161b27; --surface: #1e2538;
    --border: #2a3550; --border2: #374165; --accent: #6366f1;
    --text: #e2e8f0; --text2: #94a3b8; --green: #22c55e; --red: #ef4444;
  }}
  body {{ font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 0; }}
  nav {{ background: var(--bg2); padding: 12px 24px; display: flex; gap: 24px; border-bottom: 1px solid var(--border); box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
  nav a {{ color: var(--text2); font-weight: 500; font-size: 15px; text-decoration: none; display: flex; align-items: center; gap: 6px; padding-bottom: 4px; transition: color 0.2s; }}
  nav a.active {{ color: var(--accent); font-weight: 700; border-bottom: 2px solid var(--accent); }}
  .container {{ max-width: 900px; margin: 40px auto; padding: 0 20px; }}
  
  /* Setup Area */
  .setup-card {{ background: var(--bg2); border-radius: 16px; padding: 32px; border: 1px solid var(--border); margin-bottom: 24px; }}
  .section-label {{ font-size: 14px; font-weight: 700; color: var(--text2); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 20px; }}
  .mode-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 16px; margin-bottom: 30px; }}
  .mode-btn {{ background: var(--surface); border: 2px solid var(--border2); border-radius: 12px; padding: 16px; text-align: left; cursor: pointer; color: var(--text); font-family: inherit; transition: all 0.2s; display: flex; flex-direction: column; gap: 8px; }}
  .mode-btn:hover {{ border-color: var(--accent); transform: translateY(-2px); }}
  .mode-btn.active {{ border-color: var(--accent); background: rgba(99,102,241,0.1); }}
  .btn-primary {{ background: var(--accent); color: white; border: none; padding: 16px 32px; border-radius: 12px; font-size: 16px; font-weight: 600; cursor: pointer; transition: all 0.2s; width: 100%; text-align: center; }}
  
  /* Quiz Area */
  .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }}
  .btn-home {{ background: transparent; border: 1px solid var(--border); color: var(--text); padding: 8px 16px; border-radius: 8px; cursor: pointer; display: flex; align-items: center; gap: 8px; font-weight: 500; transition: all 0.2s; }}
  .btn-home:hover {{ background: var(--surface); }}
  .quiz-title-badge {{ background: rgba(99,102,241,0.15); color: var(--accent); padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: 600; }}
  
  .part-card {{ background: var(--bg2); padding: 24px; border-radius: 12px; margin-bottom: 24px; border: 1px solid var(--border); }}
  .question-text {{ font-size: 16px; line-height: 1.6; margin-bottom: 16px; }}
  select {{ background: var(--surface); color: var(--text); padding: 8px 12px; border: 1px solid var(--border2); border-radius: 6px; font-family: 'Inter'; outline: none; font-size: 15px; margin: 4px; }}
  select:focus {{ border-color: var(--accent); }}
  select.correct {{ border-color: var(--green); background: rgba(34,197,94,0.1); }}
  select.wrong {{ border-color: var(--red); background: rgba(239,68,68,0.1); }}
  
  /* Drag and drop styles */
  .draggable-list {{ list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 10px; }}
  .draggable-item {{ background: var(--surface); padding: 16px; border-radius: 8px; border: 1px solid var(--border); cursor: grab; display: flex; align-items: center; gap: 12px; user-select: none; transition: transform 0.2s; }}
  .draggable-item.fixed {{ cursor: default; background: rgba(255,255,255,0.05); border-color: var(--border2); }}
  .draggable-item:active {{ cursor: grabbing; }}
  .drag-handle {{ color: var(--text2); font-size: 20px; cursor: grab; }}
  .draggable-item.over {{ border: 2px dashed var(--accent); }}
  
  .preview-btn {{ background: var(--surface); border: 1px solid var(--border2); color: var(--text2); padding: 4px 12px; border-radius: 6px; font-size: 12px; cursor: pointer; transition: 0.2s; margin-left: 10px; }}
  .preview-btn:hover {{ background: var(--border); color: var(--text); }}
  
  .score-chip {{ background: var(--surface); padding: 8px 16px; border-radius: 20px; border: 1px solid var(--border); font-weight: 600; display: flex; gap: 10px; align-items: center; }}
  
  .person-block {{ margin-bottom: 20px; padding: 16px; border: 1px solid var(--border2); border-radius: 8px; }}
  .person-block p {{ margin-top: 8px; color: var(--text2); line-height: 1.5; font-size: 14px; }}

  .draggable-item.correct {{ border: 2px solid #10b981 !important; background-color: rgba(16, 185, 129, 0.1) !important; }}
  .draggable-item.wrong {{ border: 2px solid #ef4444 !important; background-color: rgba(239, 68, 68, 0.1) !important; }}

</style>
</head>
<body>
<nav>
  <a href="index.html">🎧 Listening</a>
  <a href="reading.html" class="active" style="color:var(--accent); border-bottom: 2px solid var(--accent);">📖 Reading</a>
</nav>

<div class="container">
  
  <!-- Setup Area -->
  <div id="setup-area">
    <div class="setup-card">
      <div class="section-label">🎯 Chọn Phần Muốn Luyện (Reading)</div>
      <div class="mode-grid">
        <button class="mode-btn active" id="btn-mix" onclick="selectMode('mix')">🔀 Mix Đề</button>
        <button class="mode-btn" id="btn-part1" onclick="selectMode('part1')">🎯 Phần 1</button>
        <button class="mode-btn" id="btn-part2" onclick="selectMode('part2')">🧩 Phần 2</button>
        <button class="mode-btn" id="btn-part3" onclick="selectMode('part3')">🧩 Phần 3</button>
        <button class="mode-btn" id="btn-part4" onclick="selectMode('part4')">📝 Phần 4</button>
        <button class="mode-btn" id="btn-part5" onclick="selectMode('part5')">📖 Phần 5</button>
      </div>
      
      <div class="section-label">📝 Chọn Luyện Theo Từng Đề</div>
      <div class="mode-grid" id="test-grid" style="grid-template-columns: repeat(auto-fill, minmax(80px, 1fr)); gap: 10px;">
        <!-- Populated by JS -->
      </div>
      
      <div style="margin-top:20px;">
        <button class="btn-primary" onclick="startQuiz()">▶ Bắt Đầu Luyện Tập</button>
      </div>
    </div>
  </div>

  <!-- Quiz Area -->
  <div id="quiz-area" style="display:none;">
    <div class="header">
      <div style="display:flex; align-items:center; gap:20px;">
        <button class="btn-home" onclick="backToSetup()">← Quay lại</button>
        <div>
          <h2 id="quiz-title" style="margin:0; font-size:20px;">Reading</h2>
          <span id="quiz-badge" class="quiz-title-badge">Mix</span>
        </div>
      </div>
      <div class="score-chip" id="score-chip" style="display:none;">
        <span>Score: </span>
        <span id="live-score">0</span> / <span id="live-total">0</span>
      </div>
    </div>
    
    <div id="q-container"></div>
    
    <button class="btn-primary" id="submit-btn" onclick="submitQuiz()" style="margin-top:20px;">Nộp Bài</button>
  </div>

</div>

<!-- Preview Modal -->
<div id="preview-modal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.6); z-index:9999; align-items:center; justify-content:center; padding: 20px; box-sizing: border-box;">
  <div style="background:var(--bg2); width:100%; max-width:800px; height:85vh; border-radius:12px; display:flex; flex-direction:column; overflow:hidden; border:1px solid var(--border); box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
    <div style="display:flex; justify-content:space-between; align-items:center; padding:16px 20px; background:var(--surface); border-bottom:1px solid var(--border);">
      <h3 style="margin:0; font-size:16px; font-weight: 600; color:var(--text);" id="preview-title">Reading File Preview</h3>
      <div style="display:flex; gap:10px;">
        <a id="preview-download" href="#" download style="background:var(--accent); color:#fff; text-decoration:none; padding:6px 12px; border-radius:6px; font-size:13px; font-weight:600;">📥 Tải file gốc</a>
        <button onclick="document.getElementById('preview-modal').style.display='none'" style="background:var(--bg); border:1px solid var(--border); color:var(--text); font-size:18px; width:32px; height:32px; border-radius:8px; cursor:pointer;">&times;</button>
      </div>
    </div>
    <div id="docx-container" style="flex:1; width:100%; overflow:auto; background:white; padding:20px;"></div>
  </div>
</div>

<script>
let ALL_TESTS = {json_data};
let mode = 'mix';

initTestGrid();

function initTestGrid() {{
  const tGrid = document.getElementById('test-grid');
  if(!tGrid) return;
  tGrid.innerHTML = '';
  ALL_TESTS.forEach((t, i) => {{
    const btn = document.createElement('button');
    btn.className = 'mode-btn';
    btn.style.padding = '8px';
    btn.style.fontSize = '13px';
    btn.innerHTML = `Đề ${{i+1}}`;
    btn.onclick = () => startSpecificTest(i);
    tGrid.appendChild(btn);
  }});
}}

function selectMode(m) {{
  mode = m;
  document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
  if(document.getElementById('btn-'+m)) {{
    document.getElementById('btn-'+m).classList.add('active');
  }}
}}

function backToSetup() {{
  document.getElementById('quiz-area').style.display = 'none';
  document.getElementById('setup-area').style.display = 'block';
}}

function startQuiz() {{
  if(mode === 'specific') return; 
  
  document.getElementById('setup-area').style.display = 'none';
  document.getElementById('quiz-area').style.display = 'block';
  document.getElementById('score-chip').style.display = 'none';
  document.getElementById('submit-btn').style.display = 'block';
  
  const c = document.getElementById('q-container');
  c.innerHTML = '';
  
  if(mode === 'mix') {{
    if(ALL_TESTS.length > 0) renderTest(ALL_TESTS[0], c); 
  }} else {{
    ALL_TESTS.forEach(t => renderTestPart(t, mode, c));
  }}
}}

function startSpecificTest(index) {{
  mode = 'specific';
  document.getElementById('setup-area').style.display = 'none';
  document.getElementById('quiz-area').style.display = 'block';
  document.getElementById('score-chip').style.display = 'none';
  document.getElementById('submit-btn').style.display = 'block';
  
  const t = ALL_TESTS[index];
  document.getElementById('quiz-title').textContent = t.test_name;
  document.getElementById('quiz-badge').textContent = `Full Test`;
  
  const c = document.getElementById('q-container');
  c.innerHTML = '';
  renderTest(t, c);
}}

function makeSelect(options, correctAns) {{
  let opts = `<option value="">--</option>` + options.map(o => `<option value="${{o}}">${{o}}</option>`).join('');
  return `<select data-ans="${{correctAns || ''}}" onchange="checkSelect(this)">${{opts}}</select>`;
}}

function renderTestPart(t, part, container) {{
  const div = document.createElement('div');
  div.className = 'part-card';
  
  let header = `<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
    <h3 style="margin:0;">${{part.toUpperCase()}}</h3>
    <button class="preview-btn" onclick="openPreview('${{t.test_name}}')">📄 Xem File Gốc</button>
  </div>`;
  div.innerHTML = header;
  
  let content = document.createElement('div');
  
  if (part === 'part1' && t.part1 && t.part1.length > 0) {{
    let html = '';
    t.part1.forEach(q => {{
      let htmlQ = q.question.replace('___', makeSelect(q.options, q.answer));
      html += `<p>${{htmlQ}}</p>`;
    }});
    content.innerHTML = html;
  }} 
  else if ((part === 'part2' || part === 'part3') && t[part] && t[part].sentences) {{
    let pObj = t[part];
    let html = `<p style="color:var(--text2);margin-bottom:16px;">Sắp xếp các câu sau cho đúng thứ tự đoạn văn:</p>`;
    html += `<ul class="draggable-list" id="drag-${{part}}-${{t.test_name.replace(/[^a-zA-Z0-9]/g, '')}}">`;
    if(pObj.fixed) {{
      html += `<li class="draggable-item fixed"><strong>0.</strong> ${{pObj.fixed}}</li>`;
    }}
    // shuffle
    let sents = pObj.sentences.map((s, i) => ({{text: s, idx: i}}));
    sents.sort(() => Math.random() - 0.5);
    
    sents.forEach(sObj => {{
      html += `<li class="draggable-item" draggable="true" data-idx="${{sObj.idx}}">
        <span class="drag-handle">☰</span> 
        <span style="flex:1">${{sObj.text}}</span>
      </li>`;
    }});
    html += `</ul>`;
    html += `<button class="preview-btn" style="margin-top:16px;" onclick="checkDrag(this)">Kiểm tra</button>`;
    content.innerHTML = html;
    
    // Setup drag and drop
    setTimeout(() => {{
      const list = document.getElementById(`drag-${{part}}-${{t.test_name.replace(/[^a-zA-Z0-9]/g, '')}}`);
      if(!list) return;
      let dragEl = null;
      list.querySelectorAll('.draggable-item:not(.fixed)').forEach(item => {{
        item.addEventListener('dragstart', (e) => {{ dragEl = item; e.dataTransfer.effectAllowed = 'move'; }});
        item.addEventListener('dragover', (e) => {{ e.preventDefault(); e.dataTransfer.dropEffect = 'move'; item.classList.add('over'); }});
        item.addEventListener('dragleave', (e) => {{ item.classList.remove('over'); }});
        item.addEventListener('drop', (e) => {{
          e.preventDefault(); item.classList.remove('over');
          if (dragEl && dragEl !== item) {{
            let all = [...list.querySelectorAll('.draggable-item')];
            let dragIdx = all.indexOf(dragEl);
            let dropIdx = all.indexOf(item);
            if (dragIdx < dropIdx) item.after(dragEl);
            else item.before(dragEl);
            
            list.querySelectorAll('.draggable-item').forEach(li => li.classList.remove('correct', 'wrong'));
            if(list.nextElementSibling && list.nextElementSibling.tagName === 'BUTTON') {{
              list.nextElementSibling.disabled = false;
            }}
          }}
        }});
      }});
    }}, 100);
  }}
  else if (part === 'part4' && t.part4 && t.part4.length > 0) {{
    let html = `<p style="color:var(--text2);margin-bottom:16px;">Đọc đoạn văn và điền Người (A/B/C/D) vào chỗ trống phù hợp:</p>`;
    
    // Get unique people
    let uniquePeople = [...new Set(t.part4.map(p => p.person))].sort();
    
    // Shuffle the statements so they are not in order A, B, B, C, C, D, D
    let statements = [...t.part4];
    statements.sort(() => Math.random() - 0.5);
    
    // show questions
    statements.forEach((p, idx) => {{
      html += `<p style="margin-bottom:12px;"><strong>${{idx+1}}. </strong> ${{makeSelect(uniquePeople, p.person)}} ${{p.statement}}</p>`;
    }});
    
    html += `<div style="margin-top:24px; border-top:1px solid var(--border); padding-top:16px;">`;
    // Render unique paragraphs
    let renderedPeople = new Set();
    t.part4.forEach(p => {{
      if (!renderedPeople.has(p.person)) {{
        renderedPeople.add(p.person);
        html += `<div class="person-block" style="margin-bottom:16px; padding:12px; background:var(--bg2); border-radius:8px;"><strong>Person ${{p.person}}</strong><p style="margin-top:8px;">${{p.paragraph}}</p></div>`;
      }}
    }});
    html += `</div>`;
    content.innerHTML = html;
  }}
  else if (part === 'part5' && t.part5 && t.part5.length > 0) {{
    let html = `<p style="color:var(--text2);margin-bottom:16px;">Chọn Header đúng cho mỗi đoạn văn:</p>`;
    let headers = t.part5.map(p => p.header);
    
    t.part5.forEach((p, idx) => {{
      html += `<div class="person-block" style="margin-bottom:24px;">
        <div style="margin-bottom:12px;"><strong>Đoạn ${{idx+1}}: </strong> ${{makeSelect(headers, p.header)}}</div>
        <p>${{p.paragraph}}</p>
      </div>`;
    }});
    content.innerHTML = html;
  }}
  else {{
    content.innerHTML = `<p style="color:var(--text2)">Nội dung phần này không có sẵn. Vui lòng xem File Gốc.</p>`;
  }}
  
  div.appendChild(content);
  container.appendChild(div);
}}

function renderTest(t, container) {{
  ['part1', 'part2', 'part3', 'part4', 'part5'].forEach(p => renderTestPart(t, p, container));
}}


function checkSelect(sel) {{
  sel.classList.remove('correct', 'wrong');
  if(!sel.value) return;
  if(sel.value.trim().toLowerCase() === sel.dataset.ans.trim().toLowerCase()) {{
    sel.classList.add('correct');
    sel.disabled = true;
  }} else {{
    sel.classList.add('wrong');
  }}
}}

function checkDrag(btn) {{
  const list = btn.previousElementSibling;
  const items = list.querySelectorAll('.draggable-item:not(.fixed)');
  let ok = true;
  items.forEach((item, i) => {{
    item.classList.remove('correct', 'wrong');
    if (parseInt(item.dataset.idx) === i) {{
      item.classList.add('correct');
    }} else {{
      item.classList.add('wrong');
      ok = false;
    }}
  }});
  if(ok) btn.disabled = true;
}}

function submitQuiz() {{
  document.querySelectorAll('select').forEach(sel => {{
    sel.classList.remove('correct', 'wrong');
    if(sel.dataset.ans) {{
      if (sel.value.trim().toLowerCase() === sel.dataset.ans.trim().toLowerCase()) sel.classList.add('correct');
      else sel.classList.add('wrong');
    }}
  }});
  document.getElementById('submit-btn').style.display = 'none';
  window.scrollTo({{top:0, behavior:'smooth'}});
}}

function openPreview(testName) {{
  document.getElementById('preview-modal').style.display = 'flex';
  document.getElementById('preview-title').textContent = testName;
  document.getElementById('preview-download').href = 'data/reading/' + testName.replace(/ /g, '_') + '.docx';
  
  const docContainer = document.getElementById('docx-container');
  docContainer.innerHTML = '<div style="text-align:center; padding: 40px; color:black;">Đang tải file gốc...</div>';
  
  fetch('data/reading/' + testName.replace(/ /g, '_') + '.docx')
    .then(res => res.blob())
    .then(blob => {{
      docx.renderAsync(blob, docContainer);
    }}).catch(err => {{
      docContainer.innerHTML = '<div style="color:red">Lỗi tải file.</div>';
    }});
}}
</script>
</body>
</html>
"""

with open('/Users/anhlee/Downloads/Listening/reading.html', 'w', encoding='utf-8') as f:
    f.write(html_template)
with open('/Users/anhlee/Downloads/source/reading.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("reading.html updated for both locations")
