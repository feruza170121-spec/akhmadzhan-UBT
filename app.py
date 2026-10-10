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

body.locked{user-select:none;-webkit-user-select:none}
#lock-ov{display:none;position:fixed;inset:0;z-index:100000;background:rgba(15,23,42,.97);color:#fff;align-items:center;justify-content:center;text-align:center;padding:24px}
#lock-ov.show{display:flex}
#lock-ov .box{max-width:440px}
#lock-ov h2{margin:10px 0}
#lock-ov p{opacity:.85;margin-bottom:18px;font-size:14px}
.stat-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:12px}
.stat{background:var(--bg);border-radius:10px;padding:10px;text-align:center}
.stat b{display:block;font-size:20px;color:var(--p)}
.stat span{font-size:11px;color:var(--m)}
.chart-wrap{overflow-x:auto}
.tbar{display:flex;align-items:center;gap:8px;font-size:12px;margin:7px 0}
.tbar .tn{width:38%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.tbar .tb{flex:1;background:#e2e8f0;border-radius:10px;height:10px;overflow:hidden}
.tbar .tb i{display:block;height:100%;background:var(--p);border-radius:10px}
.tbar .tv{width:44px;text-align:right;font-weight:600}
@media(max-width:768px){.stat-grid{grid-template-columns:repeat(2,1fr)}}
/* ===== Қосымша мүмкіндіктер ===== */
#theme-btn{position:fixed;right:12px;bottom:12px;z-index:90;width:42px;height:42px;border-radius:50%;padding:0;font-size:18px;box-shadow:0 2px 10px rgba(0,0,0,.18)}
body.in-test #theme-btn{display:none}
#confetti{position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:99990}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px}
.chip{background:var(--c);border:1px solid var(--b);border-radius:20px;padding:6px 14px;font-size:13px}
.chip.warn{background:#fef3c7;color:#92400e;border-color:#fcd34d}
.quote{background:linear-gradient(135deg,#eff6ff,#f5f3ff);border-left:4px solid var(--p);border-radius:12px;padding:12px 14px;font-size:14px;font-style:italic;margin:10px 0;color:#1e293b;cursor:pointer}
.qotd-op{display:flex;gap:10px;align-items:flex-start;padding:10px 12px;border:2px solid var(--b);border-radius:11px;cursor:pointer;margin-bottom:7px;font-size:13px}
.qotd-op:hover{border-color:#93c5fd}
.qotd-op.ok{border-color:var(--ok);background:#dcfce7;color:#14532d}
.qotd-op.bad{border-color:var(--err);background:#fee2e2;color:#7f1d1d}
.qotd-op.lock{cursor:default}
.fcard{background:var(--c);border:2px solid var(--b);border-radius:18px;min-height:240px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:26px 20px;cursor:pointer;position:relative;animation:flipin .25s}
.fcard.back{border-color:var(--p);background:#eff6ff;color:#0f172a}
.fcard .flab{position:absolute;top:12px;left:16px;font-size:11px;font-weight:700;color:var(--m);text-transform:uppercase}
.fcard .ftxt{font-size:20px;font-weight:600;line-height:1.5}
.fcard .fhint{position:absolute;bottom:10px;font-size:11px;color:var(--m)}
@keyframes flipin{from{transform:rotateX(70deg);opacity:.3}to{transform:none;opacity:1}}
.podium{display:flex;align-items:flex-end;justify-content:center;gap:10px;margin:8px 0 20px}
.pod{flex:1;max-width:150px;text-align:center;min-width:0}
.pod .pcup{font-size:38px;line-height:1.1}
.pod.p1 .pcup{font-size:56px;animation:bob 2s ease-in-out infinite}
@keyframes bob{50%{transform:translateY(-6px)}}
.pod .pname{font-weight:700;font-size:13px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.pod .ppts{font-size:12px;color:var(--m)}
.pod .pbase{border-radius:10px 10px 0 0;color:#fff;font-weight:800;padding-top:8px;margin-top:6px;font-size:18px}
.pod.p1 .pbase{background:linear-gradient(#fbbf24,#f59e0b);height:84px}
.pod.p2 .pbase{background:linear-gradient(#cbd5e1,#94a3b8);height:62px}
.pod.p3 .pbase{background:linear-gradient(#fdba74,#c2763a);height:46px}
.item.me{border-color:var(--p);background:#eff6ff;color:#0f172a}
.item.me .info p{color:#475569}
.plan-day{background:var(--c);border:1px solid var(--b);border-radius:12px;padding:10px 14px;margin-bottom:8px}
.plan-day.today{border-color:var(--p);box-shadow:0 0 0 2px rgba(37,99,235,.15)}
.plan-day h4{font-size:13px;margin-bottom:6px}
.plan-day label{display:flex;gap:8px;align-items:flex-start;font-size:13px;margin-bottom:4px;cursor:pointer}
.plan-day label.done span{text-decoration:line-through;opacity:.55}
.ttable{width:100%;border-collapse:collapse;font-size:13px}
.ttable th,.ttable td{padding:8px 6px;border-bottom:1px solid var(--b);text-align:left;vertical-align:middle}
.ttable th{font-size:11px;color:var(--m);text-transform:uppercase}
.tscroll{overflow-x:auto}
.gl-item{background:var(--c);border:1px solid var(--b);border-radius:12px;padding:12px 14px}
.gl-item h4{font-size:14px;margin-bottom:3px}
.gl-item p{font-size:13px;color:var(--t)}
.gl-cat{font-size:10px;font-weight:700;color:var(--p);text-transform:uppercase;letter-spacing:.5px}
.katex{font-size:1.05em}
.katex-display{overflow-x:auto;overflow-y:hidden}

/* ===== Қараңғы режим ===== */
body.dark{--bg:#0b1220;--c:#162033;--t:#e5e7eb;--m:#9aa8bd;--b:#2b3a52;--p:#3b82f6;--pd:#2563eb;color-scheme:dark}
body.dark .prog-t,body.dark .timer,body.dark .qnum{background:#1e3a5f;color:#93c5fd}
body.dark .timer.warn{background:#3b2f0b;color:#fbbf24}
body.dark .timer.dang{background:#3f1515;color:#f87171}
body.dark .qn.cur{background:#1e3a5f}
body.dark .qn.ans{background:#14532d;color:#86efac;border-color:#166534}
body.dark .qn.flg{background:#422006;border-color:#a16207}
body.dark .op:hover{background:#1e293b}
body.dark .op.sel{background:#1e3a5f}
body.dark .rev .ra.u{background:#3f1515}
body.dark .rev .ra.c{background:#12301f}
body.dark .badge-pub{background:#1e3a5f}
body.dark .badge-priv{background:#1e293b}
body.dark .prog-w,body.dark .tbar .tb{background:#2b3a52}
body.dark .flag.on{background:#422006}
body.dark .quote{background:linear-gradient(135deg,#16233a,#1d1a38);color:#e5e7eb}
body.dark .fcard.back{background:#16233a;color:#e5e7eb}
body.dark .item.me{background:#16233a;color:#e5e7eb}
body.dark .item.me .info p{color:#9aa8bd}
body.dark .chip.warn{background:#422006;color:#fcd34d;border-color:#a16207}
body.dark .qotd-op.ok{background:#12301f;color:#bbf7d0}
body.dark .qotd-op.bad{background:#3f1515;color:#fecaca}
body.dark [style*="background:#eff6ff"],body.dark [style*="background:#f1f5f9"],body.dark [style*="background:#f0fdf4"],body.dark [style*="background:#fef2f2"],body.dark [style*="background:#fef3c7"],body.dark [style*="background:#dbeafe"],body.dark [style*="background:#f8fafc"],body.dark [style*="background:#fffbeb"]{background:#1e293b!important;color:#e5e7eb!important}
body.dark #contact-box,body.dark #contact-box *{color:#111}
body.dark #contact-box [style*="background:#075e54"] *,body.dark #contact-box [style*="background:#075e54"]{color:#fff}
body.dark #admin-chat input,body.dark #admin-chat textarea{color:#111}
.cbox{margin-top:8px}
.cmsgs{height:260px;overflow-y:auto;background:var(--bg);border:1px solid var(--b);border-radius:12px;padding:10px;display:flex;flex-direction:column;gap:6px}
.cmsg{max-width:82%;padding:7px 11px;border-radius:12px;font-size:13px;white-space:pre-wrap;word-break:break-word}
.cmsg.me{align-self:flex-end;background:var(--p);color:#fff}
.cmsg.other{align-self:flex-start;background:var(--c);border:1px solid var(--b)}
.cmsg.sys{align-self:center;background:#fef3c7;color:#92400e;font-size:12px;text-align:center}
.cmsg small{display:block;opacity:.7;font-size:10px;margin-top:2px}
.crow{display:flex;gap:8px;margin-top:8px}
.crow input{flex:1;padding:10px 12px;border:1px solid var(--b);border-radius:10px;background:var(--bg);color:var(--t);font-family:inherit;font-size:14px}
body.dark .cmsg.sys{background:#422006;color:#fcd34d}
</style>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js" onload="mathScreen()"></script>
</head>
<body>

<button id="theme-btn" class="btn btn-s" onclick="toggleTheme()" title="Қараңғы / жарық режим">🌙</button>
<canvas id="confetti"></canvas>

<div id="lock-ov"><div class="box"><div style="font-size:46px">🔒</div><h2 id="lock-title">Тест жалғасуда</h2><p id="lock-msg"></p><button class="btn btn-p" onclick="returnToTest()">Толық экранға оралу</button></div></div>

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
      <button class="btn btn-s btn-sm" style="width:100%;margin-bottom:10px" onclick="showTeacherReg()">👨‍🏫 Мұғалімдерге арналған кабинет</button>
      <button class="btn btn-w btn-sm" style="width:100%" onclick="showContactAdmin()">💬 Админге жазу</button>
    </div>
    <div class="card" id="register-box" style="display:none">
      <h3 style="margin-bottom:12px">Тіркелу</h3>
      <div class="fg"><label>Атыңыз (логин) *</label><input id="reg-name" placeholder="Атыңыз" maxlength="30"></div>
      <div class="fg"><label>Пароль *</label><input id="reg-pass" type="password" placeholder="Кемінде 4 таңба"></div>
      <div class="fg"><label>Парольді қайталаңыз *</label><input id="reg-pass2" type="password" placeholder="Қайталаңыз"></div>
      <button class="btn btn-p" style="width:100%;margin-bottom:10px" onclick="doRegister()">Тіркелу</button>
      <button class="btn btn-s btn-sm" style="width:100%;margin-bottom:10px" onclick="showTeacherReg()">👨‍🏫 Мұғалім ретінде тіркелу</button>
      <button class="btn btn-s" style="width:100%" onclick="showLoginBox()">Артқа</button>
    </div>
    <div class="card" id="teacher-reg-box" style="display:none">
      <h3 style="margin-bottom:6px">👨‍🏫 Мұғалімдерге арналған кабинет</h3>
      <p class="sub" style="margin-bottom:12px">Тіркелгеннен кейін өтініш админге түседі. Админ рұқсат бергенше мұғалім мүмкіндіктері ашылмайды.</p>
      <div class="fg"><label>Аты-жөніңіз (логин) *</label><input id="tr-name" placeholder="Мыс: Айгүл Серікқызы" maxlength="30"></div>
      <div class="fg"><label>Мектеп / пән</label><input id="tr-info" placeholder="Мыс: №12 мектеп, математика" maxlength="80"></div>
      <div class="fg"><label>Пароль *</label><input id="tr-pass" type="password" placeholder="Кемінде 4 таңба"></div>
      <div class="fg"><label>Парольді қайталаңыз *</label><input id="tr-pass2" type="password" placeholder="Қайталаңыз"></div>
      <button class="btn btn-p" style="width:100%;margin-bottom:10px" onclick="doRegisterTeacher()">Өтініш жіберу</button>
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
    <div class="card"><h3 style="margin-bottom:10px">📈 График</h3><div id="uv-chart"></div></div>
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
    <div id="home-extras"></div>
    <div class="grid2" style="margin-bottom:20px">
      <div class="mode" onclick="showPublicTests()"><div class="ic">🌐</div><h3>Жария тесттер</h3><p>Админ мақұлдаған</p></div>
      <div class="mode" onclick="showMyTests()"><div class="ic">📚</div><h3>Менің тесттерім</h3><p>Өз тесттеріңіз</p></div>
      <div class="mode" onclick="showCreate()"><div class="ic">➕</div><h3>Тест құру</h3><p>Атауы + сұрақтар</p></div>
      <div class="mode" onclick="showRanking()"><div class="ic">🏆</div><h3>Рейтинг</h3><p>Ортақ көшбасшылар</p></div>
    </div>
    <div class="row">
      <button class="btn btn-s btn-sm" onclick="showFormulas()">📐 Формула</button>
      <button class="btn btn-s btn-sm" onclick="showMistakes()">❌ Қателер</button>
      <button class="btn btn-s btn-sm" onclick="showHistory()">📋 Тарих</button>
      <button class="btn btn-s btn-sm" onclick="startQuickSubject()">⚡ Жылдам</button>
      <button class="btn btn-s btn-sm" onclick="showFileTest()">📂 Файлдан</button>
      <button class="btn btn-s btn-sm" onclick="showMyProfile()">📈 График</button>
      <button class="btn btn-s btn-sm" onclick="showFlash()">🃏 Флеш-карталар</button>
      <button class="btn btn-s btn-sm" onclick="showGloss()">📖 Глоссарий</button>
      <button class="btn btn-s btn-sm" onclick="showBookmarks()">🔖 Таңдаулылар</button>
      <button class="btn btn-s btn-sm" onclick="showPlanner()">🗓 Жоспар</button>
      <button class="btn btn-s btn-sm" onclick="showTeacher()">👨‍🏫 Мұғалім</button>
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
    <div class="card" id="prof-extra"></div>
    <div class="card"><h3 style="margin-bottom:10px">📈 Менің графигім</h3><div id="prof-chart"></div></div>
    <div class="card"><h3 style="margin-bottom:10px">📊 Тақырыптар бойынша орташа нәтиже</h3><div id="prof-topics"></div></div>
    <div class="row"><button class="btn btn-s" onclick="goHome()">Артқа</button></div>
  </div>
</div>

<div id="s-ranking" class="screen">
  <div class="wrap">
    <div class="hdr"><h2>🏆 Рейтинг</h2><p class="sub" id="rank-sub">Ең көп ұпай жинағандар</p></div>
    <div class="row" id="rank-tabs" style="margin-bottom:14px"></div>
    <div id="rank-podium"></div>
    <div id="rank-list" class="list"></div>
    <div id="rank-hall"></div>
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
    <div class="hdr"><h2>➕ Тест құру</h2><p class="sub">Тестке ат беріп, пәнді таңдаңыз да, сұрақтарды өзіңіз қосыңыз</p></div>
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
      <div class="fg"><label>Тест атауы * <span class="sub">(мыс: «Функция», «Ньютон заңдары»)</span></label><input id="c-topic" placeholder="Атауын жазыңыз (файл атынан автоматты толады)"></div>
      <div class="fg"><label>Сипаттама (міндетті емес)</label><input id="c-desc" placeholder="Қысқаша сипаттама"></div>
      <div class="fg"><label class="switch"><input type="checkbox" id="c-request"> 🌐 Жариялауға жіберу (админ мақұлдаған соң шығады)</label></div>
    </div>
    <div id="c-manual-host"></div>
    <div class="row">
      <button class="btn btn-p" onclick="createFromFile()">💾 Тестті сақтау</button>
      <button class="btn btn-s" onclick="goHome()">Болдырмау</button>
    </div>
  </div>
</div>

<div id="s-edit" class="screen">
  <div class="wrap">
    <div class="hdr"><h2 id="edit-title">Тестті өңдеу</h2><p class="sub">Жаңа сұрақтарды қолмен қосыңыз</p></div>
    <div id="e-manual-host"></div>
    <div id="edit-qlist" class="list"></div>
    <div class="row" style="margin-top:16px"><button class="btn btn-s" onclick="showMyTests()">Артқа</button></div>
  </div>
</div>

<div id="s-file" class="screen">
  <div class="wrap">
    <div class="hdr"><h2>📂 Файлдан тест тапсыру</h2><p class="sub">Сұрақтар файлын таңдаңыз немесе мәтінді қойыңыз</p></div>
    <div id="f-bulk-host"></div>
    <div class="row" style="margin-top:16px"><button class="btn btn-s" onclick="goHome()">Артқа</button></div>
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
        <div class="prog-t" id="viol" style="display:none;background:#fef2f2;color:var(--err)"></div>
      </div>
      <div class="qc">
        <div class="qh"><span class="qnum" id="qnum">Сұрақ 1</span><span style="display:flex;gap:6px"><button class="flag" id="bm" onclick="togBm()" title="Таңдаулыға сақтау">☆</button><button class="flag" id="flag" onclick="togFlag()">🚩</button></span></div>
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
      <div class="fg"><label>Формула</label><textarea id="f-body" placeholder="x = (-b ± √(b²-4ac)) / 2a  немесе LaTeX: $x=\frac{-b\pm\sqrt{D}}{2a}$"></textarea></div>
      <button class="btn btn-ok btn-sm" onclick="addFormula()">Сақтау</button>
    </div>
    <div id="formula-list" class="list"></div>
    <div class="row" style="margin-top:16px"><button class="btn btn-s" onclick="goHome()">Артқа</button></div>
  </div>
</div>

<div id="s-flash" class="screen">
  <div class="wrap">
    <div class="hdr"><h2>🃏 Флеш-карталар</h2><p class="sub">Карточканы басыңыз — артқы жағында жауабы шығады</p></div>
    <div class="card">
      <div class="fg"><label>Не жаттаймыз?</label><select id="fl-src"></select></div>
      <div class="row" style="justify-content:flex-start">
        <button class="btn btn-p btn-sm" onclick="startFlash(false)">▶ Бастау</button>
        <button class="btn btn-s btn-sm" onclick="startFlash(true)">🔀 Араластырып бастау</button>
      </div>
    </div>
    <div id="fl-area"></div>
    <div class="row" style="margin-top:16px"><button class="btn btn-s" onclick="goHome()">Артқа</button></div>
  </div>
</div>

<div id="s-gloss" class="screen">
  <div class="wrap">
    <div class="hdr"><h2>📖 Глоссарий</h2><p class="sub">ҰБТ-дағы маңызды даталар, терминдер, ережелер</p></div>
    <div class="fg"><input id="gl-q" placeholder="🔍 Іздеу: 1465, дискриминант, метафора..." oninput="renderGloss()"></div>
    <div class="row" id="gl-cats" style="justify-content:flex-start;margin-bottom:12px"></div>
    <div id="gl-count" class="sub" style="margin-bottom:8px"></div>
    <div id="gl-list" class="list"></div>
    <div class="row" style="margin-top:16px"><button class="btn btn-s" onclick="goHome()">Артқа</button></div>
  </div>
</div>

<div id="s-bm" class="screen">
  <div class="wrap">
    <div class="hdr"><h2>🔖 Таңдаулылар</h2><p class="sub">Қайталап қарайтын қиын немесе ұнаған сұрақтар</p></div>
    <div id="bm-list" class="list"></div>
    <div class="row" style="margin-top:16px">
      <button class="btn btn-p" id="bm-start" style="display:none" onclick="startBm()">▶ Таңдаулыларды шешу</button>
      <button class="btn btn-s" onclick="goHome()">Артқа</button>
    </div>
  </div>
</div>

<div id="s-plan" class="screen">
  <div class="wrap">
    <div class="hdr"><h2>🗓 Жеке оқу жоспары</h2><p class="sub">ҰБТ күнін таңдаңыз — күнделікті жоспар автоматты құрылады</p></div>
    <div class="card">
      <div class="fg"><label>ҰБТ тапсыратын күн</label><input type="date" id="pl-date"></div>
      <div class="fg"><label>Дайындалатын пәндер</label><div id="pl-subs"></div></div>
      <button class="btn btn-p btn-sm" onclick="savePlan()">💾 Жоспар құру</button>
    </div>
    <div id="pl-out"></div>
    <div class="row" style="margin-top:16px"><button class="btn btn-s" onclick="goHome()">Артқа</button></div>
  </div>
</div>

<div id="s-teacher" class="screen">
  <div class="wrap wide">
    <div class="hdr"><h2>👨‍🏫 Мұғалім / Куратор</h2><p class="sub">Сынып құрып, оқушылардың нәтижесін бақылаңыз</p></div>
    <div id="tch-notice"></div>
    <div class="card" id="tch-create-card">
      <h3 style="margin-bottom:10px">➕ Жаңа сынып</h3>
      <div class="fg"><input id="tch-name" placeholder="Сынып атауы (мыс: 11 «А»)" maxlength="40"></div>
      <button class="btn btn-ok btn-sm" onclick="createClass()">Сынып құру</button>
    </div>
    <div class="card" id="tch-req-card">
      <h3 style="margin-bottom:6px">📨 Сынып ашуға өтініш</h3>
      <p class="sub" style="margin-bottom:10px">Өтінішті админ қарайды. Админ 12 сағат ішінде жауап береді. Келесі өтінішті немесе хабарламаны 1 минуттан кейін жібере аласыз.</p>
      <div class="fg"><input id="tch-req-name" placeholder="Сынып атауы (мыс: 11 «А»)" maxlength="40"></div>
      <div class="fg"><textarea id="tch-req-note" placeholder="Қосымша ақпарат (міндетті емес): пән, оқушылар саны..." maxlength="300"></textarea></div>
      <button class="btn btn-p btn-sm" id="tch-req-btn" onclick="submitClassRequest()">📨 Өтініш жіберу</button>
      <span class="sub" id="tch-req-cd" style="margin-left:8px"></span>
    </div>
    <div id="tch-reqs"></div>
    <div id="tch-classes"></div>
    <div id="tch-chat"></div>
    <div id="tch-detail"></div>
    <div class="card">
      <h3 style="margin-bottom:6px">🔑 Оқушы: сыныпқа қосылу</h3>
      <p class="sub" style="margin-bottom:10px">Мұғалім берген кодты енгізіңіз</p>
      <div class="fg"><input id="tch-code" placeholder="Сынып коды" maxlength="8" style="text-transform:uppercase"></div>
      <button class="btn btn-p btn-sm" onclick="joinClass()">Қосылу</button>
      <div id="tch-joined" style="margin-top:12px"></div>
    </div>
    <div class="row"><button class="btn btn-s" onclick="goHome()">Артқа</button></div>
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
      <h3 style="margin-bottom:12px">🏫 Сынып ашу өтініштері</h3>
      <div id="admin-class-req" class="list"></div>
    </div>
    <div class="card" style="padding:20px">
      <h3 style="margin-bottom:12px">💬 Сынып чаттары</h3>
      <div id="admin-class-threads" class="list"></div>
      <div id="admin-class-chat"></div>
    </div>
    <div class="card" style="padding:20px">
      <h3 style="margin-bottom:12px">👨‍🏫 Мұғалім өтініштері</h3>
      <div id="admin-teacher-req" class="list"></div>
    </div>
    <div class="card" style="padding:20px">
      <h3 style="margin-bottom:12px">👥 Тіркелгендер</h3>
      <div class="fg"><input id="admin-user-q" placeholder="🔍 Атын жазып іздеу..." oninput="renderAdminUsers()"></div>
      <div id="admin-user-count" class="sub" style="margin-bottom:8px"></div>
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
  renderProgress('prof-chart','prof-topics',getProg(user.id));
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
(function(){const u=LS.get('ubt_current');if(u&&u.name){user=u;enterApp()}})();

function renderAdminUsers(){
  const el=document.getElementById('admin-users');if(!el)return;
  const q=((document.getElementById('admin-user-q')||{}).value||'').trim().toLowerCase();
  const tests=allTests();
  let users=Object.values(LS.get('ubt_profiles',{})).map(p=>{
    const st0=getUserStats(p.id);
    const pub=tests.filter(t=>t.authorId===p.id&&(t.isPublic||t.status==='approved'));
    return{p,s:st0,pub};
  });
  users.sort((a,b)=>(b.s.stars||0)-(a.s.stars||0)||(b.s.title?1:0)-(a.s.title?1:0)||(b.s.points||0)-(a.s.points||0)||String(a.p.name).localeCompare(String(b.p.name)));
  if(q)users=users.filter(u=>String(u.p.name||'').toLowerCase().indexOf(q)>=0);
  const cnt=document.getElementById('admin-user-count');
  if(cnt)cnt.textContent=q?('Табылды: '+users.length):('Барлығы: '+users.length+' · атақты/жұлдызы көптен бастап');
  el.innerHTML=users.length?users.map(u=>{
    const p=u.p,s=u.s;
    return `<div class="item" style="flex-wrap:wrap">
      <div style="position:relative">
        <div style="width:40px;height:40px;border-radius:50%;background:var(--p);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700">${esc((p.name||'?')[0].toUpperCase())}</div>
        ${s.verified?'<span style="position:absolute;bottom:-2px;right:-2px;background:#2563eb;color:#fff;width:16px;height:16px;border-radius:50%;font-size:10px;line-height:16px;text-align:center">✓</span>':''}
      </div>
      <div class="info"><h4>${esc(p.name)} ${p.role==='teacher'?(p.teacherApproved?'<span class="badge badge-pub">👨‍🏫 Мұғалім</span>':'<span class="badge" style="background:#fef3c7;color:#92400e">⏳ Мұғалім өтініші</span>'):''}</h4>
        <p>🔑 пароль: <b>${esc(p.password||'—')}</b></p>
        <p>⭐ ${s.points||0} · ${esc(s.title||'Атақ жоқ')} · <span style="color:#f59e0b">${starStr(s.stars||0)}</span></p>
        <p>🌐 Жариялаған тест: <b>${u.pub.length}</b>${u.pub.length?' — '+esc(u.pub.slice(0,3).map(t=>t.topic).join(', '))+(u.pub.length>3?'…':''):''}</p></div>
      <div class="acts">
        <button class="btn btn-p btn-sm" onclick="adminViewUser(${jsq(p.id)})">Профиль</button>
        <button class="btn btn-sm ${p.role==='teacher'&&p.teacherApproved?'btn-s':'btn-ok'}" onclick="adminSetTeacher(${jsq(p.id)},${!(p.role==='teacher'&&p.teacherApproved)})">${p.role==='teacher'&&p.teacherApproved?'Мұғалімді алу':'Мұғалім ету'}</button>
        <button class="btn btn-ok btn-sm" onclick="adminToggleVerify(${jsq(p.id)})">${s.verified?'✓ Бар':'Галочка'}</button>
        <button class="btn btn-w btn-sm" onclick="adminSetTitle(${jsq(p.id)})">Атақ</button>
        <button class="btn btn-s btn-sm" onclick="adminSetStars(${jsq(p.id)})">Жұлдыз</button>
        <button class="btn btn-d btn-sm" onclick="adminDelUser(${jsq(p.id)})">Өшіру</button>
      </div></div>`}).join(''):'<p class="sub">Ешкім табылмады</p>';
}
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

  renderAdminUsers();
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
  renderProgress('uv-chart',null,getProg(id));
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
function goHome(){if(lock.on)return;stopTimer();st=baseState();showScr('s-home')}

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

function showCreate(){
  document.getElementById('c-subject').value='';
  document.getElementById('c-topic').value='';
  document.getElementById('c-desc').value='';
  const req=document.getElementById('c-request');if(req)req.checked=false;
  clearManual('c');showScr('s-create');
}
function createFromFile(){
  const subjEl=document.getElementById('c-subject');
  const subject=subjEl.value;
  const subjectName=subjEl.options[subjEl.selectedIndex]?.text||'';
  const topic=document.getElementById('c-topic').value.trim();
  const requestPub=document.getElementById('c-request')?.checked||false;
  if(!subject){alert('Пәнді таңдаңыз!');return}
  if(!topic){alert('Тест атауын жазыңыз!');return}
  if(!draftQs.length){alert('Кемінде 1 сұрақ қосыңыз!');return}
  const r={qs:draftQs.slice()};
  const test={id:'t_'+Date.now(),subject,subjectName,topic,desc:document.getElementById('c-desc').value.trim(),isPublic:false,status:requestPub?'pending':'private',authorId:user.id,authorName:user.name,questions:r.qs,createdAt:new Date().toISOString()};
  if((user.isAdmin||isTeacherUser())&&requestPub){test.isPublic=true;test.status='approved'}
  const all=allTests();all.unshift(test);saveAllTests(all);
  clearManual('c');
  alert(requestPub&&!(user.isAdmin||isTeacherUser())?'✅ Тест сақталды ('+r.qs.length+' сұрақ). Админ мақұлдаған соң жарияланады.':'✅ Тест сақталды: '+r.qs.length+' сұрақ');
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
      <button class="btn btn-s btn-sm" onclick="editTest('${t.id}')">+ Сұрақ қосу</button>
      <button class="btn btn-s btn-sm" onclick="exportTest('${t.id}')">⬇ Файл</button>
      ${t.status!=='pending'&&t.status!=='approved'&&!t.isPublic?`<button class="btn btn-w btn-sm" onclick="requestPub('${t.id}')">Жариялауға</button>`:''}
      <button class="btn btn-d btn-sm" onclick="delTest('${t.id}')">✕</button>
    </div></div>`}).join('')}
  showScr('s-mytests');
}
function requestPub(id){
  const all=allTests();const t=all.find(x=>x.id===id);
  if(!t)return;
  if(user.isAdmin||isTeacherUser()){t.isPublic=true;t.status='approved';saveAllTests(all);alert('Жарияланды!');showMyTests();return}
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
  clearManual('e');renderEditList(t);showScr('s-edit');
}
function renderEditList(t){
  document.getElementById('edit-qlist').innerHTML=t.questions.map((q,i)=>`<div class="item"><div class="info"><h4>${i+1}. ${esc(q.text)}</h4></div>
    <div class="acts"><button class="btn btn-d btn-sm" onclick="removeQFromTest('${t.id}',${i})">✕</button></div></div>`).join('');
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
function beginTest(){showScr('s-test');renderNav();renderQ();startTimer();updateProg();lockStart()}
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

function startTimer(){stopTimer();updTimer();st.timerInterval=setInterval(()=>{st.timerSeconds--;updTimer();if(st.timerSeconds<=0){stopTimer();guardPause(()=>alert('Уақыт аяқталды!'));finishTest(true)}},1000)}
function stopTimer(){if(st.timerInterval){clearInterval(st.timerInterval);st.timerInterval=null}}
function updTimer(){const t=Math.max(0,st.timerSeconds);const h=Math.floor(t/3600),m=Math.floor((t%3600)/60),s=t%60;const el=document.getElementById('timer');el.textContent=`${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;el.classList.remove('warn','dang');if(t<=300)el.classList.add('dang');else if(t<=900)el.classList.add('warn')}

function finishTest(force){
  if(!force){const ok=guardPause(()=>confirm('Тестті аяқтау керек пе?'));if(!ok){lockReassert();return}}
  stopTimer();lockEnd();
  let score=0,max=st.questions.length,wrong=[];
  st.questions.forEach(q=>{if(st.answers[q.id]===q.correct)score++;else wrong.push({...q,userAnswer:st.answers[q.id]})});
  if(!st.isMistakes&&wrong.length){let m=LS.get('ubt_mistakes_'+user.id,[]);const ids=new Set(m.map(x=>x.id));wrong.forEach(q=>{if(!ids.has(q.id))m.push(q)});LS.set('ubt_mistakes_'+user.id,m)}
  {let pg=getProg(user.id);pg.push({t:Date.now(),score,max,topic:st.subjectName,viol:lock.viol});if(pg.length>200)pg=pg.slice(-200);LS.set('ubt_prog_'+user.id,pg)}
  let hist=LS.get('ubt_hist_'+user.id,[]);hist.unshift({date:new Date().toLocaleString('kk-KZ'),score,max,topic:st.subjectName,viol:lock.viol,answers:{...st.answers},questions:st.questions.map(q=>({id:q.id,text:q.text,options:q.options,correct:q.correct}))});
  if(hist.length>40)hist.pop();LS.set('ubt_hist_'+user.id,hist);
  // Points: 10 per correct + bonus for high %
  let gained=score*10;
  const pct=max?score/max:0;
  if(pct>=1) gained+=50; else if(pct>=0.8) gained+=25; else if(pct>=0.5) gained+=10;
  if(!st.isMistakes) addPoints(gained);
  st.lastWrong=wrong;st.lastScore={score,max,gained};
  document.getElementById('sc').textContent=score;document.getElementById('sm').textContent=max;
  document.getElementById('res-break').innerHTML=`<div class="res-row"><span>${esc(st.subjectName||'Тест')}</span><span style="font-weight:700;color:var(--p)">${score} / ${max}</span></div>
    ${!st.isMistakes?`<div class="res-row"><span>Алынған ұпай</span><span style="font-weight:700;color:var(--ok)">+${gained} ⭐</span></div>`:''}
    ${lock.viol?`<div class="res-row"><span>Ереже бұзу ескертулері</span><span style="font-weight:700;color:var(--err)">${lock.viol} / ${MAX_VIOL}</span></div>`:''}`;
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

// ================= Көп сұрақты бірден қосу / файлға сақтау / файлдан тапсыру =================
const MAX_Q=500;
const SAMPLE_TXT=`Тақырып: Қазақ хандығы
Пән: Қазақстан тарихы

1. Қазақ хандығы қай жылы құрылды?
A) 1456
B) 1465
C) 1480
D) 1511
Жауап: B

2. «Жеті жарғы» кімдікі?
A) Қасым хан
B) Есім хан
*C) Тәуке хан
D) Абылай хан

3. Тәуелсіздік күні?
A) 16 желтоқсан
B) 25 қазан
C) 30 тамыз
D) 1 мамыр
Жауап: A
`;
const RU_ORDER='АБВГД',LAT_ORDER='ABCDE';
function normLetter(ch){ch=String(ch||'').toUpperCase();return({'А':'A','В':'B','С':'C','Е':'E'})[ch]||ch}
function letterIdx(ch,ru){
  ch=String(ch||'').toUpperCase();
  if(ru){const i=RU_ORDER.indexOf(ch);if(i>=0)return i}
  const j=LAT_ORDER.indexOf(normLetter(ch));
  if(j>=0)return j;
  return ch==='Д'?3:-1;
}
function shortT(x){x=String(x||'').trim();return x.length>40?x.slice(0,40)+'…':x}
function checkQ(q){
  if(!q.text||!String(q.text).trim())return 'сұрақ мәтіні жоқ';
  if(!Array.isArray(q.options)||q.options.length!==4)return 'нұсқа саны 4 болуы керек (табылды: '+(Array.isArray(q.options)?q.options.length:0)+')';
  if(q.options.some(o=>!String(o).trim()))return 'бос нұсқа бар';
  if(!(q.correct>=0&&q.correct<4))return 'дұрыс жауап көрсетілмеген (мыс: «Жауап: B» немесе *B)';
  return null;
}
function addParsed(res,q){
  const err=checkQ(q);
  if(err)res.errors.push({line:q.line||0,msg:'«'+shortT(q.text)+'» — '+err});
  else res.questions.push({text:String(q.text).trim(),options:q.options.map(o=>String(o).trim()),correct:q.correct});
}
function parseQuestions(text,fname){
  text=String(text||'').replace(/^\uFEFF/,'').replace(/\r\n?/g,'\n');
  const ext=((fname||'').split('.').pop()||'').toLowerCase();
  const t0=text.trim();
  if(ext==='json'||t0[0]==='['||t0[0]==='{'){
    const r=parseJSONQs(t0);
    if(r)return r;
    if(ext==='json')return{questions:[],errors:[{line:0,msg:'JSON форматы қате'}],meta:{},format:'json'};
  }
  const ne=text.split('\n').filter(l=>l.trim());
  const sepCount=(l,c)=>(l.split(c).length-1);
  const tableLike=ne.length&&[',',';'].some(c=>ne.slice(0,2).every(l=>sepCount(l,c)>=5)&&!/^\s*\d+\s*[.)]/.test(ne[0]));
  if(ext==='csv'||ext==='tsv'||(ne[0]&&sepCount(ne[0],'\t')>=5)||tableLike)return parseTableQs(text,ext);
  return parseTextQs(text);
}
function parseJSONQs(t){
  let data;try{data=JSON.parse(t)}catch(e){return null}
  const res={questions:[],errors:[],meta:{},format:'json'};
  const arr=Array.isArray(data)?data:(data&&Array.isArray(data.questions)?data.questions:null);
  if(!arr){res.errors.push({line:0,msg:'JSON ішінен сұрақтар тізімі табылмады'});return res}
  if(!Array.isArray(data)){res.meta.topic=data.topic||data.title||'';res.meta.subject=data.subject||''}
  arr.forEach((o,i)=>{
    o=o||{};
    const q={text:o.text||o.question||o.q||'',options:o.options||o.answers||o.variants||[],correct:-1,line:i+1};
    const c=o.correct!==undefined?o.correct:o.answer;
    if(typeof c==='number')q.correct=c;
    else if(typeof c==='string'){
      const m=/^[A-Da-dА-Да-д]$/.exec(c.trim());
      q.correct=m?letterIdx(c.trim()):q.options.findIndex(x=>String(x).trim().toLowerCase()===c.trim().toLowerCase());
    }
    addParsed(res,q);
  });
  return res;
}
function csvRows(text,d){
  const rows=[];let row=[],cell='',inq=false;
  for(let i=0;i<text.length;i++){
    const ch=text[i];
    if(inq){if(ch==='"'){if(text[i+1]==='"'){cell+='"';i++}else inq=false}else cell+=ch}
    else if(ch==='"'&&cell===''){inq=true}
    else if(ch===d){row.push(cell);cell=''}
    else if(ch==='\n'){row.push(cell);rows.push(row);row=[];cell=''}
    else cell+=ch;
  }
  row.push(cell);
  if(row.length>1||row[0].trim())rows.push(row);
  return rows;
}
function parseTableQs(text,ext){
  const res={questions:[],errors:[],meta:{},format:'table'};
  const first=(text.split('\n').find(l=>l.trim())||'');
  let d='\t';
  if(ext!=='tsv'&&!(first.includes('\t')&&ext!=='csv')){
    const c=(first.match(/,/g)||[]).length,sc=(first.match(/;/g)||[]).length;
    d=sc>c?';':',';
  }
  const rows=csvRows(text,d).filter(r=>r.some(c=>String(c).trim()));
  let off=0,start=0;
  const h0=rows.length?rows[0].map(c=>String(c).trim()):[];
  const hw=/^(сұрақ|вопрос|question)$/i;
  if(h0.length&&(hw.test(h0[0])||(/^(№|#|n|nr|id)$/i.test(h0[0])&&hw.test(h0[1]||'')))){
    start=1;
    if(!hw.test(h0[0]))off=1;
  }
  const ru=rows.slice(start).some(r=>/^[БбГг]$/.test(String(r[off+5]||'').trim()));
  for(let i=start;i<rows.length;i++){
    const r=rows[i].map(c=>String(c).trim());
    const q={text:r[off]||'',options:[r[off+1],r[off+2],r[off+3],r[off+4]].map(x=>x||''),correct:-1,line:i+1};
    const v=(r[off+5]||'').trim();
    if(/^[1-4]$/.test(v))q.correct=+v-1;
    else if(/^[A-Da-dА-Да-д]$/.test(v))q.correct=letterIdx(v,ru);
    else if(v)q.correct=q.options.findIndex(x=>x.toLowerCase()===v.toLowerCase());
    addParsed(res,q);
  }
  return res;
}
function parseTextQs(text){
  const res={questions:[],errors:[],meta:{},format:'text'};
  const lines=text.split('\n');
  const optRe=/^\s*([*+]?)\s*([AaBbCcDdEeАаБбВвГгДдЕеСс])\s*[).:]\s*(.*)$/;
  const ansRe=/^\s*(?:жауап(?:ы)?|дұрыс(?:\s+жауап)?|ответ|answer|ans|key)\s*[:=\-–]\s*(.+?)\s*$/i;
  const metaRe=/^\s*(тақырып|тема|topic|пән|предмет|subject)\s*[:=]\s*(.+?)\s*$/i;
  const numRe=/^\s*\d+\s*[.)]\s*(.*)$/;
  let cur=null,blank=false,started=false,orphan=false;
  function fin(){
    if(!cur)return;
    const q=cur;cur=null;
    if(q.correct<0&&q.marks.length===1)q.correct=q.marks[0];
    else if(q.correct<0&&q.marks.length>1){res.errors.push({line:q.line,msg:'«'+shortT(q.text)+'» — бірнеше дұрыс жауап белгіленген'});return}
    addParsed(res,q);
  }
  for(let i=0;i<lines.length;i++){
    const L=i+1,line=lines[i].trim();
    if(!line){if(cur)blank=true;continue}
    if(!started&&!cur){
      const mm=metaRe.exec(line);
      if(mm){const k=mm[1].toLowerCase();if(/тақырып|тема|topic/.test(k))res.meta.topic=mm[2];else res.meta.subject=mm[2];continue}
    }
    const am=ansRe.exec(line);
    if(am&&cur&&cur.options.length){
      const v=am[1].trim();
      let idx=-1;
      const m1=/^([A-Za-zА-Яа-я]|[1-9])\s*[).]?$/.exec(v);
      if(m1){
        if(/\d/.test(m1[1]))idx=+m1[1]-1;
        else{
          const want=normLetter(m1[1]);
          idx=cur.labels.findIndex(l=>normLetter(l)===want);
          if(idx<0)idx=letterIdx(m1[1],cur.labels.some(l=>/[БбГг]/.test(l)));
        }
      }
      else idx=cur.options.findIndex(x=>x.trim().toLowerCase()===v.toLowerCase());
      cur.correct=idx;
      fin();blank=false;continue;
    }
    const om=optRe.exec(line);
    if(om){
      if(!cur){if(!orphan){res.errors.push({line:L,msg:'нұсқа сұрақсыз тұр: «'+shortT(line)+'»'});orphan=true}continue}
      cur.options.push(om[3]);cur.labels.push(om[2]);
      if(om[1])cur.marks.push(cur.options.length-1);
      blank=false;continue;
    }
    const nm=numRe.exec(line);
    if(cur&&cur.options.length){
      if(nm||blank||cur.options.length>=4)fin();
      else{cur.options[cur.options.length-1]+=' '+line;continue}
    }else if(cur){
      if(nm||blank)fin();
      else{cur.text+=' '+line;blank=false;continue}
    }
    cur={text:nm?nm[1]:line,options:[],labels:[],marks:[],correct:-1,line:L};
    started=true;blank=false;orphan=false;
  }
  fin();
  return res;
}

const bulk={c:null,e:null,f:null};
const bulkName={c:'',e:'',f:''};
function bulkInfoHTML(r){
  if(!r)return '';
  let h='';
  if(r.questions.length)h+='<div style="background:#f0fdf4;border:1px solid #86efac;border-radius:10px;padding:10px 12px;font-size:13px;margin-bottom:8px">✅ <b>'+r.questions.length+'</b> сұрақ танылды'+(r.meta&&r.meta.topic?' · тақырып: <b>'+esc(r.meta.topic)+'</b>':'')+'</div>';
  if(r.errors.length){
    h+='<div style="background:#fef2f2;border:1px solid #fca5a5;border-radius:10px;padding:10px 12px;font-size:12px;margin-bottom:8px">⚠ <b>'+r.errors.length+'</b> сұрақта қате бар (олар қосылмайды):<ul style="margin:6px 0 0 18px">'
      +r.errors.slice(0,8).map(e=>'<li>'+(e.line?e.line+'-жол: ':'')+esc(e.msg)+'</li>').join('')+'</ul>'+(r.errors.length>8?'<div>… және тағы '+(r.errors.length-8)+'</div>':'')+'</div>';
  }
  if(!r.questions.length&&!r.errors.length)h='<div class="sub">Сұрақ табылмады. Үлгі форматты қараңыз.</div>';
  return h;
}
function bulkRefresh(ctx,fname){
  const txt=document.getElementById(ctx+'-bulk-text').value;
  bulk[ctx]=txt.trim()?parseQuestions(txt,fname||''):null;
  document.getElementById(ctx+'-bulk-info').innerHTML=bulkInfoHTML(bulk[ctx]);
  if(ctx==='c'&&bulk.c)autoFillCreate();
}
function autoFillCreate(){
  const r=bulk.c,tp=document.getElementById('c-topic'),sel=document.getElementById('c-subject');
  const nm=(bulkName.c||'').replace(/\.[^.]+$/,'');
  if(tp&&!tp.value.trim()){const v=(r.meta&&r.meta.topic)||nm;if(v)tp.value=v}
  const so=matchSubject(r.meta&&r.meta.subject);if(so&&sel&&!sel.value)sel.value=so.value;
}
function bulkFromFile(ctx,inp){
  const f=inp.files&&inp.files[0];if(!f)return;
  if(f.size>2*1024*1024){alert('Файл тым үлкен (2 МБ-тан аспауы керек)');inp.value='';return}
  const rd=new FileReader();
  rd.onload=()=>{
    const txt=String(rd.result);
    if(txt.indexOf('\uFFFD')>=0)alert('Файл UTF-8 кодтауында емес болуы мүмкін. Excel-де «CSV UTF-8» ретінде сақтаңыз.');
    document.getElementById(ctx+'-bulk-text').value=txt;
    bulkName[ctx]=f.name;
    bulkRefresh(ctx,f.name);
  };
  rd.onerror=()=>alert('Файлды оқу мүмкін болмады');
  rd.readAsText(f,'utf-8');
}
function clearBulk(ctx){
  bulk[ctx]=null;bulkName[ctx]='';
  const t=document.getElementById(ctx+'-bulk-text');if(t)t.value='';
  const fi=document.getElementById(ctx+'-bulk-file');if(fi)fi.value='';
  const inf=document.getElementById(ctx+'-bulk-info');if(inf)inf.innerHTML='';
}
function bulkBlock(ctx){
  const btns={
    c:'',
    e:'',
    f:'<button class="btn btn-p" onclick="startFromFile()">▶ Тестті бастау</button><button class="btn btn-ok" onclick="saveFromFile()">💾 Менің тесттеріме сақтау</button>'
  }[ctx];
  return `<div class="card">
    <h3 style="margin-bottom:6px">📥 ${ctx==='c'?'Сұрақтар файлы (барлық сұрақ бір файлда)':ctx==='f'?'Сұрақтар файлы':'Файлдан сұрақ қосу'}</h3>
    <p class="sub" style="margin-bottom:10px">Файл таңдаңыз (.txt, .csv) немесе мәтінді / Excel-ден көшірілген кестені қойыңыз. Бір реттен 500 сұраққа дейін.</p>
    <details style="margin-bottom:12px"><summary style="cursor:pointer;font-size:13px;font-weight:600;color:var(--p)">Формат үлгісі</summary>
      <pre style="font-size:12px;background:var(--bg);border-radius:10px;padding:10px;margin:8px 0;white-space:pre-wrap">1. Сұрақ мәтіні
A) нұсқа
B) нұсқа
C) нұсқа
D) нұсқа
Жауап: B

(Жауапты *C) деп белгілеуге де болады.
Excel/CSV: 6 баған — сұрақ, A, B, C, D, дұрыс жауап (A–D))</pre>
      <button class="btn btn-s btn-sm" onclick="downloadSample()">⬇ Үлгі файл</button>
    </details>
    <div class="fg"><label>Файлдан жүктеу</label><input type="file" id="${ctx}-bulk-file" accept=".txt,.csv,.tsv,.json,text/plain,text/csv" onchange="bulkFromFile('${ctx}',this)"></div>
    <div class="fg"><label>немесе мәтінді осында қойыңыз</label><textarea id="${ctx}-bulk-text" style="min-height:160px;font-family:monospace;font-size:13px" placeholder="1. Сұрақ...&#10;A) ...&#10;B) ...&#10;C) ...&#10;D) ...&#10;Жауап: B" oninput="bulkRefresh('${ctx}','')"></textarea></div>
    <div id="${ctx}-bulk-info"></div>
    <div class="row" style="justify-content:flex-start">${btns}</div>
  </div>`;
}
function takeBulkQs(ctx){
  const r=bulk[ctx];
  if(!r||!r.questions.length){alert('Алдымен сұрақтарды қойыңыз немесе файл таңдаңыз');return null}
  if(r.errors.length&&!confirm(r.errors.length+' сұрақта қате бар, олар қосылмайды. Жалғастыру керек пе?'))return null;
  const base='q_'+Date.now().toString(36);
  return{qs:r.questions.map((q,i)=>({id:base+'_'+i,text:q.text,options:q.options.slice(),correct:q.correct,points:1})),meta:r.meta||{}};
}
function matchSubject(sub){
  const el=document.getElementById('c-subject');
  if(!sub||!el)return null;
  const x=String(sub).trim().toLowerCase();
  return Array.from(el.options||[]).find(o=>o.value&&(o.value===x||String(o.text).toLowerCase()===x))||null;
}
function showFileTest(){clearBulk('f');showScr('s-file')}
function startFromFile(){
  const r=takeBulkQs('f');if(!r)return;
  const label=r.meta.topic||(bulkName.f||'').replace(/\.[^.]+$/,'')||'Файлдан тест';
  st=baseState();
  st.questions=r.qs.map(q=>({...q,subjectName:label}));
  st.subjectName=label;
  st.timerSeconds=Math.max(r.qs.length*90,600);
  beginTest();
}
function saveFromFile(){
  const r=takeBulkQs('f');if(!r)return;
  let topic=prompt('Тест тақырыбы:',r.meta.topic||(bulkName.f||'').replace(/\.[^.]+$/,'')||'');
  if(topic===null)return;
  topic=topic.trim();
  if(!topic){alert('Тақырыпты жазыңыз');return}
  const so=matchSubject(r.meta.subject);
  const test={id:'t_'+Date.now(),subject:so?so.value:'other',subjectName:so?so.text:(r.meta.subject||'Басқа'),topic,desc:'',isPublic:false,status:'private',authorId:user.id,authorName:user.name,questions:r.qs,createdAt:new Date().toISOString()};
  const all=allTests();all.unshift(test);saveAllTests(all);
  clearBulk('f');alert('✅ Тест сақталды: '+r.qs.length+' сұрақ');showMyTests();
}
function testToText(topic,subjectName,qs){
  let o='Тақырып: '+topic+'\n'+(subjectName?'Пән: '+subjectName+'\n':'')+'\n';
  qs.forEach((q,i)=>{
    o+=(i+1)+'. '+String(q.text).replace(/\s*\n\s*/g,' ')+'\n';
    q.options.forEach((x,j)=>{o+='ABCD'[j]+') '+String(x).replace(/\s*\n\s*/g,' ')+'\n'});
    o+='Жауап: '+'ABCD'[q.correct]+'\n\n';
  });
  return o;
}
function safeName(x){return String(x||'test').replace(/[\\/:*?"<>|]+/g,'_').trim().slice(0,60)||'test'}
function downloadText(name,text){
  try{
    const blob=new Blob(['\uFEFF'+text],{type:'text/plain;charset=utf-8'});
    const a=document.createElement('a');
    a.href=URL.createObjectURL(blob);a.download=name;
    document.body.appendChild(a);a.click();
    setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove()},1000);
  }catch(e){alert('Файлды жүктеу мүмкін болмады')}
}
function exportTest(id){
  const t=allTests().find(x=>x.id===id);
  if(!t||!t.questions.length){alert('Сұрақ жоқ');return}
  downloadText(safeName(t.topic)+'.txt',testToText(t.topic,t.subjectName,t.questions));
}
function downloadSample(){downloadText('ulgi_suraqtar.txt',SAMPLE_TXT)}
let draftQs=[];
function manualBlock(ctx){
  const L=['A','B','C','D'];
  return `<div class="card">
    <h3 style="margin-bottom:10px">✍️ Жаңа сұрақ</h3>
    <div class="fg"><label>Сұрақ мәтіні</label><textarea id="${ctx}-mq-text" placeholder="Сұрақты жазыңыз (формула үшін: $x^2+1$)"></textarea></div>
    <div class="fg"><label>Жауап нұсқалары <span class="sub">(дұрыс жауаптың жанындағы дөңгелекті басыңыз)</span></label>
      ${L.map((l,i)=>`<div style="display:flex;align-items:center;gap:10px;margin-bottom:8px"><input type="radio" name="${ctx}-mq-ok" value="${i}" style="width:20px;height:20px;flex:none;accent-color:var(--p)"><b style="width:18px;flex:none">${l}</b><input id="${ctx}-mq-o${i}" placeholder="${l} нұсқасы" style="flex:1"></div>`).join('')}
    </div>
    <div class="row" style="justify-content:flex-start"><button class="btn btn-ok" onclick="addManualQ('${ctx}')">➕ Сұрақ қосу</button></div>
    <div id="${ctx}-mq-list" style="margin-top:14px"></div>
  </div>`;
}
function resetManualForm(ctx){
  const t=document.getElementById(ctx+'-mq-text');if(t)t.value='';
  for(let i=0;i<4;i++){const o=document.getElementById(ctx+'-mq-o'+i);if(o)o.value=''}
  document.querySelectorAll('input[name="'+ctx+'-mq-ok"]').forEach(r=>r.checked=false);
}
function clearManual(ctx){
  if(ctx==='c'){draftQs=[];renderDraft()}
  resetManualForm(ctx);
}
function renderDraft(){
  const el=document.getElementById('c-mq-list');if(!el)return;
  if(!draftQs.length){el.innerHTML='';return}
  el.innerHTML='<div class="sub" style="margin-bottom:8px">Қосылған сұрақтар: <b>'+draftQs.length+'</b></div><div class="list">'
    +draftQs.map((q,i)=>`<div class="item"><div class="info"><h4>${i+1}. ${esc(q.text)}</h4><p>✓ ${esc(q.options[q.correct])}</p></div><div class="acts"><button class="btn btn-d btn-sm" onclick="removeDraftQ(${i})">✕</button></div></div>`).join('')+'</div>';
}
function removeDraftQ(i){draftQs.splice(i,1);renderDraft()}
function addManualQ(ctx){
  const text=document.getElementById(ctx+'-mq-text').value.trim();
  if(!text){alert('Сұрақ мәтінін жазыңыз');return}
  const sel=document.querySelector('input[name="'+ctx+'-mq-ok"]:checked');
  const selIdx=sel?+sel.value:-1;
  const opts=[];let correct=-1;
  for(let i=0;i<4;i++){
    const v=document.getElementById(ctx+'-mq-o'+i).value.trim();
    if(v){if(i===selIdx)correct=opts.length;opts.push(v)}
  }
  if(opts.length<2){alert('Кемінде 2 жауап нұсқасын жазыңыз');return}
  if(selIdx<0){alert('Дұрыс жауапты белгілеңіз');return}
  if(correct<0){alert('Дұрыс жауап ретінде бос нұсқа белгіленген');return}
  const q={id:'q_'+Date.now().toString(36)+'_'+Math.random().toString(36).slice(2,6),text,options:opts,correct,points:1};
  if(ctx==='c'){
    if(draftQs.length>=MAX_Q){alert('Бір тестте '+MAX_Q+' сұрақтан аспауы керек');return}
    draftQs.push(q);renderDraft();
  }else{
    const all=allTests();const t=all.find(x=>x.id===editingId);if(!t)return;
    if(t.questions.length>=MAX_Q){alert('Бір тестте '+MAX_Q+' сұрақтан аспауы керек');return}
    t.questions.push(q);saveAllTests(all);renderEditList(t);
  }
  resetManualForm(ctx);
  document.getElementById(ctx+'-mq-text').focus();
}
['c','e'].forEach(c=>{const h=document.getElementById(c+'-manual-host');if(h)h.innerHTML=manualBlock(c)});
['f'].forEach(c=>{const h=document.getElementById(c+'-bulk-host');if(h)h.innerHTML=bulkBlock(c)});

document.addEventListener('click',e=>{const side=document.getElementById('sidebar');if(side&&side.classList.contains('open')&&!side.contains(e.target)&&!e.target.classList.contains('side-tog'))side.classList.remove('open')});

// ================= Тест кезіндегі толық экран құлпы =================
const MAX_VIOL=3;
const lock={on:false,paused:false,viol:0,last:0,fsOk:false,oldStyle:null,pdoc:null,oldOv:''};
function guardPause(fn){lock.paused=true;try{return fn()}finally{setTimeout(()=>{lock.paused=false},900)}}
function inFs(){return !!(document.fullscreenElement||document.webkitFullscreenElement)}
function lockFs(){
  try{
    const el=document.documentElement;
    const f=el.requestFullscreen||el.webkitRequestFullscreen;
    if(f){const p=f.call(el);if(p&&p.catch)p.catch(()=>{})}
  }catch(e){}
}
function lockExpand(){
  try{
    const fe=window.frameElement;if(!fe)return;
    if(lock.oldStyle===null)lock.oldStyle=fe.getAttribute('style')||'';
    fe.style.cssText=(lock.oldStyle?lock.oldStyle+';':'')+'position:fixed!important;top:0;left:0;width:100vw!important;height:100vh!important;z-index:2147483647;border:0;background:#fff';
    lock.pdoc=fe.ownerDocument;lock.oldOv=lock.pdoc.body.style.overflow;lock.pdoc.body.style.overflow='hidden';
  }catch(e){}
}
function lockRestore(){
  try{
    const fe=window.frameElement;
    if(fe&&lock.oldStyle!==null){if(lock.oldStyle)fe.setAttribute('style',lock.oldStyle);else fe.removeAttribute('style')}
    if(lock.pdoc)lock.pdoc.body.style.overflow=lock.oldOv||'';
  }catch(e){}
  lock.oldStyle=null;lock.pdoc=null;
}
function showOv(title,msg){document.getElementById('lock-title').textContent=title;document.getElementById('lock-msg').textContent=msg;document.getElementById('lock-ov').classList.add('show')}
function hideOv(){document.getElementById('lock-ov').classList.remove('show')}
function updViol(){
  const el=document.getElementById('viol');if(!el)return;
  if(lock.on&&lock.viol>0){el.style.display='block';el.textContent='⚠ Ескерту '+lock.viol+' / '+MAX_VIOL}else el.style.display='none';
}
function lockStart(){
  lock.on=true;lock.viol=0;lock.last=0;lock.fsOk=false;
  document.body.classList.add('locked');
  lockExpand();lockFs();hideOv();updViol();
  try{history.pushState({lock:1},'',location.href)}catch(e){}
  setTimeout(()=>{if(lock.on)lock.fsOk=inFs()},900);
}
function lockEnd(){
  lock.on=false;document.body.classList.remove('locked');hideOv();updViol();
  try{if(inFs())(document.exitFullscreen||document.webkitExitFullscreen).call(document)}catch(e){}
  lockRestore();
}
function lockReassert(){if(lock.on&&lock.fsOk&&!inFs())lockFs()}
function returnToTest(){
  lockFs();hideOv();
  setTimeout(()=>{if(lock.on&&lock.fsOk&&!inFs())showOv('Толық экранға оралыңыз','Төмендегі батырманы қайта басыңыз.')},600);
}
function lockViolation(){
  if(!lock.on||lock.paused)return;
  const now=Date.now();if(now-lock.last<1200)return;lock.last=now;
  lock.viol++;updViol();
  if(lock.viol>=MAX_VIOL){
    hideOv();
    guardPause(()=>alert('Тесттен '+MAX_VIOL+' рет шықтыңыз. Тест автоматты түрде аяқталды.'));
    finishTest(true);return;
  }
  showOv('⚠ Тестке қайтыңыз','Тест кезінде толық экраннан немесе беттен шығуға болмайды. Ескерту: '+lock.viol+' / '+MAX_VIOL+'. Тағы '+(MAX_VIOL-lock.viol)+' рет шықсаңыз, тест автоматты түрде аяқталады.');
}
function onFsChange(){
  if(!lock.on)return;
  if(inFs()){lock.fsOk=true;hideOv();return}
  if(lock.fsOk)lockViolation();
}
document.addEventListener('fullscreenchange',onFsChange);
document.addEventListener('webkitfullscreenchange',onFsChange);
document.addEventListener('visibilitychange',()=>{if(lock.on&&document.hidden)lockViolation()});
window.addEventListener('blur',()=>{if(lock.on&&!lock.paused)setTimeout(()=>{if(lock.on&&!lock.paused&&!document.hasFocus())lockViolation()},250)});
const blockEv=e=>{if(lock.on){e.preventDefault();return false}};
['contextmenu','copy','cut','paste','dragstart','selectstart'].forEach(n=>document.addEventListener(n,blockEv));
document.addEventListener('keydown',e=>{
  if(!lock.on)return;
  const k=String(e.key||''),c=e.ctrlKey||e.metaKey;
  const bad=/^F(1|3|5|6|7|10|11|12)$/.test(k)||k==='ContextMenu'||k==='PrintScreen'||(c&&/^[a-z]$/i.test(k))||(c&&e.shiftKey)||(e.altKey&&/^Arrow(Left|Right)$/.test(k));
  if(bad){e.preventDefault();e.stopPropagation();return false}
},true);
function onBeforeUnload(e){if(lock.on){e.preventDefault();e.returnValue='Тест жүріп жатыр!';return e.returnValue}}
window.addEventListener('beforeunload',onBeforeUnload);
try{window.parent.addEventListener('beforeunload',onBeforeUnload)}catch(e){}
window.addEventListener('popstate',()=>{if(lock.on){try{history.pushState({lock:1},'',location.href)}catch(e){}}});

// ================= Әр пайдаланушының жеке графигі =================
function getProg(id){
  let pg=LS.get('ubt_prog_'+id,[]);
  if(!pg.length)pg=LS.get('ubt_hist_'+id,[]).slice().reverse().map(h=>({t:0,score:h.score,max:h.max,topic:h.topic,viol:h.viol||0}));
  return pg;
}
function pctOf(p){return p.max?Math.round(p.score/p.max*100):0}
function renderProgress(chartId,topicId,prog){
  const el=document.getElementById(chartId);if(!el)return;
  const tel=topicId?document.getElementById(topicId):null;
  if(!prog.length){
    el.innerHTML='<div class="empty"><div class="ic">📈</div><p>Әзірге график жоқ.<br>Тест тапсырсаңыз, нәтижеңіз осында көрінеді.</p></div>';
    if(tel)tel.innerHTML='';return;
  }
  const all=prog.map(pctOf),n=all.length;
  const pts=all.slice(-30),off=n-pts.length;
  const avg=Math.round(all.reduce((a,b)=>a+b,0)/n),best=Math.max(...all),last=all[n-1];
  const diff=n>1?last-all[n-2]:0;
  const arrow=n>1?(diff>0?' ▲ +'+diff:diff<0?' ▼ '+diff:' ＝'):'';
  const W=640,H=260,l=42,r=16,t=16,b=30,iw=W-l-r,ih=H-t-b;
  const X=i=>pts.length===1?l+iw/2:l+iw*i/(pts.length-1);
  const Y=v=>t+ih*(100-v)/100;
  let g='';
  [0,25,50,75,100].forEach(v=>{g+=`<line x1="${l}" x2="${W-r}" y1="${Y(v)}" y2="${Y(v)}" stroke="#e2e8f0"/><text x="${l-6}" y="${Y(v)+4}" font-size="11" text-anchor="end" fill="#64748b">${v}%</text>`});
  const line=pts.map((v,i)=>X(i).toFixed(1)+','+Y(v).toFixed(1)).join(' ');
  const area=X(0).toFixed(1)+','+Y(0)+' '+line+' '+X(pts.length-1).toFixed(1)+','+Y(0);
  const dots=pts.map((v,i)=>{
    const c=v>=80?'#16a34a':v>=50?'#2563eb':'#dc2626',p=prog[off+i];
    return `<circle cx="${X(i).toFixed(1)}" cy="${Y(v).toFixed(1)}" r="5" fill="${c}" stroke="#fff" stroke-width="2"><title>${esc((p.topic||'Тест')+': '+p.score+'/'+p.max+' ('+v+'%)')}</title></circle>`;
  }).join('');
  const labs=pts.map((_,i)=>(i===0||i===pts.length-1||(i+1)%5===0)?`<text x="${X(i).toFixed(1)}" y="${H-8}" font-size="11" text-anchor="middle" fill="#64748b">${off+i+1}</text>`:'').join('');
  el.innerHTML=`<div class="stat-grid">
      <div class="stat"><b>${n}</b><span>Тапсырылған тест</span></div>
      <div class="stat"><b>${avg}%</b><span>Орташа нәтиже</span></div>
      <div class="stat"><b>${best}%</b><span>Үздік нәтиже</span></div>
      <div class="stat"><b>${last}%${arrow}</b><span>Соңғы тест</span></div>
    </div>
    <div class="chart-wrap"><svg viewBox="0 0 ${W} ${H}" style="width:100%;min-width:420px;height:auto">${g}<polygon points="${area}" fill="rgba(37,99,235,.10)"/><polyline points="${line}" fill="none" stroke="#2563eb" stroke-width="2.5" stroke-linejoin="round"/>${dots}${labs}</svg></div>
    <p class="sub" style="text-align:center">Көлденең — тест нөмірі · Тік — нәтиже (%) · 🟢 80%+ · 🔵 50%+ · 🔴 50%-тен төмен</p>`;
  if(tel){
    const m={};
    prog.forEach(p=>{const k=p.topic||'Тест';(m[k]=m[k]||{s:0,c:0});m[k].s+=pctOf(p);m[k].c++});
    const rows=Object.entries(m).map(([k,v])=>({k,avg:Math.round(v.s/v.c),c:v.c})).sort((a,b)=>b.c-a.c).slice(0,8);
    tel.innerHTML=rows.map(x=>`<div class="tbar"><span class="tn" title="${esc(x.k)}">${esc(x.k)} (${x.c})</span><span class="tb"><i style="width:${x.avg}%"></i></span><span class="tv">${x.avg}%</span></div>`).join('');
  }
}

// ================= Дайын тест: «Функция» (50 сұрақ) =================
const SEED_FUNKSIYA=`Тақырып: Функция
Пән: Математика

1. f(x) = 2x + 3 болса, f(4) неге тең?
A) 8
B) 14
C) 11
D) 10
Жауап: C

2. f(x) = x² − 4x + 3 болса, f(2) неге тең?
A) 0
B) 1
C) 3
D) −1
Жауап: D

3. f(x) = 3x − 5 болса, f(−2) неге тең?
A) −1
B) −11
C) 1
D) 11
Жауап: B

4. y = kx + b түріндегі сызықтық функцияның графигі қандай сызық?
A) Түзу
B) Парабола
C) Гипербола
D) Синусоида
Жауап: A

5. y = x² функциясының графигі төмендегі нүктелердің қайсысы арқылы өтеді?
A) (1; 1)
B) (2; 2)
C) (2; 3)
D) (3; 6)
Жауап: A

6. y = 1/x функциясының анықталу облысы қандай?
A) x > 0
B) x ≥ 0
C) x < 0
D) x ≠ 0
Жауап: D

7. y = √x функциясының анықталу облысы қандай?
A) x > 0
B) x ≤ 0
C) x ≥ 0
D) x ≠ 0
Жауап: C

8. y = √(x − 3) функциясының анықталу облысы қандай?
A) x ≤ 3
B) x ≥ 3
C) x > 3
D) x ≥ −3
Жауап: B

9. y = 1/(x − 5) функциясының анықталу облысы қандай?
A) x ≠ 5
B) x ≠ −5
C) x > 5
D) x ≠ 0
Жауап: A

10. y = x² функциясының мәндер жиыны қандай?
A) y ≤ 0
B) y ≥ 0
C) y > 0
D) y — кез келген сан
Жауап: B

11. y = x² + 2 функциясының мәндер жиыны қандай?
A) y ≥ 0
B) y ≤ 2
C) y ≥ 2
D) y ≥ −2
Жауап: C

12. y = −x² функциясының мәндер жиыны қандай?
A) y ≥ 0
B) y < 0
C) y ≥ −1
D) y ≤ 0
Жауап: D

13. Төмендегі функциялардың қайсысы жұп функция?
A) y = x³
B) y = x + 1
C) y = 2x
D) y = x²
Жауап: D

14. Төмендегі функциялардың қайсысы тақ функция?
A) y = x²
B) y = |x|
C) y = x³
D) y = x² + 1
Жауап: C

15. y = x² − 6x + 5 параболасының төбесінің абсциссасы неге тең?
A) 3
B) −3
C) 5
D) 1
Жауап: A

16. y = x² − 6x + 5 функциясының нөлдері қандай?
A) −1 және −5
B) 1 және 5
C) 1 және −5
D) 2 және 3
Жауап: B

17. y = x² − 4 функциясының нөлдері қандай?
A) 4 және −4
B) 0 және 2
C) −2 және 2
D) 2
Жауап: C

18. y = 2x − 6 функциясының графигі Ox осін қай нүктеде қиып өтеді?
A) (0; 3)
B) (−3; 0)
C) (0; −6)
D) (3; 0)
Жауап: D

19. y = 2x − 6 функциясының графигі Oy осін қай нүктеде қиып өтеді?
A) (0; 6)
B) (0; −6)
C) (3; 0)
D) (−6; 0)
Жауап: B

20. y = x² + 4x + 3 функциясының графигі Oy осін қай нүктеде қиып өтеді?
A) (0; 3)
B) (3; 0)
C) (0; 4)
D) (0; −3)
Жауап: A

21. y = 2x + 1 және y = −x + 4 функцияларының графиктері қай нүктеде қиылысады?
A) (3; 1)
B) (1; 2)
C) (1; 3)
D) (2; 5)
Жауап: C

22. y = 3x − 2 функциясының бұрыштық коэффициенті неге тең?
A) −2
B) 3
C) 2
D) −3
Жауап: B

23. y = −2x + 5 функциясы қалай өзгереді?
A) Кемиді
B) Өседі
C) Тұрақты
D) Алдымен өседі, кейін кемиді
Жауап: A

24. y = x² функциясы [0; +∞) аралығында қалай өзгереді?
A) Кемиді
B) Тұрақты
C) Анықталмаған
D) Өседі
Жауап: D

25. g(x) = x + 2 және f(x) = x² болса, f(g(1)) неге тең?
A) 3
B) 5
C) 1
D) 9
Жауап: D

26. f(x) = 2x және g(x) = x − 1 болса, g(f(3)) неге тең?
A) 6
B) 5
C) 4
D) 2
Жауап: B

27. f(x) = 2x + 4 функциясының кері функциясы қайсы?
A) f⁻¹(x) = (x − 4)/2
B) f⁻¹(x) = 2x − 4
C) f⁻¹(x) = (x + 4)/2
D) f⁻¹(x) = x/2 + 4
Жауап: A

28. Функция дегеніміз не?
A) Әр x мәніне екі y мәні сәйкес келетін сәйкестік
B) Тек сызықтық теңдеу
C) Әр x мәніне бір ғана y мәні сәйкес келетін сәйкестік
D) Тек график
Жауап: C

29. y = 2ˣ функциясы үшін x = 3 болғанда y неге тең?
A) 8
B) 6
C) 9
D) 5
Жауап: A

30. y = 2ˣ функциясы қалай өзгереді?
A) Кемиді
B) Тұрақты
C) Тек теріс мәндер қабылдайды
D) Өседі
Жауап: D

31. y = (1/2)ˣ функциясы қалай өзгереді?
A) Өседі
B) Кемиді
C) Тұрақты
D) Жұп функция
Жауап: B

32. y = log₂x функциясы үшін x = 8 болғанда y неге тең?
A) 2
B) 4
C) 3
D) 16
Жауап: C

33. y = log₃x функциясының анықталу облысы қандай?
A) x ≥ 0
B) x > 0
C) x ≠ 0
D) x < 0
Жауап: B

34. y = sin x функциясының мәндер жиыны қандай?
A) [−1; 1]
B) [0; 1]
C) (−∞; +∞)
D) [−2; 2]
Жауап: A

35. y = sin x функциясының негізгі периоды неге тең?
A) π
B) π/2
C) 2π
D) 4π
Жауап: C

36. y = tg x функциясының негізгі периоды неге тең?
A) 2π
B) π/2
C) 3π
D) π
Жауап: D

37. Төмендегі функциялардың қайсысы жұп функция?
A) y = sin x
B) y = tg x
C) y = x³
D) y = cos x
Жауап: D

38. y = x² + 3 графигі y = x² графигінен қалай алынады?
A) 3 бірлік төмен жылжыту арқылы
B) 3 бірлік жоғары жылжыту арқылы
C) 3 бірлік оңға жылжыту арқылы
D) 3 бірлік солға жылжыту арқылы
Жауап: B

39. y = (x − 2)² графигі y = x² графигінен қалай алынады?
A) 2 бірлік оңға жылжыту арқылы
B) 2 бірлік солға жылжыту арқылы
C) 2 бірлік жоғары жылжыту арқылы
D) 2 бірлік төмен жылжыту арқылы
Жауап: A

40. y = −x² графигі y = x² графигіне қатысты қалай орналасқан?
A) Oy осіне қатысты симметриялы
B) Координат басына қатысты симметриялы
C) Ox осіне қатысты симметриялы
D) 2 бірлік жоғары жылжыған
Жауап: C

41. y = ax² + bx + c функциясында a > 0 болса, парабола бұтақтары қайда бағытталған?
A) Төмен
B) Оңға
C) Солға
D) Жоғары
Жауап: D

42. y = x² − 2x + 1 функциясының ең кіші мәні неге тең?
A) 0
B) 1
C) −1
D) 2
Жауап: A

43. y = −x² + 4 функциясының ең үлкен мәні неге тең?
A) −4
B) 4
C) 0
D) 2
Жауап: B

44. f(x) = x³ болса, f(−2) неге тең?
A) 8
B) −6
C) −8
D) 6
Жауап: C

45. y = (x + 1)/(x − 2) функциясының анықталу облысы қандай?
A) x ≠ −1
B) x ≠ −2
C) x > 2
D) x ≠ 2
Жауап: D

46. y = √(4 − x) функциясының анықталу облысы қандай?
A) x ≥ 4
B) x ≤ 4
C) x < 4
D) x ≤ −4
Жауап: B

47. f(x) = 5 тұрақты функциясының графигі қандай?
A) Ox осіне параллель түзу
B) Oy осіне параллель түзу
C) Координат басы арқылы өтетін түзу
D) Парабола
Жауап: A

48. y = x² − 4x + 4 параболасының төбесінің ординатасы неге тең?
A) 2
B) 4
C) 0
D) −4
Жауап: C

49. f(x) = x² + px + 6 функциясы үшін f(2) = 0 болса, p неге тең?
A) −5
B) 5
C) −2
D) 2
Жауап: A

50. Графигі (0; 2) және (1; 5) нүктелері арқылы өтетін сызықтық функцияны табыңыз.
A) y = 2x + 3
B) y = 5x + 2
C) y = 3x − 2
D) y = 3x + 2
Жауап: D
`;
function seedBuiltin(){
  try{
    if(LS.get('ubt_seed_funksiya',false))return;
    const r=parseTextQs(SEED_FUNKSIYA);
    if(!r.questions.length)return;
    const all=allTests();
    if(!all.some(t=>t.id==='seed_funksiya')){
      all.push({id:'seed_funksiya',subject:'math',subjectName:'Математика',topic:'Функция',desc:'Дайын тест · '+r.questions.length+' сұрақ',isPublic:true,status:'approved',authorId:'system',authorName:'ҰБТ+',
        questions:r.questions.map((q,i)=>({id:'fn_'+i,text:q.text,options:q.options,correct:q.correct,points:1})),createdAt:new Date().toISOString()});
      saveAllTests(all);
    }
    LS.set('ubt_seed_funksiya',true);
  }catch(e){}
}
seedBuiltin();

// ================= Қосымша мүмкіндіктер: дерек =================
const QUOTES=[
"Бүгін оқыған әр бет — ертеңгі жеңістің бір қадамы.",
"Тамшыдан көл болады: күн сайын азын-аздап оқы.",
"Еңбек етсең — емерсің.",
"Қате — жеңіліс емес, келесі жауаптың сабағы.",
"Мақсаты бар адам жолдан адаспайды.",
"Білім — ешкім тартып ала алмайтын байлық.",
"Үлкен нәтиже кішкентай әдеттерден басталады.",
"Бүгінгі жалқаулық ертеңгі қиындыққа айналады.",
"Сен ойлағаннан да күштісің — тек жалғастыр.",
"Ең жақсы уақыт — дәл қазір.",
"Қиын сұрақ — өсу мүмкіндігі.",
"Тәртіп пен тұрақтылық таланттан артық жеңеді.",
"Бір тест — бір қадам. Тоқтама!",
"Жеңіс — күн сайын тырысқандардікі.",
"Жеті рет өлшеп, бір рет кес: қатеңді талдап, қайта жаттық."
];
const PLAN_SUBJECTS=['Қазақстан тарихы','Оқу сауаттылығы','Математикалық сауаттылық','Математика','Физика','Химия','Биология','География','Информатика','Ағылшын тілі','Қазақ тілі','Дүниежүзі тарихы','Құқық негіздері'];
const GLOSS=[].concat([
['Тарих','751 ж.','Талас шайқасы — араб-қытай шайқасы; түркі тайпалары (қарлұқтар) араб жағында шайқасқан.'],
['Тарих','1465 ж.','Қазақ хандығының құрылуы. Негізін Керей мен Жәнібек сұлтандар қалады.'],
['Тарих','1511–1523 жж.','Қасым хан билік құрған жылдар. «Қасқа жол» заңдары қабылданды деп есептеледі.'],
['Тарих','1643 ж.','Орбұлақ шайқасы. Жәңгір сұлтан шағын әскермен жоңғар әскерін жеңді.'],
['Тарих','1680–1718 жж.','Тәуке хан билік құрған кезең. «Жеті жарғы» заңдар жинағы осы кезде жасалды.'],
['Тарих','1729–1730 жж.','Аңырақай шайқасы — қазақ жасақтарының жоңғарларға қарсы шешуші жеңісі.'],
['Тарих','1783–1797 жж.','Сырым Датұлы бастаған ұлт-азаттық көтеріліс.'],
['Тарих','1836–1838 жж.','Исатай Тайманұлы мен Махамбет Өтемісұлы бастаған көтеріліс.'],
['Тарих','1837–1847 жж.','Кенесары Қасымұлы бастаған ұлт-азаттық көтеріліс.'],
['Тарих','1916 ж.','Орта Азия мен Қазақстандағы ұлт-азаттық көтеріліс. Торғайда Амангелді Иманов басқарды.'],
['Тарих','1917 ж. (желтоқсан)','Алашорда автономиялық үкіметі жарияланды. Басшысы — Әлихан Бөкейхан.'],
['Тарих','1920 ж.','Қырғыз (Қазақ) Автономиялы Кеңестік Социалистік Республикасының құрылуы.'],
['Тарих','1936 ж.','Қазақ КСР-і одақтас республика мәртебесін алды.'],
['Тарих','1986 ж. (желтоқсан)','Алматыдағы Желтоқсан көтерілісі.'],
['Тарих','1991 ж. 16 желтоқсан','Қазақстан Республикасының мемлекеттік тәуелсіздігі жарияланды.'],
['Тарих','1995 ж.','Қазақстанның қазіргі Конституциясы қабылданды (30 тамыз, республикалық референдум).'],
['Тарих','1997–1998 жж.','Астана Ақмолаға көшірілді (1997), ал 1998 жылы қала «Астана» деп аталды.'],
['Математика','Дискриминант','Квадрат теңдеудің $ax^2+bx+c=0$ дискриминанты: $D=b^2-4ac$. $D>0$ — екі түбір, $D=0$ — бір түбір, $D<0$ — нақты түбір жоқ.'],
['Математика','Квадрат теңдеу түбірлері','$x_{1,2}=\\dfrac{-b\\pm\\sqrt{D}}{2a}$'],
['Математика','Виет теоремасы','$x_1+x_2=-\\dfrac{b}{a}$, $x_1x_2=\\dfrac{c}{a}$ (келтірілген емес теңдеу үшін).'],
['Математика','Пифагор теоремасы','Тікбұрышты үшбұрышта: $a^2+b^2=c^2$, мұндағы $c$ — гипотенуза.'],
['Математика','Арифметикалық прогрессия','$a_n=a_1+(n-1)d$; алғашқы $n$ мүшенің қосындысы: $S_n=\\dfrac{a_1+a_n}{2}\\cdot n$.'],
['Математика','Геометриялық прогрессия','$b_n=b_1q^{\\,n-1}$; алғашқы $n$ мүшенің қосындысы: $S_n=\\dfrac{b_1(q^n-1)}{q-1}$.'],
['Математика','Дөңгелек','Ауданы $S=\\pi r^2$, шеңбер ұзындығы $C=2\\pi r$.'],
['Математика','Негізгі тригонометриялық теңдік','$\\sin^2\\alpha+\\cos^2\\alpha=1$'],
['Математика','Дәреже туындысы','$(x^n)\'=nx^{n-1}$'],
['Математика','Логарифмнің негізгі тепе-теңдігі','$a^{\\log_a b}=b$, мұндағы $a>0$, $a\\ne1$, $b>0$.'],
['Физика','Ньютонның екінші заңы','Дененің үдеуі әсер етуші күшке тура, массаға кері пропорционал: $F=ma$.'],
['Физика','Механикалық жұмыс','$A=Fs\\cos\\alpha$'],
['Физика','Қуат','$N=\\dfrac{A}{t}$ — уақыт бірлігінде орындалған жұмыс.'],
['Физика','Кинетикалық энергия','$E_k=\\dfrac{mv^2}{2}$'],
['Физика','Тығыздық','$\\rho=\\dfrac{m}{V}$'],
['Физика','Ом заңы (тізбек бөлігі үшін)','$I=\\dfrac{U}{R}$'],
['Физика','Жарық жылдамдығы (вакуумда)','$c\\approx3\\cdot10^8$ м/с'],
['Химия','Менделеевтің периодтық заңы','Элементтердің қасиеттері атом ядросының зарядына байланысты периодты түрде өзгереді. Кесте 1869 жылы жасалған.'],
['Химия','Зат мөлшері','$n=\\dfrac{m}{M}$, өлшем бірлігі — моль.'],
['Химия','Авогадро саны','$N_A\\approx6{,}02\\cdot10^{23}$ моль$^{-1}$'],
['Химия','pH','$pH=-\\lg[H^+]$. $pH<7$ — қышқылдық, $pH=7$ — бейтарап, $pH>7$ — сілтілік орта.'],
['Химия','Изотоптар','Протон саны бірдей, нейтрон саны әртүрлі (массалық саны әртүрлі) бір элемент атомдары.'],
['Биология','Митохондрия','Жасушаның «энергия станциясы»: АТФ синтезделетін органоид.'],
['Биология','ДНҚ','Дезоксирибонуклеин қышқылы — тұқым қуалайтын ақпаратты сақтайтын молекула.'],
['Биология','Фотосинтез','Жарық энергиясының әсерінен көмірқышқыл газы мен судан органикалық заттар түзілу процесі; хлоропластарда жүреді.'],
['Биология','Мейоз','Жыныс жасушалары (гаметалар) түзілетін бөліну; хромосома саны екі есе азаяды.'],
['География','Қазақстанның ауданы','Шамамен 2,7 млн км² — әлемде аумағы жағынан 9-орындағы ел.'],
['География','Хан Тәңірі шыңы','Қазақстандағы ең биік нүктелердің бірі — 7010 м (Тянь-Шань).'],
['Әдебиет','Метафора','Заттың белгісін басқасына ауыстырып, жасырын салыстыру («күн күлді»).'],
['Әдебиет','Теңеу','Бір затты екінші затқа ұқсатып салыстыру («қардай аппақ»).'],
['Әдебиет','Эпитет','Затты, құбылысты бейнелі сипаттайтын анықтауыш сөз («алтын күз»).'],
['Әдебиет','Гипербола','Қасиетті әсірелеп көрсету («көк тіреген шаңырақ»).'],
['Әдебиет','Абайдың «Қара сөздері»','Абай Құнанбайұлының прозалық шығармалар жинағы — 45 қара сөз.'],
['Әдебиет','«Абай жолы»','Мұхтар Әуезовтің Абай өмірі туралы роман-эпопеясы.']
]).map(a=>({c:a[0],t:a[1],d:a[2]}));

// ================= Қосымша мүмкіндіктер: логика =================
function dayKey(d){d=d||new Date();return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')}
function parseDay(k){const a=String(k).split('-').map(Number);return new Date(a[0],a[1]-1,a[2])}
function addDays(d,n){const x=new Date(d);x.setDate(x.getDate()+n);return x}
function daysBetween(a,b){return Math.round((parseDay(b)-parseDay(a))/86400000)}
function monthKey(d){d=d||new Date();return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')}
function weekKey(d){
  d=d?new Date(d):new Date();
  const t=new Date(Date.UTC(d.getFullYear(),d.getMonth(),d.getDate()));
  const dn=t.getUTCDay()||7;t.setUTCDate(t.getUTCDate()+4-dn);
  const y0=new Date(Date.UTC(t.getUTCFullYear(),0,1));
  return t.getUTCFullYear()+'-W'+String(Math.ceil(((t-y0)/86400000+1)/7)).padStart(2,'0');
}
function hash(s){s=String(s);let h=0;for(let i=0;i<s.length;i++){h=(h*31+s.charCodeAt(i))|0}return Math.abs(h)}
const MONTHS=['Қаңтар','Ақпан','Наурыз','Сәуір','Мамыр','Маусым','Шілде','Тамыз','Қыркүйек','Қазан','Қараша','Желтоқсан'];
const WDAYS=['Жс','Дс','Сс','Ср','Бс','Жм','Сб'];
function seasonLabel(tag){
  const t=tag.slice(0,1),k=tag.slice(2);
  if(t==='m'){const p=k.split('-');return p[0]+' · '+MONTHS[(+p[1])-1]}
  const p=k.split('-W');return p[0]+' · '+(+p[1])+'-апта';
}

// ---------- Қараңғы режим ----------
function applyTheme(){
  const on=!!LS.get('ubt_dark',false);
  document.body.classList.toggle('dark',on);
  const b=document.getElementById('theme-btn');if(b)b.textContent=on?'☀️':'🌙';
}
function toggleTheme(){LS.set('ubt_dark',!LS.get('ubt_dark',false));applyTheme()}

// ---------- LaTeX (KaTeX) ----------
const MATH_DELIMS=[{left:'$$',right:'$$',display:true},{left:'\\[',right:'\\]',display:true},{left:'\\(',right:'\\)',display:false},{left:'$',right:'$',display:false}];
function mathIn(el){try{if(el&&window.renderMathInElement)window.renderMathInElement(el,{delimiters:MATH_DELIMS,throwOnError:false})}catch(e){}}
function mathScreen(){mathIn(document.querySelector('.screen.active'))}

// ---------- Отшашу ----------
function confetti(n){
  const c=document.getElementById('confetti');if(!c)return;
  c.width=window.innerWidth;c.height=window.innerHeight;
  const x=c.getContext('2d');
  const cols=['#ef4444','#f59e0b','#22c55e','#3b82f6','#a855f7','#ec4899'];
  const P=Array.from({length:n||150},()=>({x:Math.random()*c.width,y:-20-Math.random()*c.height*.5,w:6+Math.random()*6,h:8+Math.random()*8,vy:2+Math.random()*4,vx:-2+Math.random()*4,r:Math.random()*6,vr:-.2+Math.random()*.4,c:cols[Math.floor(Math.random()*cols.length)]}));
  let f=0;
  (function loop(){
    x.clearRect(0,0,c.width,c.height);
    P.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.r+=p.vr;x.save();x.translate(p.x,p.y);x.rotate(p.r);x.fillStyle=p.c;x.fillRect(-p.w/2,-p.h/2,p.w,p.h);x.restore()});
    if(++f<230)requestAnimationFrame(loop);else x.clearRect(0,0,c.width,c.height);
  })();
}

// ---------- Цитаталар ----------
let homeQuote=null;
function randQuote(){return QUOTES[Math.floor(Math.random()*QUOTES.length)]}
function newQuote(){homeQuote=randQuote();renderHomeExtras()}
function quoteCard(){if(!homeQuote)homeQuote=randQuote();return `<div class="quote" onclick="newQuote()" title="Басып жаңасын көріңіз">💬 ${esc(homeQuote)}</div>`}

// ---------- Streak ----------
function getStreak(){return LS.get('ubt_streak_'+user.id,{last:'',count:0,best:0})}
function currentStreak(){const s=getStreak();return(s.last&&daysBetween(s.last,dayKey())<=1)?s.count:0}
function touchStreak(){
  const s=getStreak(),today=dayKey();
  if(s.last===today)return{count:s.count,bonus:0,isNew:false};
  const gap=s.last?daysBetween(s.last,today):99;
  s.count=(gap===1)?s.count+1:1;s.last=today;s.best=Math.max(s.best||0,s.count);
  LS.set('ubt_streak_'+user.id,s);
  let bonus=Math.min(s.count,7)*5;
  if(s.count%7===0)bonus+=50;
  return{count:s.count,bonus,isNew:true};
}

// ---------- Маусымдық рейтинг ----------
function recordSeason(p){
  if(!user||user.isAdmin||!p)return;
  const idx=LS.get('ubt_season_idx',[]);let ch=false;
  [['w',weekKey()],['m',monthKey()]].forEach(a=>{
    const tag=a[0]+'_'+a[1],key='ubt_season_'+tag,d=LS.get(key,{});
    d[user.id]=(d[user.id]||0)+p;LS.set(key,d);
    if(!idx.includes(tag)){idx.push(tag);ch=true}
  });
  if(ch)LS.set('ubt_season_idx',idx);
}
function seasonBoard(tag){
  const d=LS.get('ubt_season_'+tag,{}),profiles=Object.values(LS.get('ubt_profiles',{}));
  return Object.keys(d).filter(id=>d[id]>0).map(id=>{const pr=profiles.find(x=>x.id===id);return{id,name:pr?pr.name:'?',points:d[id]}}).sort((a,b)=>b.points-a.points);
}
function checkRollover(){
  const idx=LS.get('ubt_season_idx',[]),done=LS.get('ubt_awarded',[]);
  const cw='w_'+weekKey(),cm='m_'+monthKey();
  const tr=LS.get('ubt_trophies',[]);let ch=false;
  idx.forEach(tag=>{
    if(tag===cw||tag===cm||done.includes(tag))return;
    seasonBoard(tag).slice(0,3).forEach((u,i)=>tr.push({tag,rank:i+1,id:u.id,name:u.name,points:u.points}));
    done.push(tag);ch=true;
  });
  if(ch){LS.set('ubt_trophies',tr);LS.set('ubt_awarded',done)}
}
let rankMode='all';
function showRanking(mode){
  if(mode)rankMode=mode;
  checkRollover();
  const tabs=[['all','Жалпы'],['w','Апта'],['m','Ай']];
  document.getElementById('rank-tabs').innerHTML=tabs.map(t=>`<button class="btn ${rankMode===t[0]?'btn-p':'btn-s'} btn-sm" onclick="showRanking('${t[0]}')">${t[1]}</button>`).join('');
  let board;
  if(rankMode==='all'){board=getLeaderboard();document.getElementById('rank-sub').textContent='Ең көп ұпай жинағандар'}
  else{
    const tag=rankMode+'_'+(rankMode==='w'?weekKey():monthKey());
    board=seasonBoard(tag);
    document.getElementById('rank-sub').textContent=(rankMode==='w'?'Апталық жарыс':'Айлық жарыс')+' · '+seasonLabel(tag)+' · аяқталғанда топ-3 кубок алады';
  }
  const cups=['🏆','🥈','🥉'];
  document.getElementById('rank-podium').innerHTML=board.length?`<div class="podium">`+[1,0,2].filter(i=>board[i]).map(i=>`<div class="pod p${i+1}"><div class="pcup">${cups[i]}</div><div class="pname">${esc(board[i].name)}</div><div class="ppts">⭐ ${board[i].points}</div><div class="pbase">${i+1}</div></div>`).join('')+`</div>`:'';
  const el=document.getElementById('rank-list');
  if(!board.length)el.innerHTML='<div class="empty"><div class="ic">🏆</div><p>Әзірге ешкім жоқ</p></div>';
  else{
    const medals=['🥇','🥈','🥉'];
    el.innerHTML=board.map((u,i)=>`<div class="item${user&&u.id===user.id?' me':''}">
      <div style="width:36px;height:36px;border-radius:50%;background:var(--p);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;flex-shrink:0">${esc(String(u.name||'?')[0].toUpperCase())}</div>
      <div class="info"><h4>${medals[i]||('#'+(i+1))} ${esc(u.name)} ${user&&u.id===user.id?'(сіз)':''}</h4><p>${esc(u.title||(u.stars?('⭐'.repeat(Math.min(u.stars,5))):'—'))}</p></div>
      <div style="font-weight:700;color:var(--p);font-size:16px">⭐ ${u.points}</div></div>`).join('');
  }
  const type=rankMode==='w'?'w':'m';
  const hall=LS.get('ubt_trophies',[]).filter(t=>t.tag.slice(0,1)===type);
  const tags=[];hall.slice().reverse().forEach(t=>{if(!tags.includes(t.tag))tags.push(t.tag)});
  document.getElementById('rank-hall').innerHTML=tags.length?`<div class="card" style="margin-top:16px"><h3 style="margin-bottom:10px">🏛 Кубоктар залы</h3>`+tags.slice(0,6).map(tag=>`<div style="margin-bottom:8px"><b style="font-size:13px">${esc(seasonLabel(tag))}</b><div class="sub">`+hall.filter(t=>t.tag===tag).sort((a,b)=>a.rank-b.rank).map(t=>cups[t.rank-1]+' '+esc(t.name)+' ('+t.points+'⭐)').join(' · ')+`</div></div>`).join('')+`</div>`:'';
  showScr('s-ranking');
}

// ---------- Таңдаулылар ----------
function getBm(){return LS.get('ubt_bm_'+user.id,[])}
function isBm(q){return getBm().some(x=>x.text===q.text)}
function toggleBm(q){
  const a=getBm(),i=a.findIndex(x=>x.text===q.text);
  if(i>=0)a.splice(i,1);else a.unshift({id:q.id,text:q.text,options:q.options.slice(),correct:q.correct,subjectName:q.subjectName||st.subjectName||'',points:1});
  LS.set('ubt_bm_'+user.id,a);
}
function togBm(){const q=st.questions[st.currentIndex];if(!q)return;toggleBm(q);updBmBtn()}
function updBmBtn(){const q=st.questions[st.currentIndex],b=document.getElementById('bm');if(!b||!q)return;const on=isBm(q);b.textContent=on?'★':'☆';b.classList.toggle('on',on)}
function showBookmarks(){renderBookmarks();showScr('s-bm')}
function renderBookmarks(){
  const a=getBm(),el=document.getElementById('bm-list');
  el.innerHTML=a.length?a.map((q,i)=>`<div class="item" style="align-items:flex-start"><div class="info"><h4 style="white-space:normal">${esc(q.text)}</h4><p>✓ ${esc(q.options[q.correct])}${q.subjectName?' · '+esc(q.subjectName):''}</p></div><div class="acts"><button class="btn btn-d btn-sm" onclick="delBm(${i})">✕</button></div></div>`).join(''):'<div class="empty"><div class="ic">🔖</div><p>Таңдаулы сұрақ жоқ.<br>Тест кезінде ☆ батырмасын басыңыз.</p></div>';
  document.getElementById('bm-start').style.display=a.length?'inline-flex':'none';
  mathIn(el);
}
function delBm(i){const a=getBm();a.splice(i,1);LS.set('ubt_bm_'+user.id,a);renderBookmarks()}
function startBm(){
  const a=getBm();if(!a.length)return;
  st=baseState();
  st.questions=a.map(q=>({...q,id:'bm_'+hash(q.text),subjectName:q.subjectName||'Таңдаулылар'}));
  st.subjectName='Таңдаулылар';st.isMistakes=true;st.timerSeconds=Math.max(a.length*90,600);beginTest();
}

// ---------- Күн сұрағы ----------
function getQotd(){
  const today=dayKey(),saved=LS.get('ubt_qotd_day',null);
  if(saved&&saved.date===today&&saved.q)return saved.q;
  const pool=[];
  Object.values(BANK).forEach(b=>b.qs.forEach(q=>pool.push({text:q.text,options:q.options,correct:q.correct,subjectName:b.name})));
  publicTests().forEach(t=>t.questions.forEach(q=>{if(q.options&&q.options.length>=2)pool.push({text:q.text,options:q.options,correct:q.correct,subjectName:t.topic})}));
  if(!pool.length)return null;
  const q=pool[hash(today)%pool.length];
  LS.set('ubt_qotd_day',{date:today,q});
  return q;
}
function qotdHTML(){
  const q=getQotd();if(!q)return '';
  const rec=LS.get('ubt_qotd_'+user.id,null),answered=rec&&rec.date===dayKey();
  const L=['A','B','C','D','E'];
  const ops=q.options.map((o,i)=>{
    let cls='qotd-op';
    if(answered){cls+=' lock';if(i===q.correct)cls+=' ok';else if(i===rec.ans)cls+=' bad'}
    return `<div class="${cls}" ${answered?'':`onclick="answerQotd(${i})"`}><b>${L[i]}</b><span>${esc(o)}</span></div>`;
  }).join('');
  const msg=answered?(rec.ans===q.correct?'<div style="color:var(--ok);font-weight:700;font-size:13px">✅ Дұрыс! +20 ⭐ бонус алдыңыз</div>':'<div style="color:var(--err);font-weight:700;font-size:13px">❌ Бұл жолы болмады. Ертең жаңа сұрақ!</div>'):'<div class="sub">Дұрыс жауап берсеңіз +20 ⭐</div>';
  return `<div class="card"><h3 style="margin-bottom:8px">❓ Күн сұрағы <span class="sub" style="font-weight:400">· ${esc(q.subjectName||'')}</span></h3><div style="font-size:14px;margin-bottom:10px">${esc(q.text)}</div>${ops}${msg}</div>`;
}
function answerQotd(i){
  const q=getQotd();if(!q||!user||user.isAdmin)return;
  const rec=LS.get('ubt_qotd_'+user.id,null);if(rec&&rec.date===dayKey())return;
  LS.set('ubt_qotd_'+user.id,{date:dayKey(),ans:i});
  if(i===q.correct){addPoints(20);confetti(90)}
  renderHomeExtras();
}

// ---------- Оқу жоспары ----------
let planAll=false;
function planDays(p){
  const n=daysBetween(p.start||dayKey(),p.date);if(n<0)return[];
  const subs=p.subjects.length?p.subjects:['Жалпы қайталау'],out=[];let k=0;
  for(let i=0;i<=n;i++){
    const d=dayKey(addDays(parseDay(p.start||dayKey()),i)),left=n-i;let tasks=[];
    if(left===0)tasks=['🎯 ҰБТ күні — сәттілік!'];
    else if(left===1)tasks=['😌 Демалыңыз, формулаларды жеңіл шолыңыз','🔖 Таңдаулы сұрақтарды қараңыз'];
    else if(left<=7)tasks=['📝 Толық сынақ тест тапсырыңыз','❌ Қателермен жұмыс'];
    else{
      const per=Math.min(2,subs.length);
      for(let j=0;j<per;j++)tasks.push('📖 '+subs[(k+j)%subs.length]+': тақырып + тест');
      k+=per;
      if(i%7===6)tasks.push('🔁 Апталық қайталау: қателер мен таңдаулылар');
    }
    out.push({date:d,tasks,left});
  }
  return out;
}
function showPlanner(){
  const p=LS.get('ubt_plan_'+user.id,null),chosen=p?p.subjects:PLAN_SUBJECTS.slice(0,3);
  document.getElementById('pl-subs').innerHTML=PLAN_SUBJECTS.map((s,i)=>`<label class="switch" style="margin-bottom:6px"><input type="checkbox" class="pl-sub" value="${i}" ${chosen.includes(s)?'checked':''}> ${esc(s)}</label>`).join('');
  const de=document.getElementById('pl-date');de.min=dayKey();de.value=p?p.date:'';
  planAll=false;renderPlan();showScr('s-plan');
}
function savePlan(){
  const date=document.getElementById('pl-date').value;
  if(!date){alert('ҰБТ күнін таңдаңыз');return}
  if(daysBetween(dayKey(),date)<0){alert('Бұл күн өтіп кеткен. Болашақ күнді таңдаңыз');return}
  const subjects=Array.from(document.querySelectorAll('.pl-sub:checked')).map(c=>PLAN_SUBJECTS[+c.value]);
  if(!subjects.length){alert('Кемінде 1 пән таңдаңыз');return}
  LS.set('ubt_plan_'+user.id,{date,subjects,start:dayKey()});
  LS.set('ubt_plan_done_'+user.id,{});
  renderPlan();
}
function planDone(){return LS.get('ubt_plan_done_'+user.id,{})}
function togPlanTask(date,idx){
  const d=planDone(),k=date+'|'+idx;
  if(d[k])delete d[k];else d[k]=1;
  LS.set('ubt_plan_done_'+user.id,d);
  if(document.getElementById('s-plan').classList.contains('active'))renderPlan();else renderHomeExtras();
}
function planTaskHTML(day,t,idx,done){
  const on=!!done[day.date+'|'+idx];
  return `<label class="${on?'done':''}"><input type="checkbox" ${on?'checked':''} onchange="togPlanTask('${day.date}',${idx})"><span>${esc(t)}</span></label>`;
}
function renderPlan(){
  const el=document.getElementById('pl-out'),p=LS.get('ubt_plan_'+user.id,null);
  if(!p){el.innerHTML='';return}
  const today=dayKey(),left=daysBetween(today,p.date);
  if(left<0){el.innerHTML='<div class="empty"><div class="ic">🎓</div><p>ҰБТ күні өтті. Жаңа күн таңдаңыз.</p></div>';return}
  const all=planDays(p),done=planDone();
  let total=0,cnt=0;all.forEach(d=>d.tasks.forEach((t,i)=>{total++;if(done[d.date+'|'+i])cnt++}));
  const pct=total?Math.round(cnt/total*100):0;
  const upcoming=all.filter(d=>d.date>=today),shown=planAll?upcoming:upcoming.slice(0,14);
  el.innerHTML=`<div class="card"><h3>🎯 ҰБТ-ға <b style="color:var(--p)">${left}</b> күн қалды</h3>
    <div class="sub" style="margin:4px 0 8px">Орындалды: ${cnt} / ${total} (${pct}%)</div>
    <div class="prog-w" style="height:8px"><div class="prog-f" style="width:${pct}%"></div></div></div>`
    +shown.map(d=>{const dt=parseDay(d.date);
      return `<div class="plan-day${d.date===today?' today':''}"><h4>${WDAYS[dt.getDay()]} · ${String(dt.getDate()).padStart(2,'0')}.${String(dt.getMonth()+1).padStart(2,'0')}${d.date===today?' <span class="badge badge-pub">Бүгін</span>':''}</h4>${d.tasks.map((t,i)=>planTaskHTML(d,t,i,done)).join('')}</div>`}).join('')
    +(upcoming.length>14?`<div class="row"><button class="btn btn-s btn-sm" onclick="planAll=!planAll;renderPlan()">${planAll?'Қысқарту':'Барлығын көрсету ('+upcoming.length+' күн)'}</button></div>`:'');
}
function todayPlanHTML(){
  const p=LS.get('ubt_plan_'+user.id,null);if(!p)return '';
  const today=dayKey(),day=planDays(p).find(d=>d.date===today);if(!day)return '';
  const done=planDone();
  return `<div class="card"><h3 style="margin-bottom:8px">🗓 Бүгінгі жоспар <button class="btn btn-s btn-sm" style="float:right" onclick="showPlanner()">Толық</button></h3><div class="plan-day" style="border:none;padding:0;margin:0">${day.tasks.map((t,i)=>planTaskHTML(day,t,i,done)).join('')}</div></div>`;
}

// ---------- Флеш-карталар ----------
let fl={deck:[],total:0,known:0,flip:false};
function qCard(q){return{f:q.text,b:q.options[q.correct]}}
function flashCards(k){
  if(k==='gloss')return GLOSS.map(g=>({f:g.t,b:g.d}));
  if(k==='formulas')return LS.get('ubt_formulas',[]).map(f=>({f:f.title,b:f.body}));
  if(k==='mist')return LS.get('ubt_mistakes_'+user.id,[]).map(qCard);
  if(k==='bm')return getBm().map(qCard);
  if(k.indexOf('bank:')===0)return((BANK[k.slice(5)]||{qs:[]}).qs).map(qCard);
  if(k.indexOf('test:')===0){const t=allTests().find(x=>x.id===k.slice(5));return t?t.questions.map(qCard):[]}
  return [];
}
function showFlash(){
  const s=[['gloss','📖 Глоссарий (даталар, терминдер)'],['formulas','📐 Формулалар'],['mist','❌ Қателерім'],['bm','🔖 Таңдаулылар']];
  Object.keys(BANK).forEach(k=>s.push(['bank:'+k,'⚡ '+BANK[k].name]));
  const seen={};
  myTests().concat(publicTests()).forEach(t=>{if(seen[t.id]||!t.questions.length)return;seen[t.id]=1;s.push(['test:'+t.id,'📚 '+t.topic])});
  document.getElementById('fl-src').innerHTML=s.map(a=>`<option value="${esc(a[0])}">${esc(a[1])}</option>`).join('');
  fl={deck:[],total:0,known:0,flip:false};renderFlash();showScr('s-flash');
}
function startFlash(shuffle){
  const cards=flashCards(document.getElementById('fl-src').value);
  if(!cards.length){alert('Бұл дереккөзде карточка жоқ');return}
  if(shuffle){for(let i=cards.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));const t=cards[i];cards[i]=cards[j];cards[j]=t}}
  fl={deck:cards,total:cards.length,known:0,flip:false};renderFlash();
}
function renderFlash(){
  const el=document.getElementById('fl-area');
  if(!fl.total){el.innerHTML='';return}
  if(!fl.deck.length){el.innerHTML=`<div class="card" style="text-align:center"><div style="font-size:48px">🎉</div><h3>Барлығын жаттадыңыз!</h3><p class="sub">${fl.total} карточка</p></div>`;confetti();return}
  const c=fl.deck[0];
  el.innerHTML=`<div class="sub" style="text-align:center;margin-bottom:8px">Жатталды: <b>${fl.known}</b> / ${fl.total} · қалды ${fl.deck.length}</div>
    <div class="fcard ${fl.flip?'back':''}" onclick="flFlip()"><div class="flab">${fl.flip?'Жауап':'Сұрақ / термин'}</div><div class="ftxt">${esc(fl.flip?c.b:c.f)}</div><div class="fhint">басып аударыңыз ↻</div></div>
    <div class="row" style="margin-top:14px"><button class="btn btn-w" onclick="flAgain()">↺ Қайталау</button><button class="btn btn-ok" onclick="flKnow()">✓ Білемін</button></div>`;
  mathIn(el);
}
function flFlip(){if(!fl.deck.length)return;fl.flip=!fl.flip;renderFlash()}
function flKnow(){if(!fl.deck.length)return;fl.deck.shift();fl.known++;fl.flip=false;renderFlash()}
function flAgain(){if(!fl.deck.length)return;fl.deck.push(fl.deck.shift());fl.flip=false;renderFlash()}

// ---------- Глоссарий ----------
let glCat='';
function showGloss(){
  const cats=[''].concat(GLOSS.map(g=>g.c).filter((c,i,a)=>a.indexOf(c)===i));
  document.getElementById('gl-cats').innerHTML=cats.map(c=>`<button class="btn ${glCat===c?'btn-p':'btn-s'} btn-sm" onclick="glCat=${jsq(c)};showGloss()">${c?esc(c):'Барлығы'}</button>`).join('');
  renderGloss();showScr('s-gloss');
}
function renderGloss(){
  const q=(document.getElementById('gl-q').value||'').trim().toLowerCase();
  const list=GLOSS.filter(g=>(!glCat||g.c===glCat)&&(!q||(g.t+' '+g.d).toLowerCase().indexOf(q)>=0));
  document.getElementById('gl-count').textContent='Табылды: '+list.length;
  const el=document.getElementById('gl-list');
  el.innerHTML=list.length?list.map(g=>`<div class="gl-item"><div class="gl-cat">${esc(g.c)}</div><h4>${esc(g.t)}</h4><p>${esc(g.d)}</p></div>`).join(''):'<div class="empty"><div class="ic">🔍</div><p>Ештеңе табылмады</p></div>';
  mathIn(el);
}

// ---------- Мұғалім / Куратор ----------
let tchOpen=null;
function getClasses(){return LS.get('ubt_classes',[])}
function saveClasses(a){LS.set('ubt_classes',a)}
function profileById(id){return Object.values(LS.get('ubt_profiles',{})).find(p=>p.id===id)||null}
function genClassCode(){const ch='ABCDEFGHJKLMNPQRSTUVWXYZ23456789';let s='';for(let i=0;i<6;i++)s+=ch[Math.floor(Math.random()*ch.length)];return s}
function studentStats(id){
  const pg=getProg(id),n=pg.length;
  const avg=n?Math.round(pg.map(pctOf).reduce((a,b)=>a+b,0)/n):0;
  return{n,avg,last:n?pg[n-1]:null,mist:LS.get('ubt_mistakes_'+id,[]).length,points:getUserStats(id).points||0};
}
function showTeacher(){tchOpen=null;document.getElementById('tch-detail').innerHTML='';renderTeacher();showScr('s-teacher')}
function createClass(){
  if(!user||!user.isAdmin)return;
  const n=document.getElementById('tch-name').value.trim();
  if(!n){alert('Сынып атауын жазыңыз');return}
  const a=getClasses();let code;
  do{code=genClassCode()}while(a.some(c=>c.code===code));
  a.push({id:'c_'+Date.now().toString(36),name:n,teacherId:user.id,teacherName:user.name,code,students:[]});
  saveClasses(a);document.getElementById('tch-name').value='';renderTeacher();
}
function delClass(id){
  if(!confirm('Сыныпты өшіру керек пе?'))return;
  saveClasses(getClasses().filter(c=>c.id!==id));
  document.getElementById('tch-detail').innerHTML='';renderTeacher();
}
function addStudent(cid){
  if(!isTeacherUser())return;
  const inp=document.getElementById('tch-add-'+cid),login=inp.value.trim();if(!login)return;
  const u=findUserByLogin(login);
  if(!u){alert('Мұндай оқушы тіркелмеген. Алдымен оқушы «Тіркелу» арқылы аккаунт ашуы керек.');return}
  const a=getClasses(),c=a.find(x=>x.id===cid);if(!c)return;
  if(c.students.includes(u.id)){alert('Оқушы сыныпта бар');return}
  c.students.push(u.id);saveClasses(a);renderTeacher();
}
function removeStudent(cid,sid){
  if(!confirm('Оқушыны сыныптан шығару керек пе?'))return;
  const a=getClasses(),c=a.find(x=>x.id===cid);if(!c)return;
  c.students=c.students.filter(x=>x!==sid);saveClasses(a);
  document.getElementById('tch-detail').innerHTML='';renderTeacher();
}
function joinClass(){
  const code=document.getElementById('tch-code').value.trim().toUpperCase();if(!code)return;
  const a=getClasses(),c=a.find(x=>x.code===code);
  if(!c){alert('Мұндай код табылмады');return}
  if(c.teacherId===user.id){alert('Бұл — сіздің сыныбыңыз');return}
  if(c.students.includes(user.id)){alert('Сіз бұл сыныптасыз');return}
  c.students.push(user.id);saveClasses(a);
  document.getElementById('tch-code').value='';renderTeacher();alert('✅ Сыныпқа қосылдыңыз: '+c.name);
}
function leaveClass(cid){
  if(!confirm('Сыныптан шығу керек пе?'))return;
  const a=getClasses(),c=a.find(x=>x.id===cid);if(!c)return;
  c.students=c.students.filter(x=>x!==user.id);saveClasses(a);renderTeacher();
}
function classCardHTML(c){
  const rows=c.students.map(id=>{
    const p=profileById(id),s=studentStats(id);
    return `<tr><td><b>${esc(p?p.name:'?')}</b></td><td>${s.n}</td><td>${s.n?s.avg+'%':'—'}</td><td>${s.mist}</td><td>⭐ ${s.points}</td><td style="white-space:nowrap"><button class="btn btn-s btn-sm" onclick="showStudent('${c.id}','${id}')">Қарау</button> <button class="btn btn-d btn-sm" onclick="removeStudent('${c.id}','${id}')">✕</button></td></tr>`;
  }).join('');
  const withT=c.students.map(id=>studentStats(id)).filter(s=>s.n);
  const avg=withT.length?Math.round(withT.reduce((a,s)=>a+s.avg,0)/withT.length)+'%':'—';
  return `<div class="card">
    <div style="display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:8px">
      <h3>${esc(c.name)} <span class="badge badge-pub">Код: ${esc(c.code)}</span></h3>
      <div style="display:flex;gap:6px;flex-wrap:wrap"><button class="btn btn-s btn-sm" onclick="openTchChat('${threadOfClass(c)}')">💬 Админмен чат</button><button class="btn btn-d btn-sm" onclick="delClass('${c.id}')">Сыныпты өшіру</button></div>
    </div>
    <div class="sub" style="margin-bottom:10px">Оқушылар: <b>${c.students.length}</b> · сыныптың орташа балы: <b>${avg}</b></div>
    ${c.students.length?`<div class="tscroll"><table class="ttable"><tr><th>Оқушы</th><th>Тест</th><th>Орташа</th><th>Қате</th><th>Ұпай</th><th></th></tr>${rows}</table></div>`:'<div class="sub">Оқушы жоқ. Төмендегі өріс арқылы логин бойынша қосыңыз немесе кодты оқушыларға беріңіз.</div>'}
    <div style="display:flex;gap:8px;margin-top:12px"><input id="tch-add-${c.id}" placeholder="Оқушы логині" style="flex:1;padding:9px 12px;border:1px solid var(--b);border-radius:10px;background:var(--bg);color:var(--t);font-family:inherit"><button class="btn btn-ok btn-sm" onclick="addStudent('${c.id}')">➕ Қосу</button></div>
  </div>`;
}
function renderTeacher(){
  const all=getClasses(),mine=all.filter(c=>c.teacherId===user.id),joined=all.filter(c=>c.students.includes(user.id));
  document.getElementById('tch-classes').innerHTML=mine.length?mine.map(classCardHTML).join(''):'<div class="empty"><div class="ic">🏫</div><p>Сынып жоқ. Жоғарыда жаңа сынып құрыңыз.</p></div>';
  document.getElementById('tch-joined').innerHTML=joined.length?joined.map(c=>`<div class="item" style="margin-bottom:6px"><div class="info"><h4>${esc(c.name)}</h4><p>Мұғалім: ${esc(c.teacherName||'')}</p></div><button class="btn btn-s btn-sm" onclick="leaveClass('${c.id}')">Шығу</button></div>`).join(''):'';
}
function showStudent(cid,sid){
  if(!isTeacherUser())return;
  const p=profileById(sid),s=studentStats(sid);
  const hist=LS.get('ubt_hist_'+sid,[]).slice(0,10),pg=getProg(sid),mist=LS.get('ubt_mistakes_'+sid,[]);
  const topics={};pg.forEach(x=>{const k=x.topic||'Тест';(topics[k]=topics[k]||[]).push(pctOf(x))});
  const tl=Object.keys(topics).map(k=>({k,avg:Math.round(topics[k].reduce((a,b)=>a+b,0)/topics[k].length),n:topics[k].length})).sort((a,b)=>a.avg-b.avg);
  document.getElementById('tch-detail').innerHTML=`<div class="card" style="border-color:var(--p)">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px"><h3>👤 ${esc(p?p.name:'?')}</h3><button class="btn btn-s btn-sm" onclick="document.getElementById('tch-detail').innerHTML=''">Жабу</button></div>
    <div class="stat-grid"><div class="stat"><b>${s.n}</b><span>Тест</span></div><div class="stat"><b>${s.n?s.avg+'%':'—'}</b><span>Орташа бал</span></div><div class="stat"><b>${s.mist}</b><span>Қате сұрақ</span></div><div class="stat"><b>${s.points}</b><span>Ұпай</span></div></div>
    <h4 style="margin:10px 0 6px">📊 Тақырыптар бойынша (әлсізден күштіге)</h4>
    ${tl.length?tl.map(t=>`<div class="tbar"><div class="tn">${esc(t.k)}</div><div class="tb"><i style="width:${t.avg}%"></i></div><div class="tv">${t.avg}%</div></div>`).join(''):'<div class="sub">Нәтиже жоқ</div>'}
    <h4 style="margin:14px 0 6px">📋 Соңғы тесттер</h4>
    ${hist.length?hist.map(h=>`<div class="res-row"><span>${esc(h.topic||'Тест')} <span class="sub">· ${esc(h.date)}</span></span><b>${h.score}/${h.max}</b></div>`).join(''):'<div class="sub">Тарих бос</div>'}
    <h4 style="margin:14px 0 6px">❌ Қателері</h4>
    ${mist.length?mist.slice(0,10).map(q=>`<div class="res-row" style="font-size:13px"><span>${esc(q.text)}</span><span class="sub" style="margin-left:8px">✓ ${esc(q.options[q.correct])}</span></div>`).join(''):'<div class="sub">Қате жоқ 🎉</div>'}
  </div>`;
  mathIn(document.getElementById('tch-detail'));
  document.getElementById('tch-detail').scrollIntoView({behavior:'smooth',block:'start'});
}

// ---------- Басты бет блогы ----------
function renderHomeExtras(){
  const el=document.getElementById('home-extras');if(!el||!user)return;
  try{checkRollover()}catch(e){}
  if(user.isAdmin){el.innerHTML=quoteCard();return}
  const sk=currentStreak(),s=getStreak(),plan=LS.get('ubt_plan_'+user.id,null);
  let chips=`<div class="chip">🔥 <b>${sk}</b> күн streak</div>`;
  if(sk>0&&s.last!==dayKey())chips+=`<div class="chip warn">⚠ Streak сақтау үшін бүгін тест тапсырыңыз</div>`;
  if(plan&&plan.date){const n=daysBetween(dayKey(),plan.date);if(n>=0)chips+=`<div class="chip" style="cursor:pointer" onclick="showPlanner()">🎯 ҰБТ-ға <b>${n}</b> күн қалды</div>`}
  el.innerHTML=`<div class="chips">${chips}</div>`+quoteCard()+qotdHTML()+todayPlanHTML();
  mathIn(el);
}

// ---------- Тест аяқталған соң ----------
let _seenScore=null;
function afterFinish(){
  if(!user)return;
  const ls=st.lastScore;if(!ls)return;
  const rb=document.getElementById('res-break');
  if(user.isAdmin){rb.insertAdjacentHTML('beforeend',`<div class="quote">💬 ${esc(randQuote())}</div>`);return}
  const pct=ls.max?ls.score/ls.max:0,cur=Math.round(pct*100);
  let extra='';
  const sk=touchStreak();
  if(sk.isNew){
    if(sk.bonus)addPoints(sk.bonus);
    extra+=`<div class="res-row"><span>🔥 Streak: ${sk.count} күн қатарынан</span><span style="font-weight:700;color:var(--ok)">+${sk.bonus} ⭐</span></div>`;
  }else extra+=`<div class="res-row"><span>🔥 Streak</span><span style="font-weight:700">${sk.count} күн</span></div>`;
  const prev=getProg(user.id).slice(0,-1).filter(p=>p.max>=5).map(pctOf);
  const isRec=!st.isMistakes&&ls.max>=5&&prev.length>0&&cur>Math.max.apply(null,prev);
  if(isRec)extra+=`<div class="res-row"><span>🏆 Жаңа жеке рекорд!</span><span style="font-weight:700;color:var(--warn)">${cur}%</span></div>`;
  extra+=`<div class="quote">💬 ${esc(randQuote())}</div>`;
  rb.insertAdjacentHTML('beforeend',extra);
  if(pct>=0.8||isRec)confetti();
}

// ---------- Профиль: streak + кубоктар ----------
function profExtra(){
  const el=document.getElementById('prof-extra');if(!el||!user||user.isAdmin){if(el)el.innerHTML='';return}
  const s=getStreak(),tr=LS.get('ubt_trophies',[]).filter(t=>t.id===user.id);
  const cups=['🏆','🥈','🥉'];
  el.innerHTML=`<h3 style="margin-bottom:10px">🔥 Streak және кубоктар</h3>
    <div class="stat-grid" style="grid-template-columns:repeat(2,1fr)"><div class="stat"><b>${currentStreak()}</b><span>Қазіргі streak (күн)</span></div><div class="stat"><b>${s.best||0}</b><span>Ең ұзақ streak</span></div></div>
    ${tr.length?tr.slice().reverse().map(t=>`<div class="res-row"><span>${cups[t.rank-1]} ${esc(seasonLabel(t.tag))} · ${t.tag.slice(0,1)==='m'?'айлық':'апталық'}</span><b>${t.rank}-орын · ⭐ ${t.points}</b></div>`).join(''):'<div class="sub">Кубок әзірге жоқ. Ай/апта соңында топ-3-ке кіріңіз!</div>'}`;
}

// ---------- Ілмектер (hooks) ----------
(function(){
  const _ss=showScr;
  showScr=function(id){
    _ss(id);
    try{document.body.classList.toggle('in-test',id==='s-test');if(id==='s-home')renderHomeExtras();mathScreen()}catch(e){}
  };
  const _rq=renderQ;
  renderQ=function(){_rq();try{updBmBtn();mathIn(document.getElementById('s-test'))}catch(e){}};
  const _rf=renderFormulas;
  renderFormulas=function(){_rf();try{mathIn(document.getElementById('formula-list'))}catch(e){}};
  const _ra=reviewAns;
  reviewAns=function(){
    _ra();
    try{
      document.querySelectorAll('#rev-list .rev').forEach((el,i)=>{
        const q=st.questions[i],h=el.querySelector('.rh');if(!q||!h)return;
        const b=document.createElement('button');
        const sync=()=>{const on=isBm(q);b.className='flag'+(on?' on':'');b.textContent=on?'★':'☆'};
        b.title='Таңдаулыға сақтау';b.onclick=()=>{toggleBm(q);sync()};sync();h.appendChild(b);
      });
      mathIn(document.getElementById('rev-list'));
    }catch(e){}
  };
  const _ap=addPoints;
  addPoints=function(p){_ap(p);try{recordSeason(p)}catch(e){}};
  const _ft=finishTest;
  finishTest=function(force){
    _ft(force);
    try{
      if(document.getElementById('s-res').classList.contains('active')&&st.lastScore&&st.lastScore!==_seenScore){
        _seenScore=st.lastScore;afterFinish();
      }
    }catch(e){}
  };
  const _mp=showMyProfile;
  showMyProfile=function(){_mp();try{profExtra()}catch(e){}};
  const _lo=doLogout;
  doLogout=function(){homeQuote=null;_lo()};
})();
applyTheme();

// ================= Мұғалім рөлі =================
function isTeacherUser(){
  if(!user)return false;if(user.isAdmin)return true;
  const p=findUserByLogin(user.name);
  return !!(p&&p.role==='teacher'&&p.teacherApproved);
}
function isTeacherPending(){
  if(!user||user.isAdmin)return false;
  const p=findUserByLogin(user.name);
  return !!(p&&p.role==='teacher'&&!p.teacherApproved);
}
function showTeacherReg(){
  ['login-box','register-box','forgot-box','contact-box'].forEach(i=>document.getElementById(i).style.display='none');
  document.getElementById('teacher-reg-box').style.display='block';
}
function doRegisterTeacher(){
  const name=document.getElementById('tr-name').value.trim();
  const info=document.getElementById('tr-info').value.trim();
  const pass=document.getElementById('tr-pass').value,pass2=document.getElementById('tr-pass2').value;
  if(!name||name.length<2){alert('Аты-жөніңізді жазыңыз');return}
  if(!pass||pass.length<4){alert('Пароль кемінде 4 таңба');return}
  if(pass!==pass2){alert('Парольдер сәйкес емес');return}
  if(findUserByLogin(name)||name.toLowerCase()==='админ'||name.toLowerCase()==='admin'){alert('Бұл ат тіркелген. Басқа ат таңдаңыз');return}
  const key=name.toLowerCase(),profiles=LS.get('ubt_profiles',{});
  const u={name:name,password:pass,id:'u_'+key.replace(/[^\p{L}\p{N}]+/gu,'_')+'_'+Date.now().toString(36).slice(-4),isAdmin:false,role:'teacher',teacherApproved:false,teacherInfo:info};
  profiles[key]=u;LS.set('ubt_profiles',profiles);
  setUserStats(u.id,{points:0,title:'',stars:0,verified:false});
  ['tr-name','tr-info','tr-pass','tr-pass2'].forEach(i=>document.getElementById(i).value='');
  alert('✅ Өтініш админге жіберілді. Қазір оқушы ретінде кіре аласыз; админ рұқсат бергесін мұғалім кабинеті ашылады.');
  showLoginBox();document.getElementById('login-name').value=u.name;
}
function mutateProfile(id,fn){
  const profiles=LS.get('ubt_profiles',{});let ok=false;
  Object.keys(profiles).forEach(k=>{if(profiles[k].id===id){fn(profiles[k]);ok=true}});
  if(ok)LS.set('ubt_profiles',profiles);return ok;
}
function adminSetTeacher(id,on){
  if(!user||!user.isAdmin)return;
  mutateProfile(id,p=>{
    if(on){p.role='teacher';p.teacherApproved=true}
    else{delete p.role;delete p.teacherApproved;delete p.teacherInfo}
  });
  if(on){const s=getUserStats(id);if(!s.title){s.title='👨‍🏫 Мұғалім';setUserStats(id,s)}}
  showAdmin();
}
function renderTeacherReq(){
  const el=document.getElementById('admin-teacher-req');if(!el)return;
  const pend=Object.values(LS.get('ubt_profiles',{})).filter(p=>p.role==='teacher'&&!p.teacherApproved);
  el.innerHTML=pend.length?pend.map(p=>`<div class="item"><div class="info"><h4>${esc(p.name)}</h4><p>${esc(p.teacherInfo||'—')}</p></div><div class="acts"><button class="btn btn-ok btn-sm" onclick="adminSetTeacher(${jsq(p.id)},true)">✓ Мұғалім ету</button><button class="btn btn-d btn-sm" onclick="adminRejectTeacher(${jsq(p.id)})">✕ Бас тарту</button></div></div>`).join(''):'<p class="sub">Жаңа өтініш жоқ</p>';
}
function adminRejectTeacher(id){
  if(!confirm('Өтінішті қабылдамау керек пе? Аккаунт оқушы ретінде қалады.'))return;
  mutateProfile(id,p=>{delete p.role;delete p.teacherApproved;delete p.teacherInfo});showAdmin();
}
(function(){
  ['showLoginBox','showRegister','showForgot','showContactAdmin'].forEach(n=>{
    const f=window[n];
    window[n]=function(){f.apply(this,arguments);const b=document.getElementById('teacher-reg-box');if(b)b.style.display='none'};
  });
  const _sa=showAdmin;
  showAdmin=function(){_sa();try{renderTeacherReq()}catch(e){}};
  const _rt=renderTeacher;
  renderTeacher=function(){
    _rt();
    const T=isTeacherUser();
    ['tch-create-card','tch-classes','tch-detail'].forEach(i=>{const e=document.getElementById(i);if(e)e.style.display=T?'':'none'});
    const n=document.getElementById('tch-notice');
    n.innerHTML=T?'':(isTeacherPending()
      ?'<div class="card"><h3>⏳ Өтініш қаралуда</h3><p class="sub">Админ мұғалім рұқсатын бергенше сынып құру ашылмайды. Қазір сыныпқа кодпен қосыла аласыз.</p></div>'
      :'<div class="card"><h3>🔒 Мұғалім кабинеті</h3><p class="sub">Сынып құру тек админ рұқсат берген мұғалімдерге ашық. Оқушы болсаңыз, төмендегі кодпен сыныпқа қосылыңыз.</p></div>');
  };
})();

// ================= Сынып ашу өтініші + сынып чаттары =================
const RESP_MS=12*3600*1000, CD_MS=60*1000;
function cdLeft(key){const t=LS.get('ubt_cd_'+key,0);return Math.max(0,CD_MS-(Date.now()-t))}
function cdCheck(key){
  const l=cdLeft(key);
  if(l>0){alert('⏳ Келесі өтінішті/хабарламаны 1 минуттан кейін жібере аласыз. Қалды: '+Math.ceil(l/1000)+' сек.');return false}
  return true;
}
function cdStamp(key){LS.set('ubt_cd_'+key,Date.now())}
function fmtT(t){return new Date(t).toLocaleString('kk-KZ',{day:'2-digit',month:'2-digit',hour:'2-digit',minute:'2-digit'})}
function getReqs(){return LS.get('ubt_class_reqs',[])}
function getCC(){return LS.get('ubt_class_chat',{})}
function threadMsgs(tid){return getCC()[tid]||[]}
function postThread(tid,from,name,text){
  const a=getCC();(a[tid]=a[tid]||[]).push({from,name,text,t:Date.now()});LS.set('ubt_class_chat',a);
}
function threadOfClass(c){return c.reqId||('cls_'+c.id)}
function threadTitle(tid){
  const r=getReqs().find(x=>x.id===tid);if(r)return r.name+' · '+r.teacherName;
  const c=getClasses().find(x=>threadOfClass(x)===tid);return c?(c.name+' · '+(c.teacherName||'')):'Чат';
}
function chatBoxHTML(tid,who){
  const msgs=threadMsgs(tid);
  const body=msgs.length?msgs.map(m=>{
    if(m.from==='system')return `<div class="cmsg sys">${esc(m.text)}<small>${fmtT(m.t)}</small></div>`;
    const me=m.from===who;
    return `<div class="cmsg ${me?'me':'other'}"><b style="font-size:11px">${me?'Сіз':(m.from==='admin'?'Админ':esc(m.name||'Мұғалім'))}</b><br>${esc(m.text)}<small>${fmtT(m.t)}</small></div>`;
  }).join(''):'<div class="sub" style="text-align:center;margin:auto">Хабарлама жоқ</div>';
  return `<div class="cbox"><div class="cmsgs" id="cmsgs">${body}</div>
    <div class="crow"><input id="cin-${tid}" maxlength="500" placeholder="Хабарлама жазыңыз..." onkeydown="if(event.key==='Enter')sendThread('${tid}','${who}')"><button class="btn btn-ok" onclick="sendThread('${tid}','${who}')">➤</button></div>
    ${who==='admin'?'':'<div class="sub" style="margin-top:4px">Хабарламалар арасы — 1 минут</div>'}</div>`;
}
function sendThread(tid,who){
  const inp=document.getElementById('cin-'+tid);if(!inp)return;
  const text=inp.value.trim();if(!text)return;
  if(who!=='admin'){if(!cdCheck(user.id))return;cdStamp(user.id)}
  postThread(tid,who,user.name,text);
  if(who==='admin')renderAdminClassChat();else renderTeacherChat();
}
function scrollChat(){const m=document.getElementById('cmsgs');if(m)m.scrollTop=m.scrollHeight}

// --- Мұғалім жағы ---
let tchThread=null;
function submitClassRequest(){
  if(!user||user.isAdmin||!isTeacherUser())return;
  const name=document.getElementById('tch-req-name').value.trim();
  const note=document.getElementById('tch-req-note').value.trim();
  if(!name){alert('Сынып атауын жазыңыз');return}
  if(!cdCheck(user.id))return;
  const reqs=getReqs();
  if(reqs.filter(r=>r.teacherId===user.id&&r.status==='pending').length>=5){alert('Күтіп тұрған өтініш тым көп (5). Админнің жауабын күтіңіз.');return}
  const id='r_'+Date.now().toString(36),now=Date.now();
  reqs.push({id,teacherId:user.id,teacherName:user.name,name,note,status:'pending',createdAt:now,dueAt:now+RESP_MS});
  LS.set('ubt_class_reqs',reqs);
  postThread(id,'system','','Өтініш жіберілді: «'+name+'». Админ 12 сағат ішінде жауап береді.');
  if(note)postThread(id,'teacher',user.name,note);
  cdStamp(user.id);
  document.getElementById('tch-req-name').value='';document.getElementById('tch-req-note').value='';
  tchThread=id;renderTeacher();
  alert('✅ Өтініш админге жіберілді. 12 сағат ішінде жауап беріледі.');
}
function openTchChat(tid){tchThread=tid;renderTeacher();const e=document.getElementById('tch-chat');if(e)e.scrollIntoView({behavior:'smooth',block:'start'})}
function closeTchChat(){tchThread=null;renderTeacher()}
function renderTeacherChat(){
  const el=document.getElementById('tch-chat');if(!el)return;
  if(!tchThread){el.innerHTML='';return}
  el.innerHTML=`<div class="card"><div style="display:flex;justify-content:space-between;align-items:center"><h3>💬 ${esc(threadTitle(tchThread))}</h3><button class="btn btn-s btn-sm" onclick="closeTchChat()">Жабу</button></div>${chatBoxHTML(tchThread,'teacher')}</div>`;
  scrollChat();
}
function renderTeacherReqs(){
  const el=document.getElementById('tch-reqs');if(!el)return;
  const mine=getReqs().filter(r=>r.teacherId===user.id).sort((a,b)=>b.createdAt-a.createdAt);
  const st={pending:'<span class="badge" style="background:#fef3c7;color:#92400e">⏳ Күтуде</span>',approved:'<span class="badge badge-pub">✓ Мақұлданды</span>',rejected:'<span class="badge badge-err">✕ Қабылданбады</span>'};
  el.innerHTML=mine.length?`<div class="card"><h3 style="margin-bottom:10px">📋 Менің өтініштерім</h3><div class="list">`+mine.map(r=>`<div class="item"><div class="info"><h4>${esc(r.name)}</h4><p>${st[r.status]||''} · ${fmtT(r.createdAt)}${r.status==='pending'?' · жауап мерзімі: '+fmtT(r.dueAt):''}</p></div><button class="btn btn-s btn-sm" onclick="openTchChat('${r.id}')">💬 Чат</button></div>`).join('')+`</div></div>`:'';
}
function tickCooldown(){
  const b=document.getElementById('tch-req-btn'),l=document.getElementById('tch-req-cd');if(!b||!user)return;
  const left=cdLeft(user.id);
  b.disabled=left>0;l.textContent=left>0?('Келесі өтініш: '+Math.ceil(left/1000)+' сек.'):'';
}
setInterval(tickCooldown,1000);

// --- Админ жағы ---
let admThread=null;
function renderClassReqs(){
  const el=document.getElementById('admin-class-req');if(!el)return;
  const pend=getReqs().filter(r=>r.status==='pending').sort((a,b)=>a.createdAt-b.createdAt);
  el.innerHTML=pend.length?pend.map(r=>{
    const over=Date.now()>r.dueAt;
    return `<div class="item" style="flex-wrap:wrap"><div class="info"><h4>${esc(r.name)}</h4><p>👨‍🏫 ${esc(r.teacherName)} · ${fmtT(r.createdAt)}</p><p>${over?'<b style="color:var(--err)">⚠ Жауап мерзімі өтті</b>':'Жауап мерзімі: '+fmtT(r.dueAt)}${r.note?' · '+esc(r.note):''}</p></div><div class="acts"><button class="btn btn-ok btn-sm" onclick="adminApproveClass('${r.id}')">✓ Мақұлдау</button><button class="btn btn-d btn-sm" onclick="adminRejectClass('${r.id}')">✕ Бас тарту</button><button class="btn btn-s btn-sm" onclick="openAdmChat('${r.id}')">💬</button></div></div>`}).join(''):'<p class="sub">Жаңа өтініш жоқ</p>';
}
function adminApproveClass(rid){
  if(!user||!user.isAdmin)return;
  const reqs=getReqs(),r=reqs.find(x=>x.id===rid);if(!r||r.status!=='pending')return;
  const a=getClasses();let code;do{code=genClassCode()}while(a.some(c=>c.code===code));
  const cid='c_'+Date.now().toString(36);
  a.push({id:cid,name:r.name,teacherId:r.teacherId,teacherName:r.teacherName,code,students:[],reqId:r.id});
  saveClasses(a);r.status='approved';r.classId=cid;LS.set('ubt_class_reqs',reqs);
  postThread(r.id,'system','','✅ Өтініш мақұлданды. Сынып ашылды. Сынып коды: '+code);
  showAdmin();
}
function adminRejectClass(rid){
  if(!user||!user.isAdmin)return;
  if(!confirm('Өтінішті қабылдамау керек пе?'))return;
  const reqs=getReqs(),r=reqs.find(x=>x.id===rid);if(!r||r.status!=='pending')return;
  r.status='rejected';LS.set('ubt_class_reqs',reqs);
  postThread(r.id,'system','','❌ Өтініш қабылданбады. Себебін чатта сұрай аласыз.');
  showAdmin();
}
function renderAdminThreads(){
  const el=document.getElementById('admin-class-threads');if(!el)return;
  const reqs=getReqs(),cls=getClasses();
  const rows=reqs.map(r=>({tid:r.id,title:r.name,teacher:r.teacherName,status:r.status}));
  cls.filter(c=>!c.reqId).forEach(c=>rows.push({tid:threadOfClass(c),title:c.name,teacher:c.teacherName||'',status:'approved'}));
  rows.forEach(r=>{const m=threadMsgs(r.tid);r.n=m.length;r.last=m.length?m[m.length-1].t:0});
  rows.sort((a,b)=>(a.status==='pending'?0:1)-(b.status==='pending'?0:1)||b.last-a.last);
  const lab={pending:'⏳ Күтуде',approved:'✓ Сынып ашық',rejected:'✕ Қабылданбады'};
  el.innerHTML=rows.length?rows.map(r=>`<div class="item"><div class="info"><h4>${esc(r.title)}</h4><p>👨‍🏫 ${esc(r.teacher)} · ${lab[r.status]} · ${r.n} хабарлама${r.last?' · '+fmtT(r.last):''}</p></div><button class="btn ${admThread===r.tid?'btn-p':'btn-s'} btn-sm" onclick="openAdmChat('${r.tid}')">💬 Ашу</button></div>`).join(''):'<p class="sub">Чат жоқ</p>';
}
function openAdmChat(tid){admThread=tid;renderAdminThreads();renderAdminClassChat()}
function renderAdminClassChat(){
  const el=document.getElementById('admin-class-chat');if(!el)return;
  if(!admThread){el.innerHTML='';return}
  el.innerHTML=`<div style="margin-top:14px;border-top:1px solid var(--b);padding-top:12px"><div style="display:flex;justify-content:space-between;align-items:center"><h3>💬 ${esc(threadTitle(admThread))}</h3><button class="btn btn-s btn-sm" onclick="admThread=null;renderAdminThreads();renderAdminClassChat()">Жабу</button></div>${chatBoxHTML(admThread,'admin')}</div>`;
  scrollChat();
}
(function(){
  const _rt=renderTeacher;
  renderTeacher=function(){
    _rt();
    if(!user)return;
    const T=isTeacherUser(),A=!!user.isAdmin;
    const cc=document.getElementById('tch-create-card');if(cc)cc.style.display=A?'':'none';
    ['tch-req-card','tch-reqs','tch-chat'].forEach(i=>{const e=document.getElementById(i);if(e)e.style.display=(T&&!A)?'':'none'});
    if(T&&!A){renderTeacherReqs();renderTeacherChat();tickCooldown()}
  };
  const _sa=showAdmin;
  showAdmin=function(){_sa();try{renderClassReqs();renderAdminThreads();renderAdminClassChat()}catch(e){}};
  const _sc=sendChatMsg;
  sendChatMsg=function(){
    const key='support_'+threadKey(chatLogin||'');
    if(chatLogin&&!cdCheck(key))return;
    const n0=getChatMessages().length;
    _sc();
    if(getChatMessages().length>n0)cdStamp(key);
  };
})();
try{if(user&&document.getElementById('s-home').classList.contains('active'))renderHomeExtras()}catch(e){}
</script>
</body>
</html>
"""

components.html(html_code, height=950, scrolling=True)
