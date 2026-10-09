import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="ҰБТ Тренажер",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding: 0 !important; max-width: 100% !important;}
    iframe {border: none !important;}
</style>
""", unsafe_allow_html=True)

html_code = r"""
<!DOCTYPE html>
<html lang="kk">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ҰБТ Тренажер</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
:root {
  --primary: #2563eb; --primary-dark: #1d4ed8; --success: #16a34a;
  --danger: #dc2626; --warning: #f59e0b; --bg: #f1f5f9;
  --card: #ffffff; --text: #0f172a; --text-muted: #64748b; --border: #e2e8f0; --sidebar-w: 280px;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Inter', system-ui, sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; line-height: 1.5; }
.screen { display: none; min-height: 100vh; }
.screen.active { display: block; }
.container { max-width: 720px; margin: 0 auto; padding: 40px 20px; }
.container.wide { max-width: 900px; }
.main-header { text-align: center; margin-bottom: 32px; }
.logo {
  display: inline-flex; align-items: center; justify-content: center;
  width: 64px; height: 64px; background: var(--primary); color: white;
  font-weight: 700; font-size: 22px; border-radius: 16px; margin-bottom: 16px;
}
.main-header h1 { font-size: 28px; font-weight: 700; margin-bottom: 6px; }
.main-header h2 { font-size: 24px; margin-bottom: 6px; }
.subtitle { color: var(--text-muted); font-size: 15px; }

/* Home action buttons */
.home-actions {
  display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; margin-bottom: 28px;
}
.home-actions .btn { font-size: 13px; padding: 10px 16px; }

.mode-cards { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 28px; }
.mode-card {
  background: var(--card); border: 2px solid var(--border); border-radius: 16px;
  padding: 24px 16px; text-align: center; cursor: pointer; transition: all 0.2s;
}
.mode-card:hover { border-color: var(--primary); transform: translateY(-2px); box-shadow: 0 8px 24px rgba(37,99,235,0.12); }
.mode-icon { font-size: 32px; margin-bottom: 10px; }
.mode-card h3 { font-size: 17px; margin-bottom: 6px; }
.mode-card p { font-size: 13px; color: var(--text-muted); }

.subject-select { margin-bottom: 24px; }
.subject-select.hidden { display: none; }
.subject-select h3 { margin-bottom: 14px; text-align: center; }
.subject-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 10px; margin-bottom: 20px; }
.subject-btn {
  background: var(--card); border: 2px solid var(--border); border-radius: 12px;
  padding: 12px 10px; font-size: 13px; font-weight: 500; cursor: pointer; transition: all 0.15s; text-align: center;
}
.subject-btn:hover { border-color: var(--primary); }
.subject-btn.selected { background: var(--primary); color: white; border-color: var(--primary); }

.info-box { background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 12px; padding: 16px; font-size: 13px; }
.info-box h4 { margin-bottom: 6px; color: var(--primary-dark); }

.btn {
  display: inline-flex; align-items: center; justify-content: center; gap: 6px;
  padding: 12px 22px; border-radius: 10px; font-size: 14px; font-weight: 600;
  border: none; cursor: pointer; transition: all 0.15s; font-family: inherit;
}
.btn.primary { background: var(--primary); color: white; }
.btn.primary:hover:not(:disabled) { background: var(--primary-dark); }
.btn.primary:disabled { opacity: 0.5; cursor: not-allowed; }
.btn.secondary { background: var(--card); color: var(--text); border: 1px solid var(--border); }
.btn.secondary:hover { background: var(--bg); }
.btn.danger { background: var(--danger); color: white; }
.btn.success { background: var(--success); color: white; }
.btn.warning { background: var(--warning); color: #1c1917; }
.btn.small { padding: 8px 14px; font-size: 12px; }
#start-full-btn { width: 100%; margin-bottom: 10px; }

/* Test layout */
.test-layout { display: flex; min-height: 100vh; }
.sidebar {
  width: var(--sidebar-w); background: var(--card); border-right: 1px solid var(--border);
  display: flex; flex-direction: column; position: sticky; top: 0; height: 100vh;
}
.sidebar-header {
  padding: 14px; border-bottom: 1px solid var(--border);
  display: flex; justify-content: space-between; align-items: center; font-weight: 600; font-size: 13px;
}
.sidebar-toggle { display: none; background: none; border: none; font-size: 20px; cursor: pointer; }
.question-nav {
  flex: 1; overflow-y: auto; padding: 10px;
  display: grid; grid-template-columns: repeat(5, 1fr); gap: 5px; align-content: start;
}
.q-nav-btn {
  width: 100%; aspect-ratio: 1; border: 1px solid var(--border); border-radius: 8px;
  background: var(--bg); font-size: 12px; font-weight: 500; cursor: pointer;
  transition: all 0.15s; display: flex; align-items: center; justify-content: center;
}
.q-nav-btn:hover { border-color: var(--primary); }
.q-nav-btn.current { border-color: var(--primary); background: #dbeafe; color: var(--primary); font-weight: 700; }
.q-nav-btn.answered { background: #dcfce7; border-color: #86efac; color: var(--success); }
.q-nav-btn.flagged { background: #fef3c7; border-color: #fcd34d; }
.q-nav-btn.answered.flagged { background: linear-gradient(135deg, #dcfce7 50%, #fef3c7 50%); }
.q-nav-btn.wrong { background: #fee2e2; border-color: #fca5a5; color: var(--danger); }
.sidebar-footer { padding: 14px; border-top: 1px solid var(--border); }

.test-main { flex: 1; padding: 20px 28px; max-width: 800px; }
.test-topbar {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 20px; flex-wrap: wrap; gap: 10px;
}
.progress-bar-wrap {
  flex: 1; min-width: 180px; background: #e2e8f0; border-radius: 20px; height: 10px; overflow: hidden;
}
.progress-bar-fill { height: 100%; background: var(--primary); border-radius: 20px; transition: width 0.3s; }
.q-progress-text {
  font-size: 15px; font-weight: 700; color: var(--primary);
  background: #eff6ff; padding: 6px 14px; border-radius: 20px; white-space: nowrap;
}
.timer {
  font-size: 24px; font-weight: 700; font-variant-numeric: tabular-nums;
  color: var(--primary); background: #eff6ff; padding: 6px 16px; border-radius: 12px;
}
.timer.warning { color: var(--warning); background: #fffbeb; }
.timer.danger { color: var(--danger); background: #fef2f2; animation: pulse 1s infinite; }
@keyframes pulse { 50% { opacity: 0.7; } }

.question-card {
  background: var(--card); border-radius: 16px; padding: 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06); margin-bottom: 20px;
}
.q-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; }
.q-number {
  font-size: 13px; font-weight: 600; color: var(--primary);
  background: #eff6ff; padding: 4px 12px; border-radius: 20px;
}
.flag-btn {
  background: none; border: 1px solid var(--border); border-radius: 8px;
  padding: 5px 10px; cursor: pointer; font-size: 15px;
}
.flag-btn.active { background: #fef3c7; border-color: #fcd34d; }
.q-text { font-size: 16px; margin-bottom: 20px; line-height: 1.6; }
.options { display: flex; flex-direction: column; gap: 8px; }
.option {
  display: flex; align-items: flex-start; gap: 10px; padding: 12px 14px;
  border: 2px solid var(--border); border-radius: 12px; cursor: pointer;
  transition: all 0.15s; background: var(--card);
}
.option:hover { border-color: #93c5fd; background: #f8fafc; }
.option.selected { border-color: var(--primary); background: #eff6ff; }
.option-letter {
  width: 26px; height: 26px; border-radius: 50%; background: var(--bg);
  display: flex; align-items: center; justify-content: center;
  font-weight: 600; font-size: 12px; flex-shrink: 0; color: var(--text-muted);
}
.option.selected .option-letter { background: var(--primary); color: white; }
.option-text { flex: 1; padding-top: 2px; font-size: 14px; }
.nav-buttons { display: flex; justify-content: space-between; gap: 10px; }

/* Results */
.score-circle {
  width: 130px; height: 130px; border-radius: 50%;
  background: linear-gradient(135deg, #2563eb, #3b82f6); color: white;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  margin: 20px auto; font-size: 38px; font-weight: 700;
  box-shadow: 0 8px 32px rgba(37,99,235,0.3);
}
.score-circle small { font-size: 14px; font-weight: 400; opacity: 0.85; }
.results-breakdown { background: var(--card); border-radius: 16px; padding: 6px; margin-bottom: 24px; }
.result-row {
  display: flex; justify-content: space-between; align-items: center;
  padding: 12px 14px; border-bottom: 1px solid var(--border);
}
.result-row:last-child { border-bottom: none; }
.result-row .subject-name { font-weight: 500; font-size: 14px; }
.result-row .subject-score { font-weight: 700; color: var(--primary); }
.results-actions { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; }

/* Review */
.review-item {
  background: var(--card); border-radius: 12px; padding: 16px; margin-bottom: 12px;
  border-left: 4px solid var(--border);
}
.review-item.correct { border-left-color: var(--success); }
.review-item.wrong { border-left-color: var(--danger); }
.review-item .rev-header { display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 12px; color: var(--text-muted); }
.review-item .rev-q { font-weight: 500; margin-bottom: 10px; font-size: 14px; }
.review-item .rev-answer { font-size: 13px; padding: 7px 10px; border-radius: 8px; margin-bottom: 5px; }
.review-item .rev-answer.user { background: #fef2f2; }
.review-item .rev-answer.correct-ans { background: #f0fdf4; }

/* History & Mistakes cards */
.card-list { display: flex; flex-direction: column; gap: 12px; }
.hist-card, .mistake-card {
  background: var(--card); border: 1px solid var(--border); border-radius: 14px;
  padding: 16px; display: flex; justify-content: space-between; align-items: center; gap: 12px;
}
.hist-card .info h4 { font-size: 15px; margin-bottom: 4px; }
.hist-card .info p { font-size: 12px; color: var(--text-muted); }
.hist-score { font-size: 20px; font-weight: 700; color: var(--primary); white-space: nowrap; }

/* Add question panel */
.add-panel {
  background: var(--card); border-radius: 16px; padding: 24px;
  border: 1px solid var(--border); margin-bottom: 20px;
}
.add-panel h3 { margin-bottom: 16px; font-size: 18px; }
.form-group { margin-bottom: 14px; }
.form-group label { display: block; font-size: 13px; font-weight: 600; margin-bottom: 6px; color: var(--text-muted); }
.form-group input, .form-group select, .form-group textarea {
  width: 100%; padding: 10px 12px; border: 1px solid var(--border); border-radius: 10px;
  font-size: 14px; font-family: inherit; background: var(--bg);
}
.form-group textarea { min-height: 70px; resize: vertical; }
.opt-row { display: flex; gap: 8px; margin-bottom: 8px; align-items: center; }
.opt-row input[type="text"] { flex: 1; }
.opt-row input[type="radio"] { width: 18px; height: 18px; accent-color: var(--primary); }
.form-actions { display: flex; gap: 10px; margin-top: 16px; flex-wrap: wrap; }

.empty-state { text-align: center; padding: 40px 20px; color: var(--text-muted); }
.empty-state .icon { font-size: 40px; margin-bottom: 12px; }

@media (max-width: 768px) {
  .mode-cards { grid-template-columns: 1fr; }
  .sidebar { position: fixed; left: -100%; z-index: 100; transition: left 0.3s; width: 85%; max-width: 300px; }
  .sidebar.open { left: 0; }
  .sidebar-toggle { display: block; }
  .test-main { padding: 14px; }
  .timer { font-size: 20px; padding: 5px 12px; }
  .question-card { padding: 16px; }
  .home-actions { flex-direction: column; }
}
  </style>
</head>
<body>

<!-- ========== HOME ========== -->
<div id="home-screen" class="screen active">
  <div class="container">
    <header class="main-header">
      <div class="logo">ҰБТ</div>
      <h1>ҰБТ Тренажер</h1>
      <p class="subtitle">Өз тесттеріңізбен дайындалыңыз</p>
    </header>

    <div class="home-actions">
      <button class="btn secondary" onclick="showHistory()">📋 Тесттерді қарау</button>
      <button class="btn warning" onclick="showMistakes()">❌ Қатемен жұмыс</button>
      <button class="btn success" onclick="showAddPanel()">➕ Сұрақ қосу</button>
    </div>

    <div class="mode-cards">
      <div class="mode-card" onclick="startFullTest()">
        <div class="mode-icon">📋</div>
        <h3>Толық ҰБТ</h3>
        <p>5 пән • 120 сұрақ • 240 мин<br>Макс. 140 балл</p>
      </div>
      <div class="mode-card" onclick="showSubjectSelect()">
        <div class="mode-icon">📚</div>
        <h3>Пән бойынша</h3>
        <p>Бір пәнді таңдап<br>жаттығыңыз</p>
      </div>
    </div>

    <div id="subject-select" class="subject-select hidden">
      <h3>Пәнді таңдаңыз</h3>
      <div class="subject-grid" id="subject-grid"></div>
    </div>

    <div class="info-box">
      <h4>📌 Кеңес</h4>
      <p>«Сұрақ қосу» арқылы өз тесттеріңізді қосыңыз. Қателер автоматты сақталады.</p>
    </div>
  </div>
</div>

<!-- ========== PROFILE SELECT ========== -->
<div id="profile-select-screen" class="screen">
  <div class="container">
    <header class="main-header">
      <h2>Бейіндік пәндерді таңдаңыз</h2>
      <p class="subtitle">Екі пән таңдау керек</p>
    </header>
    <div class="subject-grid" id="profile-grid"></div>
    <button id="start-full-btn" class="btn primary" disabled onclick="confirmFullTest()">Тестті бастау</button>
    <button class="btn secondary" onclick="goHome()">Артқа</button>
  </div>
</div>

<!-- ========== TEST ========== -->
<div id="test-screen" class="screen">
  <div class="test-layout">
    <aside class="sidebar" id="sidebar">
      <div class="sidebar-header">
        <span id="current-subject-name">Пән</span>
        <button class="sidebar-toggle" onclick="toggleSidebar()">☰</button>
      </div>
      <div class="question-nav" id="question-nav"></div>
      <div class="sidebar-footer">
        <button class="btn danger small" onclick="finishTest()">Тестті аяқтау</button>
      </div>
    </aside>
    <main class="test-main">
      <div class="test-topbar">
        <div class="q-progress-text" id="q-progress-text">Сұрақ 1 / 20</div>
        <div class="progress-bar-wrap"><div class="progress-bar-fill" id="progress-bar" style="width:0%"></div></div>
        <div class="timer" id="timer">04:00:00</div>
      </div>
      <div class="question-card">
        <div class="q-header">
          <span class="q-number" id="q-number">Сұрақ 1</span>
          <button class="flag-btn" id="flag-btn" onclick="toggleFlag()">🚩</button>
        </div>
        <div class="q-text" id="q-text"></div>
        <div class="options" id="options"></div>
      </div>
      <div class="nav-buttons">
        <button class="btn secondary" id="prev-btn" onclick="prevQuestion()">← Алдыңғы</button>
        <button class="btn primary" id="next-btn" onclick="nextQuestion()">Келесі →</button>
      </div>
    </main>
  </div>
</div>

<!-- ========== RESULTS ========== -->
<div id="results-screen" class="screen">
  <div class="container">
    <header class="main-header">
      <h1>Нәтижеңіз</h1>
      <div class="score-circle">
        <span id="total-score">0</span>
        <small>/ <span id="max-score">140</span></small>
      </div>
    </header>
    <div class="results-breakdown" id="results-breakdown"></div>
    <div class="results-actions">
      <button class="btn primary" onclick="reviewAnswers()">Жауаптарды қарау</button>
      <button class="btn warning" onclick="startMistakesFromLast()">Қателерді шешу</button>
      <button class="btn secondary" onclick="goHome()">Басты бетке</button>
    </div>
  </div>
</div>

<!-- ========== REVIEW ========== -->
<div id="review-screen" class="screen">
  <div class="container wide">
    <header class="main-header">
      <h2>Жауаптарды қарау</h2>
      <button class="btn secondary" onclick="showResults()">Нәтижеге қайту</button>
    </header>
    <div id="review-list"></div>
  </div>
</div>

<!-- ========== HISTORY ========== -->
<div id="history-screen" class="screen">
  <div class="container">
    <header class="main-header">
      <h2>📋 Тесттерді қарау</h2>
      <p class="subtitle">Өткен нәтижелеріңіз</p>
    </header>
    <div id="history-list" class="card-list"></div>
    <div style="text-align:center;margin-top:24px">
      <button class="btn secondary" onclick="goHome()">Артқа</button>
    </div>
  </div>
</div>

<!-- ========== MISTAKES ========== -->
<div id="mistakes-screen" class="screen">
  <div class="container">
    <header class="main-header">
      <h2>❌ Қатемен жұмыс</h2>
      <p class="subtitle">Қате шешілген сұрақтар</p>
    </header>
    <div id="mistakes-list" class="card-list"></div>
    <div style="text-align:center;margin-top:20px;display:flex;gap:10px;justify-content:center;flex-wrap:wrap">
      <button class="btn primary" id="start-mistakes-btn" onclick="startMistakesTest()" style="display:none">Қателерді шешу</button>
      <button class="btn danger small" onclick="clearMistakes()">Тазалау</button>
      <button class="btn secondary" onclick="goHome()">Артқа</button>
    </div>
  </div>
</div>

<!-- ========== ADD QUESTION ========== -->
<div id="add-screen" class="screen">
  <div class="container">
    <header class="main-header">
      <h2>➕ Сұрақ қосу</h2>
      <p class="subtitle">Өз тесттеріңізді қосыңыз</p>
    </header>
    <div class="add-panel">
      <div class="form-group">
        <label>Пән</label>
        <select id="add-subject"></select>
      </div>
      <div class="form-group">
        <label>Сұрақ мәтіні</label>
        <textarea id="add-text" placeholder="Сұрақты жазыңыз..."></textarea>
      </div>
      <div class="form-group">
        <label>Нұсқалар (дұрысын белгілеңіз)</label>
        <div class="opt-row"><input type="radio" name="correct" value="0" checked><input type="text" id="opt0" placeholder="A нұсқасы"></div>
        <div class="opt-row"><input type="radio" name="correct" value="1"><input type="text" id="opt1" placeholder="B нұсқасы"></div>
        <div class="opt-row"><input type="radio" name="correct" value="2"><input type="text" id="opt2" placeholder="C нұсқасы"></div>
        <div class="opt-row"><input type="radio" name="correct" value="3"><input type="text" id="opt3" placeholder="D нұсқасы"></div>
      </div>
      <div class="form-actions">
        <button class="btn primary" onclick="addQuestion()">Сақтау</button>
        <button class="btn secondary" onclick="goHome()">Артқа</button>
      </div>
    </div>
    <div id="add-success" style="display:none;text-align:center;color:var(--success);font-weight:600;margin-top:12px">✓ Сұрақ қосылды!</div>
  </div>
</div>

<script>
/* ========== DATA ========== */
const DEFAULT_SUBJECTS = {
  history: { id:"history", name:"Қазақстан тарихы", short:"Тарих", type:"mandatory", maxPoints:20, questions:[
    {id:"h1",text:"Қазақ хандығы қай жылы құрылды?",options:["1456 ж.","1465 ж.","1480 ж.","1511 ж."],correct:1,points:1},
    {id:"h2",text:"Абылай ханның шын есімі кім болған?",options:["Әбілмансұр","Тәуке","Қасым","Хақназар"],correct:0,points:1},
    {id:"h3",text:"«Жеті жарғы» заңдар жинағын кім құрастырған?",options:["Қасым хан","Есім хан","Тәуке хан","Абылай хан"],correct:2,points:1},
    {id:"h4",text:"Қазақстан Республикасының Тәуелсіздік күні қашан?",options:["16 желтоқсан","25 қазан","30 тамыз","1 мамыр"],correct:0,points:1},
    {id:"h5",text:"Алаш Орда үкіметі қай жылы құрылды?",options:["1916 ж.","1917 ж.","1918 ж.","1920 ж."],correct:1,points:1}
  ]},
  reading: { id:"reading", name:"Оқу сауаттылығы", short:"Оқу сауат.", type:"mandatory", maxPoints:10, questions:[
    {id:"r1",text:"Мәтін бойынша: «Кітап — білімнің қайнар көзі». Негізгі идеясы?",options:["Кітап қымбат зат","Кітап арқылы білім алуға болады","Кітап оқу қиын","Кітаптар ескірген"],correct:1,points:1},
    {id:"r2",text:"«Ғылым — адамзаттың ең үлкен жетістігі». Негізгі сөз?",options:["Ғылым","адамзаттың","үлкен","жетістігі"],correct:0,points:1}
  ]},
  mathlit: { id:"mathlit", name:"Математикалық сауаттылық", short:"Мат. сауат.", type:"mandatory", maxPoints:10, questions:[
    {id:"m1",text:"Бір кітап 1500 тг. 4 кітап қанша?",options:["4500 тг","6000 тг","5500 тг","5000 тг"],correct:1,points:1},
    {id:"m2",text:"Тіктөртбұрыш 12×5 см. Периметрі?",options:["34 см","60 см","17 см","30 см"],correct:0,points:1}
  ]},
  math: { id:"math", name:"Математика", short:"Математика", type:"profile", maxPoints:50, questions:[
    {id:"math1",text:"2x + 5 = 17. x = ?",options:["x = 5","x = 6","x = 7","x = 12"],correct:1,points:1},
    {id:"math2",text:"f(x) = x² − 4x + 3. f(2) = ?",options:["−1","0","1","3"],correct:0,points:1},
    {id:"math3",text:"Үшбұрыш бұрыштарының қосындысы?",options:["90°","180°","270°","360°"],correct:1,points:1}
  ]},
  physics: { id:"physics", name:"Физика", short:"Физика", type:"profile", maxPoints:50, questions:[
    {id:"ph1",text:"Жарық жылдамдығы (вакуум)?",options:["3×10⁸ м/с","3×10⁶ м/с","3×10¹⁰ м/с","300 м/с"],correct:0,points:1},
    {id:"ph2",text:"Ньютонның 2-заңы?",options:["F = ma","E = mc²","P = mv","W = Fs"],correct:0,points:1}
  ]},
  chemistry: { id:"chemistry", name:"Химия", short:"Химия", type:"profile", maxPoints:50, questions:[
    {id:"ch1",text:"Сутегінің атомдық нөмірі?",options:["1","2","8","16"],correct:0,points:1},
    {id:"ch2",text:"H₂O байланыс түрі?",options:["Иондық","Коваленттік полярлы","Металдық","Сутектік"],correct:1,points:1}
  ]},
  biology: { id:"biology", name:"Биология", short:"Биология", type:"profile", maxPoints:50, questions:[
    {id:"bio1",text:"Жасушаның энергетикалық станциясы?",options:["Ядро","Митохондрия","Рибосома","Гольджи аппараты"],correct:1,points:1},
    {id:"bio2",text:"ДНҚ толық атауы?",options:["Дезоксирибонуклеин қышқылы","Рибонуклеин қышқылы","Аденозинтрифосфат","Аминқышқылы"],correct:0,points:1}
  ]},
  geography: { id:"geography", name:"География", short:"География", type:"profile", maxPoints:50, questions:[
    {id:"geo1",text:"Қазақстанның ең биік нүктесі?",options:["Хан Тәңірі","Белуха","Талғар","Мұзтау"],correct:0,points:1}
  ]},
  informatics: { id:"informatics", name:"Информатика", short:"Информатика", type:"profile", maxPoints:50, questions:[
    {id:"inf1",text:"1 байт = ? бит",options:["4","8","16","32"],correct:1,points:1},
    {id:"inf2",text:"HTML не үшін?",options:["Мәліметтер базасы","Веб-беттерді белгілеу","Бағдарламалау тілі","ОЖ"],correct:1,points:1}
  ]},
  english: { id:"english", name:"Ағылшын тілі", short:"Ағылшын", type:"profile", maxPoints:50, questions:[
    {id:"en1",text:"She _____ to school every day.",options:["go","goes","going","gone"],correct:1,points:1}
  ]},
  kazakh: { id:"kazakh", name:"Қазақ тілі", short:"Қазақ тілі", type:"profile", maxPoints:50, questions:[
    {id:"kz1",text:"«Кітап» сөзінің көпше түрі?",options:["Кітаптар","Кітаптарды","Кітапқа","Кітаптың"],correct:0,points:1}
  ]},
  worldhistory: { id:"worldhistory", name:"Дүниежүзі тарихы", short:"Дж. тарих", type:"profile", maxPoints:50, questions:[
    {id:"wh1",text:"2-дүниежүзілік соғыс аяқталды?",options:["1941 ж.","1943 ж.","1945 ж.","1947 ж."],correct:2,points:1}
  ]},
  law: { id:"law", name:"Құқық негіздері", short:"Құқық", type:"profile", maxPoints:50, questions:[
    {id:"law1",text:"ҚР Конституциясы қабылданды?",options:["1991 ж.","1993 ж.","1995 ж.","1998 ж."],correct:2,points:1}
  ]}
};

function loadSubjects() {
  try {
    const saved = localStorage.getItem('ubt_subjects');
    if (saved) return JSON.parse(saved);
  } catch(e) {}
  return JSON.parse(JSON.stringify(DEFAULT_SUBJECTS));
}
function saveSubjects() {
  try { localStorage.setItem('ubt_subjects', JSON.stringify(SUBJECTS)); } catch(e) {}
}
let SUBJECTS = loadSubjects();
let PROFILE_SUBJECTS = Object.values(SUBJECTS).filter(s => s.type === "profile");

/* ========== STATE ========== */
let state = {
  mode: null, subjects: [], questions: [], currentIndex: 0,
  answers: {}, flags: {}, timerSeconds: 0, timerInterval: null,
  selectedProfiles: [], lastResult: null, isMistakesMode: false
};

function showScreen(id) {
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  document.getElementById(id).classList.add('active');
}
function goHome() {
  stopTimer();
  state = { mode:null, subjects:[], questions:[], currentIndex:0, answers:{}, flags:{}, timerSeconds:0, timerInterval:null, selectedProfiles:[], lastResult: state.lastResult, isMistakesMode:false };
  document.getElementById('subject-select').classList.add('hidden');
  showScreen('home-screen');
}

/* ========== HOME ========== */
function showSubjectSelect() {
  const grid = document.getElementById('subject-grid');
  grid.innerHTML = '';
  Object.values(SUBJECTS).forEach(subj => {
    const btn = document.createElement('button');
    btn.className = 'subject-btn';
    btn.textContent = subj.name + ` (${subj.questions.length})`;
    btn.onclick = () => startSubjectTest(subj.id);
    grid.appendChild(btn);
  });
  document.getElementById('subject-select').classList.remove('hidden');
}

function startSubjectTest(subjectId) {
  const subj = SUBJECTS[subjectId];
  if (!subj || !subj.questions.length) { alert('Бұл пәнде сұрақ жоқ!'); return; }
  state.mode = 'subject';
  state.subjects = [subj];
  state.questions = subj.questions.map(q => ({...q, subjectId: subj.id, subjectName: subj.name}));
  state.currentIndex = 0; state.answers = {}; state.flags = {};
  state.timerSeconds = Math.max(subj.questions.length * 90, 1800);
  state.isMistakesMode = false;
  startTest();
}

function startFullTest() {
  state.selectedProfiles = [];
  PROFILE_SUBJECTS = Object.values(SUBJECTS).filter(s => s.type === "profile");
  const grid = document.getElementById('profile-grid');
  grid.innerHTML = '';
  PROFILE_SUBJECTS.forEach(subj => {
    const btn = document.createElement('button');
    btn.className = 'subject-btn';
    btn.textContent = subj.name;
    btn.dataset.id = subj.id;
    btn.onclick = () => toggleProfile(btn, subj.id);
    grid.appendChild(btn);
  });
  document.getElementById('start-full-btn').disabled = true;
  showScreen('profile-select-screen');
}

function toggleProfile(btn, id) {
  const idx = state.selectedProfiles.indexOf(id);
  if (idx >= 0) { state.selectedProfiles.splice(idx,1); btn.classList.remove('selected'); }
  else {
    if (state.selectedProfiles.length >= 2) {
      const firstId = state.selectedProfiles.shift();
      document.querySelector(`#profile-grid .subject-btn[data-id="${firstId}"]`)?.classList.remove('selected');
    }
    state.selectedProfiles.push(id); btn.classList.add('selected');
  }
  document.getElementById('start-full-btn').disabled = state.selectedProfiles.length !== 2;
}

function confirmFullTest() {
  if (state.selectedProfiles.length !== 2) return;
  const subjects = [SUBJECTS.history, SUBJECTS.reading, SUBJECTS.mathlit, SUBJECTS[state.selectedProfiles[0]], SUBJECTS[state.selectedProfiles[1]]];
  const empty = subjects.filter(s => !s.questions || !s.questions.length);
  if (empty.length) { alert('Сұрақ жоқ: ' + empty.map(s=>s.name).join(', ')); return; }
  state.mode = 'full'; state.subjects = subjects; state.questions = [];
  subjects.forEach(subj => { subj.questions.forEach(q => { state.questions.push({...q, subjectId:subj.id, subjectName:subj.name}); }); });
  state.currentIndex = 0; state.answers = {}; state.flags = {};
  state.timerSeconds = 240 * 60; state.isMistakesMode = false;
  startTest();
}

/* ========== TEST ========== */
function startTest() {
  showScreen('test-screen');
  renderQuestionNav(); renderQuestion(); startTimer(); updateProgress();
}
function renderQuestionNav() {
  const nav = document.getElementById('question-nav');
  nav.innerHTML = '';
  state.questions.forEach((q,i) => {
    const btn = document.createElement('button');
    btn.className = 'q-nav-btn'; btn.textContent = i+1;
    btn.onclick = () => goToQuestion(i);
    nav.appendChild(btn);
  });
  updateNavStyles();
}
function updateNavStyles() {
  document.querySelectorAll('.q-nav-btn').forEach((btn,i) => {
    btn.classList.remove('current','answered','flagged');
    if (i === state.currentIndex) btn.classList.add('current');
    const q = state.questions[i];
    if (state.answers[q.id] !== undefined) btn.classList.add('answered');
    if (state.flags[q.id]) btn.classList.add('flagged');
  });
}
function renderQuestion() {
  const q = state.questions[state.currentIndex];
  if (!q) return;
  document.getElementById('current-subject-name').textContent = q.subjectName || 'Пән';
  document.getElementById('q-number').textContent = `Сұрақ ${state.currentIndex+1}`;
  document.getElementById('q-text').textContent = q.text;
  document.getElementById('flag-btn').classList.toggle('active', !!state.flags[q.id]);
  const opts = document.getElementById('options');
  opts.innerHTML = '';
  const letters = ['A','B','C','D','E','F'];
  q.options.forEach((opt,i) => {
    const div = document.createElement('div');
    div.className = 'option' + (state.answers[q.id]===i ? ' selected' : '');
    div.onclick = () => selectOption(i);
    div.innerHTML = `<span class="option-letter">${letters[i]}</span><span class="option-text">${opt}</span>`;
    opts.appendChild(div);
  });
  document.getElementById('prev-btn').disabled = state.currentIndex === 0;
  document.getElementById('next-btn').textContent = state.currentIndex === state.questions.length-1 ? 'Аяқтау' : 'Келесі →';
  updateNavStyles(); updateProgress();
}
function selectOption(index) {
  state.answers[state.questions[state.currentIndex].id] = index;
  renderQuestion();
}
function toggleFlag() {
  const q = state.questions[state.currentIndex];
  state.flags[q.id] = !state.flags[q.id];
  renderQuestion();
}
function nextQuestion() {
  if (state.currentIndex < state.questions.length-1) { state.currentIndex++; renderQuestion(); }
  else finishTest();
}
function prevQuestion() {
  if (state.currentIndex > 0) { state.currentIndex--; renderQuestion(); }
}
function goToQuestion(index) {
  state.currentIndex = index; renderQuestion();
  document.getElementById('sidebar').classList.remove('open');
}
function updateProgress() {
  const total = state.questions.length;
  const cur = state.currentIndex + 1;
  const answered = Object.keys(state.answers).length;
  document.getElementById('q-progress-text').textContent = `Сұрақ ${cur} / ${total}`;
  document.getElementById('progress-bar').style.width = ((answered / total) * 100) + '%';
}

/* ========== TIMER ========== */
function startTimer() {
  stopTimer(); updateTimerDisplay();
  state.timerInterval = setInterval(() => {
    state.timerSeconds--; updateTimerDisplay();
    if (state.timerSeconds <= 0) { stopTimer(); alert('Уақыт аяқталды!'); finishTest(); }
  }, 1000);
}
function stopTimer() {
  if (state.timerInterval) { clearInterval(state.timerInterval); state.timerInterval = null; }
}
function updateTimerDisplay() {
  const t = Math.max(0, state.timerSeconds);
  const h = Math.floor(t/3600), m = Math.floor((t%3600)/60), s = t%60;
  const el = document.getElementById('timer');
  el.textContent = `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;
  el.classList.remove('warning','danger');
  if (t <= 300) el.classList.add('danger');
  else if (t <= 900) el.classList.add('warning');
}

/* ========== FINISH & RESULTS ========== */
function finishTest() {
  if (!confirm('Тестті аяқтауға сенімдісіз бе?')) return;
  stopTimer();
  calculateAndShowResults();
}
function calculateAndShowResults() {
  let totalScore = 0, maxScore = 0;
  const breakdown = [];
  const wrongQs = [];

  state.subjects.forEach(subj => {
    let score = 0, max = 0;
    subj.questions.forEach(q => {
      max += q.points || 1;
      if (state.answers[q.id] === q.correct) score += q.points || 1;
      else if (state.answers[q.id] !== undefined || true) {
        // collect wrong (unanswered count as wrong for mistakes)
        if (state.answers[q.id] !== q.correct) {
          wrongQs.push({...q, subjectId: subj.id, subjectName: subj.name, userAnswer: state.answers[q.id]});
        }
      }
    });
    if (subj.maxPoints && score > subj.maxPoints) score = subj.maxPoints;
    totalScore += score;
    maxScore += subj.maxPoints || max;
    breakdown.push({ name: subj.name, score, max: subj.maxPoints || max });
  });

  // Save mistakes
  if (!state.isMistakesMode && wrongQs.length) {
    saveMistakes(wrongQs);
  }

  // Save history
  const result = {
    date: new Date().toLocaleString('kk-KZ'),
    score: totalScore, max: maxScore,
    mode: state.mode, subjects: breakdown,
    answers: {...state.answers}, questions: state.questions.map(q=>({id:q.id,text:q.text,options:q.options,correct:q.correct,subjectName:q.subjectName}))
  };
  state.lastResult = result;
  saveHistory(result);

  document.getElementById('total-score').textContent = totalScore;
  document.getElementById('max-score').textContent = maxScore;
  document.getElementById('results-breakdown').innerHTML = breakdown.map(b =>
    `<div class="result-row"><span class="subject-name">${b.name}</span><span class="subject-score">${b.score} / ${b.max}</span></div>`
  ).join('');
  showScreen('results-screen');
}
function showResults() { showScreen('results-screen'); }

function reviewAnswers() {
  const list = document.getElementById('review-list');
  list.innerHTML = '';
  state.questions.forEach((q,i) => {
    const userAns = state.answers[q.id];
    const isCorrect = userAns === q.correct;
    const letters = ['A','B','C','D','E','F'];
    const item = document.createElement('div');
    item.className = 'review-item ' + (isCorrect ? 'correct' : 'wrong');
    item.innerHTML = `
      <div class="rev-header"><span>${q.subjectName||''} • Сұрақ ${i+1}</span><span>${isCorrect?'✓ Дұрыс':'✗ Қате'}</span></div>
      <div class="rev-q">${q.text}</div>
      ${userAns!==undefined?`<div class="rev-answer user">Сіздің жауабыңыз: <strong>${letters[userAns]}) ${q.options[userAns]}</strong></div>`:`<div class="rev-answer user">Жауап берілмеген</div>`}
      ${!isCorrect?`<div class="rev-answer correct-ans">Дұрыс жауап: <strong>${letters[q.correct]}) ${q.options[q.correct]}</strong></div>`:''}
    `;
    list.appendChild(item);
  });
  showScreen('review-screen');
}

/* ========== HISTORY ========== */
function loadHistory() {
  try { return JSON.parse(localStorage.getItem('ubt_history')||'[]'); } catch(e){ return []; }
}
function saveHistory(result) {
  const hist = loadHistory();
  hist.unshift(result);
  if (hist.length > 30) hist.pop();
  try { localStorage.setItem('ubt_history', JSON.stringify(hist)); } catch(e){}
}
function showHistory() {
  const list = document.getElementById('history-list');
  const hist = loadHistory();
  if (!hist.length) {
    list.innerHTML = '<div class="empty-state"><div class="icon">📭</div><p>Әзірге тест тапсырылмаған</p></div>';
  } else {
    list.innerHTML = hist.map((h,i) => `
      <div class="hist-card">
        <div class="info">
          <h4>${h.mode==='full'?'Толық ҰБТ':(h.mode==='mistakes'?'Қателер':'Пән бойынша')}</h4>
          <p>${h.date}</p>
        </div>
        <div class="hist-score">${h.score} / ${h.max}</div>
      </div>
    `).join('');
  }
  showScreen('history-screen');
}

/* ========== MISTAKES ========== */
function loadMistakes() {
  try { return JSON.parse(localStorage.getItem('ubt_mistakes')||'[]'); } catch(e){ return []; }
}
function saveMistakes(wrongQs) {
  let existing = loadMistakes();
  const ids = new Set(existing.map(q => q.id));
  wrongQs.forEach(q => {
    if (!ids.has(q.id)) { existing.push(q); ids.add(q.id); }
  });
  try { localStorage.setItem('ubt_mistakes', JSON.stringify(existing)); } catch(e){}
}
function clearMistakes() {
  if (!confirm('Барлық қателерді өшіру керек пе?')) return;
  localStorage.removeItem('ubt_mistakes');
  showMistakes();
}
function showMistakes() {
  const list = document.getElementById('mistakes-list');
  const mistakes = loadMistakes();
  const btn = document.getElementById('start-mistakes-btn');
  if (!mistakes.length) {
    list.innerHTML = '<div class="empty-state"><div class="icon">🎉</div><p>Қате жоқ! Жарайсыз!</p></div>';
    btn.style.display = 'none';
  } else {
    list.innerHTML = mistakes.map(q => `
      <div class="mistake-card">
        <div class="info" style="flex:1">
          <h4 style="font-size:14px;margin-bottom:4px">${q.text.substring(0,80)}${q.text.length>80?'...':''}</h4>
          <p style="font-size:12px;color:var(--text-muted)">${q.subjectName||''}</p>
        </div>
      </div>
    `).join('');
    btn.style.display = 'inline-flex';
  }
  showScreen('mistakes-screen');
}
function startMistakesTest() {
  const mistakes = loadMistakes();
  if (!mistakes.length) return;
  state.mode = 'mistakes';
  state.subjects = [{ name: 'Қателер', questions: mistakes, maxPoints: mistakes.length }];
  state.questions = mistakes.map(q => ({...q}));
  state.currentIndex = 0; state.answers = {}; state.flags = {};
  state.timerSeconds = Math.max(mistakes.length * 90, 600);
  state.isMistakesMode = true;
  startTest();
}
function startMistakesFromLast() {
  // start mistakes from current wrong answers
  const wrong = [];
  state.questions.forEach(q => {
    if (state.answers[q.id] !== q.correct) wrong.push(q);
  });
  if (!wrong.length) { alert('Қате жоқ!'); return; }
  state.mode = 'mistakes';
  state.subjects = [{ name: 'Қателер', questions: wrong, maxPoints: wrong.length }];
  state.questions = wrong.map(q => ({...q}));
  state.currentIndex = 0; state.answers = {}; state.flags = {};
  state.timerSeconds = Math.max(wrong.length * 90, 600);
  state.isMistakesMode = true;
  startTest();
}

/* ========== ADD QUESTION ========== */
function showAddPanel() {
  const sel = document.getElementById('add-subject');
  sel.innerHTML = Object.values(SUBJECTS).map(s =>
    `<option value="${s.id}">${s.name} (${s.questions.length})</option>`
  ).join('');
  document.getElementById('add-text').value = '';
  ['opt0','opt1','opt2','opt3'].forEach(id => document.getElementById(id).value = '');
  document.querySelector('input[name="correct"][value="0"]').checked = true;
  document.getElementById('add-success').style.display = 'none';
  showScreen('add-screen');
}
function addQuestion() {
  const subjId = document.getElementById('add-subject').value;
  const text = document.getElementById('add-text').value.trim();
  const opts = [0,1,2,3].map(i => document.getElementById('opt'+i).value.trim());
  const correct = parseInt(document.querySelector('input[name="correct"]:checked').value);

  if (!text) { alert('Сұрақ мәтінін жазыңыз!'); return; }
  if (opts.some(o => !o)) { alert('Барлық 4 нұсқаны толтырыңыз!'); return; }

  const q = {
    id: 'custom_' + Date.now(),
    text, options: opts, correct, points: 1
  };
  SUBJECTS[subjId].questions.push(q);
  saveSubjects();
  document.getElementById('add-success').style.display = 'block';
  document.getElementById('add-text').value = '';
  ['opt0','opt1','opt2','opt3'].forEach(id => document.getElementById(id).value = '');
  // update count in select
  const sel = document.getElementById('add-subject');
  sel.innerHTML = Object.values(SUBJECTS).map(s =>
    `<option value="${s.id}" ${s.id===subjId?'selected':''}>${s.name} (${s.questions.length})</option>`
  ).join('');
}

function toggleSidebar() { document.getElementById('sidebar').classList.toggle('open'); }
document.addEventListener('click', e => {
  const sidebar = document.getElementById('sidebar');
  if (sidebar.classList.contains('open') && !sidebar.contains(e.target) && !e.target.classList.contains('sidebar-toggle')) {
    sidebar.classList.remove('open');
  }
});
</script>
</body>
</html>
"""

components.html(html_code, height=950, scrolling=True)
