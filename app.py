import hashlib
import hmac
import json
import os
import re
import secrets
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

import streamlit as st
import streamlit.components.v1 as components

# ======================================================================
# Ортақ дерекқор: барлық құрылғы мен қолданушы бір деректі көреді
# ======================================================================
_HERE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.environ.get("UBT_DATA_FILE") or os.path.join(_HERE, "ubt_data.json")
FRONT_DIR = os.path.join(_HERE, "ubt_frontend")
_NO_SYNC = ("ubt_current", "ubt_dark")

_TABLE = "ubt_kv"
_PBKDF_ITER = 100_000
_MIN_PASS = 6
_SERVER_ONLY = ("ubt_admin_pass", "ubt_admin_ph")
_ADMIN_NAMES = ("админ", "admin")
_USER_TTL = 14 * 86400
_ADMIN_TTL = 12 * 3600
_USER_PREFIXES = ("ubt_mistakes_", "ubt_hist_", "ubt_prog_", "ubt_bm_", "ubt_plan_done_",
                  "ubt_plan_", "ubt_qotd_", "ubt_streak_", "ubt_avatar_", "ubt_viol_",
                  "ubt_qbank_", "ubt_qbank_hidden_", "ubt_ubt140_selection_")
_PRIVATE_PREFIXES = ("ubt_mistakes_", "ubt_plan_done_", "ubt_plan_", "ubt_bm_",
                     "ubt_qbank_", "ubt_qbank_hidden_", "ubt_ubt140_selection_")
_SINGLE_DEVICE = True
_MAX_FAILS = 5
_FAIL_WINDOW = 600


def _sb_conf():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    try:
        url = url or st.secrets.get("SUPABASE_URL")
        key = key or st.secrets.get("SUPABASE_KEY")
    except Exception:
        pass
    if url and key:
        return str(url).strip().rstrip("/"), str(key).strip()
    return None


def _secret(name):
    v = os.environ.get(name)
    if not v:
        try:
            v = st.secrets.get(name)
        except Exception:
            v = None
    return str(v) if v else None


def _sb_call(conf, method, path, body=None, prefer=None, timeout=30):
    url, key = conf
    headers = {"apikey": key, "Content-Type": "application/json"}
    if key.startswith("eyJ"):
        headers["Authorization"] = "Bearer " + key
    if prefer:
        headers["Prefer"] = prefer
    data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url + "/rest/v1/" + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
    except urllib.error.HTTPError as e:
        detail = ""
        try:
            detail = e.read().decode("utf-8", "replace")[:200]
        except Exception:
            pass
        raise RuntimeError("HTTP %s %s" % (e.code, detail))
    return json.loads(raw.decode("utf-8")) if raw else None


def _sb_load_all(conf):
    out, off, step = {}, 0, 25
    while True:
        rows = _sb_call(conf, "GET", "%s?select=key,value&order=key.asc&limit=%d&offset=%d" % (_TABLE, step, off))
        for r in rows or []:
            if isinstance(r, dict) and isinstance(r.get("key"), str) and isinstance(r.get("value"), str):
                out[r["key"]] = r["value"]
        if not rows or len(rows) < step:
            return out
        off += step


def _sb_upsert(conf, items):
    batch, size = [], 0
    for k, v in items:
        if batch and size + len(v) > 3_000_000:
            _sb_call(conf, "POST", "%s?on_conflict=key" % _TABLE, batch, prefer="resolution=merge-duplicates,return=minimal")
            batch, size = [], 0
        batch.append({"key": k, "value": v})
        size += len(v)
    if batch:
        _sb_call(conf, "POST", "%s?on_conflict=key" % _TABLE, batch, prefer="resolution=merge-duplicates,return=minimal")


def _sb_delete(conf, key):
    _sb_call(conf, "DELETE", "%s?key=eq.%s" % (_TABLE, urllib.parse.quote(key, safe="")), prefer="return=minimal")


def _hash_pw(pw, salt=None, it=_PBKDF_ITER):
    salt = salt or secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac("sha256", pw.encode("utf-8"), bytes.fromhex(salt), it)
    return {"alg": "pbkdf2_sha256", "it": it, "salt": salt, "hash": dk.hex()}


def _check_pw(pw, ph):
    try:
        dk = hashlib.pbkdf2_hmac("sha256", pw.encode("utf-8"), bytes.fromhex(ph["salt"]), int(ph["it"]))
        return hmac.compare_digest(dk.hex(), str(ph["hash"]))
    except Exception:
        return False


def _jload(raw, typ, default):
    try:
        v = json.loads(raw)
    except Exception:
        return default
    return v if isinstance(v, typ) else default


def _jdump(v):
    return json.dumps(v, ensure_ascii=False)


@st.cache_resource
def _store():
    data = {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
        for k, v in raw.items():
            data[k] = v["v"] if isinstance(v, dict) and "v" in v else v
    except Exception:
        data = {}
    state = {"db": data, "sb": _sb_conf(), "ok": False, "err": "", "dirty": set(), "deleted": set(),
             "lock": threading.RLock(), "flush_lock": threading.Lock(), "retry_t": 0.0,
             "sessions": {}, "chat_claims": {}, "fails": {}, "reg": {}}
    _remote_sync(state)
    _migrate_start(state)
    return state


def _put(state, k, v):
    state["db"][k] = v
    state["dirty"].add(k)
    state["deleted"].discard(k)


def _drop(state, k):
    state["db"].pop(k, None)
    state["dirty"].discard(k)
    state["deleted"].add(k)


def _commit(state):
    try:
        _db_save(state["db"])
    except Exception:
        pass
    _flush_async(state)


def _remote_sync(state):
    conf = state.get("sb")
    state["retry_t"] = time.time()
    if not conf:
        return
    try:
        remote = _sb_load_all(conf)
    except Exception as e:
        state["err"] = repr(e)[:200]
        return
    with state["lock"]:
        db = state["db"]
        for k, v in remote.items():
            if k not in state["dirty"] and k not in state["deleted"]:
                db[k] = v
        for k in list(db.keys()):
            if k not in remote:
                state["dirty"].add(k)
        state["ok"] = True
        state["err"] = ""
    _flush_async(state)
    _migrate_start(state)


def _flush(state):
    conf = state.get("sb")
    if not conf:
        return
    with state["flush_lock"]:
        with state["lock"]:
            items = [(k, state["db"][k]) for k in list(state["dirty"]) if k in state["db"]]
            for k in list(state["dirty"]):
                if k not in state["db"]:
                    state["dirty"].discard(k)
            dels = list(state["deleted"])
        if items:
            try:
                _sb_upsert(conf, items)
            except Exception as e:
                state["err"] = repr(e)[:200]
                return
            with state["lock"]:
                for k, v in items:
                    if state["db"].get(k) == v:
                        state["dirty"].discard(k)
                state["err"] = ""
        for k in dels:
            try:
                _sb_delete(conf, k)
            except Exception as e:
                state["err"] = repr(e)[:200]
                break
            with state["lock"]:
                state["deleted"].discard(k)


def _flush_async(state):
    threading.Thread(target=_flush, args=(state,), daemon=True).start()


def _ensure_remote(state):
    if not state.get("sb"):
        return
    if not state["ok"]:
        if time.time() - state["retry_t"] > 20:
            _remote_sync(state)
    elif state["dirty"] or state["deleted"]:
        _flush_async(state)


def _db_save(db):
    tmp = DATA_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False)
    os.replace(tmp, DATA_FILE)


def _migrate_once(state):
    with state["lock"]:
        raw = state["db"].get("ubt_profiles")
        profs = _jload(raw, dict, None) if isinstance(raw, str) else None
        todo = []
        if profs:
            for k, p in profs.items():
                if isinstance(p, dict) and "password" in p:
                    todo.append((k, p.get("password")))
    hashes = {}
    for k, pw in todo:
        if isinstance(pw, str) and pw:
            hashes[k] = (pw, _hash_pw(pw))
    changed = False
    with state["lock"]:
        raw = state["db"].get("ubt_profiles")
        profs = _jload(raw, dict, None) if isinstance(raw, str) else None
        if profs:
            for k, p in profs.items():
                if isinstance(p, dict) and "password" in p:
                    old = p.pop("password")
                    h = hashes.get(k)
                    if h and h[0] == old and not p.get("ph"):
                        p["ph"] = h[1]
                    changed = True
            if changed:
                _put(state, "ubt_profiles", _jdump(profs))
        ap = state["db"].get("ubt_admin_pass")
        if ap is not None:
            val = _jload(ap, str, "")
            if val and len(val) >= 4 and val != "admin123" and not state["db"].get("ubt_admin_ph"):
                _put(state, "ubt_admin_ph", _jdump(_hash_pw(val)))
            _drop(state, "ubt_admin_pass")
            changed = True
        if changed:
            _commit(state)
    return changed


def _migrate_start(state):
    if state.get("migrating"):
        return
    state["migrating"] = True

    def run():
        try:
            _migrate_once(state)
        except Exception as e:
            print("[ubt-sec] migration error:", repr(e)[:200])
        finally:
            state["migrating"] = False

    threading.Thread(target=run, daemon=True).start()


def _profiles(state):
    return _jload(state["db"].get("ubt_profiles", "{}"), dict, {})


def _pub_user(p):
    return {k: v for k, v in p.items() if k not in ("ph", "password")}


def _new_session(state, uid, name, admin):
    now = time.time()
    if len(state["sessions"]) > 5000:
        for t in [t for t, s in state["sessions"].items() if s["exp"] < now]:
            state["sessions"].pop(t, None)
    if _SINGLE_DEVICE and not admin:
        for t in [t for t, x in state["sessions"].items() if x.get("uid") == uid and not x.get("admin")]:
            state["sessions"].pop(t, None)
    tok = secrets.token_urlsafe(32)
    state["sessions"][tok] = {"uid": uid, "name": name, "admin": bool(admin),
                              "exp": now + (_ADMIN_TTL if admin else _USER_TTL)}
    return tok


def _session(state, tok):
    if not isinstance(tok, str) or not tok:
        return None
    s = state["sessions"].get(tok)
    if not s:
        return None
    if s["exp"] < time.time():
        state["sessions"].pop(tok, None)
        return None
    return s


def _revoke_uid(state, uid):
    for t in [t for t, s in state["sessions"].items() if s["uid"] == uid]:
        state["sessions"].pop(t, None)


def _is_teacher(state, uid):
    for p in _profiles(state).values():
        if isinstance(p, dict) and p.get("id") == uid:
            return p.get("role") == "teacher" and bool(p.get("teacherApproved"))
    return False


def _is_student(state, uid):
    return any(isinstance(p, dict) and p.get("id") == uid and p.get("role") != "teacher"
               for p in _profiles(state).values())


def _guest_chat(state, token):
    if not isinstance(token, str) or not token:
        return None
    claim = state["chat_claims"].get(token)
    if not claim:
        return None
    if claim["exp"] < time.time() or not _is_student(state, claim["uid"]):
        state["chat_claims"].pop(token, None)
        return None
    return claim


def _locked(state, key):
    now = time.time()
    lst = [t for t in state["fails"].get(key, []) if now - t < _FAIL_WINDOW]
    if lst:
        state["fails"][key] = lst
    else:
        state["fails"].pop(key, None)
    return len(lst) >= _MAX_FAILS


def _fail(state, *keys):
    if len(state["fails"]) > 20000:
        state["fails"].clear()
    for k in keys:
        state["fails"].setdefault(k, []).append(time.time())


_MSG_LOCK = "Тым көп қате әрекет. 10 минуттан кейін қайталаңыз."
_MSG_BAD = "Логин немесе пароль қате"


def _new_uid(state, key):
    ids = {p.get("id") for p in _profiles(state).values() if isinstance(p, dict)}
    while True:
        uid = "u_" + re.sub(r"[^\w]+", "_", key) + "_" + secrets.token_hex(2)
        if uid not in ids:
            return uid


def _clean_name(raw):
    name = str(raw or "").strip()
    if len(name) < 2 or len(name) > 40 or re.search(r"[\x00-\x1f<>]", name):
        return None
    return name


def _handle_req(state, sid, rq):
    typ = rq.get("type")
    d = rq.get("data") if isinstance(rq.get("data"), dict) else {}
    sess = _session(state, rq.get("tok"))

    if typ == "login":
        name = str(d.get("name") or "").strip()[:60]
        pw = str(d.get("pass") or "")[:200]
        if not name:
            return {"ok": False, "msg": "Логин жазыңыз"}
        key = name.lower()
        lk, sk = "u:" + key, "s:" + sid
        with state["lock"]:
            if _locked(state, lk) or _locked(state, sk):
                return {"ok": False, "msg": _MSG_LOCK}
            prof = _profiles(state).get(key) if key not in _ADMIN_NAMES else None
            admin_ph = _jload(state["db"].get("ubt_admin_ph", ""), dict, None)
        if key in _ADMIN_NAMES:
            sec = _secret("ADMIN_PASSWORD")
            if sec:
                r = hmac.compare_digest(pw.encode("utf-8"), sec.encode("utf-8"))
            elif admin_ph:
                r = _check_pw(pw, admin_ph)
            else:
                return {"ok": False, "msg": "Админ паролі әлі орнатылмаған. Streamlit Secrets ішіне ADMIN_PASSWORD қосыңыз."}
            with state["lock"]:
                if not r:
                    _fail(state, lk, sk)
                    return {"ok": False, "msg": _MSG_BAD}
                state["fails"].pop(lk, None)
                tok = _new_session(state, "admin", "Админ", True)
            return {"ok": True, "token": tok, "user": {"name": "Админ", "id": "admin", "isAdmin": True}}
        if not isinstance(prof, dict):
            _check_pw(pw, {"salt": "00", "it": _PBKDF_ITER, "hash": ""})
            with state["lock"]:
                _fail(state, lk, sk)
            return {"ok": False, "msg": _MSG_BAD}
        ph = prof.get("ph")
        if isinstance(ph, dict):
            good = _check_pw(pw, ph)
        elif isinstance(prof.get("password"), str) and prof["password"]:
            good = hmac.compare_digest(pw.encode("utf-8"), prof["password"].encode("utf-8"))
        else:
            return {"ok": False, "msg": "Бұл аккаунтқа пароль орнатылмаған."}
        with state["lock"]:
            if not good:
                _fail(state, lk, sk)
                return {"ok": False, "msg": _MSG_BAD}
            state["fails"].pop(lk, None)
            tok = _new_session(state, prof.get("id"), prof.get("name") or name, False)
        return {"ok": True, "token": tok, "user": _pub_user(prof)}

    if typ == "register":
        name = _clean_name(d.get("name"))
        pw = str(d.get("pass") or "")[:200]
        if not name:
            return {"ok": False, "msg": "Атыңызды жазыңыз (2-40 таңба)"}
        if len(pw) < _MIN_PASS:
            return {"ok": False, "msg": "Пароль кемінде %d таңба болсын" % _MIN_PASS}
        key = name.lower()
        now = time.time()
        ph_new = _hash_pw(pw)
        with state["lock"]:
            lst = [t for t in state["reg"].get(sid, []) if now - t < 3600]
            state["reg"][sid] = lst
            if len(lst) >= 10:
                return {"ok": False, "msg": "Тым көп тіркелу әрекеті."}
            profs = _profiles(state)
            if key in _ADMIN_NAMES or key in profs:
                return {"ok": False, "msg": "Бұл ат тіркелген."}
            if len(profs) >= 20000:
                return {"ok": False, "msg": "Тіркелу уақытша жабық"}
            uid = _new_uid(state, key)
            prof = {"name": name, "id": uid, "isAdmin": False, "ph": ph_new}
            if d.get("teacher"):
                prof["role"] = "teacher"
                prof["teacherApproved"] = False
                prof["teacherInfo"] = str(d.get("info") or "")[:200]
            profs[key] = prof
            _put(state, "ubt_profiles", _jdump(profs))
            stats = _jload(state["db"].get("ubt_user_stats", "{}"), dict, {})
            stats[uid] = {"points": 0, "title": "", "stars": 0, "verified": False}
            _put(state, "ubt_user_stats", _jdump(stats))
            lst.append(now)
            _commit(state)
        return {"ok": True}

    if typ == "resume":
        with state["lock"]:
            if not sess:
                return {"ok": False, "msg": "expired"}
            tok = rq.get("tok")
            if sess["admin"]:
                return {"ok": True, "token": tok, "user": {"name": "Админ", "id": "admin", "isAdmin": True}}
            for p in _profiles(state).values():
                if isinstance(p, dict) and p.get("id") == sess["uid"]:
                    return {"ok": True, "token": tok, "user": _pub_user(p)}
            state["sessions"].pop(tok, None)
            return {"ok": False, "msg": "expired"}

    if typ == "logout":
        with state["lock"]:
            state["sessions"].pop(rq.get("tok"), None)
        return {"ok": True}

    if typ == "chat_claim":
        login = str(d.get("login") or "").strip()[:60]
        with state["lock"]:
            if sess and not sess["admin"] and _is_student(state, sess["uid"]):
                return {"ok": True, "login": sess["name"]}
            prof = _profiles(state).get(login.lower())
            if not isinstance(prof, dict) or prof.get("role") == "teacher":
                return {"ok": False, "msg": "Мұндай оқушы логині тіркелмеген."}
            if len(state["chat_claims"]) > 5000:
                state["chat_claims"] = {k: c for k, c in state["chat_claims"].items() if c["exp"] > time.time()}
            token = secrets.token_urlsafe(32)
            messages = _jload(state["db"].get("ubt_chat", "[]"), list, [])
            state["chat_claims"][token] = {"name": prof["name"], "uid": prof["id"],
                                            "exp": time.time() + 3600, "start": len(messages)}
        return {"ok": True, "login": prof["name"], "chatToken": token}

    if typ == "admin_setpass":
        if not (sess and sess["admin"]):
            return {"ok": False, "msg": "Рұқсат жоқ"}
        pw = str(d.get("pass") or "")[:200]
        uid = str(d.get("uid") or "")
        if len(pw) < _MIN_PASS:
            return {"ok": False, "msg": "Пароль кемінде %d таңба болсын" % _MIN_PASS}
        ph_new = _hash_pw(pw)
        with state["lock"]:
            profs = _profiles(state)
            hit = False
            for p in profs.values():
                if isinstance(p, dict) and p.get("id") == uid:
                    p["ph"] = ph_new
                    p.pop("password", None)
                    hit = True
            if not hit:
                return {"ok": False, "msg": "Қолданушы табылмады"}
            _put(state, "ubt_profiles", _jdump(profs))
            _revoke_uid(state, uid)
            _commit(state)
        return {"ok": True}

    if typ == "admin_deluser":
        if not (sess and sess["admin"]):
            return {"ok": False, "msg": "Рұқсат жоқ"}
        uid = str(d.get("uid") or "")
        if not uid or uid == "admin":
            return {"ok": False, "msg": "Қате"}
        with state["lock"]:
            profs = _profiles(state)
            for k in [k for k, p in profs.items() if isinstance(p, dict) and p.get("id") == uid]:
                profs.pop(k, None)
            _put(state, "ubt_profiles", _jdump(profs))
            stats = _jload(state["db"].get("ubt_user_stats", "{}"), dict, {})
            stats.pop(uid, None)
            _put(state, "ubt_user_stats", _jdump(stats))
            tests = _jload(state["db"].get("ubt_tests", "[]"), list, [])
            _put(state, "ubt_tests", _jdump([t for t in tests if not (isinstance(t, dict) and t.get("authorId") == uid)]))
            schs = _jload(state["db"].get("ubt_schemes", "[]"), list, [])
            _put(state, "ubt_schemes", _jdump([t for t in schs if not (isinstance(t, dict) and t.get("authorId") == uid)]))
            _revoke_uid(state, uid)
            _commit(state)
        return {"ok": True}

    return {"ok": False, "msg": "Белгісіз сұраныс"}


def _process_reqs(state, sid, reqs):
    if not isinstance(reqs, list):
        return False
    done = st.session_state.setdefault("_ubt_reqdone", {})
    out = st.session_state.setdefault("_ubt_authres", {}).setdefault(sid, {})
    last = done.get(sid, 0)
    new = False
    valid = [r for r in reqs if isinstance(r, dict) and isinstance(r.get("id"), int)]
    for rq in sorted(valid, key=lambda r: r["id"])[:10]:
        if rq["id"] <= last:
            continue
        try:
            r = _handle_req(state, sid, rq)
        except Exception as e:
            print("[ubt-sec] request error:", repr(e)[:200])
            r = {"ok": False, "msg": "Сервер қатесі."}
        out[str(rq["id"])] = r
        last = rq["id"]
        new = True
    for k in sorted(out, key=int)[:-20]:
        out.pop(k, None)
    done[sid] = last
    return new


def _merge_chat(state, sess, v, chat_token=""):
    claim = None if sess else _guest_chat(state, chat_token)
    if not sess and not claim:
        return None
    inc = _jload(v, list, None)
    if inc is None:
        return None
    if sess and sess["admin"]:
        return _jdump([m for m in inc if isinstance(m, dict)])
    if sess and not _is_student(state, sess["uid"]):
        return None
    stored = _jload(state["db"].get("ubt_chat", "[]"), list, [])
    ids = {m.get("id") for m in stored if isinstance(m, dict)}
    add = []
    for m in inc:
        if not isinstance(m, dict) or m.get("role") != "user":
            continue
        mid, text = m.get("id"), m.get("text")
        if not isinstance(mid, str) or not mid or len(mid) > 60 or mid in ids:
            continue
        if not isinstance(text, str) or not text.strip() or len(text) > 2000:
            continue
        frm = sess["name"] if sess else claim["name"]
        add.append({"id": mid, "from": frm, "thread": frm.strip().lower(), "text": text, "role": "user",
                    "time": str(m.get("time") or "")[:40], "read": False})
        ids.add(mid)
        if len(add) >= 20:
            break
    if not add:
        return None
    return _jdump(stored + add)


def _merge_profiles(state, sess, v):
    inc = _jload(v, dict, None)
    if inc is None:
        return None
    stored = _profiles(state)
    out = dict(stored)
    admin = sess["admin"]
    for k, p in inc.items():
        if not isinstance(k, str) or not isinstance(p, dict):
            continue
        s = stored.get(k)
        if not isinstance(s, dict):
            if admin:
                n = {kk: vv for kk, vv in p.items() if kk not in ("password", "ph")}
                n["isAdmin"] = False
                out[k] = n
            continue
        if not admin and s.get("id") != sess["uid"]:
            continue
        n = {kk: vv for kk, vv in p.items() if kk not in ("password", "ph")}
        n["id"], n["name"], n["isAdmin"] = s.get("id"), s.get("name"), False
        if s.get("ph"):
            n["ph"] = s["ph"]
        elif s.get("password"):
            n["password"] = s["password"]
        if not admin:
            if s.get("teacherApproved"):
                for f in ("role", "teacherApproved", "teacherInfo"):
                    if f in s:
                        n[f] = s[f]
                    else:
                        n.pop(f, None)
            elif n.get("role") == "teacher":
                n["teacherApproved"] = False
                n["teacherInfo"] = str(n.get("teacherInfo") or "")[:200]
            else:
                n.pop("role", None)
                n.pop("teacherApproved", None)
        out[k] = n
    return _jdump(out)


def _merge_stats(state, sess, v):
    inc = _jload(v, dict, None)
    if inc is None:
        return None
    stored = _jload(state["db"].get("ubt_user_stats", "{}"), dict, {})
    out = dict(stored)
    if sess["admin"]:
        for uid, s in inc.items():
            if isinstance(s, dict):
                out[str(uid)] = s
        return _jdump(out)
    uid = sess["uid"]
    s = inc.get(uid)
    if not isinstance(s, dict):
        return None
    old = stored.get(uid) if isinstance(stored.get(uid), dict) else {}
    n = dict(s)
    n["title"] = old.get("title", "")
    n["stars"] = old.get("stars", 0)
    n["verified"] = bool(old.get("verified", False))
    try:
        n["points"] = max(0, int(n.get("points") or 0))
    except Exception:
        n["points"] = int(old.get("points", 0) or 0)
    out[uid] = n
    return _jdump(out)


def _merge_tests(state, sess, v):
    inc = _jload(v, list, None)
    if inc is None:
        return None
    if sess["admin"]:
        return _jdump([t for t in inc if isinstance(t, dict)])
    stored = _jload(state["db"].get("ubt_tests", "[]"), list, [])
    sby = {t.get("id"): t for t in stored if isinstance(t, dict)}
    uid = sess["uid"]
    teacher = _is_teacher(state, uid)
    out, seen = [], set()
    for t in inc:
        if not isinstance(t, dict) or not isinstance(t.get("id"), str):
            continue
        tid = t["id"]
        seen.add(tid)
        s = sby.get(tid)
        if s is not None:
            if s.get("authorId") != uid:
                out.append(s)
                continue
            n = dict(t)
            n["authorId"] = uid
            n["adminApproved"] = (bool(s.get("adminApproved"))
                                  and n.get("subject") == s.get("subject")
                                  and n.get("questions") == s.get("questions"))
            if not teacher:
                n["isPublic"] = bool(s.get("isPublic"))
                if s.get("status") != "approved" and not s.get("isPublic") and t.get("status") in ("pending", "private"):
                    n["status"] = t["status"]
                elif "status" in s:
                    n["status"] = s["status"]
                else:
                    n.pop("status", None)
            out.append(n)
        elif tid == "seed_funksiya" and t.get("authorId") == "system":
            n = dict(t)
            n["adminApproved"] = False
            out.append(n)
        else:
            n = dict(t)
            n["authorId"] = uid
            n["adminApproved"] = False
            if not teacher:
                n["isPublic"] = False
                if n.get("status") not in ("pending", "private"):
                    n["status"] = "private"
            out.append(n)
    for s in stored:
        if isinstance(s, dict) and s.get("id") not in seen and s.get("authorId") != uid:
            out.append(s)
    return _jdump(out)


_SCH_CONTENT = ("subject", "title", "tabMain", "subs", "theme", "root", "kids")
_SCH_MAX_ONE = 700_000
_SCH_MAX_ALL = 7_000_000
_SCH_MAX_PER_USER = 30


def _merge_schemes(state, sess, v):
    inc = _jload(v, list, None)
    if inc is None:
        return None
    if sess["admin"]:
        out = [t for t in inc if isinstance(t, dict) and isinstance(t.get("id"), str)]
        return _jdump(out) if len(_jdump(out)) < _SCH_MAX_ALL else None
    stored = _jload(state["db"].get("ubt_schemes", "[]"), list, [])
    sby = {t.get("id"): t for t in stored if isinstance(t, dict)}
    uid = sess["uid"]
    out, seen, mine = [], set(), 0
    for t in inc:
        if not isinstance(t, dict) or not isinstance(t.get("id"), str) or len(t["id"]) > 60:
            continue
        tid = t["id"]
        if tid in seen:
            continue
        seen.add(tid)
        s0 = sby.get(tid)
        if s0 is not None and s0.get("authorId") != uid:
            out.append(s0)
            continue
        if len(_jdump(t)) > _SCH_MAX_ONE:
            if s0 is not None:
                out.append(s0)
            continue
        mine += 1
        if mine > _SCH_MAX_PER_USER and s0 is None:
            continue
        n = dict(t)
        n["authorId"] = uid
        if s0 is not None:
            was_ok = s0.get("status") == "approved" and bool(s0.get("isPublic"))
            changed = any(n.get(k) != s0.get(k) for k in _SCH_CONTENT)
            if was_ok and not changed:
                n["status"], n["isPublic"] = "approved", True
            elif was_ok and changed:
                n["status"], n["isPublic"] = "pending", False
            else:
                n["isPublic"] = False
                n["status"] = n.get("status") if n.get("status") in ("pending", "private") else (
                    s0.get("status") if s0.get("status") in ("rejected",) and not changed else "private")
        else:
            n["isPublic"] = False
            n["status"] = n.get("status") if n.get("status") in ("pending", "private") else "private"
        out.append(n)
    for s0 in stored:
        if isinstance(s0, dict) and s0.get("id") not in seen and s0.get("authorId") != uid:
            out.append(s0)
    res = _jdump(out)
    return res if len(res) < _SCH_MAX_ALL else None


def _authorize(state, sess, k, v, chat_token=""):
    if k == "ubt_chat":
        return _merge_chat(state, sess, v, chat_token)
    if not sess:
        return None
    if k == "ubt_profiles":
        return _merge_profiles(state, sess, v)
    if k == "ubt_user_stats":
        return _merge_stats(state, sess, v)
    if k == "ubt_tests":
        return _merge_tests(state, sess, v)
    if k == "ubt_schemes":
        return _merge_schemes(state, sess, v)
    if k == "ubt_lessons":
        if not sess["admin"]:
            return None
        lst = _jload(v, list, None)
        if lst is None:
            return None
        res = _jdump([t for t in lst if isinstance(t, dict) and isinstance(t.get("id"), str)])
        return res if len(res) < 6_000_000 else None
    if k != "ubt_qotd_day" and any(k.startswith(p) for p in _USER_PREFIXES):
        if sess["admin"] or any(k == p + sess["uid"] for p in _USER_PREFIXES):
            return v
        return None
    return v


def _key_ok(k):
    return (isinstance(k, str) and k.startswith("ubt_") and len(k) < 200
            and k not in _NO_SYNC and k not in _SERVER_ONLY and not k.startswith("ubt_cd_"))


def _apply_ops(res):
    state = _store()
    _ensure_remote(state)
    if not isinstance(res, dict):
        return False
    sid = res.get("sid")
    ops = res.get("ops")
    if not isinstance(sid, str) or not isinstance(ops, list) or len(sid) > 40:
        return False
    new_req = _process_reqs(state, sid, res.get("reqs"))
    acks = st.session_state.setdefault("_ubt_ack", {})
    last = acks.get(sid, 0)
    changed = False
    with state["lock"]:
        db = state["db"]
        for op in sorted((o for o in ops if isinstance(o, dict)), key=lambda o: o.get("n", 0)):
            n = op.get("n", 0)
            if not isinstance(n, int) or n <= last:
                continue
            k, v = op.get("key"), op.get("value")
            if _key_ok(k) and isinstance(v, str) and len(v) < 8_000_000:
                nv = _authorize(state, _session(state, op.get("tok")), k, v, op.get("chat_tok"))
                if nv is None:
                    print("[ubt-sec] write rejected:", k[:60])
                elif db.get(k) != nv:
                    db[k] = nv
                    state["dirty"].add(k)
                    state["deleted"].discard(k)
                    changed = True
            last = n
        if changed:
            try:
                _db_save(db)
            except Exception:
                pass
    if changed:
        _flush_async(state)
    new = last > acks.get(sid, 0) or new_req
    acks[sid] = last
    return new


def _chat_for(raw, sess, claim, state):
    if sess and sess["admin"]:
        return raw if isinstance(raw, str) else "[]"
    guest = None if sess else _guest_chat(state, claim)
    if not sess and not guest:
        return "[]"
    key = (sess["name"] if sess else guest["name"]).strip().lower()
    if not key:
        return "[]"
    out = []
    messages = _jload(raw, list, []) if isinstance(raw, str) else []
    for m in (messages[guest["start"]:] if guest else messages):
        if not isinstance(m, dict):
            continue
        who = m.get("to") if m.get("role") == "admin" else m.get("from")
        if str(who or "").strip().lower() == key:
            out.append(m)
    return _jdump(out)


def _snapshot(tok="", claim=""):
    state = _store()
    with state["lock"]:
        db = dict(state["db"])
        sess = _session(state, tok)
        profs = _profiles(state) if sess else {}
        teacher = bool(sess and not sess["admin"] and _is_teacher(state, sess["uid"]))
    for k in _SERVER_ONLY:
        db.pop(k, None)
    with state["lock"]:
        chat = _chat_for(db.get("ubt_chat"), sess, claim, state)
    if not sess:
        return {"ubt_chat": chat}
    db["ubt_chat"] = chat
    if "ubt_profiles" in db:
        db["ubt_profiles"] = _jdump({k: _pub_user(p) for k, p in profs.items() if isinstance(p, dict)})
    if not sess["admin"] and "ubt_schemes" in db:
        sch = _jload(db.get("ubt_schemes"), list, [])
        db["ubt_schemes"] = _jdump([t for t in sch if isinstance(t, dict) and (
            t.get("authorId") == sess["uid"] or (t.get("status") == "approved" and t.get("isPublic")))])
    if not sess["admin"]:
        for k in list(db.keys()):
            if k.startswith(_PRIVATE_PREFIXES) and not (k.endswith(sess["uid"]) and any(k == p + sess["uid"] for p in _PRIVATE_PREFIXES)):
                if teacher and k.startswith("ubt_mistakes_"):
                    continue
                db.pop(k, None)
    return db


st.set_page_config(page_title="ҰБТ+", page_icon="📘", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""<style>
#MainMenu,footer,header{visibility:hidden}
</style>
<style id="ubt-manage-css">
[data-testid="manage-app-button"],[class*="_terminalButton_"],[class*="_viewerBadge_"],[class*="viewerBadge"],[class*="_profileContainer_"],.stAppDeployButton,[data-testid="stToolbar"],[data-testid="stDecoration"],[data-testid="stStatusWidget"]{display:none!important}
html,body,.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"],section.main{margin:0!important;padding:0!important}
[data-testid="stHeader"],[data-testid="stAppHeader"]{display:none!important;height:0!important}
.block-container,[data-testid="stMainBlockContainer"],[data-testid="stAppViewBlockContainer"]{padding:0!important;max-width:100%!important;margin:0!important}
[data-testid="stElementContainer"]{margin:0!important}
[data-testid="stVerticalBlock"]{gap:0!important}
iframe{border:none!important;display:block!important;width:100%!important}
</style>""", unsafe_allow_html=True)

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
:root{--vh:800px}
body{font-family:'Inter',system-ui,sans-serif;background:var(--bg);color:var(--t);min-height:var(--vh);line-height:1.5}
html,body{overflow-x:hidden}
.screen{display:none;min-height:var(--vh)}.screen.active{display:block}
.wrap{max-width:880px;margin:0 auto;padding:32px 16px 110px}
.tmain{padding-bottom:110px!important}
.topback{position:relative;z-index:60;will-change:transform;background:var(--bg);padding:8px 0;margin:-20px 0 10px;display:flex}
.topback .btn{box-shadow:0 1px 4px rgba(0,0,0,.08)}
.wrap.wide{max-width:1200px}
.hdr{text-align:center;margin-bottom:28px}
.logo{display:inline-flex;align-items:center;justify-content:center;width:72px;height:72px;background:linear-gradient(135deg,#2563eb,#7c3aed);color:#fff;font-weight:800;font-size:26px;border-radius:24px;margin-bottom:14px;box-shadow:0 8px 24px rgba(37,99,235,.35);letter-spacing:-0.5px}
.hdr h1{font-size:26px;font-weight:700;margin-bottom:4px}
.hdr h2{font-size:22px;margin-bottom:4px}
.sub{color:var(--m);font-size:14px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;padding:11px 20px;border-radius:20px;font-size:14px;font-weight:600;border:none;cursor:pointer;font-family:inherit;transition:.15s}
.btn-p{background:var(--p);color:#fff}.btn-p:hover{background:var(--pd)}.btn-p:disabled{opacity:.45;cursor:not-allowed}
.btn-s{background:var(--c);color:var(--t);border:1px solid var(--b)}.btn-s:hover{background:var(--bg)}
.btn-d{background:var(--err);color:#fff}.btn-ok{background:var(--ok);color:#fff}.btn-w{background:var(--warn);color:#1c1917}
.btn-sm{padding:7px 12px;font-size:12px}
.row{display:flex;gap:10px;flex-wrap:wrap;justify-content:center}
.card{background:var(--c);border:1px solid var(--b);border-radius:22px;padding:18px;margin-bottom:12px}
.card h3{font-size:16px;margin-bottom:6px}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.mode{background:var(--c);border:2px solid var(--b);border-radius:22px;padding:22px 14px;text-align:center;cursor:pointer;transition:.2s}
.mode:hover{border-color:var(--p);transform:translateY(-2px);box-shadow:0 6px 20px rgba(37,99,235,.1)}
.mode .ic{font-size:30px;margin-bottom:8px}
.mode h3{font-size:15px;margin-bottom:4px}
.mode p{font-size:12px;color:var(--m)}
.fg{margin-bottom:14px}
.fg label{display:block;font-size:12px;font-weight:600;color:var(--m);margin-bottom:5px}
.fg input,.fg select,.fg textarea{width:100%;padding:10px 12px;border:1px solid var(--b);border-radius:20px;font-size:14px;font-family:inherit;background:var(--bg)}
.fg textarea{min-height:72px;resize:vertical}
.opt{display:flex;gap:8px;align-items:center;margin-bottom:8px}
.opt input[type=text]{flex:1}
.opt input[type=radio]{width:18px;height:18px;accent-color:var(--p)}
.badge{display:inline-block;padding:3px 10px;border-radius:24px;font-size:11px;font-weight:600}
.badge-pub{background:#dbeafe;color:var(--p)}.badge-priv{background:#f1f5f9;color:var(--m)}
.list{display:flex;flex-direction:column;gap:10px}
.item{background:var(--c);border:1px solid var(--b);border-radius:22px;padding:14px 16px;display:flex;justify-content:space-between;align-items:center;gap:12px}
.item .info{flex:1;min-width:0}
.item .info h4{font-size:14px;margin-bottom:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.item .info p{font-size:12px;color:var(--m)}
.item .acts{display:flex;gap:6px;flex-shrink:0;flex-wrap:wrap}
.empty{text-align:center;padding:40px 16px;color:var(--m)}.empty .ic{font-size:36px;margin-bottom:10px}
.profile-bar{display:flex;justify-content:space-between;align-items:center;padding:12px 16px;background:var(--c);border-bottom:1px solid var(--b);margin-bottom:20px}
.profile-bar .name{font-weight:600;font-size:14px}
.avatar{width:36px;height:36px;border-radius:50%;background:var(--p);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px}
.tlay{display:flex;min-height:var(--vh);align-items:flex-start}
.side{width:260px;background:var(--c);border-right:1px solid var(--b);display:flex;flex-direction:column;position:relative;top:0;height:var(--vh);will-change:transform}
.side-h{padding:12px;border-bottom:1px solid var(--b);display:flex;justify-content:space-between;align-items:center;font-weight:600;font-size:13px}
.side-tog{display:none;background:none;border:none;font-size:20px;cursor:pointer}
.qnav{flex:1;overflow-y:auto;padding:8px;display:grid;grid-template-columns:repeat(5,1fr);gap:4px;align-content:start}
.qn{aspect-ratio:1;border:1px solid var(--b);border-radius:17px;background:var(--bg);font-size:11px;font-weight:500;cursor:pointer;display:flex;align-items:center;justify-content:center}
.qn.cur{border-color:var(--p);background:#dbeafe;color:var(--p);font-weight:700}
.qn.ans{background:#dcfce7;border-color:#86efac;color:var(--ok)}
.qn.flg{background:#fef3c7;border-color:#fcd34d}
.side-f{padding:12px;border-top:1px solid var(--b)}
.tmain{flex:1;padding:18px 24px;max-width:780px}
.ttop{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;flex-wrap:wrap;gap:8px}
.prog-t{font-size:14px;font-weight:700;color:var(--p);background:#eff6ff;padding:5px 12px;border-radius:24px}
.prog-w{flex:1;min-width:120px;background:#e2e8f0;border-radius:24px;height:8px;overflow:hidden}
.prog-f{height:100%;background:var(--p);border-radius:24px;transition:width .3s}
.timer{font-size:22px;font-weight:700;font-variant-numeric:tabular-nums;color:var(--p);background:#eff6ff;padding:5px 14px;border-radius:20px}
.timer.warn{color:var(--warn);background:#fffbeb}.timer.dang{color:var(--err);background:#fef2f2;animation:pulse 1s infinite}
@keyframes pulse{50%{opacity:.7}}
.qc{background:var(--c);border-radius:22px;padding:20px;box-shadow:0 1px 3px rgba(0,0,0,.05);margin-bottom:16px}
.qh{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}
.qnum{font-size:12px;font-weight:600;color:var(--p);background:#eff6ff;padding:3px 10px;border-radius:24px}
.flag{background:none;border:1px solid var(--b);border-radius:17px;padding:4px 8px;cursor:pointer;font-size:14px}
.flag.on{background:#fef3c7;border-color:#fcd34d}
.qt{font-size:15px;margin-bottom:16px;line-height:1.6}
.qimg{display:block;max-width:100%;max-height:340px;margin:0 auto 14px;border-radius:14px;border:1px solid var(--b);object-fit:contain;background:#fff}
.qtbl-w{overflow-x:auto;margin:0 0 14px}
.qtbl{border-collapse:collapse;margin:0 auto;font-size:14px}
.qtbl td,.qtbl th{border:1px solid var(--b);padding:6px 12px;text-align:center;min-width:48px}
.qtbl tr:first-child td{background:#eff6ff;font-weight:600}
.tbed{overflow-x:auto;margin:8px 0}
.tbed table{border-collapse:collapse}
.tbed td{padding:2px}
.tbed input{width:90px;padding:6px 8px;border:1px solid var(--b);border-radius:10px;font-size:13px;font-family:inherit;background:var(--bg)}
.aq-prev{max-width:240px;max-height:180px;border-radius:12px;border:1px solid var(--b);display:block;margin-top:8px}

.sch-bg{background:linear-gradient(180deg,#f8f3ea,#f3ebdd);border-radius:26px;padding:22px 14px 28px;border:1px solid #eadfcb;--sc:#3d7396}
.sch-bg h2.sch-h{text-align:center;font-size:24px;font-weight:700;margin-bottom:14px;color:#222}
.sch-tab{display:flex;justify-content:center}
.sch-tab span{background:#fff;padding:10px 38px;border-radius:24px 24px 0 0;font-size:20px;border-bottom:3px solid var(--sc);box-shadow:0
