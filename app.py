import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ҰБТ+", page_icon="📘", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""<style>#MainMenu,footer,header{visibility:hidden}.block-container{padding:0!important;max-width:100%!important}iframe{border:none!important}</style>""", unsafe_allow_html=True)

html_code = r"""
<!DOCTYPE html>
<html lang="kk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ҰБТ+</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{--p:#2563eb;--pd:#1d4ed8;--ok:#16a34a;--err:#dc2626;--warn:#f59e0b;--bg:#f1f5f9;--c:#fff;--t:#0f172a;--m:#64748b;--b:#e2e8f0}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Inter',system-ui,sans-serif;background:var(--bg);color:var(--t);min-height:100vh;line-height:1.5}
.screen{display:none;min-height:100vh}.screen.active{display:block}
.wrap{max-width:760px;margin:0 auto;padding:32px 16px}
.wrap.wide{max-width:920px}
.hdr{text-align:center;margin-bottom:28px}
.logo{display:inline-flex;align-items:center;justify-content:center;width:72px;height:72px;background:linear-gradient(135deg,#2563eb,#7c3aed);color:#fff;font-weight:800;font-size:26px;border-radius:20px;margin-bottom:14px;box-shadow:0 8px 24px rgba(37,99,235,.35);letter-spacing:-0.5px}
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
    <div class="hdr"><div class="logo">Ұ+</div><h1>ҰБТ+</h1><p class="sub">ҰБТ-ға дайындық платформасы</p></div>
    <div class="card" id="login-box">
      <div class="fg"><label>Логин (атыңыз)</label><input id="login-name" placeholder="Атыңыз" oninput="checkAdminName()"></div>
      <div class="fg"><label>Пароль</label><input id="login-pass" type="password" placeholder="Пароль"></div>
      <div class="fg" id="admin-pass-wrap" style="display:none"><label class="sub">Админ ретінде кіру</label></div>
      <button class="btn btn-p" style="width:100%;margin-bottom:10px" onclick="doLogin()">Кіру</button>
      <button class="btn btn-s" style="width:100%;margin-bottom:10px" onclick="showRegister()">Тіркелу</button>
      <button class="btn btn-s btn-sm" style="width:100%;margin-bottom:10px" onclick="showForgot()">Парольді ұмыттым</button>
      <button class="btn btn-w btn-sm" style="width:100%" onclick="showContactAdmin()">💬 Админге жазу</button>
    </div>
    <div class="card" id="register-box" style="display:none">
      <h3 style="margin-bottom:12px">Тіркелу</h3>
      <div class="fg"><label>Атыңыз (логин) *</label><input id="reg-name" placeholder="Атыңыз" maxlength="30"></div>
      <div class="fg"><label>Пароль *</label><input id="reg-pass" type="password" placeholder="Кемінде 4 таңба"></div>
      <div class="fg"><label>Парольді қайталаңыз *</label><input id="reg-pass2" type="password" placeholder="Қайталаңыз"></div>
      <button class="btn btn-p" style="width:100%;margin-bottom:10px" onclick="doRegister()">Тіркелу</button>
      <button class="btn btn-s" style="width:100%" onclick="showLoginBox()">Артқа</button>
    </div>
    <div class="card" id="forgot-box" style="display:none">
      <h3 style="margin-bottom:12px">Парольді қалпына келтіру</h3>
      <div class="fg"><label>Логин (атыңыз)</label><input id="forgot-login" placeholder="Атыңыз"></div>
      <button class="btn btn-w" style="width:100%;margin-bottom:10px" onclick="sendForgotCode()">Код алу</button>
      <div id="forgot-step2" style="display:none">
        <div class="fg"><label>Код</label><input id="forgot-code" placeholder="4 цифр" maxlength="6"></div>
        <div class="fg"><label>Жаңа пароль</label><input id="forgot-pass" type="password" placeholder="Жаңа пароль"></div>
        <button class="btn btn-p" style="width:100%;margin-bottom:10px" onclick="doForgotReset()">Парольді өзгерту</button>
      </div>
      <button class="btn btn-s" style="width:100%" onclick="showLoginBox()">Артқа</button>
    </div>
    <div class="card" id="contact-box" style="display:none;padding:0;overflow:hidden">
      <div style="background:#075e54;color:#fff;padding:14px 16px;display:flex;align-items:center;gap:12px">
        <div style="width:40px;height:40px;border-radius:50%;background:#128c7e;display:flex;align-items:center;justify-content:center;font-weight:700">А</div>
        <div style="flex:1"><div style="font-weight:600;font-size:15px">Админ</div><div id="chat-sub" style="font-size:12px;opacity:.85">ҰБТ+ қолдау</div></div>
        <button class="btn btn-sm" style="background:transparent;color:#fff;border:1px solid rgba(255,255,255,.4)" onclick="closeChat()">✕</button>
      </div>
      <div id="chat-gate" style="padding:20px 16px;background:#f0f0f0">
        <div class="fg"><label>Админмен чатты ашу үшін логиніңізді (атыңызды) жазыңыз</label><input id="chat-login" placeholder="Логин" maxlength="30" style="background:#fff" onkeydown="if(event.key==='Enter')enterChat()"></div>
        <button class="btn btn-ok" style="width:100%" onclick="enterChat()">Чатты ашу</button>
      </div>
      <div id="chat-room" style="display:none">
        <div id="chat-messages" style="height:280px;overflow-y:auto;padding:12px;background:#e5ddd5;display:flex;flex-direction:column;gap:8px"></div>
        <div style="padding:10px 12px;background:#f0f0f0;border-top:1px solid #ddd">
          <div style="display:flex;gap:8px">
            <input id="chat-text" maxlength="1000" placeholder="Хабарлама жазыңыз..." style="flex:1;padding:10px 12px;border:1px solid #ccc;border-radius:20px;font-size:14px;font-family:inherit;background:#fff" onkeydown="if(event.key==='Enter')sendChatMsg()">
            <button class="btn btn-ok" style="border-radius:50%;width:42px;height:42px;padding:0" onclick="sendChatMsg()">➤</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<div id="s-user-view" class="screen">
  <div class="wrap">
    <div class="hdr">
      <div class="avatar" id="uv-avatar" style="width:64px;height:64px;font-size:24px;margin:0 auto 10px;border:3px solid #93c5fd">?</div>
      <h2 id="uv-name">User</h2>
      <p class="sub" id="uv-info">—</p>
    </div>
    <div class="card">
      <h3 style="margin-bottom:12px">👤 Аккаунт деректері</h3>
      <div class="fg"><label>Логин</label><input id="uv-login" readonly style="background:#f1f5f9"></div>
      <div class="fg"><label>Қазіргі пароль</label><input id="uv-curpass" readonly style="background:#f1f5f9"></div>
    </div>
    <div class="card" id="uv-pass-card">
      <h3 style="margin-bottom:10px">🔑 Парольді өзгерту</h3>
      <div class="fg"><label>Жаңа пароль</label><input id="uv-newpass" type="text" placeholder="Жаңа пароль жазыңыз"></div>
      <button class="btn btn-p btn-sm" onclick="adminChangeUserPass()">Парольді сақтау</button>
    </div>
    <div class="card"><h3 style="margin-bottom:10px">📋 Тест тарихы</h3><div id="uv-hist" class="list"></div></div>
    <div class="card"><h3 style="margin-bottom:10px">❌ Қателері</h3><div id="uv-mist" class="list"></div></div>
    <div class="row"><button class="btn btn-s" onclick="showAdmin()">Артқа</button></div>
  </div>
</div>

<div id="s-home" class="screen">
  <div class="profile-bar">
    <div style="display:flex;align-items:center;gap:12px;cursor:pointer" onclick="showMyProfile()">
      <div style="position:relative">
        <div class="avatar" id="avatar" style="width:44px;height:44px;font-size:16px;border:3px solid #93c5fd">?</div>
        <span id="p-verified" style="display:none;position:absolute;bottom:-2px;right:-2px;background:#2563eb;color:#fff;width:18px;height:18px;border-radius:50%;font-size:11px;line-height:18px;text-align:center;border:2px solid #fff">✓</span>
      </div>
      <div>
        <div class="name" id="pname">User</div>
        <div class="sub" id="p-title" style="font-size:11px">—</div>
        <div id="p-stars" style="font-size:13px;letter-spacing:2px;color:#f59e0b;line-height:1.2">☆☆☆☆☆</div>
      </div>
      <div style="margin-left:8px;background:#eff6ff;padding:4px 10px;border-radius:20px;font-size:12px;font-weight:700;color:var(--p)">
        ⭐ <span id="p-points">0</span>
      </div>
    </div>
    <button class="btn btn-s btn-sm" onclick="doLogout()">Шығу</button>
  </div>
  <div class="wrap">
    <div class="hdr"><h2>Басты бет</h2><p class="sub">Тест тапсырыңыз немесе өз тестіңізді құрыңыз</p></div>
    <div class="grid2" style="margin-bottom:20px">
      <div class="mode" onclick="showPublicTests()"><div class="ic">🌐</div><h3>Жария тесттер</h3><p>Админ мақұлдаған</p></div>
      <div class="mode" onclick="showMyTests()"><div class="ic">📚</div><h3>Менің тесттерім</h3><p>Өз тесттеріңіз</p></div>
      <div class="mode" onclick="showCreate()"><div class="ic">➕</div><h3>Тест құру</h3><p>Тақырып + сұрақтар</p></div>
      <div class="mode" onclick="showRanking()"><div class="ic">🏆</div><h3>Рейтинг</h3><p>Ортақ көшбасшылар</p></div>
    </div>
    <div class="row">
      <button class="btn btn-s btn-sm" onclick="showFormulas()">📐 Формула</button>
      <button class="btn btn-s btn-sm" onclick="showMistakes()">❌ Қателер</button>
      <button class="btn btn-s btn-sm" onclick="showHistory()">📋 Тарих</button>
      <button class="btn btn-s btn-sm" onclick="startQuickSubject()">⚡ Жылдам</button>
      <button class="btn btn-w btn-sm" onclick="openContactFromApp()">💬 Админге</button>
      <button class="btn btn-w btn-sm" id="admin-btn" style="display:none" onclick="showAdmin()">🛠 Админ</button>
    </div>
  </div>
</div>

<div id="s-profile" class="screen">
  <div class="wrap">
    <div class="hdr">
      <div style="position:relative;width:80px;margin:0 auto 12px">
        <div class="avatar" id="prof-avatar" style="width:80px;height:80px;font-size:32px;border:4px solid #93c5fd">?</div>
        <span id="prof-verified" style="display:none;position:absolute;bottom:0;right:0;background:#2563eb;color:#fff;width:24px;height:24px;border-radius:50%;font-size:14px;line-height:24px;text-align:center;border:2px solid #fff">✓</span>
      </div>
      <h2 id="prof-name">User</h2>
      <p class="sub" id="prof-title">Атақ жоқ</p>
      <div id="prof-stars" style="font-size:22px;letter-spacing:3px;color:#f59e0b;margin:8px 0">☆☆☆☆☆</div>
      <div style="margin-top:8px;font-size:22px;font-weight:700;color:var(--p)">⭐ <span id="prof-points">0</span> ұпай</div>
      <p class="sub" id="prof-rank" style="margin-top:6px">Рейтинг: —</p>
    </div>
    <div class="row"><button class="btn btn-s" onclick="goHome()">Артқа</button></div>
  </div>
</div>

<div id="s-ranking" class="screen">
  <div class="wrap">
    <div class="hdr"><h2>🏆 Рейтинг</h2><p class="sub">Ең көп ұпай жинағандар</p></div>
    <div id="rank-list" class="list"></div>
    <div class="row" style="margin-top:16px"><button class="btn btn-s" onclick="goHome()">Артқа</button></div>
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
      <div class="fg"><label>Пән *</label>
        <select id="c-subject">
          <option value="">— Пәнді таңдаңыз —</option>
          <option value="history">Қазақстан тарихы</option>
          <option value="reading">Оқу сауаттылығы</option>
          <option value="mathlit">Математикалық сауаттылық</option>
          <option value="math">Математика</option>
          <option value="physics">Физика</option>
          <option value="chemistry">Химия</option>
          <option value="biology">Биология</option>
          <option value="geography">География</option>
          <option value="informatics">Информатика</option>
          <option value="english">Ағылшын тілі</option>
          <option value="kazakh">Қазақ тілі</option>
          <option value="worldhistory">Дүниежүзі тарихы</option>
          <option value="law">Құқық негіздері</option>
          <option value="other">Басқа</option>
        </select>
      </div>
      <div class="fg"><label>Тақырып * <span class="sub">(мыс: «15 ғасыр», «Ньютон заңдары»)</span></label><input id="c-topic" placeholder="Тақырыпты міндетті түрде жазыңыз"></div>
      <div class="fg"><label>Сипаттама (міндетті емес)</label><input id="c-desc" placeholder="Қысқаша сипаттама"></div>
      <div class="fg"><label class="switch"><input type="checkbox" id="c-request"> 🌐 Жариялауға жіберу (админ мақұлдаған соң шығады)</label></div>
    </div>
    <div class="card">
      <h3 style="margin-bottom:12px">Сұрақ қосу</h3>
      <div class="fg"><label>Сұрақ мәтіні</label><textarea id="c-qtext" placeholder="Сұрақты жазыңыз..."></textarea></div>
      <div class="fg"><label>Дұрыс жауап ғана</label><input id="c-correct" placeholder="Тек дұрыс жауапты жазыңыз"></div>
      <button class="btn btn-w btn-sm" onclick="genWrong()" style="margin-bottom:12px">✨ Қате нұсқаларды жасау</button>
      <div class="fg" id="opts-block" style="display:none">
        <label>Нұсқалар (қажетінше өзгертіңіз, дұрысын белгілеңіз)</label>
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

<div id="s-formulas" class="screen">
  <div class="wrap">
    <div class="hdr"><h2>📐 Формулалар</h2><p class="sub">Формула енгізіңіз немесе қараңыз</p></div>
    <div class="card">
      <div class="fg"><label>Пән</label>
        <select id="f-subject">
          <option value="math">Математика</option>
          <option value="physics">Физика</option>
          <option value="chemistry">Химия</option>
          <option value="other">Басқа</option>
        </select>
      </div>
      <div class="fg"><label>Формула атауы</label><input id="f-title" placeholder="Мыс: Квадрат теңдеу"></div>
      <div class="fg"><label>Формула</label><textarea id="f-body" placeholder="x = (-b ± √(b²-4ac)) / 2a"></textarea></div>
      <button class="btn btn-ok btn-sm" onclick="addFormula()">Сақтау</button>
    </div>
    <div id="formula-list" class="list"></div>
    <div class="row" style="margin-top:16px"><button class="btn btn-s" onclick="goHome()">Артқа</button></div>
  </div>
</div>

<div id="s-admin" class="screen">
  <div class="wrap wide">
    <div class="hdr"><h2>🛠 Админ панелі</h2><p class="sub">Толық басқару</p></div>
    <div class="grid2" id="admin-stats-grid" style="margin-bottom:16px"></div>
    <div class="card" style="padding:20px">
      <h3 style="margin-bottom:12px">⏳ Жариялау күтіп тұрған тесттер</h3>
      <div id="admin-pending" class="list"></div>
    </div>
    <div class="card" style="padding:20px">
      <h3 style="margin-bottom:12px">👥 Тіркелгендер</h3>
      <div id="admin-users" class="list"></div>
    </div>
    <div class="card" style="padding:20px">
      <h3 style="margin-bottom:12px">📚 Барлық тесттер</h3>
      <div id="admin-tests" class="list"></div>
    </div>
    <div class="card" style="padding:20px">
      <h3 style="margin-bottom:12px">📐 Формулалар</h3>
      <div id="admin-formulas" class="list"></div>
    </div>
    <div class="card" style="padding:20px">
      <h3 style="margin-bottom:12px">💬 Хабарламалар (әр логин бөлек)</h3>
      <div id="admin-chat" class="list"></div>
    </div>
    <div class="row"><button class="btn btn-s" onclick="goHome()">Артқа</button></div>
  </div>
</div>

<script>
const LS={get(k,d){try{return JSON.parse(localStorage.getItem(k))??d}catch{return d}},set(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch{}}};
function getAdminPass(){return LS.get('ubt_admin_pass','admin123')}
function setAdminPass(p){LS.set('ubt_admin_pass',p)}
let user=null;
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function jsq(s){return esc(JSON.stringify(String(s)))}
function checkAdminName(){
  const n=document.getElementById('login-name').value.trim().toLowerCase();
  document.getElementById('admin-pass-wrap').style.display=(n==='админ'||n==='admin')?'block':'none';
}
function showLoginBox(){
  document.getElementById('login-box').style.display='block';
  document.getElementById('register-box').style.display='none';
  document.getElementById('forgot-box').style.display='none';
  document.getElementById('contact-box').style.display='none';
}
function showRegister(){
  document.getElementById('login-box').style.display='none';
  document.getElementById('register-box').style.display='block';
  document.getElementById('forgot-box').style.display='none';
  document.getElementById('contact-box').style.display='none';
}
function showForgot(){
  document.getElementById('login-box').style.display='none';
  document.getElementById('register-box').style.display='none';
  document.getElementById('forgot-box').style.display='block';
  document.getElementById('contact-box').style.display='none';
  document.getElementById('forgot-step2').style.display='none';
}
let chatLogin=null;
function showContactAdmin(){
  document.getElementById('login-box').style.display='none';
  document.getElementById('register-box').style.display='none';
  document.getElementById('forgot-box').style.display='none';
  document.getElementById('contact-box').style.display='block';
  if(chatLogin){openChatRoom()}
  else{
    document.getElementById('chat-room').style.display='none';
    document.getElementById('chat-gate').style.display='block';
    document.getElementById('chat-sub').textContent='ҰБТ+ қолдау';
    document.getElementById('chat-login').value='';
  }
}
function openContactFromApp(){
  if(user&&user.isAdmin){showAdmin();return}
  chatLogin=(user&&user.name)?user.name:null;
  showScr('s-login');showContactAdmin();
}
function enterChat(){
  const l=document.getElementById('chat-login').value.trim();
  if(l.length<2){alert('Логиніңізді жазыңыз (кемінде 2 таңба)');return}
  chatLogin=l;openChatRoom();
}
function openChatRoom(){
  document.getElementById('chat-gate').style.display='none';
  document.getElementById('chat-room').style.display='block';
  document.getElementById('chat-sub').textContent='👤 '+chatLogin;
  renderChatMessages();
}
function closeChat(){
  chatLogin=null;showLoginBox();
  if(user&&!user.isAdmin)showScr('s-home');
}
function findUserByLogin(login){
  const profiles=LS.get('ubt_profiles',{});
  const key=login.toLowerCase().trim();
  if(profiles[key]) return profiles[key];
  return null;
}
function genCode(){return String(Math.floor(1000+Math.random()*9000))}
let pendingForgot=null;

function doRegister(){
  const name=document.getElementById('reg-name').value.trim();
  const pass=document.getElementById('reg-pass').value;
  const pass2=document.getElementById('reg-pass2').value;
  if(!name||name.length<2){alert('Атыңызды жазыңыз');return}
  if(!pass||pass.length<4){alert('Пароль кемінде 4 таңба');return}
  if(pass!==pass2){alert('Парольдер сәйкес емес');return}
  if(findUserByLogin(name)){alert('Бұл ат тіркелген. Басқа ат таңдаңыз');return}
  const key=name.toLowerCase();
  const profiles=LS.get('ubt_profiles',{});
  const u={name:name,password:pass,
    id:'u_'+key.replace(/[^\p{L}\p{N}]+/gu,'_')+'_'+Date.now().toString(36).slice(-4),isAdmin:false};
  profiles[key]=u;LS.set('ubt_profiles',profiles);
  setUserStats(u.id,{points:0,title:'',stars:0,verified:false});
  alert('✅ Тіркелу сәтті! Енді кіріңіз.');
  showLoginBox();
  document.getElementById('login-name').value=u.name;
}
function doLogin(){
  const login=document.getElementById('login-name').value.trim();
  const pass=document.getElementById('login-pass').value;
  if(!login){alert('Логин жазыңыз');return}
  const key=login.toLowerCase();
  if(key==='админ'||key==='admin'){
    if(pass!==getAdminPass()){alert('Қате пароль!');return}
    user={name:'Админ',id:'admin',isAdmin:true};
    LS.set('ubt_current',user);enterApp();return;
  }
  const u=findUserByLogin(login);
  if(!u){alert('Аккаунт табылмады. Тіркеліңіз.');return}
  if(u.password&&u.password!==pass){alert('Қате пароль!');return}
  // legacy users without password
  if(!u.password){u.password=pass;const profiles=LS.get('ubt_profiles',{});
    Object.keys(profiles).forEach(k=>{if(profiles[k].id===u.id)profiles[k].password=pass});LS.set('ubt_profiles',profiles)}
  user=u;LS.set('ubt_current',user);enterApp();
}
function sendForgotCode(){
  const login=document.getElementById('forgot-login').value.trim();
  const u=findUserByLogin(login);
  if(!u){alert('Бұл атпен аккаунт жоқ');return}
  const code=genCode();
  pendingForgot={userId:u.id,login,code};
  alert('🔑 Демо код:\n\n'+code+'\n\n(Нақты SMS кейін қосылады)');
  document.getElementById('forgot-step2').style.display='block';
}
function doForgotReset(){
  if(!pendingForgot)return;
  const code=document.getElementById('forgot-code').value.trim();
  const pass=document.getElementById('forgot-pass').value;
  if(code!==pendingForgot.code){alert('Код қате!');return}
  if(!pass||pass.length<4){alert('Пароль кемінде 4 таңба');return}
  const profiles=LS.get('ubt_profiles',{});
  Object.keys(profiles).forEach(k=>{if(profiles[k].id===pendingForgot.userId)profiles[k].password=pass});
  LS.set('ubt_profiles',profiles);
  pendingForgot=null;
  alert('✅ Пароль өзгертілді! Кіріңіз.');
  showLoginBox();
}
function getChatMessages(){return LS.get('ubt_chat',[])}
function saveChatMessages(m){LS.set('ubt_chat',m)}
function threadKey(x){return String(x||'').trim().toLowerCase()}
function threadOf(m){return threadKey(m.role==='admin'?m.to:m.from)}
function newMsgId(){return 'm_'+Date.now()+'_'+Math.random().toString(36).slice(2,7)}
function sendChatMsg(){
  if(!chatLogin){alert('Алдымен логиніңізді жазыңыз');return}
  const text=document.getElementById('chat-text').value.trim();
  if(!text){alert('Хабарлама жазыңыз');return}
  const msgs=getChatMessages();
  msgs.push({id:newMsgId(),from:chatLogin,thread:threadKey(chatLogin),text:text,role:'user',time:new Date().toLocaleString('kk-KZ'),read:false});
  saveChatMessages(msgs);
  document.getElementById('chat-text').value='';
  renderChatMessages();
}
// Пайдаланушы тек өз логинінің чатын көреді; өшіру батырмасы жоқ
function renderChatMessages(){
  const el=document.getElementById('chat-messages');
  if(!el||!chatLogin)return;
  const key=threadKey(chatLogin);
  const list=getChatMessages().filter(m=>threadOf(m)===key);
  if(!list.length){
    el.innerHTML='<div style="text-align:center;color:#667;padding:40px 16px;font-size:13px">Хабарлама жоқ.<br>Админге сұрағыңызды жіберіңіз.</div>';
    return;
  }
  el.innerHTML=list.map(m=>{
    const isUser=m.role==='user';
    return `<div style="display:flex;justify-content:${isUser?'flex-end':'flex-start'}">
      <div style="max-width:75%;padding:8px 12px;border-radius:12px;font-size:13px;line-height:1.4;background:${isUser?'#dcf8c6':'#fff'};box-shadow:0 1px 1px rgba(0,0,0,.08);word-break:break-word">
        ${!isUser?'<div style="font-size:11px;color:#075e54;font-weight:600;margin-bottom:2px">Админ</div>':''}
        <div>${esc(m.text)}</div>
        <div style="font-size:10px;color:#667;text-align:right;margin-top:4px">${esc(m.time||'')}</div>
      </div>
    </div>`;
  }).join('');
  el.scrollTop=el.scrollHeight;
}

// ---------- Админ жағы: әр логин бөлек чат, өшіруді тек админ жасай алады ----------
let adminOpenThread=null;
function renderAdminChat(){
  const el=document.getElementById('admin-chat');if(!el)return;
  const msgs=getChatMessages();
  const threads={};
  msgs.forEach((m,idx)=>{
    const k=threadOf(m);if(!k)return;
    const t=threads[k]||(threads[k]={key:k,name:'',list:[],lastIdx:0});
    t.list.push(m);t.lastIdx=idx;
    if(m.role!=='admin'&&m.from)t.name=m.from;
  });
  const arr=Object.values(threads).sort((a,b)=>b.lastIdx-a.lastIdx);
  if(!arr.length){el.innerHTML='<p class="sub">Хабарлама жоқ</p>';return}
  el.innerHTML=arr.map((t,i)=>{
    const name=t.name||t.list[0].to||t.key;
    const unread=t.list.filter(m=>m.role!=='admin'&&!m.read).length;
    const inId='ar_'+i;
    return `<details class="card" style="padding:12px 14px;margin-bottom:0" ${adminOpenThread===t.key?'open':''} ontoggle="adminToggleThread(${jsq(t.key)},this.open)">
      <summary style="cursor:pointer;display:flex;align-items:center;gap:8px;flex-wrap:wrap">
        <b>👤 ${esc(name)}</b>
        ${unread?`<span class="badge" style="background:#fee2e2;color:var(--err)">${unread} жаңа</span>`:''}
        <span class="sub">${t.list.length} хабарлама</span>
      </summary>
      <div style="display:flex;flex-direction:column;gap:8px;margin:12px 0;max-height:320px;overflow-y:auto;padding:10px;background:#e5ddd5;border-radius:10px">
        ${t.list.map(m=>{
          const isUser=m.role!=='admin';
          return `<div style="display:flex;justify-content:${isUser?'flex-start':'flex-end'}">
            <div style="max-width:80%;padding:8px 12px;border-radius:12px;font-size:13px;background:${isUser?'#fff':'#dcf8c6'};word-break:break-word">
              <div style="font-size:11px;color:#075e54;font-weight:600;margin-bottom:2px">${isUser?esc(m.from||name):'Админ'}</div>
              <div>${esc(m.text)}</div>
              <div style="display:flex;justify-content:space-between;align-items:center;gap:10px;margin-top:4px">
                <span style="font-size:10px;color:#667">${esc(m.time||'')}</span>
                <button class="btn btn-d btn-sm" style="padding:2px 8px;font-size:11px" onclick="adminDelChatMsg(${jsq(m.id)})">✕</button>
              </div>
            </div></div>`}).join('')}
      </div>
      <div style="display:flex;gap:8px;margin-bottom:8px">
        <input id="${inId}" placeholder="Жауап жазыңыз..." style="flex:1;padding:10px 12px;border:1px solid var(--b);border-radius:10px;font-size:14px;font-family:inherit" onkeydown="if(event.key==='Enter')adminSendReply(${jsq(t.key)},'${inId}')">
        <button class="btn btn-p btn-sm" onclick="adminSendReply(${jsq(t.key)},'${inId}')">Жіберу</button>
      </div>
      <button class="btn btn-d btn-sm" onclick="adminDelThread(${jsq(t.key)})">🗑 Бүкіл чатты өшіру</button>
    </details>`;
  }).join('');
}
function adminToggleThread(key,isOpen){
  if(!user||!user.isAdmin)return;
  if(isOpen){
    adminOpenThread=key;
    const msgs=getChatMessages();let ch=false;
    msgs.forEach(m=>{if(threadOf(m)===key&&m.role!=='admin'&&!m.read){m.read=true;ch=true}});
    if(ch)saveChatMessages(msgs);
  }else if(adminOpenThread===key){adminOpenThread=null}
}
function adminSendReply(key,inputId){
  if(!user||!user.isAdmin)return;
  const inp=document.getElementById(inputId);if(!inp)return;
  const text=inp.value.trim();if(!text)return;
  const msgs=getChatMessages();
  const first=msgs.find(m=>threadOf(m)===key&&m.role!=='admin');
  msgs.push({id:newMsgId(),from:'Админ',to:first?first.from:key,thread:key,text:text,role:'admin',time:new Date().toLocaleString('kk-KZ'),read:true});
  saveChatMessages(msgs);
  adminOpenThread=key;renderAdminChat();
}
function adminDelChatMsg(id){
  if(!user||!user.isAdmin)return;
  if(!confirm('Хабарламаны өшіру?'))return;
  saveChatMessages(getChatMessages().filter(m=>m.id!==id));
  renderAdminChat();
}
function adminDelThread(key){
  if(!user||!user.isAdmin)return;
  if(!confirm('Осы адаммен барлық хабарламаны өшіру?'))return;
  saveChatMessages(getChatMessages().filter(m=>threadOf(m)!==key));
  if(adminOpenThread===key)adminOpenThread=null;
  renderAdminChat();
}
function doLogout(){LS.set('ubt_current',null);user=null;chatLogin=null;showLoginBox();showScr('s-login')}
function getUserStats(id){
  const all=LS.get('ubt_user_stats',{});
  if(!all[id]) all[id]={points:0,title:'',stars:0,verified:false};
  return all[id];
}
function starStr(n){
  n=Math.max(0,Math.min(5,n||0));
  return '★'.repeat(n)+'☆'.repeat(5-n);
}
function setUserStats(id,stats){
  const all=LS.get('ubt_user_stats',{});
  all[id]=stats;LS.set('ubt_user_stats',all);
}
function addPoints(pts){
  if(!user||user.isAdmin) return;
  const s=getUserStats(user.id);
  s.points=(s.points||0)+pts;
  setUserStats(user.id,s);
  refreshProfileBar();
}
function refreshProfileBar(){
  if(!user)return;
  document.getElementById('pname').textContent=user.name;
  document.getElementById('avatar').textContent=user.name[0].toUpperCase();
  const s=user.isAdmin?{points:0,title:'👑 Админ',stars:5,verified:true}:getUserStats(user.id);
  document.getElementById('p-points').textContent=s.points||0;
  document.getElementById('p-title').textContent=s.title||'Жаңа ойыншы';
  document.getElementById('p-stars').textContent=starStr(s.stars||0);
  const v=document.getElementById('p-verified');
  if(v){v.style.display=s.verified?'block':'none'}
  document.getElementById('admin-btn').style.display=user.isAdmin?'inline-flex':'none';
}
function enterApp(){
  refreshProfileBar();
  showScr('s-home');
}
function showMyProfile(){
  const s=user.isAdmin?{points:0,title:'👑 Админ',stars:5,verified:true}:getUserStats(user.id);
  document.getElementById('prof-avatar').textContent=user.name[0].toUpperCase();
  document.getElementById('prof-name').textContent=user.name+(s.verified?' ✓':'');
  document.getElementById('prof-title').textContent=s.title||'Атақ жоқ';
  document.getElementById('prof-stars').textContent=starStr(s.stars||0);
  document.getElementById('prof-points').textContent=s.points||0;
  const pv=document.getElementById('prof-verified');
  if(pv) pv.style.display=s.verified?'block':'none';
  const rank=getRankPosition(user.id);
  document.getElementById('prof-rank').textContent=rank?('Рейтинг: #'+rank):'Рейтинг: —';
  showScr('s-profile');
}
function getRankPosition(id){
  const board=getLeaderboard();
  const i=board.findIndex(x=>x.id===id);
  return i>=0?i+1:null;
}
function getLeaderboard(){
  const profiles=LS.get('ubt_profiles',{});
  const stats=LS.get('ubt_user_stats',{});
  const list=Object.values(profiles).map(p=>{
    const s=stats[p.id]||{points:0,title:'',stars:0};
    return {id:p.id,name:p.name,points:s.points||0,title:s.title||'',stars:s.stars||0};
  });
  list.sort((a,b)=>b.points-a.points);
  return list;
}
function showRanking(){
  const board=getLeaderboard();
  const el=document.getElementById('rank-list');
  if(!board.length){el.innerHTML='<div class="empty"><div class="ic">🏆</div><p>Әзірге ешкім жоқ</p></div>';showScr('s-ranking');return}
  const medals=['🥇','🥈','🥉'];
  el.innerHTML=board.map((u,i)=>`
    <div class="item" style="${u.id===user.id?'border-color:var(--p);background:#eff6ff':''}">
      <div style="width:36px;height:36px;border-radius:50%;background:var(--p);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;flex-shrink:0">${esc(u.name[0].toUpperCase())}</div>
      <div class="info">
        <h4>${medals[i]||('#'+(i+1))} ${esc(u.name)} ${u.id===user.id?'(сіз)':''}</h4>
        <p>${esc(u.title||(u.stars?('⭐'.repeat(Math.min(u.stars,5))):'—'))}</p>
      </div>
      <div style="font-weight:700;color:var(--p);font-size:16px">⭐ ${u.points}</div>
    </div>`).join('');
  showScr('s-ranking');
}
(function(){const u=LS.get('ubt_current');if(u&&u.name){user=u;enterApp()}})();

function showAdmin(){
  if(!user||!user.isAdmin){alert('Қолжетімсіз');return}
  const tests=allTests();
  const profiles=LS.get('ubt_profiles',{});
  const formulas=LS.get('ubt_formulas',[]);
  const pending=tests.filter(t=>t.status==='pending');
  const approved=tests.filter(t=>t.isPublic||t.status==='approved');
  const users=Object.values(profiles);

  document.getElementById('admin-stats-grid').innerHTML=`
    <div class="mode" style="cursor:default"><div class="ic">👥</div><h3>${users.length}</h3><p>Тіркелгендер</p></div>
    <div class="mode" style="cursor:default"><div class="ic">📚</div><h3>${tests.length}</h3><p>Барлық тест</p></div>
    <div class="mode" style="cursor:default"><div class="ic">⏳</div><h3>${pending.length}</h3><p>Күтіп тұр</p></div>
    <div class="mode" style="cursor:default"><div class="ic">🌐</div><h3>${approved.length}</h3><p>Жарияланған</p></div>`;

  document.getElementById('admin-pending').innerHTML=pending.length?pending.map(t=>`
    <div class="item"><div class="info"><h4>${esc(t.topic)}</h4>
      <p>${esc(t.subjectName||'')} · ${t.questions.length} сұрақ · ${esc(t.authorName||'')}</p></div>
      <div class="acts">
        <button class="btn btn-ok btn-sm" onclick="approveTest('${t.id}')">✓ Мақұлдау</button>
        <button class="btn btn-d btn-sm" onclick="rejectTest('${t.id}')">✕ Бас тарту</button>
      </div></div>`).join(''):'<p class="sub">Күтіп тұрған тест жоқ</p>';

  document.getElementById('admin-users').innerHTML=users.length?users.map(p=>{
    const s=getUserStats(p.id);
    return `<div class="item" style="flex-wrap:wrap">
      <div style="position:relative">
        <div style="width:40px;height:40px;border-radius:50%;background:var(--p);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700">${esc((p.name||'?')[0].toUpperCase())}</div>
        ${s.verified?'<span style="position:absolute;bottom:-2px;right:-2px;background:#2563eb;color:#fff;width:16px;height:16px;border-radius:50%;font-size:10px;line-height:16px;text-align:center">✓</span>':''}
      </div>
      <div class="info"><h4>${esc(p.name)}</h4><p>⭐ ${s.points||0} · ${esc(s.title||'Атақ жоқ')} · <span style="color:#f59e0b">${starStr(s.stars||0)}</span></p></div>
      <div class="acts">
        <button class="btn btn-p btn-sm" onclick="adminViewUser(${jsq(p.id)})">Профиль</button>
        <button class="btn btn-ok btn-sm" onclick="adminToggleVerify(${jsq(p.id)})">${s.verified?'✓ Бар':'Галочка'}</button>
        <button class="btn btn-w btn-sm" onclick="adminSetTitle(${jsq(p.id)})">Атақ</button>
        <button class="btn btn-s btn-sm" onclick="adminSetStars(${jsq(p.id)})">Жұлдыз</button>
        <button class="btn btn-d btn-sm" onclick="adminDelUser(${jsq(p.id)})">Өшіру</button>
      </div></div>`}).join(''):'<p class="sub">Профиль жоқ</p>';
  // password change block
  let passBox=document.getElementById('admin-pass-box');
  if(!passBox){
    const wrap=document.getElementById('admin-users').parentElement;
    passBox=document.createElement('div');
    passBox.id='admin-pass-box';
    passBox.className='card';
    passBox.style.padding='20px';
    passBox.style.marginTop='12px';
    passBox.innerHTML=`<h3 style="margin-bottom:12px">🔑 Админ паролі</h3>
      <div class="fg"><label>Жаңа пароль</label><input id="new-admin-pass" type="password" placeholder="Жаңа пароль"></div>
      <button class="btn btn-p btn-sm" onclick="changeAdminPass()">Парольді өзгерту</button>`;
    wrap.appendChild(passBox);
  }

  document.getElementById('admin-tests').innerHTML=tests.length?tests.map(t=>`
    <div class="item"><div class="info"><h4>${esc(t.topic)}</h4>
      <p>${esc(t.subjectName||'')} · ${t.questions.length} сұрақ · ${esc(t.authorName||'')} · ${t.isPublic||t.status==='approved'?'🌐 Жария':t.status==='pending'?'⏳ Күту':'🔒 Жеке'}</p></div>
    <div class="acts"><button class="btn btn-d btn-sm" onclick="adminDelTest('${t.id}')">Өшіру</button></div></div>`).join(''):'<p class="sub">Тест жоқ</p>';

  document.getElementById('admin-formulas').innerHTML=formulas.length?formulas.map((f,i)=>`
    <div class="item"><div class="info"><h4>${esc(f.title)}</h4><p>${esc(f.subject)} · ${esc(f.authorName||'')} · ${esc(f.body)}</p></div>
    <div class="acts"><button class="btn btn-d btn-sm" onclick="adminDelFormula(${i})">Өшіру</button></div></div>`).join(''):'<p class="sub">Формула жоқ</p>';

  renderAdminChat();

  showScr('s-admin');
}
function adminDelTest(id){if(!confirm('Тестті өшіру?'))return;saveAllTests(allTests().filter(t=>t.id!==id));showAdmin()}
function approveTest(id){
  const all=allTests();const t=all.find(x=>x.id===id);
  if(t){t.isPublic=true;t.status='approved';saveAllTests(all);showAdmin()}
}
function rejectTest(id){
  const all=allTests();const t=all.find(x=>x.id===id);
  if(t){t.isPublic=false;t.status='rejected';saveAllTests(all);showAdmin()}
}
function adminDelUser(id){
  if(!user||!user.isAdmin)return;
  const profiles=LS.get('ubt_profiles',{});
  const pr=Object.values(profiles).find(x=>x.id===id);
  if(!confirm((pr?pr.name:'')+' профилін өшіру?'))return;
  Object.keys(profiles).forEach(k=>{if(profiles[k].id===id)delete profiles[k]});
  LS.set('ubt_profiles',profiles);
  saveAllTests(allTests().filter(t=>t.authorId!==id));
  const stats=LS.get('ubt_user_stats',{});delete stats[id];LS.set('ubt_user_stats',stats);
  showAdmin();
}
function adminSetTitle(id){
  const s=getUserStats(id);
  const t=prompt('Атақ беріңіз (мыс: Алтын оқушы, Шебер):',s.title||'');
  if(t===null)return;
  s.title=t.trim();setUserStats(id,s);showAdmin();
}
function adminSetStars(id){
  const s=getUserStats(id);
  const n=prompt('Жұлдыз саны (0-5):',String(s.stars||0));
  if(n===null)return;
  s.stars=Math.max(0,Math.min(5,parseInt(n)||0));setUserStats(id,s);showAdmin();
}
function adminToggleVerify(id){
  const s=getUserStats(id);
  s.verified=!s.verified;
  setUserStats(id,s);showAdmin();
}
function changeAdminPass(){
  const p=document.getElementById('new-admin-pass').value.trim();
  if(!p||p.length<4){alert('Пароль кемінде 4 таңба болсын!');return}
  setAdminPass(p);
  document.getElementById('new-admin-pass').value='';
  alert('Админ паролі өзгертілді!');
}
let viewingUserId=null;
function adminViewUser(id){
  if(!user||!user.isAdmin)return;
  viewingUserId=id;
  const profiles=LS.get('ubt_profiles',{});
  const p=Object.values(profiles).find(x=>x.id===id);
  if(!p){alert('Табылмады');return}
  const s=getUserStats(id);
  document.getElementById('uv-avatar').textContent=(p.name||'?')[0].toUpperCase();
  document.getElementById('uv-name').textContent=p.name+(s.verified?' ✓':'');
  document.getElementById('uv-info').textContent=`⭐ ${s.points||0} · ${s.title||'атақ жоқ'} · ${starStr(s.stars||0)}`;
  document.getElementById('uv-login').value=p.name||'';
  document.getElementById('uv-curpass').value=p.password||'(пароль жоқ)';
  const hist=LS.get('ubt_hist_'+id,[]);
  document.getElementById('uv-hist').innerHTML=hist.length?hist.map(h=>`
    <div class="item"><div class="info"><h4>${esc(h.topic||'Тест')}</h4><p>${h.date}</p></div>
    <div style="font-weight:700;color:var(--p)">${h.score}/${h.max}</div></div>`).join(''):'<p class="sub">Тест тапсырмаған</p>';
  const mist=LS.get('ubt_mistakes_'+id,[]);
  document.getElementById('uv-mist').innerHTML=mist.length?mist.map(q=>`
    <div class="item"><div class="info"><h4>${esc((q.text||'').substring(0,80))}</h4><p>${esc(q.subjectName||'')}</p></div></div>`).join(''):'<p class="sub">Қате жоқ</p>';
  document.getElementById('uv-newpass').value='';
  showScr('s-user-view');
}
function adminChangeUserPass(){
  if(!viewingUserId)return;
  const pass=document.getElementById('uv-newpass').value;
  if(!pass||pass.length<4){alert('Пароль кемінде 4 таңба');return}
  const profiles=LS.get('ubt_profiles',{});
  Object.keys(profiles).forEach(k=>{if(profiles[k].id===viewingUserId)profiles[k].password=pass});
  LS.set('ubt_profiles',profiles);
  document.getElementById('uv-newpass').value='';
  document.getElementById('uv-curpass').value=pass;
  alert('Пароль өзгертілді!');
}
function adminDelFormula(i){
  if(!confirm('Формуланы өшіру?'))return;
  const f=LS.get('ubt_formulas',[]);f.splice(i,1);LS.set('ubt_formulas',f);showAdmin();
}

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
function publicTests(){return allTests().filter(t=>(t.isPublic||t.status==='approved')&&t.questions.length>0)}
function showFormulas(){
  renderFormulas();showScr('s-formulas');
}
function renderFormulas(){
  const list=document.getElementById('formula-list');
  const all=LS.get('ubt_formulas',[]);
  if(!all.length){list.innerHTML='<div class="empty"><div class="ic">📐</div><p>Әзірге формула жоқ</p></div>';return}
  list.innerHTML=all.map(f=>`<div class="item"><div class="info"><h4>${esc(f.title)}</h4>
    <p style="font-family:monospace;font-size:14px;color:var(--t);margin:6px 0">${esc(f.body)}</p>
    <p>${esc(f.subject)} · ${esc(f.authorName||'')}</p></div></div>`).join('');
}
function addFormula(){
  const title=document.getElementById('f-title').value.trim();
  const body=document.getElementById('f-body').value.trim();
  const subject=document.getElementById('f-subject').value;
  if(!title||!body){alert('Атау мен формуланы жазыңыз!');return}
  const all=LS.get('ubt_formulas',[]);
  all.unshift({title,body,subject,authorId:user.id,authorName:user.name,createdAt:new Date().toISOString()});
  LS.set('ubt_formulas',all);
  document.getElementById('f-title').value='';document.getElementById('f-body').value='';
  renderFormulas();alert('Формула сақталды!');
}

let draft={questions:[]};
function showCreate(){
  draft={questions:[]};
  document.getElementById('c-subject').value='';
  document.getElementById('c-topic').value='';document.getElementById('c-desc').value='';
  const req=document.getElementById('c-request');if(req)req.checked=false;
  document.getElementById('c-qtext').value='';document.getElementById('c-correct').value='';
  ['c-o0','c-o1','c-o2','c-o3'].forEach(id=>document.getElementById(id).value='');
  document.getElementById('opts-block').style.display='none';
  document.querySelector('input[name="c-cor"][value="0"]').checked=true;renderDraftQs();showScr('s-create');
}
function genWrong(){
  const correct=document.getElementById('c-correct').value.trim();
  if(!correct){alert('Алдымен дұрыс жауапты жазыңыз!');return false}
  const wrongs=makeDistractors(correct);
  const pos=Math.floor(Math.random()*4);
  const opts=['','','',''];
  opts[pos]=correct;
  if(wrongs){let wi=0;for(let i=0;i<4;i++){if(i!==pos)opts[i]=wrongs[wi++]}}
  opts.forEach((o,i)=>document.getElementById('c-o'+i).value=o);
  document.querySelector('input[name="c-cor"][value="'+pos+'"]').checked=true;
  document.getElementById('opts-block').style.display='block';
  if(!wrongs){alert('Бұл жауап үшін қате нұсқаларды автоматты түрде жасау мүмкін емес. Қалған 3 нұсқаны өзіңіз жазыңыз.');return false}
  return true;
}
// Тек жыл/сан түріндегі жауаптарға ғана сапалы қате нұсқа жасайды, әйтпесе null қайтарады
function makeDistractors(ans){
  const out=new Set();
  const yearM=ans.match(/(\d{3,4})/);
  if(yearM){
    const y=+yearM[1];
    const deltas=[-100,-50,-20,-15,-10,-5,-3,-2,-1,1,2,3,5,10,15,20,50,100].sort(()=>Math.random()-0.5);
    for(const d of deltas){
      const ny=y+d;if(ny<100)continue;
      out.add(ans.replace(yearM[1],String(ny)));
      if(out.size>=3)break;
    }
  }
  const numM=ans.match(/^(-?\d+(?:[.,]\d+)?)(\s+[^\d].*|[°%])?$/);
  if(out.size<3&&numM){
    const comma=numM[1].includes(',');
    const n=parseFloat(numM[1].replace(',','.'));
    const suf=numM[2]||'';
    const cands=[n+1,n-1,n+2,n-2,n*2,n/2,n+10,n-10,n+5,n-5,n*10,-n].filter(x=>isFinite(x)&&x!==n).sort(()=>Math.random()-0.5);
    for(const c of cands){
      let t=String(Math.round(c*100)/100);
      if(comma)t=t.replace('.',',');
      out.add(t+suf);
      if(out.size>=3)break;
    }
  }
  const res=[...out].filter(x=>x!==ans);
  return res.length>=3?res.slice(0,3):null;
}
function addQToDraft(){
  const text=document.getElementById('c-qtext').value.trim();
  const correctOnly=document.getElementById('c-correct').value.trim();
  // auto-gen if options empty
  if(correctOnly&&!document.getElementById('c-o0').value.trim()){if(!genWrong())return}
  const opts=[0,1,2,3].map(i=>document.getElementById('c-o'+i).value.trim());
  const correct=+document.querySelector('input[name="c-cor"]:checked').value;
  if(!text){alert('Сұрақ жазыңыз!');return}
  if(opts.some(o=>!o)){alert('Алдымен «Қате нұсқаларды жасау» басыңыз немесе 4 нұсқаны толтырыңыз!');return}
  draft.questions.push({id:'q_'+Date.now(),text,options:opts,correct,points:1});
  document.getElementById('c-qtext').value='';document.getElementById('c-correct').value='';
  ['c-o0','c-o1','c-o2','c-o3'].forEach(id=>document.getElementById(id).value='');
  document.getElementById('opts-block').style.display='none';
  document.querySelector('input[name="c-cor"][value="0"]').checked=true;renderDraftQs();
}
function renderDraftQs(){
  document.getElementById('c-count').textContent=draft.questions.length;
  const el=document.getElementById('c-qlist');
  if(!draft.questions.length){el.innerHTML='<p class="sub">Әзірге сұрақ жоқ</p>';return}
  el.innerHTML=draft.questions.map((q,i)=>`<div class="item"><div class="info"><h4>${i+1}. ${esc(q.text)}</h4><p>Дұрыс: ${['A','B','C','D'][q.correct]}</p></div>
    <div class="acts"><button class="btn btn-d btn-sm" onclick="draft.questions.splice(${i},1);renderDraftQs()">✕</button></div></div>`).join('');
}
function saveTest(){
  const subjEl=document.getElementById('c-subject');
  const subject=subjEl.value;
  const subjectName=subjEl.options[subjEl.selectedIndex]?.text||'';
  const topic=document.getElementById('c-topic').value.trim();
  const requestPub=document.getElementById('c-request')?.checked||false;
  if(!subject){alert('Пәнді таңдаңыз!');return}
  if(!topic){alert('Тақырыпты міндетті түрде жазыңыз!');return}
  if(!draft.questions.length){alert('Кемінде 1 сұрақ қосыңыз!');return}
  const test={
    id:'t_'+Date.now(),subject,subjectName,topic,
    desc:document.getElementById('c-desc').value.trim(),
    isPublic:false,
    status:requestPub?'pending':'private',
    authorId:user.id,authorName:user.name,
    questions:draft.questions,createdAt:new Date().toISOString()
  };
  // admin can publish directly
  if(user.isAdmin&&requestPub){test.isPublic=true;test.status='approved'}
  const all=allTests();all.unshift(test);saveAllTests(all);
  alert(requestPub&&!user.isAdmin?'✅ Тест сақталды. Админ мақұлдаған соң жарияланады.':'✅ Тест сақталды!');
  showMyTests();
}

function showMyTests(){
  const list=document.getElementById('my-list');const tests=myTests();
  if(!tests.length){list.innerHTML='<div class="empty"><div class="ic">📭</div><p>Сізде әзірге тест жоқ.<br>«Тест құру» арқылы жасаңыз.</p></div>'}
  else{list.innerHTML=tests.map(t=>{
    let badge='<span class="badge badge-priv">🔒 Жеке</span>';
    if(t.isPublic||t.status==='approved')badge='<span class="badge badge-pub">🌐 Жария</span>';
    else if(t.status==='pending')badge='<span class="badge" style="background:#fef3c7;color:#92400e">⏳ Күтуде</span>';
    else if(t.status==='rejected')badge='<span class="badge badge-err">Бас тартылған</span>';
    return `<div class="item"><div class="info"><h4>${esc(t.topic)}</h4>
    <p>${esc(t.subjectName||'')} · ${t.questions.length} сұрақ · ${badge}</p></div>
    <div class="acts">
      <button class="btn btn-p btn-sm" onclick="startUserTest('${t.id}')">Бастау</button>
      <button class="btn btn-s btn-sm" onclick="editTest('${t.id}')">+ Сұрақ</button>
      ${t.status!=='pending'&&t.status!=='approved'&&!t.isPublic?`<button class="btn btn-w btn-sm" onclick="requestPub('${t.id}')">Жариялауға</button>`:''}
      <button class="btn btn-d btn-sm" onclick="delTest('${t.id}')">✕</button>
    </div></div>`}).join('')}
  showScr('s-mytests');
}
function requestPub(id){
  const all=allTests();const t=all.find(x=>x.id===id);
  if(!t)return;
  if(user.isAdmin){t.isPublic=true;t.status='approved';saveAllTests(all);alert('Жарияланды!');showMyTests();return}
  t.status='pending';t.isPublic=false;saveAllTests(all);alert('Админге жіберілді. Мақұлдаған соң жарияланады.');showMyTests();
}
function delTest(id){if(!confirm('Тестті өшіру керек пе?'))return;saveAllTests(allTests().filter(t=>t.id!==id));showMyTests()}

function showPublicTests(){
  const list=document.getElementById('public-list');const tests=publicTests();
  if(!tests.length){list.innerHTML='<div class="empty"><div class="ic">🌐</div><p>Әзірге жария тест жоқ.<br>Өзіңіз құрып, «Интернетке шығару» белгілеңіз.</p></div>'}
  else{list.innerHTML=tests.map(t=>`<div class="item"><div class="info"><h4>${esc(t.topic)}</h4>
    <p>${esc(t.subjectName||'')} · ${t.questions.length} сұрақ · Автор: ${esc(t.authorName||'Аноним')}${t.desc?' · '+esc(t.desc):''}</p></div>
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
  document.getElementById('edit-qlist').innerHTML=t.questions.map((q,i)=>`<div class="item"><div class="info"><h4>${i+1}. ${esc(q.text)}</h4></div>
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
  const label=(t.subjectName?t.subjectName+' · ':'')+(t.topic||'Тест');
  st=baseState();st.questions=t.questions.map(q=>({...q,subjectName:label}));st.subjectName=label;st.testId=id;
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
  document.getElementById('opts').innerHTML=q.options.map((o,i)=>`<div class="op${st.answers[q.id]===i?' sel':''}" onclick="selOpt(${i})"><span class="ol">${L[i]}</span><span class="ot">${esc(o)}</span></div>`).join('');
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

function startTimer(){stopTimer();updTimer();st.timerInterval=setInterval(()=>{st.timerSeconds--;updTimer();if(st.timerSeconds<=0){stopTimer();alert('Уақыт аяқталды!');finishTest(true)}},1000)}
function stopTimer(){if(st.timerInterval){clearInterval(st.timerInterval);st.timerInterval=null}}
function updTimer(){const t=Math.max(0,st.timerSeconds);const h=Math.floor(t/3600),m=Math.floor((t%3600)/60),s=t%60;const el=document.getElementById('timer');el.textContent=`${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;el.classList.remove('warn','dang');if(t<=300)el.classList.add('dang');else if(t<=900)el.classList.add('warn')}

function finishTest(force){
  if(!force&&!confirm('Тестті аяқтау керек пе?'))return;stopTimer();
  let score=0,max=st.questions.length,wrong=[];
  st.questions.forEach(q=>{if(st.answers[q.id]===q.correct)score++;else wrong.push({...q,userAnswer:st.answers[q.id]})});
  if(!st.isMistakes&&wrong.length){let m=LS.get('ubt_mistakes_'+user.id,[]);const ids=new Set(m.map(x=>x.id));wrong.forEach(q=>{if(!ids.has(q.id))m.push(q)});LS.set('ubt_mistakes_'+user.id,m)}
  let hist=LS.get('ubt_hist_'+user.id,[]);hist.unshift({date:new Date().toLocaleString('kk-KZ'),score,max,topic:st.subjectName,answers:{...st.answers},questions:st.questions.map(q=>({id:q.id,text:q.text,options:q.options,correct:q.correct}))});
  if(hist.length>40)hist.pop();LS.set('ubt_hist_'+user.id,hist);
  // Points: 10 per correct + bonus for high %
  let gained=score*10;
  const pct=max?score/max:0;
  if(pct>=1) gained+=50; else if(pct>=0.8) gained+=25; else if(pct>=0.5) gained+=10;
  if(!st.isMistakes) addPoints(gained);
  st.lastWrong=wrong;st.lastScore={score,max,gained};
  document.getElementById('sc').textContent=score;document.getElementById('sm').textContent=max;
  document.getElementById('res-break').innerHTML=`<div class="res-row"><span>${esc(st.subjectName||'Тест')}</span><span style="font-weight:700;color:var(--p)">${score} / ${max}</span></div>
    ${!st.isMistakes?`<div class="res-row"><span>Алынған ұпай</span><span style="font-weight:700;color:var(--ok)">+${gained} ⭐</span></div>`:''}`;
  showScr('s-res');
}
function reviewAns(){
  const L=['A','B','C','D'];
  document.getElementById('rev-list').innerHTML=st.questions.map((q,i)=>{const ua=st.answers[q.id],ok=ua===q.correct;
    return `<div class="rev ${ok?'ok':'bad'}"><div class="rh"><span>Сұрақ ${i+1}</span><span>${ok?'✓ Дұрыс':'✗ Қате'}</span></div>
      <div class="rq">${esc(q.text)}</div>${ua!==undefined?`<div class="ra u">Сіз: <b>${L[ua]}) ${esc(q.options[ua])}</b></div>`:'<div class="ra u">Жауап жоқ</div>'}
      ${!ok?`<div class="ra c">Дұрыс: <b>${L[q.correct]}) ${esc(q.options[q.correct])}</b></div>`:''}</div>`}).join('');
  showScr('s-rev');
}
function showHistory(){
  const hist=LS.get('ubt_hist_'+user.id,[]);
  document.getElementById('hist-list').innerHTML=hist.length?hist.map(h=>`<div class="item"><div class="info"><h4>${esc(h.topic||'Тест')}</h4><p>${h.date}</p></div>
    <div style="font-weight:700;color:var(--p)">${h.score}/${h.max}</div></div>`).join(''):'<div class="empty"><div class="ic">📭</div><p>Тарих бос</p></div>';
  showScr('s-hist');
}
function showMistakes(){
  const m=LS.get('ubt_mistakes_'+user.id,[]);const btn=document.getElementById('mist-start');
  if(!m.length){document.getElementById('mist-list').innerHTML='<div class="empty"><div class="ic">🎉</div><p>Қате жоқ!</p></div>';btn.style.display='none'}
  else{document.getElementById('mist-list').innerHTML=m.map(q=>`<div class="item"><div class="info"><h4>${esc(q.text.substring(0,70)+(q.text.length>70?'...':''))}</h4><p>${esc(q.subjectName||'')}</p></div></div>`).join('');btn.style.display='inline-flex'}
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
