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

html_code = open("index.html", encoding="utf-8").read() if False else r'''
<!DOCTYPE html>
<html lang="kk">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ҰБТ Тренажер</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
:root{--primary:#2563eb;--primary-dark:#1d4ed8;--success:#16a34a;--danger:#dc2626;--warning:#f59e0b;--bg:#f1f5f9;--card:#ffffff;--text:#0f172a;--text-muted:#64748b;--border:#e2e8f0;--sidebar-w:280px}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Inter',system-ui,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;line-height:1.5}
.screen{display:none;min-height:100vh}.screen.active{display:block}
.container{max-width:720px;margin:0 auto;padding:40px 20px}.container.wide{max-width:900px}
.main-header{text-align:center;margin-bottom:40px}
.logo{display:inline-flex;align-items:center;justify-content:center;width:64px;height:64px;background:var(--primary);color:#fff;font-weight:700;font-size:22px;border-radius:16px;margin-bottom:16px}
.main-header h1{font-size:32px;font-weight:700;margin-bottom:8px}
.main-header h2{font-size:26px;margin-bottom:8px}
.subtitle{color:var(--text-muted);font-size:16px}
.mode-cards{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:32px}
.mode-card{background:var(--card);border:2px solid var(--border);border-radius:16px;padding:28px 20px;text-align:center;cursor:pointer;transition:.2s}
.mode-card:hover{border-color:var(--primary);transform:translateY(-2px);box-shadow:0 8px 24px rgba(37,99,235,.12)}
.mode-icon{font-size:36px;margin-bottom:12px}
.mode-card h3{font-size:18px;margin-bottom:8px}
.mode-card p{font-size:14px;color:var(--text-muted)}
.subject-select{margin-bottom:32px}.subject-select.hidden{display:none}
.subject-select h3{margin-bottom:16px;text-align:center}
.subject-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px;margin-bottom:24px}
.subject-btn{background:var(--card);border:2px solid var(--border);border-radius:12px;padding:14px 12px;font-size:14px;font-weight:500;cursor:pointer;transition:.15s;text-align:center}
.subject-btn:hover{border-color:var(--primary)}
.subject-btn.selected{background:var(--primary);color:#fff;border-color:var(--primary)}
.info-box{background:#eff6ff;border:1px solid #bfdbfe;border-radius:12px;padding:20px;font-size:14px}
.info-box h4{margin-bottom:8px;color:var(--primary-dark)}
.info-box code{background:#dbeafe;padding:2px 6px;border-radius:4px;font-size:13px}
.btn{display:inline-flex;align-items:center;justify-content:center;padding:12px 24px;border-radius:10px;font-size:15px;font-weight:600;border:none;cursor:pointer;transition:.15s;font-family:inherit}
.btn.primary{background:var(--primary);color:#fff}
.btn.primary:hover:not(:disabled){background:var(--primary-dark)}
.btn.primary:disabled{opacity:.5;cursor:not-allowed}
.btn.secondary{background:var(--card);color:var(--text);border:1px solid var(--border)}
.btn.secondary:hover{background:var(--bg)}
.btn.danger{background:var(--danger);color:#fff}
.btn.small{padding:8px 16px;font-size:13px}
#start-full-btn{width:100%;margin-bottom:12px}
.test-layout{display:flex;min-height:100vh}
.sidebar{width:var(--sidebar-w);background:var(--card);border-right:1px solid var(--border);display:flex;flex-direction:column;position:sticky;top:0;height:100vh}
.sidebar-header{padding:16px;border-bottom:1px solid var(--border);display:flex;justify-content:space-between;align-items:center;font-weight:600;font-size:14px}
.sidebar-toggle{display:none;background:none;border:none;font-size:20px;cursor:pointer}
.question-nav{flex:1;overflow-y:auto;padding:12px;display:grid;grid-template-columns:repeat(5,1fr);gap:6px;align-content:start}
.q-nav-btn{width:100%;aspect-ratio:1;border:1px solid var(--border);border-radius:8px;background:var(--bg);font-size:13px;font-weight:500;cursor:pointer;transition:.15s;display:flex;align-items:center;justify-content:center}
.q-nav-btn:hover{border-color:var(--primary)}
.q-nav-btn.current{border-color:var(--primary);background:#dbeafe;color:var(--primary);font-weight:700}
.q-nav-btn.answered{background:#dcfce7;border-color:#86efac;color:var(--success)}
.q-nav-btn.flagged{background:#fef3c7;border-color:#fcd34d}
.q-nav-btn.answered.flagged{background:linear-gradient(135deg,#dcfce7 50%,#fef3c7 50%)}
.sidebar-footer{padding:16px;border-top:1px solid var(--border)}
.test-main{flex:1;padding:24px 32px;max-width:800px}
.test-topbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px}
.timer{font-size:28px;font-weight:700;font-variant-numeric:tabular-nums;color:var(--primary);background:#eff6ff;padding:8px 20px;border-radius:12px}
.timer.warning{color:var(--warning);background:#fffbeb}
.timer.danger{color:var(--danger);background:#fef2f2;animation:pulse 1s infinite}
@keyframes pulse{50%{opacity:.7}}
.progress-info{font-size:14px;color:var(--text-muted)}
.question-card{background:var(--card);border-radius:16px;padding:28px;box-shadow:0 1px 3px rgba(0,0,0,.06);margin-bottom:24px}
.q-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px}
.q-number{font-size:14px;font-weight:600;color:var(--primary);background:#eff6ff;padding:4px 12px;border-radius:20px}
.flag-btn{background:none;border:1px solid var(--border);border-radius:8px;padding:6px 10px;cursor:pointer;font-size:16px}
.flag-btn.active{background:#fef3c7;border-color:#fcd34d}
.q-text{font-size:17px;margin-bottom:24px;line-height:1.6}
.options{display:flex;flex-direction:column;gap:10px}
.option{display:flex;align-items:flex-start;gap:12px;padding:14px 16px;border:2px solid var(--border);border-radius:12px;cursor:pointer;transition:.15s;background:var(--card)}
.option:hover{border-color:#93c5fd;background:#f8fafc}
.option.selected{border-color:var(--primary);background:#eff6ff}
.option-letter{width:28px;height:28px;border-radius:50%;background:var(--bg);display:flex;align-items:center;justify-content:center;font-weight:600;font-size:13px;flex-shrink:0;color:var(--text-muted)}
.option.selected .option-letter{background:var(--primary);color:#fff}
.option-text{flex:1;padding-top:2px;font-size:15px}
.nav-buttons{display:flex;justify-content:space-between;gap:12px}
.score-circle{width:140px;height:140px;border-radius:50%;background:linear-gradient(135deg,#2563eb,#3b82f6);color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;margin:24px auto;font-size:42px;font-weight:700;box-shadow:0 8px 32px rgba(37,99,235,.3)}
.score-circle small{font-size:16px;font-weight:400;opacity:.85}
.results-breakdown{background:var(--card);border-radius:16px;padding:8px;margin-bottom:32px}
.result-row{display:flex;justify-content:space-between;align-items:center;padding:14px 16px;border-bottom:1px solid var(--border)}
.result-row:last-child{border-bottom:none}
.result-row .subject-name{font-weight:500}
.result-row .subject-score{font-weight:700;color:var(--primary)}
.results-actions{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.review-item{background:var(--card);border-radius:12px;padding:20px;margin-bottom:16px;border-left:4px solid var(--border)}
.review-item.correct{border-left-color:var(--success)}
.review-item.wrong{border-left-color:var(--danger)}
.review-item .rev-header{display:flex;justify-content:space-between;margin-bottom:10px;font-size:13px;color:var(--text-muted)}
.review-item .rev-q{font-weight:500;margin-bottom:12px}
.review-item .rev-answer{font-size:14px;padding:8px 12px;border-radius:8px;margin-bottom:6px}
.review-item .rev-answer.user{background:#fef2f2}
.review-item .rev-answer.correct-ans{background:#f0fdf4}
@media(max-width:768px){.mode-cards{grid-template-columns:1fr}.sidebar{position:fixed;left:-100%;z-index:100;transition:left .3s;width:85%;max-width:300px}.sidebar.open{left:0}.sidebar-toggle{display:block}.test-main{padding:16px}.timer{font-size:22px;padding:6px 14px}.question-card{padding:20px}}
  </style>
</head>
<body>
  <div id="home-screen" class="screen active">
    <div class="container">
      <header class="main-header">
        <div class="logo">ҰБТ</div>
        <h1>ҰБТ Тренажер</h1>
        <p class="subtitle">Өз тесттеріңізбен дайындалыңыз</p>
      </header>
      <div class="mode-cards">
        <div class="mode-card" onclick="startFullTest()">
          <div class="mode-icon">📋</div>
          <h3>Толық ҰБТ</h3>
          <p>5 пән • 120 сұрақ • 240 минут<br>Макс. 140 балл</p>
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
        <h4>📌 Қалай өз тесттеріңізді қосуға болады?</h4>
        <p>Кодтағы SUBJECTS объектісін ашып, сұрақтарды қосыңыз.</p>
      </div>
    </div>
  </div>

  <div id="profile-select-screen" class="screen">
    <div class="container">
      <header class="main-header">
        <h2>Бейіндік пәндерді таңдаңыз</h2>
        <p>Екі пән таңдау керек</p>
      </header>
      <div class="subject-grid" id="profile-grid"></div>
      <button id="start-full-btn" class="btn primary" disabled onclick="confirmFullTest()">Тестті бастау</button>
      <button class="btn secondary" onclick="goHome()">Артқа</button>
    </div>
  </div>

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
          <div class="timer" id="timer">04:00:00</div>
          <div class="progress-info"><span id="answered-count">0</span> / <span id="total-count">0</span> жауап берілді</div>
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
        <button class="btn secondary" onclick="goHome()">Басты бетке</button>
      </div>
    </div>
  </div>

  <div id="review-screen" class="screen">
    <div class="container wide">
      <header class="main-header">
        <h2>Жауаптарды қарау</h2>
        <button class="btn secondary" onclick="showResults()">Нәтижеге қайту</button>
      </header>
      <div id="review-list"></div>
    </div>
  </div>

<script>
const SUBJECTS={history:{id:"history",name:"Қазақстан тарихы",short:"Тарих",type:"mandatory",maxPoints:20,questions:[{id:"h1",text:"Қазақ хандығы қай жылы құрылды?",options:["1456 ж.","1465 ж.","1480 ж.","1511 ж."],correct:1,points:1},{id:"h2",text:"Абылай ханның шын есімі кім болған?",options:["Әбілмансұр","Тәуке","Қасым","Хақназар"],correct:0,points:1},{id:"h3",text:"«Жеті жарғы» заңдар жинағын кім құрастырған?",options:["Қасым хан","Есім хан","Тәуке хан","Абылай хан"],correct:2,points:1},{id:"h4",text:"Қазақстан Республикасының Тәуелсіздік күні қашан?",options:["16 желтоқсан","25 қазан","30 тамыз","1 мамыр"],correct:0,points:1},{id:"h5",text:"Алаш Орда үкіметі қай жылы құрылды?",options:["1916 ж.","1917 ж.","1918 ж.","1920 ж."],correct:1,points:1}]},reading:{id:"reading",name:"Оқу сауаттылығы",short:"Оқу сауат.",type:"mandatory",maxPoints:10,questions:[{id:"r1",text:"Мәтін бойынша: «Кітап — білімнің қайнар көзі». Бұл сөйлемнің негізгі идеясы қандай?",options:["Кітап қымбат зат","Кітап арқылы білім алуға болады","Кітап оқу қиын","Кітаптар ескірген"],correct:1,points:1},{id:"r2",text:"Төмендегі сөйлемдегі негізгі сөзді көрсетіңіз: «Ғылым — адамзаттың ең үлкен жетістігі».",options:["Ғылым","адамзаттың","үлкен","жетістігі"],correct:0,points:1}]},mathlit:{id:"mathlit",name:"Математикалық сауаттылық",short:"Мат. сауат.",type:"mandatory",maxPoints:10,questions:[{id:"m1",text:"Егер бір кітаптың бағасы 1500 теңге болса, 4 кітап қанша тұрады?",options:["4500 тг","6000 тг","5500 тг","5000 тг"],correct:1,points:1},{id:"m2",text:"Тіктөртбұрыштың ұзындығы 12 см, ені 5 см. Периметрі қанша?",options:["34 см","60 см","17 см","30 см"],correct:0,points:1}]},math:{id:"math",name:"Математика",short:"Математика",type:"profile",maxPoints:50,questions:[{id:"math1",text:"Теңдеуді шешіңіз: 2x + 5 = 17",options:["x = 5","x = 6","x = 7","x = 12"],correct:1,points:1},{id:"math2",text:"Функция f(x) = x² − 4x + 3. f(2) мәнін табыңыз.",options:["−1","0","1","3"],correct:0,points:1},{id:"math3",text:"Үшбұрыштың бұрыштарының қосындысы неге тең?",options:["90°","180°","270°","360°"],correct:1,points:1}]},physics:{id:"physics",name:"Физика",short:"Физика",type:"profile",maxPoints:50,questions:[{id:"ph1",text:"Жарықтың вакуумдағы жылдамдығы шамамен неге тең?",options:["3×10⁸ м/с","3×10⁶ м/с","3×10¹⁰ м/с","300 м/с"],correct:0,points:1},{id:"ph2",text:"Ньютонның екінші заңы қалай жазылады?",options:["F = ma","E = mc²","P = mv","W = Fs"],correct:0,points:1}]},chemistry:{id:"chemistry",name:"Химия",short:"Химия",type:"profile",maxPoints:50,questions:[{id:"ch1",text:"Сутегінің атомдық нөмірі қанша?",options:["1","2","8","16"],correct:0,points:1},{id:"ch2",text:"H₂O молекуласындағы байланыс түрі қандай?",options:["Иондық","Коваленттік полярлы","Металдық","Сутектік"],correct:1,points:1}]},biology:{id:"biology",name:"Биология",short:"Биология",type:"profile",maxPoints:50,questions:[{id:"bio1",text:"Жасушаның энергетикалық станциясы деп нені атайды?",options:["Ядро","Митохондрия","Рибосома","Гольджи аппараты"],correct:1,points:1},{id:"bio2",text:"ДНҚ-ның толық атауы қандай?",options:["Дезоксирибонуклеин қышқылы","Рибонуклеин қышқылы","Аденозинтрифосфат","Аминқышқылы"],correct:0,points:1}]},geography:{id:"geography",name:"География",short:"География",type:"profile",maxPoints:50,questions:[{id:"geo1",text:"Қазақстанның ең биік нүктесі қайда орналасқан?",options:["Хан Тәңірі","Белуха","Талғар","Мұзтау"],correct:0,points:1}]},informatics:{id:"informatics",name:"Информатика",short:"Информатика",type:"profile",maxPoints:50,questions:[{id:"inf1",text:"1 байт қанша битке тең?",options:["4","8","16","32"],correct:1,points:1},{id:"inf2",text:"HTML не үшін қолданылады?",options:["Мәліметтер базасын басқару","Веб-беттерді белгілеу","Бағдарламалау тілі","Операциялық жүйе"],correct:1,points:1}]},english:{id:"english",name:"Ағылшын тілі",short:"Ағылшын",type:"profile",maxPoints:50,questions:[{id:"en1",text:"Choose the correct form: She _____ to school every day.",options:["go","goes","going","gone"],correct:1,points:1}]},kazakh:{id:"kazakh",name:"Қазақ тілі",short:"Қазақ тілі",type:"profile",maxPoints:50,questions:[{id:"kz1",text:"«Кітап» сөзінің көпше түрі қандай?",options:["Кітаптар","Кітаптарды","Кітапқа","Кітаптың"],correct:0,points:1}]},worldhistory:{id:"worldhistory",name:"Дүниежүзі тарихы",short:"Дж. тарих",type:"profile",maxPoints:50,questions:[{id:"wh1",text:"Екінші дүниежүзілік соғыс қай жылы аяқталды?",options:["1941 ж.","1943 ж.","1945 ж.","1947 ж."],correct:2,points:1}]},law:{id:"law",name:"Құқық негіздері",short:"Құқық",type:"profile",maxPoints:50,questions:[{id:"law1",text:"Қазақстан Республикасының Конституциясы қай жылы қабылданды?",options:["1991 ж.","1993 ж.","1995 ж.","1998 ж."],correct:2,points:1}]}};
const PROFILE_SUBJECTS=Object.values(SUBJECTS).filter(s=>s.type==="profile");
let state={mode:null,subjects:[],questions:[],currentIndex:0,answers:{},flags:{},timerSeconds:0,timerInterval:null,selectedProfiles:[]};
function showScreen(id){document.querySelectorAll('.screen').forEach(s=>s.classList.remove('active'));document.getElementById(id).classList.add('active')}
function goHome(){stopTimer();state={mode:null,subjects:[],questions:[],currentIndex:0,answers:{},flags:{},timerSeconds:0,timerInterval:null,selectedProfiles:[]};document.getElementById('subject-select').classList.add('hidden');showScreen('home-screen')}
function showSubjectSelect(){const grid=document.getElementById('subject-grid');grid.innerHTML='';Object.values(SUBJECTS).forEach(subj=>{const btn=document.createElement('button');btn.className='subject-btn';btn.textContent=subj.name;btn.onclick=()=>startSubjectTest(subj.id);grid.appendChild(btn)});document.getElementById('subject-select').classList.remove('hidden')}
function startSubjectTest(subjectId){const subj=SUBJECTS[subjectId];if(!subj||subj.questions.length===0){alert('Бұл пәнде әзірге сұрақ жоқ!');return}state.mode='subject';state.subjects=[subj];state.questions=subj.questions.map(q=>({...q,subjectId:subj.id,subjectName:subj.name}));state.currentIndex=0;state.answers={};state.flags={};state.timerSeconds=Math.max(subj.questions.length*90,1800);startTest()}
function startFullTest(){state.selectedProfiles=[];const grid=document.getElementById('profile-grid');grid.innerHTML='';PROFILE_SUBJECTS.forEach(subj=>{const btn=document.createElement('button');btn.className='subject-btn';btn.textContent=subj.name;btn.dataset.id=subj.id;btn.onclick=()=>toggleProfile(btn,subj.id);grid.appendChild(btn)});document.getElementById('start-full-btn').disabled=true;showScreen('profile-select-screen')}
function toggleProfile(btn,id){const idx=state.selectedProfiles.indexOf(id);if(idx>=0){state.selectedProfiles.splice(idx,1);btn.classList.remove('selected')}else{if(state.selectedProfiles.length>=2){const firstId=state.selectedProfiles.shift();document.querySelector(`#profile-grid .subject-btn[data-id="${firstId}"]`)?.classList.remove('selected')}state.selectedProfiles.push(id);btn.classList.add('selected')}document.getElementById('start-full-btn').disabled=state.selectedProfiles.length!==2}
function confirmFullTest(){if(state.selectedProfiles.length!==2)return;const subjects=[SUBJECTS.history,SUBJECTS.reading,SUBJECTS.mathlit,SUBJECTS[state.selectedProfiles[0]],SUBJECTS[state.selectedProfiles[1]]];const empty=subjects.filter(s=>!s.questions||s.questions.length===0);if(empty.length){alert('Келесі пәндерде сұрақ жоқ: '+empty.map(s=>s.name).join(', '));return}state.mode='full';state.subjects=subjects;state.questions=[];subjects.forEach(subj=>{subj.questions.forEach(q=>{state.questions.push({...q,subjectId:subj.id,subjectName:subj.name})})});state.currentIndex=0;state.answers={};state.flags={};state.timerSeconds=240*60;startTest()}
function startTest(){showScreen('test-screen');renderQuestionNav();renderQuestion();startTimer();updateProgress()}
function renderQuestionNav(){const nav=document.getElementById('question-nav');nav.innerHTML='';state.questions.forEach((q,i)=>{const btn=document.createElement('button');btn.className='q-nav-btn';btn.textContent=i+1;btn.onclick=()=>goToQuestion(i);nav.appendChild(btn)});updateNavStyles()}
function updateNavStyles(){document.querySelectorAll('.q-nav-btn').forEach((btn,i)=>{btn.classList.remove('current','answered','flagged');if(i===state.currentIndex)btn.classList.add('current');const q=state.questions[i];if(state.answers[q.id]!==undefined)btn.classList.add('answered');if(state.flags[q.id])btn.classList.add('flagged')})}
function renderQuestion(){const q=state.questions[state.currentIndex];if(!q)return;document.getElementById('current-subject-name').textContent=q.subjectName;document.getElementById('q-number').textContent=`Сұрақ ${state.currentIndex+1} / ${state.questions.length}`;document.getElementById('q-text').textContent=q.text;document.getElementById('flag-btn').classList.toggle('active',!!state.flags[q.id]);const opts=document.getElementById('options');opts.innerHTML='';const letters=['A','B','C','D','E','F'];q.options.forEach((opt,i)=>{const div=document.createElement('div');div.className='option'+(state.answers[q.id]===i?' selected':'');div.onclick=()=>selectOption(i);div.innerHTML=`<span class="option-letter">${letters[i]}</span><span class="option-text">${opt}</span>`;opts.appendChild(div)});document.getElementById('prev-btn').disabled=state.currentIndex===0;document.getElementById('next-btn').textContent=state.currentIndex===state.questions.length-1?'Аяқтау':'Келесі →';updateNavStyles();updateProgress()}
function selectOption(index){state.answers[state.questions[state.currentIndex].id]=index;renderQuestion()}
function toggleFlag(){const q=state.questions[state.currentIndex];state.flags[q.id]=!state.flags[q.id];renderQuestion()}
function nextQuestion(){if(state.currentIndex<state.questions.length-1){state.currentIndex++;renderQuestion()}else finishTest()}
function prevQuestion(){if(state.currentIndex>0){state.currentIndex--;renderQuestion()}}
function goToQuestion(index){state.currentIndex=index;renderQuestion();document.getElementById('sidebar').classList.remove('open')}
function updateProgress(){document.getElementById('answered-count').textContent=Object.keys(state.answers).length;document.getElementById('total-count').textContent=state.questions.length}
function startTimer(){stopTimer();updateTimerDisplay();state.timerInterval=setInterval(()=>{state.timerSeconds--;updateTimerDisplay();if(state.timerSeconds<=0){stopTimer();alert('Уақыт аяқталды!');finishTest()}},1000)}
function stopTimer(){if(state.timerInterval){clearInterval(state.timerInterval);state.timerInterval=null}}
function updateTimerDisplay(){const t=Math.max(0,state.timerSeconds);const h=Math.floor(t/3600),m=Math.floor((t%3600)/60),s=t%60;const el=document.getElementById('timer');el.textContent=`${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;el.classList.remove('warning','danger');if(t<=300)el.classList.add('danger');else if(t<=900)el.classList.add('warning')}
function finishTest(){if(!confirm('Тестті аяқтауға сенімдісіз бе?'))return;stopTimer();calculateAndShowResults()}
function calculateAndShowResults(){let totalScore=0,maxScore=0;const breakdown=[];state.subjects.forEach(subj=>{let score=0,max=0;subj.questions.forEach(q=>{max+=q.points||1;if(state.answers[q.id]===q.correct)score+=q.points||1});if(subj.maxPoints&&score>subj.maxPoints)score=subj.maxPoints;totalScore+=score;maxScore+=subj.maxPoints||max;breakdown.push({name:subj.name,score,max:subj.maxPoints||max})});document.getElementById('total-score').textContent=totalScore;document.getElementById('max-score').textContent=maxScore;document.getElementById('results-breakdown').innerHTML=breakdown.map(b=>`<div class="result-row"><span class="subject-name">${b.name}</span><span class="subject-score">${b.score} / ${b.max}</span></div>`).join('');showScreen('results-screen')}
function showResults(){showScreen('results-screen')}
function reviewAnswers(){const list=document.getElementById('review-list');list.innerHTML='';state.questions.forEach((q,i)=>{const userAns=state.answers[q.id];const isCorrect=userAns===q.correct;const letters=['A','B','C','D','E','F'];const item=document.createElement('div');item.className='review-item '+(isCorrect?'correct':'wrong');item.innerHTML=`<div class="rev-header"><span>${q.subjectName} • Сұрақ ${i+1}</span><span>${isCorrect?'✓ Дұрыс':'✗ Қате'}</span></div><div class="rev-q">${q.text}</div>${userAns!==undefined?`<div class="rev-answer user">Сіздің жауабыңыз: <strong>${letters[userAns]}) ${q.options[userAns]}</strong></div>`:`<div class="rev-answer user">Жауап берілмеген</div>`}${!isCorrect?`<div class="rev-answer correct-ans">Дұрыс жауап: <strong>${letters[q.correct]}) ${q.options[q.correct]}</strong></div>`:''}`;list.appendChild(item)});showScreen('review-screen')}
function toggleSidebar(){document.getElementById('sidebar').classList.toggle('open')}
document.addEventListener('click',e=>{const sidebar=document.getElementById('sidebar');if(sidebar.classList.contains('open')&&!sidebar.contains(e.target)&&!e.target.classList.contains('sidebar-toggle')){sidebar.classList.remove('open')}});
</script>
</body>
</html>
'''

components.html(html_code, height=900, scrolling=True)
