import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ҰБТ Тренажер", page_icon="📝", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""<style>#MainMenu,footer,header{visibility:hidden}.block-container{padding:0!important;max-width:100%!important}iframe{border:none!important}</style>""", unsafe_allow_html=True)

html_code = r"""
<!DOCTYPE html>
<html lang="kk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ҰБТ Тренажер</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{--p:#2563eb;--pd:#1d4ed8;--ok:#16a34a;--err:#dc2626;--warn:#f59e0b;--bg:#f1f5f9;--c:#fff;--t:#0f172a;--m:#64748b;--b:#e2e8f0}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Inter',system-ui,sans-serif;background:var(--bg);color:var(--t);min-height:100vh;line-height:1.5}
.screen{display:none;min-height:100vh}.screen.active{display:block}
.wrap{max-width:760px;margin:0 auto;padding:32px 16px}
.wrap.wide{max-width:920px}
.hdr{text-align:center;margin-bottom:28px}
.logo{display:inline-flex;align-items:center;justify-content:center;width:56px;height:56px;background:var(--p);color:#fff;font-weight:700;font-size:20px;border-radius:14px;margin-bottom:12px}
.hdr h1{font-size:26px;font-weight:700;margin-bottom:4px}
.hdr h2{font-size:22px;margin-bottom:4px}
.sub{color:var(--m);font-size:14px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;padding:11px 20px;border-radius:10px;font-size:14px;font-weight:600;border:none;cursor:pointer;font-family:inherit;transition:.15s}
.btn-p{background:var(--p);color:#fff}.btn-p:hover{background:var(--pd)}.btn-p:disabled{opacity:.45;cursor:not-allowed}
.btn-s{background:var(--c);color:var(--t);border:1px solid var(--b)}.btn-s:hover{background:var(--bg)}
.btn-d{background:var(--err);color:#fff}.btn-ok{background:var(--ok);color:#fff}.btn-w{background:var(--warn);color:#1c1917}
.btn-sm{padding:7px 12px;font-size:12px}
.row{display:flex;gap:10px;flex-wrap:wrap;justify-content:center}
.card{background:var(--c);border:1px solid var(--b);border-radius:14px;padding:18px;margin-bottom:12px}
.card h3{font-size:16px;margin-bottom:6px}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.mode{background:var(--c);border:2px solid var(--b);border-radius:14px;padding:22px 14px;text-align:center;cursor:pointer;transition:.2s}
.mode:hover{border-color:var(--p);transform:translateY(-2px);box-shadow:0 6px 20px rgba(37,99,235,.1)}
.mode .ic{font-size:30px;margin-bottom:8px}
.mode h3{font-size:15px;margin-bottom:4px}
.mode p{font-size:12px;color:var(--m)}
.fg{margin-bottom:14px}
.fg label{display:block;font-size:12px;font-weight:600;color:var(--m);margin-bottom:5px}
.fg input,.fg select,.fg textarea{width:100%;padding:10px 12px;border:1px solid var(--b);border-radius:10px;font-size:14px;font-family:inherit;background:var(--bg)}
.fg textarea{min-height:72px;resize:vertical}
.opt{display:flex;gap:8px;align-items:center;margin-bottom:8px}
.opt input[type=text]{flex:1}
.opt input[type=radio]{width:18px;height:18px;accent-color:var(--p)}
.badge{display:inline-block;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:600}
.badge-pub{background:#dbeafe;color:var(--p)}.badge-priv{background:#f1f5f9;color:var(--m)}
.list{display:flex;flex-direction:column;gap:10px}
.item{background:var(--c);border:1px solid var(--b);border-radius:12px;padding:14px 16px;display:flex;justify-content:space-between;align-items:center;gap:12px}
.item .info{flex:1;min-width:0}
.item .info h4{font-size:14px;margin-bottom:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.item .info p{font-size:12px;color:var(--m)}
.item .acts{display:flex;gap:6px;flex-shrink:0;flex-wrap:wrap}
.empty{text-align:center;padding:40px 16px;color:var(--m)}.empty .ic{font-size:36px;margin-bottom:10px}
.profile-bar{display:flex;justify-content:space-between;align-items:center;padding:12px 16px;background:var(--c);border-bottom:1px solid var(--b);margin-bottom:20px}
.profile-bar .name{font-weight:600;font-size:14px}
.avatar{width:36px;height:36px;border-radius:50%;background:var(--p);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px}
.tlay{display:flex;min-height:100vh}
.side{width:260px;background:var(--c);border-right:1px solid var(--b);display:flex;flex-direction:column;position:sticky;top:0;height:100vh}
.side-h{padding:12px;border-bottom:1px solid var(--b);display:flex;justify-content:space-between;align-items:center;font-weight:600;font-size:13px}
.side-tog{display:none;background:none;border:none;font-size:20px;cursor:pointer}
.qnav{flex:1;overflow-y:auto;padding:8px;display:grid;grid-template-columns:repeat(5,1fr);gap:4px;align-content:start}
.qn{aspect-ratio:1;border:1px solid var(--b);border-radius:7px;background:var(--bg);font-size:11px;font-weight:500;cursor:pointer;display:flex;align-items:center;justify-content:center}
.qn.cur{border-color:var(--p);background:#dbeafe;color:var(--p);font-weight:700}
.qn.ans{background:#dcfce7;border-color:#86efac;color:var(--ok)}
.qn.flg{background:#fef3c7;border-color:#fcd34d}
.side-f{padding:12px;border-top:1px solid var(--b)}
.tmain{flex:1;padding:18px 24px;max-width:780px}
.ttop{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;flex-wrap:wrap;gap:8px}
.prog-t{font-size:14px;font-weight:700;color:var(--p);background:#eff6ff;padding:5px 12px;border-radius:20px}
.prog-w{flex:1;min-width:120px;background:#e2e8f0;border-radius:20px;height:8px;overflow:hidden}
.prog-f{height:100%;background:var(--p);border-radius:20px;transition:width .3s}
.timer{font-size:22px;font-weight:700;font-variant-numeric:tabular-nums;color:var(--p);background:#eff6ff;padding:5px 14px;border-radius:10px}
.timer.warn{color:var(--warn);background:#fffbeb}.timer.dang{color:var(--err);background:#fef2f2;animation:pulse 1s infinite}
@keyframes pulse{50%{opacity:.7}}
.qc{background:var(--c);border-radius:14px;padding:20px;box-shadow:0 1px 3px rgba(0,0,0,.05);margin-bottom:16px}
.qh{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}
.qnum{font-size:12px;font-weight:600;color:var(--p);background:#eff6ff;padding:3px 10px;border-radius:20px}
.flag{background:none;border:1px solid var(--b);border-radius:7px;padding:4px 8px;cursor:pointer;font-size:14px}
.flag.on{background:#fef3c7;border-color:#fcd34d}
.qt{font-size:15px;margin-bottom:16px;line-height:1.6}
.opts{display:flex;flex-direction:column;gap:7px}
.op{display:flex;align-items:flex-start;gap:10px;padding:11px 12px;border:2px solid var(--b);border-radius:11px;cursor:pointer;transition:.15s}
.op:hover{border-color:#93c5fd;background:#f8fafc}
.op.sel{border-color:var(--p);background:#eff6ff}
.ol{width:24px;height:24px;border-radius:50%;background:var(--bg);display:flex;align-items:center;justify-content:center;font-weight:600;font-size:11px;flex-shrink:0;color:var(--m)}
.op.sel .ol{background:var(--p);color:#fff}
.ot{flex:1;padding-top:1px;font-size:13px}
.navb{display:flex;justify-content:space-between;gap:10px}
.score-c{width:120px;height:120px;border-radius:50%;background:linear-gradient(135deg,#2563eb,#3b82f6);color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;margin:16px auto;font-size:34px;font-weight:700;box-shadow:0 6px 24px rgba(37,99,235,.25)}
.score-c small{font-size:13px;font-weight:400;opacity:.85}
.res-row{display:flex;justify-content:space-between;padding:11px 14px;border-bottom:1px solid var(--b);font-size:14px}
.res-row:last-child{border-bottom:none}
.rev{background:var(--c);border-radius:11px;padding:14px;margin-bottom:10px;border-left:4px solid var(--b)}
.rev.ok{border-left-color:var(--ok)}.rev.bad{border-left-color:var(--err)}
.rev .rh{display:flex;justify-content:space-between;margin-bottom:6px;font-size:11px;color:var(--m)}
.rev .rq{font-weight:500;margin-bottom:8px;font-size:13px}
.rev .ra{font-size:12px;padding:6px 10px;border-radius:7px;margin-bottom:4px}
.rev .ra.u{background:#fef2f2}.rev .ra.c{background:#f0fdf4}
.switch{display:flex;align-items:center;gap:8px;font-size:13px}
.switch input{width:18px;height:18px;accent-color:var(--p)}
@media(max-width:768px){
  .grid2{grid-template-columns:1fr}
  .side{position:fixed;left:-100%;z-index:100;transition:left .3s;width:80%;max-width:280px}
  .side.open{left:0}.side-tog{display:block}
  .tmain{padding:12px}.timer{font-size:18px}
}
</style>
</head>
<body>

<div id="s-login" class="screen active">
  <div class="wrap">
    <div class="hdr"><div class="logo">ҰБТ</div><h1>ҰБТ Тренажер</h1><p class="sub">Профиліңізге кіріңіз немесе тіркеліңіз</p></div>
    <div class="card">
      <div class="fg"><label>Атыңыз / Никнейм</label><input id="login-name" placeholder="Мысалы: Айгүл" maxlength="30"></div>
      <button class="btn btn-p" style="width:100%" onclick="doLogin()">Кіру / Тіркелу</button>
    </div>
    <p class="sub" style="text-align:center;margin-top:16px">Профиль осы құрылғыда сақталады</p>
  </div>
</div>

<div id="s-home" class="screen">
  <div class="profile-bar">
    <div style="display:flex;align-items:center;gap:10px">
      <div class="avatar" id="avatar">?</div>
      <span class="name" id="pname">User</span>
    </div>
    <button class="btn btn-s btn-sm" onclick="doLogout()">Шығу</button>
  </div>
  <div class="wrap">
    <div class="hdr"><h2>Басты бет</h2><p class="sub">Тест тапсырыңыз немесе өз тестіңізді құрыңыз</p></div>
    <div class="grid2" style="margin-bottom:20px">
      <div class="mode" onclick="showPublicTests()"><div class="ic">🌐</div><h3>Жария тесттер</h3><p>Басқалардың тесттері</p></div>
      <div class="mode" onclick="showMyTests()"><div class="ic">📚</div><h3>Менің тесттерім</h3><p>Өз тесттеріңіз</p></div>
      <div class="mode" onclick="showCreate()"><div class="ic">➕</div><h3>Тест құру</h3><p>Тақырып + сұрақтар</p></div>
      <div class="mode" onclick="showMistakes()"><div class="ic">❌</div><h3>Қатемен жұмыс</h3><p>Қателерді қайта шешу</p></div>
    </div>
    <div class="row">
      <button class="btn btn-s btn-sm" onclick="showHistory()">📋 Тарих</button>
      <button class="btn btn-s btn-sm" onclick="startQuickSubject()">⚡ Жылдам жаттығу</button>
    </div>
  </div>
</div>

<div id="s-public" class="screen">
  <div class="wrap">
    <div class="hdr"><h2>🌐 Жария тесттер</h2><p class="sub">Барлық пайдаланушылардың тесттері</p></div>
    <div id="public-list" class="list"></div>
    <div class="row" style="margin-top:20px"><button class="btn btn-s" onclick="goHome()">Артқа</button></div>
  </div>
</div>

<div id="s-mytests" class="screen">
  <div class="wrap">
    <div class="hdr"><h2>📚 Менің тесттерім</h2><p class="sub">Сіз құрған тесттер</p></div>
    <div id="my-list" class="list"></div>
    <div class="row" style="margin-top:20px">
      <button class="btn btn-p" onclick="showCreate()">➕ Жаңа тест</button>
      <button class="btn btn-s" onclick="goHome()">Артқа</button>
    </div>
  </div>
</div>

<div id="s-create" class="screen">
  <div class="wrap">
    <div class="hdr"><h2>➕ Тест құру</h2><p class="sub">Тақырып жазып, сұрақтар қосыңыз</p></div>
    <div class="card">
      <div class="fg"><label>Тақырып / Пән атауы *</label><input id="c-topic" placeholder="Мысалы: Қазақстан тарихы — 15 ғ."></div>
      <div class="fg"><label>Сипаттама (міндетті емес)</label><input id="c-desc" placeholder="Қысқаша сипаттама"></div>
      <div class="fg"><label class="switch"><input type="checkbox" id="c-public"> 🌐 Интернетке шығару (барлыққа көрінеді)</label></div>
    </div>
    <div class="card">
      <h3 style="margin-bottom:12px">Сұрақ қосу</h3>
      <div class="fg"><label>Сұрақ мәтіні</label><textarea id="c-qtext" placeholder="Сұрақты жазыңыз..."></textarea></div>
      <div class="fg">
        <label>Нұсқалар (дұрысын белгілеңіз)</label>
        <div class="opt"><input type="radio" name="c-cor" value="0" checked><input type="text" id="c-o0" placeholder="A"></div>
        <div class="opt"><input type="radio" name="c-cor" value="1"><input type="text" id="c-o1" placeholder="B"></div>
        <div class="opt"><input type="radio" name="c-cor" value="2"><input type="text" id="c-o2" placeholder="C"></div>
        <div class="opt"><input type="radio" name="c-cor" value="3"><input type="text" id="c-o3" placeholder="D"></div>
      </div>
      <button class="btn btn-ok btn-sm" onclick="addQToDraft()">+ Сұрақты қосу</button>
    </div>
    <div class="card">
      <h3 style="margin-bottom:10px">Қосылған сұрақтар (<span id="c-count">0</span>)</h3>
      <div id="c-qlist" class="list"></div>
    </div>
    <div class="row">
      <button class="btn btn-p" onclick="saveTest()">Тестті сақтау</button>
      <button class="btn btn-s" onclick="goHome()">Болдырмау</button>
    </div>
  </div>
</div>

<div id="s-edit" class="screen">
  <div class="wrap">
    <div class="hdr"><h2 id="edit-title">Тестті өңдеу</h2></div>
    <div class="card">
      <div class="fg"><label>Сұрақ мәтіні</label><textarea id="e-qtext"></textarea></div>
      <div class="fg">
        <label>Нұсқалар</label>
        <div class="opt"><input type="radio" name="e-cor" value="0" checked><input type="text" id="e-o0"></div>
        <div class="opt"><input type="radio" name="e-cor" value="1"><input type="text" id="e-o1"></div>
        <div class="opt"><input type="radio" name="e-cor" value="2"><input type="text" id="e-o2"></div>
        <div class="opt"><input type="radio" name="e-cor" value="3"><input type="text" id="e-o3"></div>
      </div>
      <button class="btn btn-ok" onclick="addQToExisting()">Сұрақты қосу</button>
    </div>
    <div id="edit-qlist" class="list"></div>
    <div class="row" style="margin-top:16px"><button class="btn btn-s" onclick="showMyTests()">Артқа</button></div>
  </div>
</div>

<div id="s-subj" class="screen">
  <div class="wrap">
    <div class="hdr"><h2>Жылдам жаттығу</h2><p class="sub">Дайын пәндерден таңдаңыз</p></div>
    <div id="subj-grid" class="grid2"></div>
    <div class="row" style="margin-top:20px"><button class="btn btn-s" onclick="goHome()">Артқа</button></div>
  </div>
</div>

<div id="s-test" class="screen">
  <div class="tlay">
    <aside class="side" id="sidebar">
      <div class="side-h"><span id="t-subj">Пән</span><button class="side-tog" onclick="togSide()">☰</button></div>
      <div class="qnav" id="qnav"></div>
      <div class="side-f"><button class="btn btn-d btn-sm" style="width:100%" onclick="finishTest()">Аяқтау</button></div>
    </aside>
    <main class="tmain">
      <div class="ttop">
        <div class="prog-t" id="prog-t">Сұрақ 1 / 10</div>
        <div class="prog-w"><div class="prog-f" id="prog-f" style="width:0%"></div></div>
        <div class="timer" id="timer">00:30:00</div>
      </div>
      <div class="qc">
        <div class="qh"><span class="qnum" id="qnum">Сұрақ 1</span><button class="flag" id="flag" onclick="togFlag()">🚩</button></div>
        <div class="qt" id="qtext"></div>
        <div class="opts" id="opts"></div>
      </div>
      <div class="navb">
        <button class="btn btn-s" id="prev" onclick="prevQ()">← Алдыңғы</button>
        <button class="btn btn-p" id="next" onclick="nextQ()">Келесі →</button>
      </div>
    </main>
  </div>
</div>

<div id="s-res" class="screen">
  <div class="wrap">
    <div class="hdr"><h1>Нәтиже</h1>
      <div class="score-c"><span id="sc">0</span><small>/ <span id="sm">0</span></small></div>
    </div>
    <div class="card" id="res-break"></div>
    <div class="row">
      <button class="btn btn-p" onclick="reviewAns()">Жауаптарды қарау</button>
      <button class="btn btn-w" onclick="startMistakesFromLast()">Қателерді шешу</button>
      <button class="btn btn-s" onclick="goHome()">Басты бет</button>
    </div>
  </div>
</div>

<div id="s-rev" class="screen">
  <div class="wrap wide">
    <div class="hdr"><h2>Жауаптар</h2><button class="btn btn-s btn-sm" onclick="showScr('s-res')">Нәтижеге</button></div>
    <div id="rev-list"></div>
  </div>
</div>

<div id="s-hist" class="screen">
  <div class="wrap">
    <div class="hdr"><h2>📋 Тарих</h2></div>
    <div id="hist-list" class="list"></div>
    <div class="row" style="margin-top:20px"><button class="btn btn-s" onclick="goHome()">Артқа</button></div>
  </div>
</div>

<div id="s-mist" class="screen">
  <div class="wrap">
    <div class="hdr"><h2>❌ Қатемен жұмыс</h2></div>
    <div id="mist-list" class="list"></div>
    <div class="row" style="margin-top:16px">
      <button class="btn btn-p" id="mist-start" style="display:none" onclick="startMistakes()">Қателерді шешу</button>
      <button class="btn btn-d btn-sm" onclick="clearMist()">Тазалау</button>
      <button class="btn btn-s" onclick="goHome()">Артқа</button>
    </div>
  </div>
</div>

<script>
const LS={get(k,d){try{return JSON.parse(localStorage.getItem(k))??d}catch{return d}},set(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch{}}};
let user=null;
function doLogin(){
  const name=document.getElementById('login-name').value.trim();
  if(!name||name.length<2){alert('Атыңызды жазыңыз (кемінде 2 әріп)');return}
  const profiles=LS.get('ubt_profiles',{});
  const key=name.toLowerCase();
  if(profiles[key]) user=profiles[key];
  else{user={name,id:'u_'+key.replace(/\s+/g,'_')+'_'+Date.now().toString(36).slice(-4)};profiles[key]=user;LS.set('ubt_profiles',profiles)}
  LS.set('ubt_current',user);enterApp();
}
function doLogout(){LS.set('ubt_current',null);user=null;showScr('s-login')}
function enterApp(){document.getElementById('pname').textContent=user.name;document.getElementById('avatar').textContent=user.name[0].toUpperCase();showScr('s-home')}
(function(){const u=LS.get('ubt_current');if(u&&u.name){user=u;enterApp()}})();

function showScr(id){document.querySelectorAll('.screen').forEach(s=>s.classList.remove('active'));document.getElementById(id).classList.add('active')}
function goHome(){stopTimer();st=baseState();showScr('s-home')}

const BANK={
  history:{name:'Қазақстан тарихы',qs:[{id:'h1',text:'Қазақ хандығы қай жылы құрылды?',options:['1456','1465','1480','1511'],correct:1},{id:'h2',text:'Абылай ханның шын есімі?',options:['Әбілмансұр','Тәуке','Қасым','Хақназар'],correct:0},{id:'h3',text:'«Жеті жарғы» кімдікі?',options:['Қасым хан','Есім хан','Тәуке хан','Абылай хан'],correct:2},{id:'h4',text:'Тәуелсіздік күні?',options:['16 желтоқсан','25 қазан','30 тамыз','1 мамыр'],correct:0},{id:'h5',text:'Алаш Орда қай жылы?',options:['1916','1917','1918','1920'],correct:1}]},
  math:{name:'Математика',qs:[{id:'m1',text:'2x+5=17, x=?',options:['5','6','7','12'],correct:1},{id:'m2',text:'f(x)=x²-4x+3, f(2)=?',options:['-1','0','1','3'],correct:0},{id:'m3',text:'Үшбұрыш бұрыштары қосындысы?',options:['90°','180°','270°','360°'],correct:1}]},
  physics:{name:'Физика',qs:[{id:'p1',text:'Жарық жылдамдығы (вакуум)?',options:['3×10⁸ м/с','3×10⁶','3×10¹⁰','300'],correct:0},{id:'p2',text:'Ньютон 2-заңы?',options:['F=ma','E=mc²','P=mv','W=Fs'],correct:0}]},
  biology:{name:'Биология',qs:[{id:'b1',text:'Жасуша энергия станциясы?',options:['Ядро','Митохондрия','Рибосома','Гольджи'],correct:1},{id:'b2',text:'ДНҚ толық атауы?',options:['Дезоксирибонуклеин қышқылы','Рибонуклеин қышқылы','АТФ','Аминқышқыл'],correct:0}]}
};

function allTests(){return LS.get('ubt_tests',[])}
function saveAllTests(a){LS.set('ubt_tests',a)}
function myTests(){return allTests().filter(t=>t.authorId===user.id)}
function publicTests(){return allTests().filter(t=>t.isPublic&&t.questions.length>0)}

let draft={questions:[]};
function showCreate(){
  draft={questions:[]};
  document.getElementById('c-topic').value='';document.getElementById('c-desc').value='';document.getElementById('c-public').checked=false;
  document.getElementById('c-qtext').value='';['c-o0','c-o1','c-o2','c-o3'].forEach(id=>document.getElementById(id).value='');
  document.querySelector('input[name="c-cor"][value="0"]').checked=true;renderDraftQs();showScr('s-create');
}
function addQToDraft(){
  const text=document.getElementById('c-qtext').value.trim();
  const opts=[0,1,2,3].map(i=>document.getElementById('c-o'+i).value.trim());
  const correct=+document.querySelector('input[name="c-cor"]:checked').value;
  if(!text){alert('Сұрақ жазыңыз!');return}if(opts.some(o=>!o)){alert('4 нұсқаны толтырыңыз!');return}
  draft.questions.push({id:'q_'+Date.now(),text,options:opts,correct,points:1});
  document.getElementById('c-qtext').value='';['c-o0','c-o1','c-o2','c-o3'].forEach(id=>document.getElementById(id).value='');
  document.querySelector('input[name="c-cor"][value="0"]').checked=true;renderDraftQs();
}
function renderDraftQs(){
  document.getElementById('c-count').textContent=draft.questions.length;
  const el=document.getElementById('c-qlist');
  if(!draft.questions.length){el.innerHTML='<p class="sub">Әзірге сұрақ жоқ</p>';return}
  el.innerHTML=draft.questions.map((q,i)=>`<div class="item"><div class="info"><h4>${i+1}. ${q.text}</h4><p>Дұрыс: ${['A','B','C','D'][q.correct]}</p></div>
    <div class="acts"><button class="btn btn-d btn-sm" onclick="draft.questions.splice(${i},1);renderDraftQs()">✕</button></div></div>`).join('');
}
function saveTest(){
  const topic=document.getElementById('c-topic').value.trim();
  if(!topic){alert('Тақырып жазыңыз!');return}if(!draft.questions.length){alert('Кемінде 1 сұрақ қосыңыз!');return}
  const test={id:'t_'+Date.now(),topic,desc:document.getElementById('c-desc').value.trim(),isPublic:document.getElementById('c-public').checked,
    authorId:user.id,authorName:user.name,questions:draft.questions,createdAt:new Date().toISOString()};
  const all=allTests();all.unshift(test);saveAllTests(all);
  alert(test.isPublic?'✅ Тест сақталды және жарияланды!':'✅ Тест сақталды!');showMyTests();
}

function showMyTests(){
  const list=document.getElementById('my-list');const tests=myTests();
  if(!tests.length){list.innerHTML='<div class="empty"><div class="ic">📭</div><p>Сізде әзірге тест жоқ.<br>«Тест құру» арқылы жасаңыз.</p></div>'}
  else{list.innerHTML=tests.map(t=>`<div class="item"><div class="info"><h4>${t.topic}</h4>
    <p>${t.questions.length} сұрақ · ${t.isPublic?'<span class="badge badge-pub">🌐 Жария</span>':'<span class="badge badge-priv">🔒 Жеке</span>'}</p></div>
    <div class="acts">
      <button class="btn btn-p btn-sm" onclick="startUserTest('${t.id}')">Бастау</button>
      <button class="btn btn-s btn-sm" onclick="editTest('${t.id}')">+ Сұрақ</button>
      <button class="btn btn-s btn-sm" onclick="togglePub('${t.id}')">${t.isPublic?'Жасыру':'Жариялау'}</button>
      <button class="btn btn-d btn-sm" onclick="delTest('${t.id}')">✕</button>
    </div></div>`).join('')}
  showScr('s-mytests');
}
function togglePub(id){const all=allTests();const t=all.find(x=>x.id===id);if(t){t.isPublic=!t.isPublic;saveAllTests(all);showMyTests()}}
function delTest(id){if(!confirm('Тестті өшіру керек пе?'))return;saveAllTests(allTests().filter(t=>t.id!==id));showMyTests()}

function showPublicTests(){
  const list=document.getElementById('public-list');const tests=publicTests();
  if(!tests.length){list.innerHTML='<div class="empty"><div class="ic">🌐</div><p>Әзірге жария тест жоқ.<br>Өзіңіз құрып, «Интернетке шығару» белгілеңіз.</p></div>'}
  else{list.innerHTML=tests.map(t=>`<div class="item"><div class="info"><h4>${t.topic}</h4>
    <p>${t.questions.length} сұрақ · Автор: ${t.authorName||'Аноним'}${t.desc?' · '+t.desc:''}</p></div>
    <div class="acts"><button class="btn btn-p btn-sm" onclick="startUserTest('${t.id}')">Тапсыру</button></div></div>`).join('')}
  showScr('s-public');
}

let editingId=null;
function editTest(id){
  editingId=id;const t=allTests().find(x=>x.id===id);if(!t)return;
  document.getElementById('edit-title').textContent='Сұрақ қосу: '+t.topic;
  document.getElementById('e-qtext').value='';['e-o0','e-o1','e-o2','e-o3'].forEach(i=>document.getElementById(i).value='');
  document.querySelector('input[name="e-cor"][value="0"]').checked=true;renderEditList(t);showScr('s-edit');
}
function renderEditList(t){
  document.getElementById('edit-qlist').innerHTML=t.questions.map((q,i)=>`<div class="item"><div class="info"><h4>${i+1}. ${q.text}</h4></div>
    <div class="acts"><button class="btn btn-d btn-sm" onclick="removeQFromTest('${t.id}',${i})">✕</button></div></div>`).join('');
}
function addQToExisting(){
  const t=allTests().find(x=>x.id===editingId);if(!t)return;
  const text=document.getElementById('e-qtext').value.trim();
  const opts=[0,1,2,3].map(i=>document.getElementById('e-o'+i).value.trim());
  const correct=+document.querySelector('input[name="e-cor"]:checked').value;
  if(!text||opts.some(o=>!o)){alert('Барлығын толтырыңыз!');return}
  t.questions.push({id:'q_'+Date.now(),text,options:opts,correct,points:1});saveAllTests(allTests());
  document.getElementById('e-qtext').value='';['e-o0','e-o1','e-o2','e-o3'].forEach(i=>document.getElementById(i).value='');
  renderEditList(t);alert('Сұрақ қосылды!');
}
function removeQFromTest(tid,idx){const all=allTests();const t=all.find(x=>x.id===tid);if(t){t.questions.splice(idx,1);saveAllTests(all);renderEditList(t)}}

function baseState(){return{questions:[],currentIndex:0,answers:{},flags:{},timerSeconds:0,timerInterval:null,subjectName:'',isMistakes:false,testId:null,lastWrong:null}}
let st=baseState();

function startUserTest(id){
  const t=allTests().find(x=>x.id===id);if(!t||!t.questions.length){alert('Сұрақ жоқ!');return}
  st=baseState();st.questions=t.questions.map(q=>({...q,subjectName:t.topic}));st.subjectName=t.topic;st.testId=id;
  st.timerSeconds=Math.max(t.questions.length*90,600);beginTest();
}
function startQuickSubject(){
  document.getElementById('subj-grid').innerHTML=Object.entries(BANK).map(([k,v])=>
    `<div class="mode" onclick="startBank('${k}')"><div class="ic">📖</div><h3>${v.name}</h3><p>${v.qs.length} сұрақ</p></div>`).join('');
  showScr('s-subj');
}
function startBank(key){
  const b=BANK[key];st=baseState();st.questions=b.qs.map(q=>({...q,subjectName:b.name,points:1}));st.subjectName=b.name;
  st.timerSeconds=Math.max(b.qs.length*90,600);beginTest();
}
function beginTest(){showScr('s-test');renderNav();renderQ();startTimer();updateProg()}
function renderNav(){document.getElementById('qnav').innerHTML=st.questions.map((_,i)=>`<button class="qn" onclick="goQ(${i})">${i+1}</button>`).join('');updNav()}
function updNav(){document.querySelectorAll('.qn').forEach((b,i)=>{b.classList.remove('cur','ans','flg');if(i===st.currentIndex)b.classList.add('cur');if(st.answers[st.questions[i].id]!==undefined)b.classList.add('ans');if(st.flags[st.questions[i].id])b.classList.add('flg')})}
function renderQ(){
  const q=st.questions[st.currentIndex];if(!q)return;
  document.getElementById('t-subj').textContent=q.subjectName||st.subjectName;
  document.getElementById('qnum').textContent='Сұрақ '+(st.currentIndex+1);
  document.getElementById('qtext').textContent=q.text;
  document.getElementById('flag').classList.toggle('on',!!st.flags[q.id]);
  const L=['A','B','C','D','E'];
  document.getElementById('opts').innerHTML=q.options.map((o,i)=>`<div class="op${st.answers[q.id]===i?' sel':''}" onclick="selOpt(${i})"><span class="ol">${L[i]}</span><span class="ot">${o}</span></div>`).join('');
  document.getElementById('prev').disabled=st.currentIndex===0;
  document.getElementById('next').textContent=st.currentIndex===st.questions.length-1?'Аяқтау':'Келесі →';
  updNav();updateProg();
}
function selOpt(i){st.answers[st.questions[st.currentIndex].id]=i;renderQ()}
function togFlag(){const q=st.questions[st.currentIndex];st.flags[q.id]=!st.flags[q.id];renderQ()}
function nextQ(){if(st.currentIndex<st.questions.length-1){st.currentIndex++;renderQ()}else finishTest()}
function prevQ(){if(st.currentIndex>0){st.currentIndex--;renderQ()}}
function goQ(i){st.currentIndex=i;renderQ();document.getElementById('sidebar').classList.remove('open')}
function updateProg(){const t=st.questions.length,c=st.currentIndex+1,a=Object.keys(st.answers).length;document.getElementById('prog-t').textContent=`Сұрақ ${c} / ${t}`;document.getElementById('prog-f').style.width=(a/t*100)+'%'}
function togSide(){document.getElementById('sidebar').classList.toggle('open')}

function startTimer(){stopTimer();updTimer();st.timerInterval=setInterval(()=>{st.timerSeconds--;updTimer();if(st.timerSeconds<=0){stopTimer();alert('Уақыт аяқталды!');finishTest()}},1000)}
function stopTimer(){if(st.timerInterval){clearInterval(st.timerInterval);st.timerInterval=null}}
function updTimer(){const t=Math.max(0,st.timerSeconds);const h=Math.floor(t/3600),m=Math.floor((t%3600)/60),s=t%60;const el=document.getElementById('timer');el.textContent=`${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;el.classList.remove('warn','dang');if(t<=300)el.classList.add('dang');else if(t<=900)el.classList.add('warn')}

function finishTest(){
  if(!confirm('Тестті аяқтау керек пе?'))return;stopTimer();
  let score=0,max=st.questions.length,wrong=[];
  st.questions.forEach(q=>{if(st.answers[q.id]===q.correct)score++;else wrong.push({...q,userAnswer:st.answers[q.id]})});
  if(!st.isMistakes&&wrong.length){let m=LS.get('ubt_mistakes_'+user.id,[]);const ids=new Set(m.map(x=>x.id));wrong.forEach(q=>{if(!ids.has(q.id))m.push(q)});LS.set('ubt_mistakes_'+user.id,m)}
  let hist=LS.get('ubt_hist_'+user.id,[]);hist.unshift({date:new Date().toLocaleString('kk-KZ'),score,max,topic:st.subjectName,answers:{...st.answers},questions:st.questions.map(q=>({id:q.id,text:q.text,options:q.options,correct:q.correct}))});
  if(hist.length>40)hist.pop();LS.set('ubt_hist_'+user.id,hist);
  st.lastWrong=wrong;st.lastScore={score,max};
  document.getElementById('sc').textContent=score;document.getElementById('sm').textContent=max;
  document.getElementById('res-break').innerHTML=`<div class="res-row"><span>${st.subjectName||'Тест'}</span><span style="font-weight:700;color:var(--p)">${score} / ${max}</span></div>`;
  showScr('s-res');
}
function reviewAns(){
  const L=['A','B','C','D'];
  document.getElementById('rev-list').innerHTML=st.questions.map((q,i)=>{const ua=st.answers[q.id],ok=ua===q.correct;
    return `<div class="rev ${ok?'ok':'bad'}"><div class="rh"><span>Сұрақ ${i+1}</span><span>${ok?'✓ Дұрыс':'✗ Қате'}</span></div>
      <div class="rq">${q.text}</div>${ua!==undefined?`<div class="ra u">Сіз: <b>${L[ua]}) ${q.options[ua]}</b></div>`:'<div class="ra u">Жауап жоқ</div>'}
      ${!ok?`<div class="ra c">Дұрыс: <b>${L[q.correct]}) ${q.options[q.correct]}</b></div>`:''}</div>`}).join('');
  showScr('s-rev');
}
function showHistory(){
  const hist=LS.get('ubt_hist_'+user.id,[]);
  document.getElementById('hist-list').innerHTML=hist.length?hist.map(h=>`<div class="item"><div class="info"><h4>${h.topic||'Тест'}</h4><p>${h.date}</p></div>
    <div style="font-weight:700;color:var(--p)">${h.score}/${h.max}</div></div>`).join(''):'<div class="empty"><div class="ic">📭</div><p>Тарих бос</p></div>';
  showScr('s-hist');
}
function showMistakes(){
  const m=LS.get('ubt_mistakes_'+user.id,[]);const btn=document.getElementById('mist-start');
  if(!m.length){document.getElementById('mist-list').innerHTML='<div class="empty"><div class="ic">🎉</div><p>Қате жоқ!</p></div>';btn.style.display='none'}
  else{document.getElementById('mist-list').innerHTML=m.map(q=>`<div class="item"><div class="info"><h4>${q.text.substring(0,70)}${q.text.length>70?'...':''}</h4><p>${q.subjectName||''}</p></div></div>`).join('');btn.style.display='inline-flex'}
  showScr('s-mist');
}
function clearMist(){if(confirm('Тазалау?')){LS.set('ubt_mistakes_'+user.id,[]);showMistakes()}}
function startMistakes(){const m=LS.get('ubt_mistakes_'+user.id,[]);if(!m.length)return;st=baseState();st.questions=m.map(q=>({...q}));st.subjectName='Қателер';st.isMistakes=true;st.timerSeconds=Math.max(m.length*90,600);beginTest()}
function startMistakesFromLast(){if(!st.lastWrong||!st.lastWrong.length){alert('Қате жоқ!');return}st.questions=st.lastWrong.map(q=>({...q}));st.currentIndex=0;st.answers={};st.flags={};st.subjectName='Қателер';st.isMistakes=true;st.timerSeconds=Math.max(st.questions.length*90,600);beginTest()}

document.addEventListener('click',e=>{const side=document.getElementById('sidebar');if(side&&side.classList.contains('open')&&!side.contains(e.target)&&!e.target.classList.contains('side-tog'))side.classList.remove('open')});
</script>
</body>
</html>
"""

components.html(html_code, height=950, scrolling=True)
