import os, json, re, time, secrets, hashlib, hmac, base64, binascii, threading, tempfile, pathlib, math, datetime, urllib.request, urllib.error, urllib.parse, random, io, sqlite3, collections
import streamlit as st
import streamlit.components.v1 as components

_HERE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.environ.get('UBT_FILES_DATA_FILE', os.path.join(_HERE,'ubt_files_data.json'))
_TABLE = 'ubt_kv'
_PREFIX = 'ubt_files_v2_'
_META = _PREFIX+'index'
_PBKDF_ITER = 200_000
SUBJECTS = {'history':'Қазақстан тарихы','reading':'Оқу сауаттылығы','mathlit':'Математикалық сауаттылық','math':'Математика','informatics':'Информатика'}
PROFILE = ('math','informatics')
ADMIN_RESET_HASH = {'alg': 'pbkdf2_sha256', 'it': 200000, 'salt': '12773753ee064c80753573fe1986df77', 'hash': '89e00cb8fe4ae7f7573ddd48373efae2a0ff588ce83047f881ee1974355f4c98'}
ADMIN_RESET_TAG = 'password-only-20261118-2'
MAX_UPLOAD = 1024**3
CHUNK = 768*1024
def _jdump(v): return json.dumps(v,ensure_ascii=False,separators=(',',':'))
def _hash_pw(pw,salt=None,it=_PBKDF_ITER):
    salt=salt or secrets.token_hex(16)
    return {'alg':'pbkdf2_sha256','it':it,'salt':salt,'hash':hashlib.pbkdf2_hmac('sha256',pw.encode(),bytes.fromhex(salt),it).hex()}
def _check_pw(pw,ph):
    try: return hmac.compare_digest(hashlib.pbkdf2_hmac('sha256',pw.encode(),bytes.fromhex(ph['salt']),int(ph['it'])).hex(),ph['hash'])
    except (ValueError,TypeError,KeyError): return False
def _setting(name):
    try: return os.environ.get(name) or st.secrets.get(name)
    except Exception:return os.environ.get(name)
def _sb_conf():
    url,key=_setting('SUPABASE_URL'),_setting('SUPABASE_KEY')
    if not url and not key:return None
    if not url or not key:raise RuntimeError('SUPABASE_URL және SUPABASE_KEY бірге көрсетілсін')
    privileged=key.startswith('sb_secret_')
    if key.startswith('eyJ'):
        try:privileged=json.loads(base64.urlsafe_b64decode(key.split('.')[1]+'===')) .get('role')=='service_role'
        except Exception:pass
    if not privileged:raise RuntimeError('SUPABASE_KEY серверлік secret/service_role кілті болсын')
    return (url.rstrip('/'),key)
def _sb_call(conf,method,path,body=None):
    url,key=conf;headers={'apikey':key,'Content-Type':'application/json','Prefer':'resolution=merge-duplicates,return=minimal'}
    if key.startswith('eyJ'):headers['Authorization']='Bearer '+key
    req=urllib.request.Request(url+'/rest/v1/'+path,data=_jdump(body).encode()if body is not None else None,headers=headers,method=method)
    with urllib.request.urlopen(req,timeout=45)as r:
        raw=r.read();return json.loads(raw)if raw else None
class Repository:
    """SQLite locally, existing Supabase KV remotely; question payloads never accumulate in RAM."""
    def __init__(self,path,conf=None):
        self.path=path;self.conf=conf;self.cache=collections.OrderedDict();self.lock=threading.RLock()
        self.sqlpath=path+'.sqlite3'
        if not conf:
            os.makedirs(os.path.dirname(path)or'.',exist_ok=True)
            with self.connect()as db:
                db.execute('CREATE TABLE IF NOT EXISTS kv (key TEXT PRIMARY KEY,value TEXT NOT NULL)')
                empty=db.execute('SELECT COUNT(*) FROM kv').fetchone()[0]==0
                if empty and os.path.exists(path):
                    legacy=json.loads(pathlib.Path(path).read_text())
                    db.executemany('INSERT INTO kv VALUES (?,?)',((k,_jdump(v))for k,v in legacy.items()))
    def connect(self):
        db=sqlite3.connect(self.sqlpath,timeout=60)
        db.execute('PRAGMA journal_mode=WAL');return db
    def get(self,key,default=None,fresh=False):
        if not fresh and key in self.cache:
            value=self.cache.pop(key);self.cache[key]=value;return value
        if self.conf:
            rows=_sb_call(self.conf,'GET',_TABLE+'?select=value&key=eq.'+urllib.parse.quote(key,safe=''))
            if not rows:return default
            raw=rows[0]['value']
        else:
            with self.connect()as db:row=db.execute('SELECT value FROM kv WHERE key=?',(key,)).fetchone()
            if not row:return default
            raw=row[0]
        try:value=json.loads(raw)if isinstance(raw,str)else raw
        except ValueError:value=raw
        if key.startswith(_PREFIX+'file_'):
            self.cache[key]=value
            while len(self.cache)>4:self.cache.popitem(last=False)
        return value
    def write(self,changes):
        if self.conf:
            batch=[];size=0
            for k,v in changes.items():
                raw=_jdump(v)
                if batch and size+len(raw)>1_800_000:_sb_call(self.conf,'POST',_TABLE+'?on_conflict=key',batch);batch=[];size=0
                batch.append({'key':k,'value':raw});size+=len(raw)
            if batch:_sb_call(self.conf,'POST',_TABLE+'?on_conflict=key',batch)
        else:
            with self.connect()as db:
                db.executemany('INSERT INTO kv(key,value) VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value',((k,_jdump(v))for k,v in changes.items()))
        for k in changes:self.cache.pop(k,None)
    def index(self):return json.loads(_jdump(self.get(_META,{},fresh=True)))
    def save_index(self,meta):
        meta['revision']=meta.get('revision',0)+1;self.write({_META:meta})

def _legacy(repo,key,default):
    if repo.conf:return repo.get(key,default,fresh=True)
    try:
        raw=json.loads(pathlib.Path(os.environ.get('UBT_DATA_FILE',os.path.join(_HERE,'ubt_data.json'))).read_text()).get(key,default)
        raw=raw.get('v',raw)if isinstance(raw,dict)else raw
        if isinstance(raw,str):
            try:return json.loads(raw)
            except ValueError:return raw
        return raw
    except (OSError,ValueError):return default
def initialise(repo):
    if repo.index():return
    admin_ph=_legacy(repo,'ubt_admin_ph',None)
    if not admin_ph:
        pw=_setting('ADMIN_PASSWORD')or _legacy(repo,'ubt_admin_pass',None)
        admin_ph=_hash_pw(pw)if isinstance(pw,str)and len(pw)>=10 else dict(ADMIN_RESET_HASH)
    users={'admin':{'id':'admin','login':'admin','name':'Админ','ph':admin_ph}}
    for login,p in _legacy(repo,'ubt_profiles',{}).items():
        if not isinstance(p,dict)or p.get('accessApproved')is False or login.casefold()in('admin','админ'):continue
        ph=p.get('ph')
        if not ph and isinstance(p.get('password'),str):ph=_hash_pw(p['password'])
        if ph and p.get('id'):
            users[login.casefold()]={'id':p['id'],'login':login,'name':p.get('name',login),'ph':ph}
    repo.save_index({'version':2,'revision':0,'users':users,'folders':{},'files':{}})
def _password_stamp(ph):
    return hashlib.sha256(_jdump(ph).encode()).hexdigest()
def _apply_admin_reset(repo):
    meta=repo.index()
    if meta.get('admin_reset_tag')==ADMIN_RESET_TAG:return
    meta['users']['admin']['ph']=dict(ADMIN_RESET_HASH)
    meta['admin_reset_tag']=ADMIN_RESET_TAG
    repo.save_index(meta)
def _chrome_css(manage=False,dark=False):
    bg='#0d1424'if dark else'#f1f5f9'
    chrome='[data-testid="manage-app-button"],[data-testid*="manage-app"],[data-testid*="manageApp"],[aria-label*="Manage app" i],[title*="Manage app" i],[class*="_terminalButton_"],[class*="_viewerBadge_"],[class*="viewerBadge"],[class*="_profileContainer_"],.stAppDeployButton,[data-testid="stToolbar"],[data-testid="stStatusWidget"]'
    hidden=''if manage else chrome+',header[data-testid="stHeader"],footer{display:none!important}'
    return '<style>'+hidden+'html,body,.stApp,[data-testid="stAppViewContainer"]{background:'+bg+'!important}.block-container{padding:0!important;max-width:100%!important}iframe{border:0!important}</style>'
@st.cache_resource
def runtime():
    repo=Repository(DATA_FILE,_sb_conf());initialise(repo);_apply_admin_reset(repo)
    return {'repo':repo,'lock':repo.lock,'sessions':{},'fails':{},'uploads':{},'exams':{},'question_cache':{}}
def _owner(s):return bool(s and s['uid']=='admin')
def _session(rt,token):
    s=rt['sessions'].get(token)
    if s and s['expires']>time.time():
        user=next((u for u in rt['repo'].index()['users'].values()if u['id']==s['uid']),None)
        if user and hmac.compare_digest(str(s.get('stamp','')),_password_stamp(user['ph'])):
            if time.time()-s.get('log_touch',0)>45:_access_event(rt['repo'],s,'touch')
            return s
    rt['sessions'].pop(token,None);return None
def _require(s):
    if not s:raise ValueError('Алдымен аккаунтқа кіріңіз')
def _scope(s,value):
    _require(s)
    if value=='public':
        if not _owner(s):raise ValueError('Жария тесттерді тек админ басқарады')
        return 'public'
    if value=='bank':return 'bank'
    return s['uid']
def _can_read(s,row):return bool(s and row and row.get('scope')in('public','bank',s['uid']))
def _visible_meta(meta,s):
    return {'revision':meta.get('revision',0),'folders':[v for v in meta['folders'].values()if _can_read(s,v)],'files':[v for v in meta['files'].values()if _can_read(s,v)],'users':[{'id':u['id'],'name':u['name'],'login':u['login']}for u in meta['users'].values()]if _owner(s)else[]}
def _normalise(q,subject):
    if not isinstance(q,dict):raise ValueError('Сұрақ объект болуы керек')
    text=str(q.get('text')or q.get('question')or q.get('q')or'').strip()
    opts=q.get('options',q.get('answers',q.get('variants',[])))
    if isinstance(opts,dict):opts=list(opts.values())
    if not isinstance(opts,list)or not 2<=len(opts)<=8:raise ValueError('Әр сұрақта 2–8 жауап нұсқасы болуы керек')
    opts=[str(v).strip()for v in opts]
    correct=q.get('correct',q.get('answer',q.get('correctAnswer')))
    if isinstance(correct,str):
        c=correct.strip()
        if re.fullmatch('[A-Ha-h]',c):correct=ord(c.upper())-65
        elif c.isdigit():correct=int(c)
        else:correct=opts.index(c)if c in opts else None
    if type(correct)is not int or not 0<=correct<len(opts):raise ValueError('Дұрыс жауап индексі жоқ не жарамсыз (correct: 0-ден басталады)')
    if not text or len(text)>12000 or any(not v or len(v)>4000 for v in opts):raise ValueError('Сұрақ мәтінін және жауаптарын тексеріңіз')
    points=q.get('points',1)
    if type(points)not in(int,float)or not math.isfinite(points)or not 0<points<=100:raise ValueError('Ұпай жарамсыз')
    sub=q.get('subject')or subject
    aliases={'информатика':'informatics','математика':'math','матсау':'mathlit'}
    sub=aliases.get(str(sub).casefold(),sub)
    if sub not in SUBJECTS:sub=subject
    if sub not in SUBJECTS:raise ValueError('Пәнді таңдаңыз')
    out={'text':text,'options':opts,'correct':correct,'points':points,'subject':sub,'topic':str(q.get('topic')or'')[:200]}
    img=q.get('img')or q.get('image')
    if img:
        if not isinstance(img,str)or len(img)>1_500_000 or not re.fullmatch(r'data:image/(png|jpeg|webp);base64,[A-Za-z0-9+/=]+',img):raise ValueError('Сурет PNG/JPEG/WebP data URL болсын')
        try:base64.b64decode(img.split(',')[1],validate=True)
        except binascii.Error:raise ValueError('Суреттің base64 дерегі жарамсыз')
        out['img']=img
    if q.get('tbl'):
        tbl=q['tbl']
        if not isinstance(tbl,list)or len(tbl)>40 or any(not isinstance(r,list)or len(r)>15 for r in tbl):raise ValueError('Кесте жарамсыз')
        out['tbl']=[[str(c)[:2000]for c in row]for row in tbl]
    if q.get('explanation'):out['explanation']=str(q['explanation'])[:6000]
    return out
def _folder_path(meta,scope,path):
    parent=''
    for title in [s.strip()for s in path.replace('\\','/').split('/')if s.strip()]:
        if len(title)>120:raise ValueError('Бөлім атауы 120 таңбадан аспасын')
        found=next((f for f in meta['folders'].values()if f['scope']==scope and f['parent']==parent and f['title']==title),None)
        if found:parent=found['id']
        else:
            ident=secrets.token_hex(12);meta['folders'][ident]={'id':ident,'title':title,'scope':scope,'parent':parent};parent=ident
        if sum(1 for c in path.split('/')if c.strip())>8:raise ValueError('Бөлімдер 8 деңгейден аспасын')
    return parent
def _groups(data,title,path=''):
    if isinstance(data,list):
        if not data:raise ValueError('JSON тізімі бос')
        if all(isinstance(q,dict)and any(k in q for k in ('text','question','q'))for q in data):yield title,path,iter(data);return
        for i,child in enumerate(data,1):yield from _groups(child,f'{title}.{i}',path)
    elif isinstance(data,dict):
        name=str(data.get('title')or data.get('topic')or data.get('name')or title)[:160]
        if isinstance(data.get('questions'),list):yield name,path,iter(data['questions']);return
        nested=next((data[k]for k in ('tests','files','children','items')if isinstance(data.get(k),list)),None)
        if nested is None:raise ValueError('JSON ішінде questions тізімі болуы керек')
        nested_path='/'.join([v for v in (path,name)if v])
        for i,child in enumerate(nested,1):yield from _groups(child,f'{i}',nested_path)
    else:raise ValueError('JSON форматы жарамсыз')
def _store_group(repo,rt,rows,title,subject,scope,parent,progress=None):
    ident=secrets.token_hex(16);parts=[];block=[];bytes_n=0;counts={};n=0
    def flush():
        nonlocal block,bytes_n
        if not block:return
        key=_PREFIX+'file_'+ident+'_'+str(len(parts));repo.write({key:block})
        parts.append({'key':key,'start':n-len(block),'count':len(block)});block=[];bytes_n=0
        if progress:progress(n)
    for q in rows:
        q=_normalise(q,subject);size=len(_jdump(q).encode())
        if block and (bytes_n+size>1_800_000 or len(block)>=100):flush()
        block.append(q);bytes_n+=size;n+=1;counts[q['subject']]=counts.get(q['subject'],0)+1

    flush()
    if not n:raise ValueError('Файлда сұрақ жоқ')
    return {'id':ident,'title':title[:160],'subject':subject,'scope':scope,'folder':parent,'count':n,'subjects':counts,'parts':parts,'created':time.time()}
def _rows(repo,file):
    for part in file['parts']:
        rows=repo.get(part['key'])
        if not isinstance(rows,list)or len(rows)!=part['count']:raise ValueError('Файл деректері толық емес')
        yield from rows
def _question(repo,file,index):
    if type(index)is not int or not 0<=index<file['count']:raise ValueError('Сұрақ нөмірі жарамсыз')
    part=next(p for p in file['parts']if p['start']<=index<p['start']+p['count'])
    return repo.get(part['key'])[index-part['start']]
def _safe_q(q):
    return {k:v for k,v in q.items()if k not in('correct','explanation')}
def _files_in_folder(meta,s,folder,scope):
    if folder:
        f=meta['folders'].get(folder)
        if not _can_read(s,f):raise ValueError('Бөлімге рұқсат жоқ')
        scope=f['scope']
    elif scope not in ('public','bank'):scope=s['uid']
    wanted={folder};changed=True
    while changed:
        added={f['id']for f in meta['folders'].values()if f['scope']==scope and f['parent']in wanted}-wanted
        changed=bool(added);wanted|=added
    return sorted([f for f in meta['files'].values()if f['scope']==scope and f['folder']in wanted and _can_read(s,f)],key=lambda f:(f['created'],f['id']))
def _exam_info(exam):
    return {k:exam[k]for k in ('id','title','count','max','deadline','sections','answers')}
def _start(rt,s,d):
    repo=rt['repo'];meta=repo.index();refs=[];sections=[]
    if d.get('mode')=='140':
        pools={k:[]for k in SUBJECTS}
        # Only the administrator's published bank supplies the common 140 exam.
        for file in meta['files'].values():
            if file['scope']not in('public','bank'):continue
            for i,q in enumerate(_rows(repo,file)):pools[q['subject']].append((file['id'],i))
        spec=[('history',20),('reading',10),('mathlit',10),('math',40),('informatics',40)]
        missing=[f'{SUBJECTS[k]}: {len(pools[k])}/{n}'for k,n in spec if len(pools[k])<n]
        if missing:raise ValueError('140 форматқа сұрақ жеткіліксіз: '+'; '.join(missing))
        rng=secrets.SystemRandom()
        for sub,n in spec:
            start=len(refs);chosen=rng.sample(pools[sub],n)
            for j,(fid,index)in enumerate(chosen):refs.append({'file':fid,'index':index,'points':2 if n==40 and j>=30 else 1,'subject':sub})
            sections.append({'title':SUBJECTS[sub],'start':start,'count':n})
        title='140 формат · Инфо–мат';seconds=240*60
    elif d.get('mode')=='subject':
        sub=d.get('subject')
        if sub not in SUBJECTS:raise ValueError('Пәнді таңдаңыз')
        pool=[]
        for file in meta['files'].values():
            if file['scope']not in('public','bank'):continue
            for i,q in enumerate(_rows(repo,file)):
                if q['subject']==sub:pool.append({'file':file['id'],'index':i,'points':q['points'],'subject':sub})
        amount=d.get('count',20)
        if amount=='all':amount=len(pool)
        if type(amount)is not int or not 1<=amount<=20000:raise ValueError('Сұрақ саны 1–20 000 болсын')
        if len(pool)<amount:raise ValueError('Бұл пәнде '+str(len(pool))+' сұрақ бар')
        refs=secrets.SystemRandom().sample(pool,amount);title=SUBJECTS[sub]
        sections=[{'title':title,'start':0,'count':len(refs)}];seconds=min(86400,max(600,len(refs)*90))
    else:
        if d.get('file'):
            file=meta['files'].get(d['file'])
            if not _can_read(s,file):raise ValueError('Файлға рұқсат жоқ')
            files=[file];title=file['title']
        else:
            files=_files_in_folder(meta,s,str(d.get('folder')or''),d.get('scope'))
            title=meta['folders'].get(d.get('folder'),{}).get('title','Барлық файл')
        for file in files:
            sections.append({'title':file['title'],'start':len(refs),'count':file['count']})
            for i,q in enumerate(_rows(repo,file)):refs.append({'file':file['id'],'index':i,'points':q['points'],'subject':q['subject']})
        seconds=min(86400,max(600,len(refs)*90))
    if not refs:raise ValueError('Бұл бөлімде сұрақ жоқ')
    if len(refs)>20000:raise ValueError('Бұл бөлім 20 000 сұрақтан асады. Ішкі бөлімін таңдаңыз')
    eid=secrets.token_hex(16);exam={'id':eid,'uid':s['uid'],'title':title,'refs':refs,'count':len(refs),'max':sum(q['points']for q in refs),'deadline':time.time()+seconds,'sections':sections,'answers':{},'done':False}
    repo.write({_PREFIX+'active_'+s['uid']:exam});rt['exams'][eid]=exam
    return _exam_info(exam)
def _active(rt,s,ident=None):
    ex=rt['repo'].get(_PREFIX+'active_'+s['uid'])
    if not ex or ex.get('uid')!=s['uid']or (ident and ex['id']!=ident):raise ValueError('Белсенді тест табылмады')
    return json.loads(_jdump(ex))
def _answer_map(rt,meta,exam,incoming):
    if not isinstance(incoming,dict)or len(incoming)>exam['count']:raise ValueError('Жауаптар жарамсыз')
    result={}
    for k,v in incoming.items():
        if not str(k).isdigit():raise ValueError('Сұрақ индексі жарамсыз')
        i=int(k)
        if not 0<=i<exam['count']or type(v)is not int:raise ValueError('Жауап индексі жарамсыз')
        ref=exam['refs'][i];q=_question(rt['repo'],meta['files'][ref['file']],ref['index'])
        if not 0<=v<len(q['options']):raise ValueError('Жауап нұсқасы жарамсыз')
        result[str(i)]=v
    return result
def _access_event(repo,s,kind):
    key=_PREFIX+'access_log';rows=repo.get(key,[])
    if kind=='login':
        ident=secrets.token_hex(12);s['log_id']=ident
        rows.append({'id':ident,'uid':s['uid'],'name':s['name'],'login':s['login'],'entered':time.time(),'lastSeen':time.time(),'exited':None})
    else:
        row=next((r for r in reversed(rows)if r['id']==s.get('log_id')),None)
        if not row:return
        row['lastSeen']=time.time()
        if kind in ('logout','deleted'):row['exited']=time.time();row['reason']=kind
    repo.write({key:rows[-1000:]});s['log_touch']=time.time()
def _upload_worker(rt,up):
    repo=rt['repo'];prepared=[]
    try:
        up.update(phase='processing',scanned=0,msg='Сұрақтар тексеріліп, серверге сақталуда…')
        def progress(n):up['scanned']=sum(r['count']for r in prepared)+n
        if up['size']<=50*1024**2:
            with open(up['path'],encoding='utf-8-sig')as f:data=json.load(f)
            groups=_groups(data,up['title'])
            for title,subpath,rows in groups:
                row=_store_group(repo,rt,rows,title,up['subject'],up['scope'],'',progress)
                row['_path']='/'.join(p for p in(up['folderPath'],subpath)if p);prepared.append(row)
        else:
            with open(up['path'],encoding='utf-8-sig')as f:
                row=_store_group(repo,rt,_LargeJSONReader(f).questions(),up['title'],up['subject'],up['scope'],'',progress)
            row['_path']=up['folderPath'];prepared.append(row)
        if not prepared:raise ValueError('Файлда сұрақ жоқ')
        up.update(msg='База тізімі жаңартылуда…',phase='committing')
        with rt['lock']:
            meta=repo.index()
            if not any(u['id']==up['uid']for u in meta['users'].values()):raise ValueError('Аккаунт өшірілген')
            for row in prepared:
                row['folder']=_folder_path(meta,up['scope'],row.pop('_path'))
                row['author']=up['uid'];meta['files'][row['id']]=row
            repo.save_index(meta)
        up.update(phase='done',count=sum(r['count']for r in prepared),files=[r['id']for r in prepared],msg='Базаға толық қосылды')
    except Exception as exc:
        up.update(phase='error',error=str(exc)if isinstance(exc,ValueError)else'Серверге сақтау сәтсіз аяқталды. Қосылымды тексеріңіз.')
    finally:
        pathlib.Path(up['path']).unlink(missing_ok=True);up['finished']=time.time()

def dispatch(rt,token,action,d):
    repo=rt['repo']
    with rt['lock']:
        s=_session(rt,token);meta=repo.index()
        if action=='login':
            login=str(d.get('login')or'').strip().casefold();pw=str(d.get('password')or'')
            if len(pw)>200:raise ValueError('Пароль қате')
            if login=='админ':login='admin'
            attempt_key=login or ('password:'+str(d.get('_client')or'anonymous'))
            now=time.time();failed=[t for t in rt['fails'].get(attempt_key,[])if now-t<600]
            if len(failed)>=5:raise ValueError('Кіру әрекеті тым көп. 10 минуттан кейін қайталаңыз')
            if login:
                u=meta['users'].get(login)
                matches=[u]if u and _check_pw(pw,u['ph'])else[]
            else:
                matches=[u for u in meta['users'].values()if _check_pw(pw,u['ph'])]
            if len(matches)!=1:
                rt['fails'][attempt_key]=failed+[now]
                raise ValueError('Пароль қате'if not matches else'Бұл пароль бірнеше аккаунтта қайталанған. Админнен жеке пароль алыңыз.')
            u=matches[0];login=u['login']
            rt['fails'].pop(attempt_key,None);new=secrets.token_urlsafe(32)
            rt['sessions'][new]={'uid':u['id'],'login':login,'name':u['name'],'expires':now+14*86400,'stamp':_password_stamp(u['ph'])}
            _access_event(repo,rt['sessions'][new],'login')
            return {'ok':True,'token':new,'user':{'id':u['id'],'name':u['name'],'admin':u['id']=='admin'}}
        if action=='logout':
            if s:_access_event(repo,s,'logout')
            rt['sessions'].pop(token,None);return {'ok':True}
        if action=='view':
            return {'ok':True,'manage':_owner(s)and d.get('screen')=='s-admin','dark':d.get('dark')is True}
        _require(s)
        if action=='change_admin_password':
            if not _owner(s):raise ValueError('Парольді тек админ өзгертеді')
            old=str(d.get('current')or'');new=str(d.get('password')or'')
            if not _check_pw(old,meta['users']['admin']['ph']):raise ValueError('Қазіргі пароль қате')
            if not 10<=len(new)<=200:raise ValueError('Жаңа пароль 10–200 таңба болсын')
            if hmac.compare_digest(old,new):raise ValueError('Жаңа пароль бұрынғысынан өзгеше болсын')
            if any(u['id']!='admin'and _check_pw(new,u['ph'])for u in meta['users'].values()):raise ValueError('Бұл пароль бос емес. Басқа пароль таңдаңыз')
            ph=_hash_pw(new);meta['users']['admin']['ph']=ph
            repo.save_index(meta)
            for key,session in list(rt['sessions'].items()):
                if session['uid']=='admin'and key!=token:rt['sessions'].pop(key,None)
            s['stamp']=_password_stamp(ph)
            return {'ok':True}
        if action in('status','refresh'):
            return {'ok':True,'user':{'id':s['uid'],'name':s['name'],'admin':_owner(s)},'meta':_visible_meta(meta,s),'active':_exam_info(ex)if(ex:=repo.get(_PREFIX+'active_'+s['uid']))and not ex.get('done')else None}
        if action=='admin_users':
            if not _owner(s):raise ValueError('Тек админ')
            return {'ok':True,'users':_visible_meta(meta,s)['users'],'logs':repo.get(_PREFIX+'access_log',[])[-300:][::-1]}
        if action=='delete_user':
            if not _owner(s):raise ValueError('Адамды тек админ өшіреді')
            uid=str(d.get('uid')or'')
            if not uid or uid=='admin':raise ValueError('Админді өшіруге болмайды')
            if not any(u['id']==uid for u in meta['users'].values()):raise ValueError('Адам табылмады')
            meta['users']={k:u for k,u in meta['users'].items()if u['id']!=uid};repo.save_index(meta)
            for key,session in list(rt['sessions'].items()):
                if session['uid']==uid:_access_event(repo,session,'deleted');rt['sessions'].pop(key,None)
            return {'ok':True}
        if action=='flashcards':
            ex=repo.get(_PREFIX+'active_'+s['uid'])
            if ex and not ex.get('done'):raise ValueError('Алдымен тестті аяқтаңыз')
            sub=d.get('subject');offset=d.get('offset',0)
            if type(offset)is not int or offset<0:raise ValueError('Бет жарамсыз')
            cards=[];total=0
            for file in meta['files'].values():
                if file['scope']not in('public','bank'):continue
                for q in _rows(repo,file):
                    if sub and q['subject']!=sub:continue
                    if offset<=total<offset+20:cards.append({'front':_safe_q(q),'back':q['options'][q['correct']],'explanation':q.get('explanation','')})
                    total+=1
            return {'ok':True,'items':cards,'total':total,'offset':offset}
        if action=='create_user':
            if not _owner(s):raise ValueError('Адамды тек админ қосады')
            login=str(d.get('login')or'').strip();name=str(d.get('name')or login).strip();pw=str(d.get('password')or'')
            if not re.fullmatch(r'[\w.@+ -]{2,40}',login)or login.casefold()in meta['users']or login.casefold()in('admin','админ'):raise ValueError('Логин бос емес немесе жарамсыз (2–40 таңба)')
            if not 10<=len(pw)<=200:raise ValueError('Пароль 10–200 таңба болсын')
            if any(_check_pw(pw,u['ph'])for u in meta['users'].values()):raise ValueError('Бұл пароль бос емес. Басқа пароль таңдаңыз')
            meta['users'][login.casefold()]={'id':secrets.token_hex(12),'login':login,'name':name[:80],'ph':_hash_pw(pw)}
            repo.save_index(meta);return {'ok':True}
        if action=='create_folder':
            scope=_scope(s,d.get('scope'));path=str(d.get('path')or'').strip()
            if not path:raise ValueError('Бөлім атауын жазыңыз')
            ident=_folder_path(meta,scope,path);repo.save_index(meta);return {'ok':True,'folder':ident}
        if action=='upload_begin':
            scope=_scope(s,d.get('scope'));size=d.get('size')
            if type(size)is not int or not 0<size<=MAX_UPLOAD:raise ValueError('JSON файлы 1 ГБ-тан аспасын')
            if d.get('subject')not in SUBJECTS:raise ValueError('Пәнді таңдаңыз')
            root=pathlib.Path(tempfile.gettempdir())/'ubt_files_uploads';root.mkdir(exist_ok=True)
            for ident,up in list(rt['uploads'].items()):
                if time.time()-up['at']>3600 and up.get('phase')not in('processing','committing'):
                    pathlib.Path(up['path']).unlink(missing_ok=True);rt['uploads'].pop(ident,None)
            if sum(u['uid']==s['uid']and u.get('phase')not in('done','error')for u in rt['uploads'].values())>=2:raise ValueError('Алдыңғы жүктеуді аяқтаңыз')
            ident=secrets.token_hex(16);path=str(root/ident)
            pathlib.Path(path).touch()
            rt['uploads'][ident]={'id':ident,'uid':s['uid'],'path':path,'scope':scope,'subject':d['subject'],'folderPath':str(d.get('path')or'')[:1000],'title':str(d.get('name')or'Тест').removesuffix('.json')[:160],'size':size,'received':0,'at':time.time(),'phase':'receiving'}
            return {'ok':True,'id':ident,'chunk':CHUNK}
        if action in('upload_chunk','upload_finish','upload_cancel','upload_status'):
            up=rt['uploads'].get(d.get('id'))
            if not up or up['uid']!=s['uid']:raise ValueError('Жүктеу табылмады')
            if action=='upload_status':
                return {'ok':True,**{k:up.get(k)for k in('phase','size','received','scanned','count','msg','error','files')}}
            if action=='upload_cancel':
                if up.get('phase')in('processing','committing'):raise ValueError('Сақтау аяқталғанша күтіңіз')
                pathlib.Path(up['path']).unlink(missing_ok=True);rt['uploads'].pop(up['id'],None);return {'ok':True}
            if action=='upload_chunk':
                if up.get('phase')!='receiving':raise ValueError('Бұл жүктеу файл бөліктерін қабылдамайды')
                offset=d.get('offset');encoded=d.get('bytes')
                if type(offset)is not int or offset<0 or not isinstance(encoded,str)or len(encoded)>CHUNK*4//3+8:raise ValueError('Файл бөлігі жарамсыз')
                raw=base64.b64decode(encoded,validate=True)
                if not raw or len(raw)>CHUNK or offset+len(raw)>up['size']:raise ValueError('Бөлік өлшемі жарамсыз')
                if offset<up['received']:
                    with open(up['path'],'rb')as f:f.seek(offset);old=f.read(len(raw))
                    if not hmac.compare_digest(old,raw):raise ValueError('Қайталанған бөлік сәйкес емес')
                    return {'ok':True,'received':up['received']}
                if offset!=up['received']:raise ValueError('Файл бөліктерінің реті бұзылған')
                with open(up['path'],'ab')as f:f.write(raw)
                up['received']+=len(raw);return {'ok':True,'received':up['received']}
            if up['received']!=up['size']:raise ValueError('Файл толық жүктелмеген')
            if up.get('phase')=='receiving':
                up['phase']='processing'
                threading.Thread(target=_upload_worker,args=(rt,up),daemon=True).start()
            return {'ok':True,'phase':up['phase'],'id':up['id']}
        if action=='publish_file':
            if not _owner(s):raise ValueError('Тестті тек админ жариялайды')
            file=meta['files'].get(d.get('file'))
            if not file or file['scope']!='admin':raise ValueError('Өз жеке файлыңызды таңдаңыз')
            parent=_folder_path(meta,'public',str(d.get('path')or''))
            file['scope']='public';file['folder']=parent;repo.save_index(meta);return {'ok':True}
        if action=='preview':
            file=meta['files'].get(d.get('file'))
            if not _can_read(s,file):raise ValueError('Файлға рұқсат жоқ')
            offset=d.get('offset',0)
            if type(offset)is not int or not 0<=offset<file['count']:raise ValueError('Бет нөмірі жарамсыз')
            return {'ok':True,'questions':[_safe_q(_question(repo,file,i))for i in range(offset,min(offset+10,file['count']))],'total':file['count'],'offset':offset}
        if action=='start':
            active=repo.get(_PREFIX+'active_'+s['uid'])
            if active and not active.get('done')and not d.get('replace'):raise ValueError('Белсенді тест бар. Алдымен оны аяқтаңыз немесе жалғастырыңыз')
            return {'ok':True,'exam':_start(rt,s,d)}
        if action=='question':
            exam=_active(rt,s,d.get('exam'));i=d.get('index')
            if type(i)is not int or not 0<=i<exam['count']:raise ValueError('Сұрақ нөмірі жарамсыз')
            ref=exam['refs'][i];q=_question(repo,meta['files'][ref['file']],ref['index'])
            result=_safe_q(q);result['points']=ref['points']
            if exam.get('done'):result.update(correct=q['correct'],explanation=q.get('explanation',''))
            return {'ok':True,'question':result,'index':i,'done':exam.get('done',False)}
        if action in('save_answers','finish'):
            exam=_active(rt,s,d.get('exam'))
            if exam.get('done'):return {'ok':True,'result':exam['result'],'exam':_exam_info(exam)}
            answers=exam['answers']
            if time.time()<=exam['deadline']:
                answers=_answer_map(rt,meta,exam,d.get('answers',{}))
            if action=='save_answers'and time.time()<=exam['deadline']:
                exam['answers']=answers;repo.write({_PREFIX+'active_'+s['uid']:exam});return {'ok':True}
            score=0;by_subject={};correct_n=0
            for i,ref in enumerate(exam['refs']):
                q=_question(repo,meta['files'][ref['file']],ref['index']);right=answers.get(str(i))==q['correct'];earned=ref['points']if right else 0
                score+=earned;correct_n+=int(right);stat=by_subject.setdefault(ref['subject'],{'score':0,'max':0,'answered':0})
                stat['score']+=earned;stat['max']+=ref['points'];stat['answered']+=int(str(i)in answers)
            result={'title':exam['title'],'score':score,'max':exam['max'],'correct':correct_n,'answered':len(answers),'count':exam['count'],'subjects':by_subject,'at':time.time()}
            exam.update(done=True,answers=answers,result=result)
            key=_PREFIX+'history_'+s['uid'];history=repo.get(key,[])[-99:]+[result]
            repo.write({_PREFIX+'active_'+s['uid']:exam,key:history});return {'ok':True,'result':result,'exam':_exam_info(exam)}
        if action=='history':return {'ok':True,'items':repo.get(_PREFIX+'history_'+s['uid'],[])[-30:][::-1]}
        raise ValueError('Сұраныс табылмады')

class _LargeJSONReader:
    """Read JSON tokens with a 64KiB input window and <=2MiB captured values."""
    def __init__(self, f): self.f=f; self.buf=''; self.pos=0; self.total=0
    def peek(self):
        if self.pos >= len(self.buf): self.buf=self.f.read(65536); self.pos=0
        return self.buf[self.pos:self.pos+1]
    def take(self):
        c=self.peek()
        if not c: raise ValueError('JSON аяқталмаған')
        self.pos+=1; self.total+=1; return c
    def ws(self):
        while self.peek():
            m=re.match(r'[ \t\r\n]*', self.buf[self.pos:]); n=m.end()
            self.pos+=n; self.total+=n
            if self.pos<len(self.buf): return
    def expect(self, c):
        self.ws()
        if self.take()!=c: raise ValueError('JSON ішінде «'+c+'» күтілді')
    def string(self, capture=True, limit=2_000_000):
        if self.take()!='"': raise ValueError('JSON жолы күтілді')
        raw=['"'] if capture else None; length=0
        while True:
            if not self.peek(): raise ValueError('JSON жолының тырнақшасы жабылмаған')
            match=re.search(r'["\\\x00-\x1f]', self.buf[self.pos:])
            end=self.pos+match.start() if match else len(self.buf)
            span=self.buf[self.pos:end]; self.pos=end; self.total+=len(span); length+=len(span)
            if capture:
                if length>limit: raise ValueError('JSON ішіндегі бір жол тым үлкен')
                raw.append(span)
            if not match: continue
            c=self.take()
            if c=='"':
                if capture: raw.append(c); return json.loads(''.join(raw))
                return None
            if ord(c)<32: raise ValueError('JSON жолындағы басқару таңбасы жарамсыз')
            esc=self.take()
            if esc not in '"\\/bfnrtu': raise ValueError('JSON escape таңбасы жарамсыз')
            suffix=''
            if esc=='u':
                suffix=''.join(self.take() for _ in range(4))
                if not re.fullmatch('[0-9a-fA-F]{4}', suffix): raise ValueError('JSON Unicode таңбасы жарамсыз')
            if capture: raw.append('\\'+esc+suffix)
    def value(self, capture=True, depth=0, end=None):
        if depth>64: raise ValueError('JSON қабаттары тым көп')
        if end is None and capture: end=self.total+2_000_000
        self.ws(); c=self.peek()
        if c=='"': return self.string(capture)
        if c in ('[','{'):
            obj={} if c=='{' and capture else [] if capture else None
            close='}' if c=='{' else ']'; self.take(); self.ws()
            if self.peek()==close: self.take(); return obj
            while True:
                if c=='{': self.ws(); key=self.string(True, 1024); self.expect(':')
                v=self.value(capture, depth+1, end)
                if capture:
                    if self.total>end: raise ValueError('Бір сұрақтың JSON дерегі 2 МБ-тан үлкен')
                    if c=='{': obj[key]=v
                    else: obj.append(v)
                self.ws(); sep=self.take()
                if sep==close: return obj
                if sep!=',': raise ValueError('JSON ішінде үтір күтілді')
        token=[]
        while self.peek() and self.peek() not in ',]} \t\r\n':
            token.append(self.take())
            if len(token)>512: raise ValueError('JSON саны тым ұзын')
        if not token: raise ValueError('JSON мәні күтілді')
        value=json.loads(''.join(token), parse_constant=lambda _: (_ for _ in ()).throw(ValueError('NaN/Infinity жарамсыз')))
        return value if capture else None
    def groups(self, depth=0):
        if depth>64: raise ValueError('JSON қабаттары тым көп')
        self.ws(); c=self.peek()
        if c=='[':
            self.take(); self.ws()
            if self.peek()==']': self.take(); return
            while True:
                yield from self.groups(depth+1); self.ws(); sep=self.take()
                if sep==']': return
                if sep!=',': raise ValueError('JSON тізімінде үтір күтілді')
        elif c=='{':
            self.take(); row={}; container=False; self.ws()
            if self.peek()=='}': self.take(); return
            while True:
                self.ws(); key=self.string(True,1024); self.expect(':')
                if key in ('questions','tests','items'):
                    container=True; yield from self.groups(depth+1)
                elif key in ('text','question','options','correct','points','img','tbl','explanation','difficulty','subject','topic','id','answers','variants','answer','correctAnswer','q','image'):
                    row[key]=self.value(True,depth+1)
                    if len(_jdump(row))>2_000_000: raise ValueError('Бір сұрақ тым үлкен')
                else: self.value(False,depth+1)
                self.ws(); sep=self.take()
                if sep=='}': break
                if sep!=',': raise ValueError('JSON объектісінде үтір күтілді')
            if not container: yield row
        else: raise ValueError('JSON ішінде сұрақ не тест объектісі болуы керек')
    def questions(self):
        yield from self.groups()
        self.ws()
        if self.peek(): raise ValueError('JSON соңында артық дерек бар')

HTML = '<!doctype html><html lang="kk"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ҰБТ PLUS · Инфо–мат</title><style>\n:root{--p:#2563eb;--pd:#1d4ed8;--ok:#16a34a;--err:#dc2626;--warn:#f59e0b;--bg:#f1f5f9;--c:#fff;--t:#0f172a;--m:#64748b;--b:#e2e8f0}\n*{margin:0;padding:0;box-sizing:border-box}\n:root{--vh:800px}\nbody{font-family:\'Inter\',system-ui,sans-serif;background:var(--bg);color:var(--t);min-height:var(--vh);line-height:1.5}\nhtml,body{overflow-x:hidden}\n.screen{display:none;min-height:var(--vh)}.screen.active{display:block}\n.wrap{max-width:880px;margin:0 auto;padding:32px 16px 110px}\n.tmain{padding-bottom:110px!important}\n.topback{position:relative;z-index:60;will-change:transform;background:var(--bg);padding:8px 0;margin:-20px 0 10px;display:flex}\n.topback .btn{box-shadow:0 1px 4px rgba(0,0,0,.08)}\n.wrap.wide{max-width:1200px}\n.hdr{text-align:center;margin-bottom:28px}\n.logo{display:inline-flex;align-items:center;justify-content:center;width:72px;height:72px;background:linear-gradient(135deg,#2563eb,#7c3aed);color:#fff;font-weight:800;font-size:26px;border-radius:24px;margin-bottom:14px;box-shadow:0 8px 24px rgba(37,99,235,.35);letter-spacing:-0.5px}\n.hdr h1{font-size:26px;font-weight:700;margin-bottom:4px}\n.hdr h2{font-size:22px;margin-bottom:4px}\n.sub{color:var(--m);font-size:14px}\n.btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;padding:11px 20px;border-radius:20px;font-size:14px;font-weight:600;border:none;cursor:pointer;font-family:inherit;transition:.15s}\n.btn-p{background:var(--p);color:#fff}.btn-p:hover{background:var(--pd)}.btn-p:disabled{opacity:.45;cursor:not-allowed}\n.btn-s{background:var(--c);color:var(--t);border:1px solid var(--b)}.btn-s:hover{background:var(--bg)}\n.btn-d{background:var(--err);color:#fff}.btn-ok{background:var(--ok);color:#fff}.btn-w{background:var(--warn);color:#1c1917}\n.btn-sm{padding:7px 12px;font-size:12px}\n.row{display:flex;gap:10px;flex-wrap:wrap;justify-content:center}\n.card{background:var(--c);border:1px solid var(--b);border-radius:22px;padding:18px;margin-bottom:12px}\n.card h3{font-size:16px;margin-bottom:6px}\n.grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px}\n.mode{background:var(--c);border:2px solid var(--b);border-radius:22px;padding:22px 14px;text-align:center;cursor:pointer;transition:.2s}\n.mode:hover{border-color:var(--p);transform:translateY(-2px);box-shadow:0 6px 20px rgba(37,99,235,.1)}\n.mode .ic{font-size:30px;margin-bottom:8px}\n.mode h3{font-size:15px;margin-bottom:4px}\n.mode p{font-size:12px;color:var(--m)}\n.fg{margin-bottom:14px}\n.fg label{display:block;font-size:12px;font-weight:600;color:var(--m);margin-bottom:5px}\n.fg input,.fg select,.fg textarea{width:100%;padding:10px 12px;border:1px solid var(--b);border-radius:20px;font-size:14px;font-family:inherit;background:var(--bg)}\n.fg textarea{min-height:72px;resize:vertical}\n.opt{display:flex;gap:8px;align-items:center;margin-bottom:8px}\n.opt input[type=text]{flex:1}\n.opt input[type=radio]{width:18px;height:18px;accent-color:var(--p)}\n.badge{display:inline-block;padding:3px 10px;border-radius:24px;font-size:11px;font-weight:600}\n.badge-pub{background:#dbeafe;color:var(--p)}.badge-priv{background:#f1f5f9;color:var(--m)}\n.list{display:flex;flex-direction:column;gap:10px}\n.item{background:var(--c);border:1px solid var(--b);border-radius:22px;padding:14px 16px;display:flex;justify-content:space-between;align-items:center;gap:12px}\n.item .info{flex:1;min-width:0}\n.item .info h4{font-size:14px;margin-bottom:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}\n.item .info p{font-size:12px;color:var(--m)}\n.item .acts{display:flex;gap:6px;flex-shrink:0;flex-wrap:wrap}\n.empty{text-align:center;padding:40px 16px;color:var(--m)}.empty .ic{font-size:36px;margin-bottom:10px}\n.profile-bar{display:flex;justify-content:space-between;align-items:center;padding:12px 16px;background:var(--c);border-bottom:1px solid var(--b);margin-bottom:20px}\n.profile-bar .name{font-weight:600;font-size:14px}\n.avatar{width:36px;height:36px;border-radius:50%;background:var(--p);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px}\n.tlay{display:flex;min-height:var(--vh);align-items:flex-start}\n.side{width:260px;background:var(--c);border-right:1px solid var(--b);display:flex;flex-direction:column;position:relative;top:0;height:var(--vh);will-change:transform}\n.side-h{padding:12px;border-bottom:1px solid var(--b);display:flex;justify-content:space-between;align-items:center;font-weight:600;font-size:13px}\n.side-tog{display:none;background:none;border:none;font-size:20px;cursor:pointer}\n.qnav{flex:1;overflow-y:auto;padding:8px;display:grid;grid-template-columns:repeat(5,1fr);gap:4px;align-content:start}\n.qn{aspect-ratio:1;border:1px solid var(--b);border-radius:17px;background:var(--bg);font-size:11px;font-weight:500;cursor:pointer;display:flex;align-items:center;justify-content:center}\n.qn.cur{border-color:var(--p);background:#dbeafe;color:var(--p);font-weight:700}\n.qn.ans{background:#dcfce7;border-color:#86efac;color:var(--ok)}\n.qn.flg{background:#fef3c7;border-color:#fcd34d}\n.side-f{padding:12px;border-top:1px solid var(--b)}\n.tmain{flex:1;padding:18px 24px;max-width:780px}\n.ttop{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;flex-wrap:wrap;gap:8px}\n.prog-t{font-size:14px;font-weight:700;color:var(--p);background:#eff6ff;padding:5px 12px;border-radius:24px}\n.prog-w{flex:1;min-width:120px;background:#e2e8f0;border-radius:24px;height:8px;overflow:hidden}\n.prog-f{height:100%;background:var(--p);border-radius:24px;transition:width .3s}\n.timer{font-size:22px;font-weight:700;font-variant-numeric:tabular-nums;color:var(--p);background:#eff6ff;padding:5px 14px;border-radius:20px}\n.timer.warn{color:var(--warn);background:#fffbeb}.timer.dang{color:var(--err);background:#fef2f2;animation:pulse 1s infinite}\n@keyframes pulse{50%{opacity:.7}}\n.qc{background:var(--c);border-radius:22px;padding:20px;box-shadow:0 1px 3px rgba(0,0,0,.05);margin-bottom:16px}\n.qh{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}\n.qnum{font-size:12px;font-weight:600;color:var(--p);background:#eff6ff;padding:3px 10px;border-radius:24px}\n.flag{background:none;border:1px solid var(--b);border-radius:17px;padding:4px 8px;cursor:pointer;font-size:14px}\n.flag.on{background:#fef3c7;border-color:#fcd34d}\n.qt{font-size:15px;margin-bottom:16px;line-height:1.6}\n.qt .qprompt{white-space:pre-wrap;overflow-wrap:anywhere}\n.qt .qcode{margin:12px 0 4px;padding:16px 18px;border-radius:12px;background:#0d1117;color:#e6edf3;overflow-x:auto;tab-size:4}\n.qt .qcode code{display:block;white-space:pre;font:14px/1.55 ui-monospace,SFMono-Regular,Consolas,monospace}\n.qt .qcontext{white-space:pre-wrap;margin:10px 0 0;font-weight:550}\n.chem-table-dialog{border:0;border-radius:18px;padding:0;width:min(1100px,96vw);max-width:96vw;box-shadow:0 20px 70px #0005}\n.chem-table-dialog::backdrop{background:#0b122bcc}\n.chem-table-dialog .chem-head{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:12px 18px;background:var(--c)}\n.test-tools{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 14px}\n.chem-table-dialog .periodic-scroll{max-height:75vh;overflow:auto;padding:15px}\n.periodic-grid{display:grid;grid-template-columns:repeat(18,minmax(45px,1fr));gap:4px;min-width:880px}\n.periodic-cell{min-height:47px;border-radius:7px;background:#e5ebff;color:#14265c;padding:3px;font-size:11px;text-align:center}\n.periodic-cell b{display:block;font-size:15px}.periodic-cell small{display:block;text-align:left;font-size:9px}\n.periodic-cell.lanth{background:#fce4b8}.periodic-cell.actin{background:#fad5e0}\n.periodic-cell.marker{background:#e7ddfb;font-size:10px;display:grid;place-items:center}\n.calc-dialog,.finish-dialog{border:0;border-radius:18px;padding:18px;width:min(360px,94vw);background:var(--c);color:var(--t)}\n.calc-dialog::backdrop,.finish-dialog::backdrop{background:#0b122bcc}\n.calc-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:12px}\n.calc-grid button{min-height:48px;border-radius:12px;border:1px solid var(--b);background:var(--bg);color:var(--t);font-size:18px;cursor:pointer}\n.finish-dialog input{width:100%;font-size:20px;padding:12px;margin:12px 0;border-radius:10px;border:1px solid var(--b);background:var(--bg);color:var(--t)}\n@media(max-width:600px){.chem-table-dialog{width:100vw;max-width:100vw;height:100dvh;max-height:100dvh;border-radius:0}.chem-table-dialog .periodic-scroll{max-height:calc(100dvh - 115px)}.test-tools .btn{flex:1;min-height:44px}}\n.qimg{display:block;max-width:100%;max-height:340px;margin:0 auto 14px;border-radius:14px;border:1px solid var(--b);object-fit:contain;background:#fff}\n.qtbl-w{overflow-x:auto;margin:0 0 14px}\n.qtbl{border-collapse:collapse;margin:0 auto;font-size:14px}\n.qtbl td,.qtbl th{border:1px solid var(--b);padding:6px 12px;text-align:center;min-width:48px}\n.qtbl tr:first-child td{background:#eff6ff;font-weight:600}\n.tbed{overflow-x:auto;margin:8px 0}\n.tbed table{border-collapse:collapse}\n.tbed td{padding:2px}\n.tbed input{width:90px;padding:6px 8px;border:1px solid var(--b);border-radius:10px;font-size:13px;font-family:inherit;background:var(--bg)}\n.aq-prev{max-width:240px;max-height:180px;border-radius:12px;border:1px solid var(--b);display:block;margin-top:8px}\n\n.sch-bg{background:linear-gradient(180deg,#f8f3ea,#f3ebdd);border-radius:26px;padding:22px 14px 28px;border:1px solid #eadfcb;--sc:#3d7396}\n.sch-bg h2.sch-h{text-align:center;font-size:24px;font-weight:700;margin-bottom:14px;color:#222}\n.sch-tab{display:flex;justify-content:center}\n.sch-tab span{background:#fff;padding:10px 38px;border-radius:24px 24px 0 0;font-size:20px;border-bottom:3px solid var(--sc);box-shadow:0 -2px 10px rgba(0,0,0,.04)}\n.sch-subs{display:flex;justify-content:center;gap:6px;background:#fff;border-radius:0 0 22px 22px;padding:8px 10px;max-width:420px;margin:0 auto;box-shadow:0 4px 14px rgba(0,0,0,.06);flex-wrap:wrap}\n.sch-subs span{padding:6px 16px;border-radius:18px;font-size:14px;color:#555}\n.sch-subs span.on{background:#f3f4f6;color:#111;box-shadow:0 1px 4px rgba(0,0,0,.1)}\n.sch-stem{width:2px;height:22px;background:var(--sc);margin:0 auto}\n.sch-root{max-width:600px;margin:0 auto;border-radius:22px;padding:16px 18px 18px;color:#fff;box-shadow:0 8px 24px rgba(0,0,0,.16)}\n.sch-root h3{text-align:center;font-size:20px;margin-bottom:10px}\n.sch-card-in{display:flex;gap:14px;align-items:flex-start}\n.sch-card-in .ph{width:150px;flex:none;border-radius:16px;object-fit:cover;aspect-ratio:3/4;background:#0001}\n.sch-card-in .tx{flex:1;min-width:0}\n.sch-card-in .tx b.t{display:block;font-size:19px;margin-bottom:6px}\n.sch-card-in .tx p{font-size:13px;line-height:1.55;margin:2px 0}\n.sch-card-in .ph2{max-width:130px;max-height:96px;border-radius:10px;margin-top:6px;display:block;object-fit:contain}\n.sch-kids{display:flex;justify-content:center;gap:0;flex-wrap:nowrap}\n.sch-kid{position:relative;flex:1 1 0;max-width:340px;padding:22px 8px 0;min-width:0}\n.sch-kid::before,.sch-kid::after{content:\'\';position:absolute;top:0;width:50%;height:22px;border-top:2px solid var(--sc)}\n.sch-kid::before{right:50%;border-right:2px solid var(--sc);border-top-right-radius:16px}\n.sch-kid::after{left:50%;border-left:2px solid var(--sc);border-top-left-radius:16px}\n.sch-kid:first-child::before,.sch-kid:last-child::after{display:none}\n.sch-kid:only-child::before{display:block;border:none;border-left:2px solid var(--sc);right:auto;left:50%;width:0;border-radius:0}\n.sch-kid:first-child:not(:only-child)::after{left:50%}\n.sch-kid .lab{display:inline-block;background:#fff;padding:8px 22px;border-radius:20px 20px 0 0;font-size:16px;font-weight:600;margin-left:14px}\n.sch-kid .bd{background:#fff;border-radius:20px;padding:12px;box-shadow:0 6px 18px rgba(0,0,0,.1)}\n.sch-kid .bd .ph{width:96px;aspect-ratio:1;border-radius:12px}\n.sch-kid .tx{color:#222}\n.th-blue{background:linear-gradient(135deg,#3f86ad,#265a7c)}\n.th-green{background:linear-gradient(135deg,#3f9a6a,#22664a)}\n.th-red{background:linear-gradient(135deg,#a8403f,#722423)}\n.th-violet{background:linear-gradient(135deg,#7d5bb0,#4b3380)}\n@media(max-width:640px){\n .sch-kids{flex-direction:column;align-items:stretch}\n .sch-kid{max-width:none;padding-top:16px}\n .sch-kid::before,.sch-kid::after{display:none!important}\n .sch-card-in .ph{width:96px}\n}\n\n\n.sch-bg.mindmap{background:radial-gradient(ellipse at top,#fff 0%,#f7faf7 60%,#edf4ed 100%);border:1px solid #dce8dc;padding:26px 18px 34px;overflow:hidden;position:relative}\n.mindmap .sch-h{font-size:clamp(20px,3vw,28px);color:#20352a;margin:0 0 18px;animation:mindFade .55s both}\n.mind-top{width:max-content;max-width:100%;margin:0 auto 12px;padding:8px 24px;border-radius:22px;background:#fff;border:1px solid #d7e4d8;color:#385b42;font-weight:700;box-shadow:0 4px 12px #1d462010}\n.mind-tags{display:flex;justify-content:center;gap:8px;flex-wrap:wrap;margin:0 auto 18px}\n.mind-tags span{background:#fff;border:1px solid #dbe8dc;border-radius:18px;padding:6px 14px;font-size:13px;color:#47624c;animation:mindPop .45s both;animation-delay:var(--delay)}\n.mind-layout{display:grid;grid-template-columns:minmax(170px,230px) minmax(0,1fr);gap:24px;align-items:center;position:relative}.mind-center{display:flex;justify-content:center;position:relative;z-index:2;align-self:center}.mind-layout:before{content:"";position:absolute;left:220px;width:22px;top:50%;height:2px;background:var(--mind-line);opacity:.9}\n.mind-node{position:relative;display:flex;flex-direction:column;align-items:flex-start;text-align:left;width:100%;border:1px solid color-mix(in srgb,var(--branch,#8bb99a),white 30%);border-left:5px solid var(--branch,var(--mind));border-radius:17px;background:#fff;padding:13px 15px;box-shadow:0 5px 16px #183b1b12;cursor:pointer;font:inherit;color:#25342a;transition:transform .2s,box-shadow .2s;animation:mindSlide .5s both;animation-delay:var(--delay,0ms)}\n.mind-node:hover{transform:translateY(-3px);box-shadow:0 10px 24px #183b1b20}\n.mind-node strong{font-size:15px;line-height:1.4}.mind-main{max-width:420px;align-items:center;text-align:center;background:linear-gradient(135deg,#dff0df,#c8e4c9);border:2px solid #91bd96;border-left:2px solid #91bd96;border-radius:23px;padding:18px 24px;color:#254c30}.mind-main strong{font-size:19px}.mind-main small{font-size:11px;color:#4b7053;margin-top:4px}.mind-dot{display:grid;place-items:center;width:30px;height:30px;border-radius:50%;background:#fff;color:#438251;margin-bottom:6px}\n.mind-branches{display:grid;grid-template-columns:1fr;gap:12px;margin:0;position:relative;min-width:0}.mind-branches:before{content:"";position:absolute;left:-12px;top:calc(74px / 2);bottom:calc(74px / 2);width:2px;background:var(--mind-line)}.mind-branch{position:relative;min-width:0}.mind-connector{position:absolute;left:-24px;top:50%;height:2px;width:24px;background:var(--mind-line)}.mind-branch .mind-node{min-height:74px;padding-right:35px}.mind-subtitle{font-size:12px;color:#6b756c;margin-top:3px}.mind-toggle{position:absolute;right:12px;top:12px;width:22px;height:22px;border-radius:50%;display:grid;place-items:center;background:var(--mind-soft);color:var(--mind);font-weight:800}.mind-details{display:none;width:100%;margin-top:10px;padding-top:8px;border-top:1px solid #e5ece5;text-align:left}.mind-node.expanded .mind-details{display:block;animation:mindFade .25s both}.mind-node.expanded .mind-toggle{transform:rotate(45deg)}.mind-detail{display:grid;grid-template-columns:minmax(65px,.7fr) 1.3fr;gap:8px;padding:5px 0;font-size:12px;line-height:1.45;border-bottom:1px dashed #e6ece6}.mind-detail b{color:var(--mind)}.mind-detail span{overflow-wrap:anywhere}.mind-img{max-width:100%;max-height:150px;object-fit:contain;border-radius:10px;margin-top:8px}\n.mind-add-info{margin-top:8px;font-size:12px;padding:5px 10px}.mind-info-form{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px}.mind-info-form input{flex:1 1 130px;min-width:0;padding:7px;border:1px solid #b7d9bd;border-radius:8px}.mind-info-form button{padding:6px 10px}\n.mind-branch-row{display:flex;align-items:flex-start;gap:9px}.mind-branch-row>.mind-node{flex:1;min-width:0}.mind-arrow{flex:none;border:1px solid var(--mind-line);border-radius:12px;background:var(--mind-soft);color:var(--mind);font-size:19px;font-weight:800;min-width:38px;height:40px;cursor:pointer}.mind-arrow[aria-expanded="true"]{background:var(--mind);color:#fff}.mind-children{display:none;margin:10px 0 8px 25px;padding-left:16px;border-left:2px solid var(--mind-line)}.mind-children.open{display:grid;gap:9px;animation:mindFade .3s both}.mind-child{position:relative;border:1px solid var(--mind-line);border-radius:13px;background:#fff;padding:11px 13px;min-width:0}.mind-child:before{content:"";position:absolute;left:-16px;top:22px;width:16px;height:2px;background:var(--mind-line)}.mind-child summary{cursor:pointer;font-weight:700;color:#254c30}.mind-child .mind-detail:first-of-type{margin-top:9px}\n.mind-child-head{display:flex;justify-content:space-between;gap:8px;align-items:center}.mind-child-title{border:0;background:none;color:#254c30;font-family:inherit;font-size:15px;font-weight:700;text-align:left;cursor:pointer;padding:5px}.mind-child-info{margin-top:6px}.mind-child>.mind-children{margin-left:14px}\n.mind-tools{display:flex;gap:7px;justify-content:flex-end;align-items:center;margin:0 0 12px}.mind-tools button{min-width:34px}.mind-map-shell{overflow-x:auto;padding:4px}.mind-branch .mind-node{cursor:default}.mind-node-head{display:flex;align-items:center;gap:6px;width:100%;min-width:0;padding-right:32px}.mind-title{flex:1;min-width:0;border:0;background:none;color:inherit;text-align:left;font:inherit;cursor:pointer;padding:0}.mind-title strong{display:block}.mind-title .mind-subtitle{display:block}.mind-title:focus-visible,.mind-arrow:focus-visible,.mind-mini:focus-visible{outline:2px solid var(--mind)}.mind-mini{flex:none;border:1px solid var(--mind-line);border-radius:9px;background:#fff;color:#92483e;font-size:18px;line-height:1;min-width:28px;height:28px;cursor:pointer}.mind-controls{display:flex;gap:6px;flex-wrap:wrap;margin-top:9px}.mind-controls label{cursor:pointer}.mind-child .mind-node{min-height:0;border:0;box-shadow:none;padding:0;animation:none}.mind-child .mind-node:hover{transform:none;box-shadow:none}.mind-child .mind-node .mind-details{margin-top:6px}.mind-child .mind-children{width:auto}.mind-node .mind-img{cursor:zoom-in}.mind-main-wrap{display:flex;flex-direction:column;gap:8px;align-items:center;width:100%}.mind-photo-box img{max-width:80vw;max-height:70vh;object-fit:contain;display:block;margin:auto}\n.mind-photo-actions{display:inline-flex;align-items:center;gap:6px;flex-wrap:wrap}.mind-photo-actions .btn[disabled]{opacity:.45;cursor:not-allowed}\n.mind-map-shell{overflow:auto}.sch-bg.mindmap{overflow:visible;min-width:760px}.mind-layout{align-items:start}\n.mind-branch.branch-open,.mind-child.branch-open{display:grid;grid-template-columns:minmax(290px,1fr) minmax(310px,1fr);gap:24px;align-items:start;min-width:640px}\n.mind-branch.branch-open>.mind-children.open,.mind-child.branch-open>.mind-children.open{margin:0;padding-left:17px;position:relative}\n.mind-branch.branch-open>.mind-children.open:before,.mind-child.branch-open>.mind-children.open:before{content:"";position:absolute;left:-24px;top:24px;width:24px;height:2px;background:var(--mind-line)}\n.mind-child.branch-open{border:0;background:transparent;padding:0}.mind-child.branch-open>.mind-branch-row{border:1px solid var(--mind-line);border-radius:13px;background:#fff;padding:11px 13px}\n.mind-tools{position:sticky;left:0;width:max-content;z-index:3;background:#fff;border:1px solid #dce8dc;border-radius:12px;padding:6px 9px}.mind-zoom-level{min-width:48px;text-align:center;font-size:13px;font-weight:700;color:var(--mind)}\n@keyframes mindFade{from{opacity:0}to{opacity:1}}@keyframes mindPop{from{opacity:0;transform:translateY(-8px) scale(.96)}to{opacity:1;transform:translateY(0) scale(1)}}@keyframes mindSlide{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}\n@media(max-width:640px){.sch-bg.mindmap{padding:20px 10px}.mind-layout{grid-template-columns:1fr;gap:22px}.mind-layout:before{display:none}.mind-branches{grid-template-columns:1fr;gap:10px}.mind-branches:before{display:none}.mind-connector{display:none}.mind-branch .mind-node{margin-left:0;width:100%}.mind-main{max-width:100%}.mind-detail{grid-template-columns:1fr;gap:2px}}\n.mind-layout:before,.mind-branches:before,.mind-connector,.mind-child:before,.mind-branch.branch-open>.mind-children.open:before,.mind-child.branch-open>.mind-children.open:before{display:none!important}\n.mind-layout{gap:30px}.mind-branches{gap:18px}.mind-branch{border:2px solid var(--node-border,#d4e6d5);border-radius:20px;background:var(--node-bg,#f6fbf6);padding:12px;box-shadow:0 7px 22px #263a3510}\n.mind-branch .mind-node{border:2px solid var(--node-border,#d4e6d5);border-left:6px solid var(--branch);background:#fff;box-shadow:0 4px 14px #263a3510}\n.mind-children,.mind-children.open,.mind-branch.branch-open>.mind-children.open,.mind-child.branch-open>.mind-children.open{border:0;margin:0;padding:0;gap:14px}\n.mind-branch.branch-open,.mind-child.branch-open{gap:18px;min-width:640px}\n.mind-child,.mind-child.branch-open{border:2px solid var(--node-border,#d4e6d5);background:var(--node-bg,#f6fbf6);border-radius:17px;padding:11px;box-shadow:0 4px 16px #263a3510}\n.mind-child.branch-open>.mind-branch-row{border:0;background:transparent;padding:0}\n.mind-child .mind-node{border:0;border-left:5px solid var(--branch);background:#fff;border-radius:11px;padding:9px 10px;box-shadow:none}\n.mind-child.branch-open>.mind-branch-row>.mind-node{background:#fff;border-left:5px solid var(--branch);padding:9px 10px}\n@media(max-width:640px){.mind-branch.branch-open,.mind-child.branch-open{grid-template-columns:1fr;min-width:0;gap:12px}.mind-layout{gap:18px}.mind-branch{padding:9px}.mind-child{padding:8px}}\n\n.sch-ed .card{padding:14px}\n.sch-fr{display:flex;gap:8px;margin-bottom:6px}\n.sch-fr input{flex:1;min-width:0;padding:8px 10px;border:1px solid var(--b);border-radius:14px;font-size:13px;font-family:inherit;background:var(--bg)}\n.sch-fr input:first-child{max-width:150px}\n\n\n.les-grid{display:grid;grid-template-columns:1.25fr 1fr;gap:14px;align-items:start}\n@media(max-width:820px){.les-grid{grid-template-columns:1fr}}\n.les-frame{width:100%;border:1px solid var(--b);border-radius:16px;background:#fff;display:block}\n.les-code{background:#0f172a;color:#e2e8f0;border-radius:16px;padding:14px;font:12.5px/1.55 ui-monospace,Menlo,Consolas,monospace;max-height:520px;overflow:auto;white-space:pre;tab-size:2}\n.les-ta{width:100%;min-height:200px;padding:10px 12px;border:1px solid var(--b);border-radius:16px;font:12.5px/1.5 ui-monospace,Menlo,Consolas,monospace;background:var(--bg);white-space:pre;overflow:auto;resize:vertical}\n\n.ovl{position:fixed;inset:0;background:rgba(15,23,42,.55);z-index:9999;overflow:auto;padding:20px 12px}\n.ovl .box{max-width:760px;margin:0 auto;background:var(--c);border-radius:22px;padding:20px}\n.opts{display:flex;flex-direction:column;gap:7px}\n.op{display:flex;align-items:flex-start;gap:10px;padding:11px 12px;border:2px solid var(--b);border-radius:22px;cursor:pointer;transition:.15s}\n.op:hover{border-color:#93c5fd;background:#f8fafc}\n.op.sel{border-color:var(--p);background:#eff6ff}\n.ol{width:24px;height:24px;border-radius:50%;background:var(--bg);display:flex;align-items:center;justify-content:center;font-weight:600;font-size:11px;flex-shrink:0;color:var(--m)}\n.op.sel .ol{background:var(--p);color:#fff}\n.ot{flex:1;padding-top:1px;font-size:13px}\n.navb{display:flex;justify-content:space-between;gap:10px}\n.score-c{width:120px;height:120px;border-radius:50%;background:linear-gradient(135deg,#2563eb,#3b82f6);color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;margin:16px auto;font-size:34px;font-weight:700;box-shadow:0 6px 24px rgba(37,99,235,.25)}\n.score-c small{font-size:13px;font-weight:400;opacity:.85}\n.res-row{display:flex;justify-content:space-between;padding:11px 14px;border-bottom:1px solid var(--b);font-size:14px}\n.res-row:last-child{border-bottom:none}\n.rev{background:var(--c);border-radius:22px;padding:14px;margin-bottom:10px;border-left:4px solid var(--b)}\n.rev.ok{border-left-color:var(--ok)}.rev.bad{border-left-color:var(--err)}\n.rev .rh{display:flex;justify-content:space-between;margin-bottom:6px;font-size:11px;color:var(--m)}\n.rev .rq{font-weight:500;margin-bottom:8px;font-size:13px}\n.rev .ra{font-size:12px;padding:6px 10px;border-radius:17px;margin-bottom:4px}\n.rev .ra.u{background:#fef2f2}.rev .ra.c{background:#f0fdf4}\n.switch{display:flex;align-items:center;gap:8px;font-size:13px}\n.switch input{width:18px;height:18px;accent-color:var(--p)}\n@media(max-width:768px){\n  .grid2{grid-template-columns:1fr}\n  .side{position:fixed;top:0;left:-100%;z-index:100;transition:left .3s;width:80%;max-width:280px}\n  .side.open{left:0}.side-tog{display:block}\n  .tmain{padding:12px}.timer{font-size:18px}\n}\n\nbody.locked{user-select:none;-webkit-user-select:none}\nbody:not(.primary-owner){user-select:none;-webkit-user-select:none;-webkit-touch-callout:none}\nbody:not(.primary-owner) input,body:not(.primary-owner) textarea{user-select:text;-webkit-user-select:text}\nimg,svg{-webkit-user-drag:none}\nbody.shield #app-shield-target,body.shield .screen{filter:blur(28px) brightness(.4);pointer-events:none}\n.name-warn{background:#fef2f2;border:2px solid #dc2626;color:#7f1d1d;border-radius:22px;padding:14px 16px;font-size:16px;line-height:1.5;margin-bottom:16px}\n.name-warn .nw-t{font-size:19px;font-weight:800;margin-bottom:4px;display:block}\nbody.dark .name-warn{background:#450a0a;color:#fecaca;border-color:#ef4444}\n#wm{position:fixed;inset:0;z-index:99998;pointer-events:none;background-repeat:repeat;display:none}\n#shield-msg{display:none;position:fixed;inset:0;z-index:100001;align-items:center;justify-content:center;text-align:center;color:#fff;font-weight:700;font-size:18px;padding:24px;background:rgba(15,23,42,.55)}\nbody.shield #shield-msg{display:flex}\n@media print{body *{display:none!important}body:before{content:"Басып шығаруға тыйым салынған";display:block;font-size:24px;padding:40px}}\n#lock-ov{display:none;position:fixed;inset:0;z-index:100000;background:rgba(15,23,42,.97);color:#fff;align-items:center;justify-content:center;text-align:center;padding:24px}\n#lock-ov.show{display:flex}\n#lock-ov .box{max-width:440px}\n#lock-ov h2{margin:10px 0}\n#lock-ov p{opacity:.85;margin-bottom:18px;font-size:14px}\n.stat-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:12px}\n.stat{background:var(--bg);border-radius:20px;padding:10px;text-align:center}\n.stat b{display:block;font-size:20px;color:var(--p)}\n.stat span{font-size:11px;color:var(--m)}\n.chart-wrap{overflow-x:auto}\n.tbar{display:flex;align-items:center;gap:8px;font-size:12px;margin:7px 0}\n.tbar .tn{width:38%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}\n.tbar .tb{flex:1;background:#e2e8f0;border-radius:20px;height:10px;overflow:hidden}\n.tbar .tb i{display:block;height:100%;background:var(--p);border-radius:20px}\n.tbar .tv{width:44px;text-align:right;font-weight:600}\n@media(max-width:768px){.stat-grid{grid-template-columns:repeat(2,1fr)}}\n\n#theme-btn{position:fixed;right:12px;bottom:12px;z-index:90;width:42px;height:42px;border-radius:50%;padding:0;font-size:18px;box-shadow:0 2px 10px rgba(0,0,0,.18)}\nbody.in-test #theme-btn{display:none}\n#confetti{position:fixed;left:0;top:0;width:100%;height:var(--vh);pointer-events:none;z-index:99990}\n.chips{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px}\n.chip{background:var(--c);border:1px solid var(--b);border-radius:24px;padding:6px 14px;font-size:13px}\n.btn.btn-chip{border-radius:18px!important}\n.chip.warn{background:#fef3c7;color:#92400e;border-color:#fcd34d}\n.quote{background:linear-gradient(135deg,#eff6ff,#f5f3ff);border-left:4px solid var(--p);border-radius:22px;padding:12px 14px;font-size:14px;font-style:italic;margin:10px 0;color:#1e293b;cursor:pointer}\n.qotd-op{display:flex;gap:10px;align-items:flex-start;padding:10px 12px;border:2px solid var(--b);border-radius:22px;cursor:pointer;margin-bottom:7px;font-size:13px}\n.qotd-op:hover{border-color:#93c5fd}\n.qotd-op.ok{border-color:var(--ok);background:#dcfce7;color:#14532d}\n.qotd-op.bad{border-color:var(--err);background:#fee2e2;color:#7f1d1d}\n.qotd-op.lock{cursor:default}\n.fcard{background:var(--c);border:2px solid var(--b);border-radius:26px;min-height:240px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:26px 20px;cursor:pointer;position:relative;animation:flipin .25s}\n.fcard.back{border-color:var(--p);background:#eff6ff;color:#0f172a}\n.fcard .flab{position:absolute;top:12px;left:16px;font-size:11px;font-weight:700;color:var(--m);text-transform:uppercase}\n.fcard .ftxt{font-size:20px;font-weight:600;line-height:1.5}\n.fcard .fhint{position:absolute;bottom:10px;font-size:11px;color:var(--m)}\n@keyframes flipin{from{transform:rotateX(70deg);opacity:.3}to{transform:none;opacity:1}}\n.podium{display:flex;align-items:flex-end;justify-content:center;gap:10px;margin:8px 0 20px}\n.pod{flex:1;max-width:150px;text-align:center;min-width:0}\n.pod .pcup{font-size:38px;line-height:1.1}\n.pod.p1 .pcup{font-size:56px;animation:bob 2s ease-in-out infinite}\n@keyframes bob{50%{transform:translateY(-6px)}}\n.pod .pname{font-weight:700;font-size:13px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}\n.pod .ppts{font-size:12px;color:var(--m)}\n.pod .pbase{border-radius:20px 10px 0 0;color:#fff;font-weight:800;padding-top:8px;margin-top:6px;font-size:18px}\n.pod.p1 .pbase{background:linear-gradient(#fbbf24,#f59e0b);height:84px}\n.pod.p2 .pbase{background:linear-gradient(#cbd5e1,#94a3b8);height:62px}\n.pod.p3 .pbase{background:linear-gradient(#fdba74,#c2763a);height:46px}\n.item.me{border-color:var(--p);background:#eff6ff;color:#0f172a}\n.item.me .info p{color:#475569}\n.plan-day{background:var(--c);border:1px solid var(--b);border-radius:22px;padding:10px 14px;margin-bottom:8px}\n.plan-day.today{border-color:var(--p);box-shadow:0 0 0 2px rgba(37,99,235,.15)}\n.plan-day h4{font-size:13px;margin-bottom:6px}\n.plan-day label{display:flex;gap:8px;align-items:flex-start;font-size:13px;margin-bottom:4px;cursor:pointer}\n.plan-day label.done span{text-decoration:line-through;opacity:.55}\n.ttable{width:100%;border-collapse:collapse;font-size:13px}\n.ttable th,.ttable td{padding:8px 6px;border-bottom:1px solid var(--b);text-align:left;vertical-align:middle}\n.ttable th{font-size:11px;color:var(--m);text-transform:uppercase}\n.tscroll{overflow-x:auto}\n.gl-item{background:var(--c);border:1px solid var(--b);border-radius:22px;padding:12px 14px}\n.gl-item h4{font-size:14px;margin-bottom:3px}\n.gl-item p{font-size:13px;color:var(--t)}\n.gl-cat{font-size:10px;font-weight:700;color:var(--p);text-transform:uppercase;letter-spacing:.5px}\n.katex{font-size:1.05em}\n.katex-display{overflow-x:auto;overflow-y:hidden}\n\n\n\n.bs-folder{border:1px solid var(--b);border-radius:18px;background:var(--c);margin:10px 0;overflow:hidden}\n.bs-folder summary{cursor:pointer;list-style:none;padding:16px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}\n.bs-folder summary::-webkit-details-marker{display:none}\n.bs-folder > summary:after{content:\'▾\';margin-left:auto;color:var(--m)}\n.bs-folder[open] > summary:after{content:\'▴\'}\n.bs-folder > summary > strong{flex:1;min-width:0;overflow-wrap:anywhere}\n.bs-folder-count{font-size:12px;color:var(--m);margin-left:4px}\n.bs-folder-items{padding:8px 12px 12px;border-top:1px solid var(--b)}\n.bs-folder-items .ubt-bank-row:last-child{margin-bottom:0}\n\n\nbody.dark{--bg:#0b1220;--c:#162033;--t:#e5e7eb;--m:#9aa8bd;--b:#2b3a52;--p:#3b82f6;--pd:#2563eb;color-scheme:dark}\nbody.dark .prog-t,body.dark .timer,body.dark .qnum{background:#1e3a5f;color:#93c5fd}\nbody.dark .timer.warn{background:#3b2f0b;color:#fbbf24}\nbody.dark .timer.dang{background:#3f1515;color:#f87171}\nbody.dark .qn.cur{background:#1e3a5f}\nbody.dark .qn.ans{background:#14532d;color:#86efac;border-color:#166534}\nbody.dark .qn.flg{background:#422006;border-color:#a16207}\nbody.dark .op:hover{background:#1e293b}\nbody.dark .op.sel{background:#1e3a5f}\nbody.dark .rev .ra.u{background:#3f1515}\nbody.dark .rev .ra.c{background:#12301f}\nbody.dark .badge-pub{background:#1e3a5f}\nbody.dark .badge-priv{background:#1e293b}\nbody.dark .prog-w,body.dark .tbar .tb{background:#2b3a52}\nbody.dark .flag.on{background:#422006}\nbody.dark .quote{background:linear-gradient(135deg,#16233a,#1d1a38);color:#e5e7eb}\nbody.dark .fcard.back{background:#16233a;color:#e5e7eb}\nbody.dark .item.me{background:#16233a;color:#e5e7eb}\nbody.dark .item.me .info p{color:#9aa8bd}\nbody.dark .chip.warn{background:#422006;color:#fcd34d;border-color:#a16207}\nbody.dark .qotd-op.ok{background:#12301f;color:#bbf7d0}\nbody.dark .qotd-op.bad{background:#3f1515;color:#fecaca}\nbody.dark [style*="background:#eff6ff"],body.dark [style*="background:#f1f5f9"],body.dark [style*="background:#f0fdf4"],body.dark [style*="background:#fef2f2"],body.dark [style*="background:#fef3c7"],body.dark [style*="background:#dbeafe"],body.dark [style*="background:#f8fafc"],body.dark [style*="background:#fffbeb"]{background:#1e293b!important;color:#e5e7eb!important}\nbody.dark #contact-box,body.dark #contact-box *{color:#111}\nbody.dark #contact-box [style*="background:#075e54"] *,body.dark #contact-box [style*="background:#075e54"]{color:#fff}\nbody.dark #admin-chat input,body.dark #admin-chat textarea{color:#111}\n.cbox{margin-top:8px}\n.cmsgs{height:260px;overflow-y:auto;background:var(--bg);border:1px solid var(--b);border-radius:22px;padding:10px;display:flex;flex-direction:column;gap:6px}\n.cmsg{max-width:82%;padding:7px 11px;border-radius:22px;font-size:13px;white-space:pre-wrap;word-break:break-word}\n.cmsg.me{align-self:flex-end;background:var(--p);color:#fff}\n.cmsg.other{align-self:flex-start;background:var(--c);border:1px solid var(--b)}\n.cmsg.sys{align-self:center;background:#fef3c7;color:#92400e;font-size:12px;text-align:center}\n.cmsg small{display:block;opacity:.7;font-size:10px;margin-top:2px}\n.crow{display:flex;gap:8px;margin-top:8px}\n.crow input{flex:1;padding:10px 12px;border:1px solid var(--b);border-radius:20px;background:var(--bg);color:var(--t);font-family:inherit;font-size:14px}\nbody.dark .cmsg.sys{background:#422006;color:#fcd34d}\n\n\n:root{--r:28px;--sh:0 6px 24px rgba(30,41,59,.07);--grad:linear-gradient(135deg,#2563eb,#7c3aed)}\nbody{background:radial-gradient(900px 420px at 0% -5%,rgba(37,99,235,.14),transparent 60%),radial-gradient(800px 420px at 100% 0%,rgba(124,58,237,.13),transparent 55%),var(--bg);background-attachment:fixed}\nbody.dark{background:radial-gradient(900px 420px at 0% -5%,rgba(59,130,246,.16),transparent 60%),radial-gradient(800px 420px at 100% 0%,rgba(139,92,246,.14),transparent 55%),var(--bg);background-attachment:fixed}\n.topback{background:color-mix(in srgb,var(--bg) 90%,transparent);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px)}\n.screen.active{animation:scrIn .25s ease}\n@keyframes scrIn{from{opacity:0}to{opacity:1}}\n.hdr h1,.hdr h2{letter-spacing:-.3px}\n.card{border-radius:var(--r);box-shadow:var(--sh);border-color:rgba(148,163,184,.28)}\n.btn{border-radius:22px}\n.btn:active{transform:scale(.98)}\n.btn-p{background:var(--grad);box-shadow:0 4px 14px rgba(37,99,235,.28)}\n.btn-p:hover{background:var(--grad);filter:brightness(1.08);transform:translateY(-1px)}\n.btn-s{box-shadow:0 1px 3px rgba(15,23,42,.06)}\n.mode{border-radius:var(--r);border:1px solid rgba(148,163,184,.3);box-shadow:var(--sh);position:relative;overflow:hidden}\n.mode::before{content:\'\';position:absolute;left:0;right:0;top:0;height:4px;background:var(--grad);opacity:0;transition:.2s}\n.mode:hover::before{opacity:1}\n.mode .ic{width:58px;height:58px;border-radius:24px;background:linear-gradient(135deg,rgba(37,99,235,.12),rgba(124,58,237,.16));display:flex;align-items:center;justify-content:center;margin:0 auto 10px;font-size:28px}\n.home-tools{grid-template-columns:repeat(2,minmax(0,1fr));margin-bottom:12px}\n.home-tools .mode{width:100%;font-family:inherit;color:var(--t);min-height:150px}\n.home-tools .mode h3{line-height:1.35}\n.home-tools .mode p{line-height:1.4}\n@media(max-width:520px){.home-tools{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.home-tools .mode{min-height:135px;padding:14px 8px}.home-tools .mode h3{font-size:13px}}\n.exam-entry{grid-template-columns:repeat(2,minmax(0,1fr));margin-bottom:18px}\n.exam-entry .mode{min-height:172px;text-align:left;padding:22px;border-color:rgba(59,130,246,.27);background:linear-gradient(135deg,rgba(37,99,235,.10),rgba(124,58,237,.08)),var(--c)}\n.exam-entry .mode:nth-child(2){background:linear-gradient(135deg,rgba(16,185,129,.11),rgba(37,99,235,.08)),var(--c)}\n.exam-entry .mode .ic{margin:0 0 12px;border-radius:18px}\n.exam-entry .mode h3{font-size:18px}\n.exam-entry .mode p{font-size:13px;margin-top:4px}\n.exam-entry .mode:focus-visible,.subject-choice:focus-visible{outline:3px solid var(--p);outline-offset:3px}\n.subject-choices{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:9px;margin:14px 0 18px}\n.subject-choice{display:flex;align-items:flex-start;gap:10px;min-width:0;padding:12px;border:1px solid var(--b);border-radius:18px;background:var(--c);color:var(--t);text-align:left;cursor:pointer;font:inherit;transition:.2s}\n.subject-choice:hover,.subject-choice.selected{border-color:var(--p);background:linear-gradient(120deg,rgba(37,99,235,.12),rgba(124,58,237,.07));box-shadow:0 2px 10px rgba(37,99,235,.10)}\n.subject-choice .subject-mark{font-size:21px;line-height:1.2}\n.subject-choice strong{display:block;font-size:12px;line-height:1.4;overflow-wrap:anywhere}\n.subject-choice small{display:block;font-size:11px;color:var(--m);margin-top:3px}\n@media(max-width:700px){.subject-choices{grid-template-columns:repeat(2,minmax(0,1fr))}}\n@media(max-width:440px){.exam-entry .mode{min-height:156px;padding:15px}.exam-entry .mode h3{font-size:15px}.exam-entry .mode p{font-size:11px}.subject-choice{padding:10px;gap:7px}}\n.uv-actions{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}\n.uv-actions .btn{width:100%;min-height:48px;padding:10px 12px;text-align:center;font-size:13px;line-height:1.3}\n.uv-actions .uv-danger{grid-column:1/-1}\n@media(max-width:600px){.uv-actions{grid-template-columns:repeat(2,minmax(0,1fr))}}\n.ubt-modes{display:flex;gap:10px;flex-wrap:wrap;margin:12px 0}\n.ubt-modes label{display:flex;align-items:center;gap:8px;padding:11px 14px;border:1px solid var(--b);border-radius:18px;cursor:pointer;background:var(--c);font-size:14px;font-weight:600}\n.ubt-modes input{accent-color:var(--p);width:18px;height:18px}\n.ubt-bank-row{display:flex;gap:12px;align-items:flex-start;border:1px solid var(--b);border-radius:18px;padding:12px;margin-bottom:8px;background:var(--c)}\n.ubt-bank-row input[type=checkbox]{width:20px;height:20px;accent-color:var(--p);flex:none;margin-top:2px;cursor:pointer}\n.ubt-bank-row .info{min-width:0;flex:1}\n.ubt-bank-row .info strong{display:block;font-size:14px;overflow-wrap:anywhere}\n.ubt-bank-row .info p{font-size:12px;color:var(--m);margin-top:3px;overflow-wrap:anywhere}\n.profile-bar{border-radius:0 0 var(--r) var(--r);box-shadow:0 4px 18px rgba(30,41,59,.07);border-bottom:none}\nbody.has-app-header{padding-top:var(--app-header-height,76px)}\n.profile-bar.app-header{position:fixed;top:0;left:0;right:0;width:100%;z-index:160;margin:0;gap:12px;flex-wrap:wrap;background:var(--c)}\n.app-header .app-back-slot{display:flex;align-items:center;flex:none}\n.app-header .topback{position:static!important;transform:none!important;background:transparent;padding:0;margin:0;backdrop-filter:none;-webkit-backdrop-filter:none}\n.app-header .app-profile{flex:1;min-width:0}.app-header .app-profile .name{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}\n@media(max-width:520px){.profile-bar.app-header{gap:7px;padding:9px 10px}.app-header .app-profile{gap:6px!important}.app-header .app-profile .avatar{width:36px!important;height:36px!important}.app-header .app-profile [style*="margin-left:8px"]{margin-left:0!important;padding:3px 6px!important}.app-header .app-back-slot .btn{padding:7px 10px;font-size:12px}}\n.avatar{background:var(--grad);background-size:cover;background-position:center;box-shadow:0 2px 8px rgba(37,99,235,.3);flex-shrink:0;overflow:hidden}\n.item{border-radius:22px;box-shadow:0 2px 8px rgba(30,41,59,.04);transition:.15s}\n.item[onclick]:hover{transform:translateY(-2px);box-shadow:var(--sh);border-color:#93c5fd}\n.item.rk.r1{background:linear-gradient(90deg,rgba(251,191,36,.20),var(--c) 70%);border-color:#fbbf24}\n.item.rk.r2{background:linear-gradient(90deg,rgba(148,163,184,.24),var(--c) 70%);border-color:#cbd5e1}\n.item.rk.r3{background:linear-gradient(90deg,rgba(194,118,58,.20),var(--c) 70%);border-color:#e0a46f}\n.item.rk.me{box-shadow:0 0 0 2px var(--p)}\n.stat{border-radius:22px;background:linear-gradient(135deg,rgba(37,99,235,.07),rgba(124,58,237,.08))}\n.tbar .tb i,.prog-f{background:var(--grad)}\n.score-c{background:var(--grad)}\n.pod .avatar{margin:0 auto;border:3px solid #fff}\n.pod.p1 .pbase{box-shadow:0 8px 20px rgba(245,158,11,.35)}\n.pod{cursor:pointer}\n.fg input:focus,.fg select:focus,.fg textarea:focus{outline:none;border-color:var(--p);box-shadow:0 0 0 3px rgba(37,99,235,.15);background:var(--c)}\n#s-profile .hdr,#s-pubprof .hdr{background:var(--grad);color:#fff;border-radius:28px;padding:26px 16px 22px;box-shadow:0 12px 32px rgba(79,70,229,.35);position:relative;overflow:hidden}\n#s-profile .hdr::after,#s-pubprof .hdr::after{content:\'\';position:absolute;width:220px;height:220px;border-radius:50%;background:rgba(255,255,255,.10);right:-60px;top:-80px}\n#s-profile .hdr>*,#s-pubprof .hdr>*{position:relative;z-index:1}\n#s-profile .hdr .sub,#s-pubprof .hdr .sub{color:rgba(255,255,255,.88)}\n#s-profile .hdr [style*="color:var(--p)"]{color:#fff!important}\n#s-profile .hdr .avatar,#s-pubprof .hdr .avatar{border-color:rgba(255,255,255,.75)!important;box-shadow:0 6px 20px rgba(0,0,0,.25)}\n.ro-note{background:linear-gradient(135deg,#eff6ff,#f5f3ff);border-style:dashed;font-size:13px;text-align:center;color:#334155}\nbody.dark .ro-note{background:linear-gradient(135deg,#16233a,#1d1a38);color:#cbd5e1}\n@media(max-width:768px){.mode{padding:16px 10px}.mode .ic{width:48px;height:48px;font-size:24px}}\n\n\n.ubt-instant-switch{display:flex;gap:14px;align-items:flex-start;padding:16px;border:1px solid var(--b);border-radius:16px;background:var(--bg);cursor:pointer}\n.ubt-instant-switch input{width:22px;height:22px;flex:none;accent-color:var(--p)}\n.ubt-instant-switch strong{display:block;font-size:15px}.ubt-instant-switch small{display:block;color:var(--m);margin-top:5px;line-height:1.5}\n.op.ubt-correct{border-color:#16a34a!important;background:#dcfce7!important;color:#14532d!important}\n.op.ubt-incorrect{border-color:#dc2626!important;background:#fee2e2!important;color:#7f1d1d!important}\n.op.ubt-correct .ol{background:#16a34a;color:white}.op.ubt-incorrect .ol{background:#dc2626;color:white}\n.ubt-mark{font-size:12px;font-weight:800;margin-left:auto;white-space:nowrap}\n.ubt-feedback{margin-top:12px;padding:14px;border-radius:14px;font-size:14px;line-height:1.6}\n.ubt-feedback.yes{background:#dcfce7;color:#14532d}.ubt-feedback.no{background:#fee2e2;color:#7f1d1d}\n.ubt-feedback span{display:block;margin-top:4px}\nbody.dark .op.ubt-correct,body.dark .ubt-feedback.yes{background:#123c29!important;color:#bbf7d0!important}\nbody.dark .op.ubt-incorrect,body.dark .ubt-feedback.no{background:#451b23!important;color:#fecaca!important}\n\n\n:root{--p:#6257ed;--pd:#4f46d5;--bg:#f5f6fc;--c:#fff;--t:#18213a;--m:#68758d;--b:#e6e9f3;--grad:linear-gradient(125deg,#6257ed,#9460f3);--ok:#159d73;--err:#e04e65;--warn:#f0a22c}\nbody{background:radial-gradient(ellipse at 12% 0%,#eae8ff 0%,transparent 34%),radial-gradient(ellipse at 92% 14%,#e5f4ff 0%,transparent 32%),var(--bg);font-family:\'Inter\',system-ui,sans-serif;letter-spacing:-.012em}\n.wrap{max-width:980px;padding:38px 22px 120px}.wrap.wide{max-width:1320px}\n.hdr{margin-bottom:30px}.hdr h1{font-size:clamp(25px,3vw,35px);font-weight:800;letter-spacing:-.045em}.hdr h2{font-size:clamp(21px,2.5vw,29px);font-weight:800;letter-spacing:-.035em}\n.logo{width:80px;height:80px;border-radius:25px;background:var(--grad);box-shadow:0 14px 32px #6257ed45}\n.card,.item,.mode,.qc,.rev,.plan-day,.gl-item,.stat,.fcard{border:1px solid var(--b);border-radius:22px;box-shadow:0 6px 25px rgba(28,38,84,.045)}\n.card{padding:23px;margin-bottom:16px}.card h3{font-weight:750;font-size:17px}.item{padding:17px 19px}.item:hover,.mode:hover{border-color:#bbb6fb;box-shadow:0 12px 34px #6257ed18;transform:translateY(-2px)}\n.mode{padding:28px 20px;transition:transform .2s,box-shadow .2s,border-color .2s}.mode .ic{font-size:34px}.mode h3{font-size:16px}\n.btn{border-radius:13px;padding:11px 19px;font-weight:650;transition:transform .18s,box-shadow .18s,background .18s}.btn:hover:not(:disabled){transform:translateY(-1px)}.btn-p{background:var(--grad);box-shadow:0 5px 14px #6257ed30}.btn-p:hover{background:linear-gradient(125deg,#5147d8,#8051db);box-shadow:0 9px 22px #6257ed40}.btn-s{background:var(--c);border-color:var(--b)}.btn-sm{border-radius:10px;padding:8px 12px}\n.fg label{font-size:12px;color:var(--m);font-weight:700}.fg input,.fg select,.fg textarea,.sch-fr input{border-radius:12px;background:var(--c);padding:12px 14px;transition:border-color .2s,box-shadow .2s}.fg input:focus,.fg select:focus,.fg textarea:focus{border-color:#8d84f7;box-shadow:0 0 0 4px #6257ed17}\n.profile-bar{border-bottom-color:var(--b);padding:16px 22px;background:color-mix(in srgb,var(--c) 93%,transparent)}.avatar{background:var(--grad);box-shadow:0 3px 12px #6257ed30}\n.side{background:var(--c);border-right-color:var(--b)}.side-h{padding:18px}.qn{border-radius:12px}.qn.cur{background:#efedff;border-color:#b9b3ff;color:var(--p)}.qn.ans{background:#e0f7ed;border-color:#91d9b8;color:#117b58}\n.qc{padding:27px}.qt{font-size:17px;font-weight:550;line-height:1.75}.op{border-radius:15px;padding:14px 16px}.op.sel{background:#f0eeff;border-color:var(--p)}.ol{width:28px;height:28px}.timer,.prog-t,.qnum{background:#eeecff;color:var(--p)}.prog-f,.tbar .tb i{background:var(--grad)}\n.stat{padding:17px;background:var(--c)}.stat b{font-size:25px}.stat span{font-size:12px}.score-c{background:var(--grad);box-shadow:0 12px 30px #6257ed38}.badge{border-radius:9px;padding:5px 10px}\n.ovl{background:#10162ab8;backdrop-filter:blur(7px)}.ovl .box{border:1px solid var(--b);border-radius:24px;box-shadow:0 24px 80px #10162a40}\n.chip{border-radius:12px}.quote{border-radius:17px;background:linear-gradient(120deg,#efedff,#f4f1ff);border-left-color:var(--p)}\nbody.dark{--bg:#0c1020;--c:#171e31;--t:#f0f2ff;--m:#a0abc2;--b:#2c3650;--p:#a69bff;--pd:#8e82f7;--grad:linear-gradient(125deg,#6257ed,#8b5cf6);color-scheme:dark}\nbody.dark{background:radial-gradient(ellipse at 12% 0%,#1e1b43 0%,transparent 34%),var(--bg)}body.dark .card,body.dark .item,body.dark .mode,body.dark .qc{box-shadow:0 8px 28px #0002}body.dark .op.sel{background:#29234d}body.dark .qn.cur{background:#29234d;color:#c5beff}\n@media(max-width:768px){.wrap{padding:20px 13px 105px}.card{padding:17px}.item{padding:13px 14px}.mode{padding:19px 12px}.qc{padding:19px}.tmain{padding:13px}.hdr h1{font-size:26px}.stat{padding:12px}.btn{padding:10px 14px}}\n@media(prefers-reduced-motion:reduce){.btn,.mode,.item{transition:none!important;animation:none!important}}\n\n\n.ubt-cert-btn{background:linear-gradient(110deg,#047857,#0d9488);color:#fff}\n\n\n\nbody,body.dark{background:var(--bg);isolation:isolate}\nbody::before{content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;background-color:#dce9fb;background-image:linear-gradient(135deg,rgba(242,247,255,.76),rgba(235,239,255,.60)),url("https://img.magnific.com/free-vector/network-connection-background-gradient_23-2148879893.jpg?semt=ais_incoming&w=740&q=80");background-position:center;background-size:cover;background-repeat:no-repeat}\nbody.dark::before{background-color:#0c1429;background-image:linear-gradient(135deg,rgba(8,15,35,.56),rgba(14,12,40,.66)),url("https://img.magnific.com/free-vector/network-connection-background-gradient_23-2148879893.jpg?semt=ais_incoming&w=740&q=80")}\n#s-login > .wrap{max-width:520px;min-height:100vh;display:flex;flex-direction:column;justify-content:center;padding:54px 22px 70px}\n#s-login .ubt-welcome{margin-bottom:30px;text-align:center}\n.ubt-brand-label{font-size:10px;font-weight:700;letter-spacing:.24em;color:var(--m);margin-bottom:12px}\n#s-login .ubt-brand-title{font-size:clamp(44px,9vw,72px);font-weight:800;line-height:1.08;letter-spacing:-.055em;margin:0;color:#142651;text-shadow:0 2px 20px #ffffff60}\n#s-login .ubt-brand-title span{color:#6551df}\nbody.dark #s-login .ubt-brand-title{color:#f5f8ff;text-shadow:0 4px 24px #050b2470}\nbody.dark #s-login .ubt-brand-title span{color:#b4a4ff}\n.ubt-brand-line{width:72px;height:4px;border-radius:4px;background:linear-gradient(90deg,#38bdf8,#8b5cf6);margin:18px auto}\n#s-login .card{border-radius:26px;padding:26px;box-shadow:0 16px 48px #18294b20}\n#s-login .ubt-welcome .sub{font-size:13px}\n@media(max-width:480px){#s-login > .wrap{padding:36px 16px 50px}#s-login .card{padding:20px}.ubt-brand-label{letter-spacing:.15em}}\n\n\n/* Existing visual tokens, cards, buttons and exam layout are retained. */\n:root{--p:#4655dc;--pd:#3443c1;--grad:linear-gradient(120deg,#4655dc,#8874e8)}\nhtml,body{height:auto;min-height:0!important}body{margin:0;padding:0;background:var(--bg);font-family:Inter,system-ui,-apple-system,Arial,sans-serif;color:var(--t)}\nbody.dark{background:radial-gradient(ellipse at 85% 0%,#1b2850 0%,transparent 55%),linear-gradient(155deg,#111a2f,#080e1b);background-attachment:fixed;--bg:#0d1424;--c:#172136;--t:#edf2ff;--m:#a0acc4;--b:#2a3750}\nbutton,input,select{font:inherit}button{cursor:pointer}button:disabled{opacity:.55;cursor:wait}button:focus-visible,summary:focus-visible{outline:3px solid #99aaff;outline-offset:3px}\n[hidden]{display:none!important}.screen{display:none}.screen.active{display:block}.wrap{max-width:1120px;margin:0 auto;padding:25px 20px}.card{background:var(--c);border:1px solid var(--b);border-radius:18px;padding:24px;margin-bottom:18px;box-shadow:0 3px 14px #11182a06}.sub{color:var(--m);font-size:14px;line-height:1.6}\n.header{position:sticky;top:0;z-index:20;background:var(--c);border-bottom:1px solid var(--b);padding:12px 20px;display:flex;align-items:center;gap:12px}.brand{font-size:21px;font-weight:850;letter-spacing:-.7px}.badge{font-size:12px;border:1px solid var(--b);border-radius:20px;padding:6px 10px;color:var(--m)}.spacer{flex:1}.btn{border:1px solid transparent;border-radius:11px;padding:10px 16px;font-weight:650;font-size:14px;line-height:1.4;display:inline-flex;align-items:center;justify-content:center;gap:6px}.btn-p{background:var(--p);color:#fff}.btn-s{background:var(--bg);border-color:var(--b);color:var(--t)}.btn-d{background:#dc2626;color:#fff}.btn-sm{padding:7px 11px;font-size:12px}.row{display:flex;gap:10px;flex-wrap:wrap;align-items:center}.grid2{display:grid;grid-template-columns:1fr 1fr;gap:18px}\n.hero{background:linear-gradient(120deg,#1a2442,#283c69);border:1px solid #34496c;color:#fff;border-radius:22px;padding:30px;margin-bottom:24px}.hero h1{margin:12px 0 8px;font-size:30px;letter-spacing:-1px}.hero p{color:#b9c9e6;line-height:1.6}.hero .badge{border-color:#496086;color:#d5e6ff}.hero .btn-p{background:#67dfcb;color:#102e34}\n.mode-card{text-align:left;width:100%;min-height:140px;background:var(--c);border:1px solid var(--b);border-radius:18px;padding:23px;color:var(--t)}.mode-card h3{margin:12px 0 7px;font-size:19px}.mode-card:hover{border-color:var(--p)}.tabs{display:flex;gap:8px;flex-wrap:wrap;margin:18px 0}.tabs .selected{background:var(--p);border-color:var(--p);color:white}\ninput,select{width:100%;padding:11px 12px;border:1px solid var(--b);background:var(--bg);color:var(--t);border-radius:10px;box-sizing:border-box}label{display:block;font-size:13px;color:var(--m);margin:14px 0 5px}.formgrid{display:grid;grid-template-columns:1fr 1fr;gap:0 16px}.full{grid-column:1/-1}\n.folder{border:1px solid var(--b);border-radius:15px;background:var(--c);margin:12px 0;overflow:hidden}.folder>summary{padding:17px 18px;font-weight:750;cursor:pointer;list-style:none;display:flex;gap:10px;align-items:center}.folder>summary::before{content:\'▸\';color:var(--p)}.folder[open]>summary::before{content:\'▾\'}.folder-body{padding:0 18px 16px}.folder-bar{display:flex;gap:8px;align-items:center;flex-wrap:wrap;padding:8px 0 12px}.file{border:1px solid var(--b);border-radius:12px;margin:9px 0;background:var(--bg)}.file>summary{padding:14px;cursor:pointer;display:flex;align-items:center;gap:10px;list-style:none}.file-icon{display:flex;background:#7b86eb1c;color:var(--p);width:38px;height:44px;align-items:center;justify-content:center;border-radius:8px;font-size:10px;font-weight:850}.file-title{font-size:14px;font-weight:750;overflow-wrap:anywhere}.file-meta{font-size:12px;color:var(--m);margin-top:4px}.file-body{padding:0 15px 15px}.file-body .btn{margin:8px 0}.preview{border-top:1px solid var(--b);padding:15px 0}.preview p{white-space:pre-wrap;line-height:1.65}.qimg{display:block;width:auto;max-width:100%;height:auto;margin:16px auto;background:white;border-radius:8px}.muted-num{color:var(--m);font-size:12px}.empty{padding:35px;text-align:center;color:var(--m);border:1px dashed var(--b);border-radius:15px}.notice{background:#6476ff13;border:1px solid #6476ff33;color:var(--t);border-radius:12px;padding:14px;font-size:13px;line-height:1.6}\n#toast{position:fixed;z-index:100;bottom:20px;left:50%;transform:translateX(-50%);max-width:min(650px,90vw);padding:14px 20px;border-radius:12px;background:#1b2947;color:#fff;box-shadow:0 8px 30px #0004}\n#login{max-width:430px;margin:7vh auto}#login .brand{font-size:30px}.sidebar{position:fixed;inset:0 auto 0 0;width:270px;z-index:51;padding:22px;background:var(--c);border-right:1px solid var(--b);box-shadow:10px 0 50px #0003;box-sizing:border-box}.sidebar .btn{width:100%;justify-content:flex-start;margin-top:10px}.backdrop{position:fixed;inset:0;background:#0006;z-index:50}\n.exam-top{position:sticky;top:65px;z-index:15;background:var(--c);border:1px solid var(--b);border-radius:14px;padding:13px;margin-bottom:16px}.qnav{display:flex;flex-wrap:wrap;gap:6px;margin:13px 0;max-height:150px;overflow-y:auto}.qn{width:34px;height:33px;border-radius:8px;border:1px solid var(--b);background:var(--bg);color:var(--t);font-size:12px}.qn.answered{background:#dcebe5;color:#087b50;border-color:#a6d4be}.dark .qn.answered{background:#17483a;color:#acf5d4}.qn.marked{background:#fde4e4;color:#a81c1c;border-color:#f0a0a0}.qn.current{outline:2px solid var(--p);outline-offset:1px}.question-text{white-space:pre-wrap;font-size:18px;font-weight:650;line-height:1.8}.option{width:100%;display:flex;gap:12px;text-align:left;padding:15px 16px;margin:9px 0;background:var(--bg);color:var(--t);border:1px solid var(--b);border-radius:12px;line-height:1.6}.option.selected{border:2px solid var(--p);padding:14px 15px;background:#7180f018}.option.right{border-color:#16a34a;background:#16a34a18}.option.wrong{border-color:#dc2626;background:#dc262618}.option-letter{font-weight:800;color:var(--p)}.score{font-size:54px;font-weight:850;color:var(--p);letter-spacing:-2px}.result-row{display:flex;justify-content:space-between;gap:10px;border-bottom:1px solid var(--b);padding:13px 0}.tiny{font-size:12px;color:var(--m)}progress{width:100%;accent-color:var(--p);height:10px}\n@media(max-width:650px){.wrap{padding:16px 12px}.card{padding:18px}.grid2,.formgrid{grid-template-columns:1fr}.hero{padding:23px}.hero h1{font-size:25px}.header{padding:10px 12px;gap:8px}.header .badge{display:none}.brand{font-size:18px}.question-text{font-size:16px}.exam-top{top:58px}.folder-body{padding:0 10px 12px}.file>summary{padding:11px}.btn{padding:10px 12px}.qnav{max-height:125px}.question-card{padding:17px}}\n</style></head><body class="dark">\n<div id="toast" hidden role="status"></div>\n<header id="header" class="header" hidden><button class="btn btn-s btn-sm" onclick="menu(true)" aria-label="Мәзір">☰</button><span class="brand">ҰБТ<span style="color:var(--p)"> PLUS</span></span><span class="badge">Информатика + Математика</span><span class="spacer"></span><span id="who" class="tiny"></span><button id="theme-toggle" class="btn btn-s btn-sm" onclick="theme()" aria-label="Түнгі режимді ауыстыру">☾</button></header>\n<div id="shade" class="backdrop" hidden onclick="menu(false)"></div><aside id="menu" class="sidebar" hidden><div class="row"><span class="brand">ҰБТ PLUS</span><span class="spacer"></span><button class="btn btn-s btn-sm" onclick="menu(false)">✕</button></div><p class="tiny" style="margin:18px 0">ИНФО–МАТ БАҒЫТЫ</p><button class="btn btn-s" onclick="home()">⌂ Басты бет</button><button class="btn btn-s" onclick="exam140()">140 формат</button><button class="btn btn-s" onclick="library(\'public\')">▤ Ортақ тесттер</button><button class="btn btn-s" onclick="library(\'bank\')">▱ Сұрақтар базасы</button><button class="btn btn-s" onclick="uploadScreen()">↑ JSON жүктеу</button><button class="btn btn-s" onclick="subjectScreen()">▤ Пән бойынша</button><button class="btn btn-s" onclick="flashScreen()">▱ Флешкарталар</button><button id="admin-nav" class="btn btn-s" hidden onclick="adminScreen()">⚙ Админ</button><button id="theme-menu" class="btn btn-s" onclick="theme()">☾ Түнгі режим</button><button class="btn btn-s" onclick="logout()">Шығу</button></aside>\n<section id="s-login" class="screen active"><div id="login" class="card"><div class="brand">ҰБТ<span style="color:var(--p)"> PLUS</span></div><p class="sub" style="margin:12px 0 25px">Информатика + Математика</p><h2>Қош келдіңіз!</h2><form id="login-form"><label for="login-pass">Пароль</label><input id="login-pass" type="password" autocomplete="current-password" required maxlength="200"><p id="login-error" class="sub" role="alert" style="color:var(--err);margin:14px 0"></p><button class="btn btn-p" style="width:100%" type="submit">Кіру →</button></form><p class="tiny" style="margin-top:20px">Аккаунтты админ қосады.</p><button id="theme-login" class="btn btn-s" onclick="theme()" style="margin-top:12px;width:100%">☾ Түнгі режим</button></div></section>\n<section id="s-home" class="screen"><div class="wrap"><div class="hero"><span class="badge">ИНФО–МАТ</span><h1 id="hello">Қош келдіңіз!</h1><p>Бөлімді таңдаңыз. Пән бойынша дайындалыңыз немесе толық тест тапсырыңыз.</p><div class="row" style="margin-top:20px"><button class="btn btn-p" onclick="exam140()">140 форматты бастау →</button><button class="btn btn-s" onclick="library(\'public\')">Ортақ тесттер</button></div></div><div id="active-banner"></div><div class="grid2"><button class="mode-card" onclick="library(\'public\')"><span style="font-size:28px">▤</span><h3>Ортақ тесттер</h3><p class="sub">Админ жариялаған бөлімдер. Барлығына ортақ.</p></button><button class="mode-card" onclick="library(\'bank\')"><span style="font-size:28px">▱</span><h3>Сұрақтар базасы</h3><p class="sub">JSON тесттеріңіз. Бөліммен немесе жеке тапсыру.</p></button><button class="mode-card" onclick="subjectScreen()"><span style="font-size:28px">▤</span><h3>Пән бойынша</h3><p class="sub">Таңдаған пәніңізден тест тапсыру.</p></button><button class="mode-card" onclick="flashScreen()"><span style="font-size:28px">▱</span><h3>Флешкарталар</h3><p class="sub">Сұрақтарды қайталау және жаттау.</p></button></div></div></section>\n<section id="s-library" class="screen"><div class="wrap"><div class="row"><h2 id="library-title">Тесттер</h2><span class="spacer"></span><button class="btn btn-p" onclick="uploadScreen()">+ JSON қосу</button></div><div class="tabs"><button id="tab-public" class="btn btn-s" onclick="library(\'public\')">Ортақ тесттер</button><button id="tab-private" class="btn btn-s" onclick="library(\'bank\')">Сұрақтар базасы</button></div><div id="library-info" class="sub"></div><div class="row" style="margin:18px 0"><input id="search" type="search" placeholder="Бөлім немесе файл іздеу…" oninput="drawLibrary()" style="flex:1"><button class="btn btn-s" onclick="startFolder(\'\')">Барлығын тапсыру</button></div><div id="file-tree"></div></div></section>\n<section id="s-upload" class="screen"><div class="wrap"><button class="btn btn-s btn-sm" onclick="library(currentScope)">← Тесттерге</button><div class="card" style="margin-top:20px"><h2>JSON тесттерін сақтау</h2><p class="sub" style="margin-top:10px">Бөлім жолы: <b>1 бөлім/1.1</b>. Бірнеше JSON файлды бірге таңдауға болады. Ішінде tests немесе children бар JSON бөлімдерге автоматты бөлінеді.</p><form id="upload-form"><div class="formgrid"><div><label for="upload-scope">Қайда сақтау</label><select id="upload-scope"><option value="private">Сұрақтар базасы</option></select></div><div><label for="upload-subject">Пән</label><select id="upload-subject"></select></div><div class="full"><label for="upload-path">Бөлім / ішкі бөлім</label><input id="upload-path" placeholder="1 бөлім/1.1" maxlength="800" list="folder-paths"><datalist id="folder-paths"></datalist></div><div class="full"><label for="upload-files">JSON файлдары</label><input id="upload-files" type="file" accept=".json,application/json" multiple required></div></div><div class="notice" style="margin:16px 0">questions → text, options, correct. Дұрыс жауап 0-ден басталады. Сурет img өрісінде сақталады. Әр файл 1 ГБ-қа дейін.</div><div class="row"><button class="btn btn-p" type="submit">Файлдарды сақтау</button><button class="btn btn-s" type="button" onclick="createFolder()">Бос бөлім қосу</button></div><p id="upload-state" class="sub" style="margin:15px 0" role="status"></p><progress id="upload-progress" value="0" max="100" hidden></progress></form></div></div></section>\n<section id="s-exam" class="screen"><div class="wrap"><div class="exam-top"><div class="row"><strong id="exam-title"></strong><span class="spacer"></span><b id="exam-time"></b><button class="btn btn-p btn-sm" onclick="finishExam()">Аяқтау</button></div><div class="row" style="margin-top:10px"><select id="exam-sections" onchange="goQuestion(Number(this.value))" style="flex:1"></select><span id="exam-progress" class="tiny"></span></div><div class="row" style="margin-top:10px"><button class="btn btn-s btn-sm" onclick="navPage(-1)">‹</button><span id="nav-window" class="tiny"></span><button class="btn btn-s btn-sm" onclick="navPage(1)">›</button><span class="spacer"></span><span class="tiny">Қызыл — белгіленген</span></div><div id="qnav" class="qnav"></div></div><div class="card question-card"><div class="row"><span id="q-number" class="tiny"></span><span class="spacer"></span><button id="mark-button" class="btn btn-s btn-sm" onclick="markQuestion()">⚑ Белгілеу</button></div><div id="question" style="margin:18px 0"></div><div id="options"></div><div id="explanation" class="notice" hidden></div><div class="row" style="margin-top:20px"><button class="btn btn-s" id="previous-q" onclick="goQuestion(qIndex-1)">← Алдыңғы</button><span class="spacer"></span><button class="btn btn-p" id="next-q" onclick="goQuestion(qIndex+1)">Келесі →</button></div></div></div></section>\n<section id="s-result" class="screen"><div class="wrap"><div id="result-card" class="card"></div><div class="row"><button class="btn btn-p" onclick="home()">Басты бет</button><button class="btn btn-s" onclick="reviewExam()">Жауаптарды қарау</button></div></div></section>\n<section id="s-history" class="screen"><div class="wrap"><h2>Нәтижелерім</h2><div id="history-list" style="margin-top:20px"></div></div></section>\n<section id="s-admin" class="screen"><div class="wrap"><h2>Админ панелі</h2><div class="card" style="margin-top:20px"><h3>Қолданушылар</h3><div id="users-list"></div><details style="margin-top:18px"><summary>Адам қосу</summary><form id="user-form"><div class="formgrid"><div><label for="new-name">Аты-жөні</label><input id="new-name" required maxlength="80"></div><div><label for="new-login">Логин</label><input id="new-login" required minlength="2" maxlength="40"></div><div class="full"><label for="new-pass">Пароль · кемінде 10 таңба</label><input id="new-pass" type="password" minlength="10" maxlength="200" required autocomplete="new-password"></div></div><button class="btn btn-p" type="submit" style="margin-top:12px">Қосу</button><p id="user-state" role="status" class="sub"></p></form></details></div><div class="card"><h3>Кіру және шығу</h3><p class="tiny" style="margin:10px 0">Шығу уақыты «Шығу» батырмасы басылғанда тіркеледі. Терезе жабылса, соңғы белсенділік көрсетіледі.</p><div id="access-list"></div></div></div></section>\n<section id="s-subject" class="screen"><div class="wrap"><div class="card"><h2>Пән бойынша тест</h2><p class="sub" style="margin:12px 0">Сұрақтар ортақ тесттер мен сұрақтар базасынан алынады.</p><label for="subject-pick">Пән</label><select id="subject-pick"></select><label for="subject-count">Сұрақ саны</label><select id="subject-count"><option value="20">20 сұрақ</option><option value="40">40 сұрақ</option><option value="100">100 сұрақ</option><option value="all">Барлық сұрақ</option></select><button class="btn btn-p" style="margin-top:18px" onclick="startSubject()">Бастау →</button></div></div></section>\n<section id="s-flash" class="screen"><div class="wrap"><div class="row"><h2>Флешкарталар</h2><span class="spacer"></span><select id="flash-subject" style="max-width:260px" onchange="loadFlash(0)"></select></div><div class="card" style="margin-top:20px"><p id="flash-number" class="tiny"></p><div id="flash-front" style="margin:20px 0"></div><div id="flash-back" class="notice" hidden></div><div class="row" style="margin-top:20px"><button class="btn btn-s" onclick="flashMove(-1)">← Алдыңғы</button><button class="btn btn-p" onclick="flipFlash()">Жауабын ашу</button><button class="btn btn-s" onclick="flashMove(1)">Келесі →</button></div></div></div></section>\n<script>\n\'use strict\';\nconst $=id=>document.getElementById(id),esc=v=>String(v??\'\').replace(/[&<>"\']/g,c=>({\'&\':\'&amp;\',\'<\':\'&lt;\',\'>\':\'&gt;\',\'"\':\'&quot;\',"\'":\'&#39;\'}[c]));\nconst names={history:\'Қазақстан тарихы\',reading:\'Оқу сауаттылығы\',mathlit:\'Математикалық сауаттылық\',math:\'Математика\',informatics:\'Информатика\'};\nlet token=localStorage.getItem(\'ubt_files_token\')||\'\',user=null,meta={folders:[],files:[],users:[]},active=null,currentScope=\'public\',screen=\'s-login\',exam=null,qIndex=0,qNow=null,review=false,navOffset=0,loadJob=0,saving=Promise.resolve(),lastResult=null,uploading=false,finishing=false;\nconst openFolders=new Set(),previews=new Map();let marked=new Set();\nfunction post(type,extra={}){window.parent.postMessage({isStreamlitMessage:true,type,...extra},\'*\')}\nlet request=0,rendered=false;const pending=new Map(),queue=[];let client=localStorage.getItem(\'ubt_files_client\');if(!client){client=crypto.randomUUID();localStorage.setItem(\'ubt_files_client\',client)}\nfunction send(){post(\'streamlit:setComponentValue\',{dataType:\'json\',value:{client,token,reqs:queue}})}\nfunction api(action,data={}){return new Promise((resolve,reject)=>{const id=client+\':\'+(++request)+\':\'+Date.now();const timer=setTimeout(()=>{pending.delete(id);const i=queue.findIndex(q=>q.id===id);if(i>=0)queue.splice(i,1);reject(Error(\'Сервер жауап бермеді. Қосылымды тексеріңіз.\'))},180000);pending.set(id,{resolve,reject,timer});queue.push({id,action,data,token});send()})}\nwindow.addEventListener(\'message\',e=>{if(e.source!==window.parent||e.data?.type!==\'streamlit:render\')return;const args=e.data.args||{};for(const [id,r]of Object.entries(args.responses||{})){const p=pending.get(id);if(!p)continue;clearTimeout(p.timer);pending.delete(id);const i=queue.findIndex(q=>q.id===id);if(i>=0)queue.splice(i,1);if(r.ok)p.resolve(r);else{if(r.code===\'AUTH_REQUIRED\'){token=\'\';user=null;active=null;exam=null;localStorage.removeItem(\'ubt_files_token\');$(\'header\').hidden=true;show(\'s-login\')}p.reject(Error(r.msg||\'Қате\'))}}if(!rendered){rendered=true;boot()}height()});\nlet lastHeight=0;function height(){const h=Math.max(760,document.body.scrollHeight+20);if(Math.abs(h-lastHeight)>2){lastHeight=h;post(\'streamlit:setFrameHeight\',{height:h})}}\nnew ResizeObserver(height).observe(document.body);window.addEventListener(\'resize\',height);post(\'streamlit:componentReady\',{apiVersion:1});\nfunction toast(msg){$(\'toast\').textContent=msg;$(\'toast\').hidden=false;clearTimeout(toast.timer);toast.timer=setTimeout(()=>$(\'toast\').hidden=true,5000)}\nfunction show(id){if(screen===\'s-exam\'&&exam&&!review&&active&&id!==\'s-exam\'&&id!==\'s-result\'){toast(\'Алдымен тестті аяқтаңыз\');return false}menu(false);$(\'header\').hidden=id===\'s-exam\'||!user;document.querySelectorAll(\'.screen\').forEach(s=>s.classList.toggle(\'active\',s.id===id));screen=id;syncChrome();window.scrollTo({top:0,behavior:\'instant\'});height()}\nfunction menu(open){$(\'menu\').hidden=!open;$(\'shade\').hidden=!open}\nfunction themeLabels(){const dark=document.body.classList.contains(\'dark\');for(const id of [\'theme-menu\',\'theme-login\'])if($(id))$(id).textContent=dark?\'☀ Күндізгі режим\':\'☾ Түнгі режим\';if($(\'theme-toggle\')){$(\'theme-toggle\').textContent=dark?\'☀\':\'☾\';$(\'theme-toggle\').title=dark?\'Күндізгі режим\':\'Түнгі режим\';$(\'theme-toggle\').setAttribute(\'aria-pressed\',String(dark))}}\nfunction syncChrome(){api(\'view\',{screen,dark:document.body.classList.contains(\'dark\')}).catch(()=>{})}\nfunction theme(){document.body.classList.toggle(\'dark\');localStorage.setItem(\'ubt_files_dark\',document.body.classList.contains(\'dark\')?\'1\':\'0\');themeLabels();syncChrome()}\nif(localStorage.getItem(\'ubt_password_night_v2\')!==\'1\'){localStorage.setItem(\'ubt_files_dark\',\'1\');localStorage.setItem(\'ubt_password_night_v2\',\'1\')}document.body.classList.toggle(\'dark\',localStorage.getItem(\'ubt_files_dark\')!==\'0\');\nasync function refresh(){const r=await api(\'status\');const changed=r.meta.revision!==meta.revision;user=r.user;meta=r.meta;active=r.active;$(\'header\').hidden=false;$(\'who\').textContent=user.name;$(\'admin-nav\').hidden=!user.admin;return changed}\nasync function boot(){themeLabels();syncChrome();if(!token)return;try{await refresh();home()}catch(e){token=\'\';localStorage.removeItem(\'ubt_files_token\');show(\'s-login\')}}\n$(\'login-form\').onsubmit=async e=>{e.preventDefault();const b=e.submitter;b.disabled=true;$(\'login-error\').textContent=\'\';try{const r=await api(\'login\',{password:$(\'login-pass\').value});token=r.token;user=r.user;localStorage.setItem(\'ubt_files_token\',token);$(\'login-pass\').value=\'\';await refresh();home()}catch(err){$(\'login-error\').textContent=err.message}finally{b.disabled=false}};\nasync function logout(){if(uploading)return toast(\'Жүктеу аяқталсын\');if(exam&&!review&&screen===\'s-exam\')await saveAnswers();try{await api(\'logout\')}catch(e){}token=\'\';user=null;exam=null;localStorage.removeItem(\'ubt_files_token\');$(\'header\').hidden=true;show(\'s-login\')}\nfunction home(){if(!user)return;if(active){resumeExam();return}show(\'s-home\');$(\'hello\').textContent=\'Сәлем, \'+user.name+\'!\';$(\'active-banner\').innerHTML=active?\'<div class="notice" style="margin-bottom:20px"><div class="row"><span>Аяқталмаған тест: \'+esc(active.title)+\'</span><span class="spacer"></span><button class="btn btn-p btn-sm" onclick="resumeExam()">Жалғастыру →</button></div></div>\':\'\'}\nfunction library(scope=\'public\'){if(!user)return;currentScope=scope;show(\'s-library\');$(\'library-title\').textContent=scope===\'public\'?\'Ортақ тесттер\':\'Сұрақтар базасы\';$(\'tab-public\').classList.toggle(\'selected\',scope===\'public\');$(\'tab-private\').classList.toggle(\'selected\',scope!==\'public\');$(\'library-info\').textContent=scope===\'public\'?\'Админ жариялаған ортақ тесттер.\':\'Барлығы сұрақ қоса алатын ортақ база.\';$(\'search\').value=\'\';drawLibrary()}\nfunction actualScope(){return currentScope===\'public\'?\'public\':\'bank\'}\nfunction folderPath(id){const titles=[];let f=meta.folders.find(f=>f.id===id),guard=0;while(f&&guard++<10){titles.unshift(f.title);f=meta.folders.find(p=>p.id===f.parent)}return titles.join(\'/\')}\nfunction treeCount(id){const ids=new Set([id]);for(let i=0;i<9;i++)meta.folders.filter(f=>f.scope===actualScope()&&ids.has(f.parent)).forEach(f=>ids.add(f.id));return meta.files.filter(f=>f.scope===actualScope()&&ids.has(f.folder)).reduce((n,f)=>n+f.count,0)}\nfunction fileHTML(f){return \'<details class="file" data-file="\'+esc(f.id)+\'"><summary><span class="file-icon">JSON</span><div><div class="file-title">\'+esc(f.title)+\'.json</div><div class="file-meta">\'+f.count+\' сұрақ · \'+esc(names[f.subject]||\'Тест\')+\'</div></div><span class="spacer"></span><span class="tiny">Мазмұны ▾</span></summary><div class="file-body"><div class="row"><button class="btn btn-p btn-sm" data-start="\'+esc(f.id)+\'">Осы файлды тапсыру</button>\'+(user.admin&&f.scope===user.id?\'<button class="btn btn-s btn-sm" data-publish="\'+esc(f.id)+\'">Жариялау</button>\':\'\')+\'</div><div data-preview="\'+esc(f.id)+\'">Мазмұны жүктеледі…</div></div></details>\'}\nfunction folderHTML(f,query){const children=meta.folders.filter(c=>c.scope===actualScope()&&c.parent===f.id),files=meta.files.filter(v=>v.scope===actualScope()&&v.folder===f.id);const content=children.map(c=>folderHTML(c,query)).join(\'\')+files.filter(v=>!query||v.title.toLocaleLowerCase().includes(query)||folderPath(f.id).toLocaleLowerCase().includes(query)).map(fileHTML).join(\'\');if(query&&!content&&!f.title.toLocaleLowerCase().includes(query))return \'\';return \'<details class="folder" data-folder="\'+esc(f.id)+\'" \'+(openFolders.has(f.id)||query?\'open\':\'\')+\'><summary><span>▰</span>\'+esc(f.title)+\'<span class="spacer"></span><span class="badge">\'+treeCount(f.id)+\' сұрақ</span></summary><div class="folder-body"><div class="folder-bar"><button class="btn btn-p btn-sm" data-folder-start="\'+esc(f.id)+\'">Бөлімді толық тапсыру</button></div>\'+content+(!content?\'<p class="tiny">Бөлім әзірге бос.</p>\':\'\')+\'</div></details>\'}\nfunction drawLibrary(){if(!user)return;const scope=actualScope(),query=$(\'search\').value.trim().toLocaleLowerCase();const roots=meta.folders.filter(f=>f.scope===scope&&!f.parent).sort((a,b)=>a.title.localeCompare(b.title,\'kk\',{numeric:true}));const loose=meta.files.filter(f=>f.scope===scope&&!f.folder&&(!query||f.title.toLocaleLowerCase().includes(query)));$(\'file-tree\').innerHTML=roots.map(f=>folderHTML(f,query)).join(\'\')+loose.map(fileHTML).join(\'\')||\'<div class="empty">Әзірге файл жоқ.</div>\';$(\'file-tree\').querySelectorAll(\'[data-folder]\').forEach(el=>el.addEventListener(\'toggle\',()=>el.open?openFolders.add(el.dataset.folder):openFolders.delete(el.dataset.folder)));$(\'file-tree\').querySelectorAll(\'[data-file]\').forEach(el=>el.addEventListener(\'toggle\',()=>{if(el.open)preview(el.dataset.file,0)}));$(\'file-tree\').querySelectorAll(\'[data-start]\').forEach(b=>b.onclick=()=>startExam({file:b.dataset.start}));$(\'file-tree\').querySelectorAll(\'[data-folder-start]\').forEach(b=>b.onclick=()=>startFolder(b.dataset.folderStart));$(\'file-tree\').querySelectorAll(\'[data-publish]\').forEach(b=>b.onclick=()=>publishFile(b.dataset.publish))}\nfunction questionHTML(q,small=false){let h=\'<p class="\'+(small?\'\':\'question-text\')+\'">\'+esc(q.text)+\'</p>\';if(q.img)h+=\'<img class="qimg" loading="lazy" src="\'+esc(q.img)+\'" alt="Сұрақтың суреті">\';if(q.tbl)h+=\'<div style="overflow-x:auto"><table>\'+q.tbl.map(r=>\'<tr>\'+r.map(c=>\'<td style="padding:8px;border:1px solid var(--b)">\'+esc(c)+\'</td>\').join(\'\')+\'</tr>\').join(\'\')+\'</table></div>\';return h}\nasync function preview(id,offset){const el=document.querySelector(\'[data-preview="\'+id+\'"]\');if(!el)return;try{let r=previews.get(id+\':\'+offset);if(!r){r=await api(\'preview\',{file:id,offset});previews.set(id+\':\'+offset,r)}if(!el.isConnected)return;el.innerHTML=r.questions.map((q,i)=>\'<div class="preview"><span class="muted-num">\'+(offset+i+1)+\' / \'+r.total+\'</span>\'+questionHTML(q,true)+\'<p class="sub">\'+q.options.map((v,j)=>String.fromCharCode(65+j)+\') \'+esc(v)).join(\'<br>\')+\'</p></div>\').join(\'\')+\'<div class="row"><button class="btn btn-s btn-sm" data-back \'+(!offset?\'disabled\':\'\')+\'>← Алдыңғы 10</button><span class="tiny">\'+(offset+1)+\'–\'+Math.min(offset+10,r.total)+\' / \'+r.total+\'</span><button class="btn btn-s btn-sm" data-more \'+(offset+10>=r.total?\'disabled\':\'\')+\'>Келесі 10 →</button></div>\';el.querySelector(\'[data-back]\').onclick=()=>preview(id,Math.max(0,offset-10));el.querySelector(\'[data-more]\').onclick=()=>preview(id,offset+10);height()}catch(e){if(el.isConnected)el.textContent=e.message}}\nfunction uploadScreen(scope){if(!user)return;show(\'s-upload\');$(\'upload-scope\').innerHTML=\'<option value="bank">Сұрақтар базасы · бәріне ортақ</option>\'+(user.admin?\'<option value="public">Ортақ тесттер · бәріне ортақ</option>\':\'\');$(\'upload-scope\').value=(scope||currentScope)===\'public\'&&user.admin?\'public\':\'bank\';$(\'upload-subject\').innerHTML=[\'math\',\'informatics\',\'history\',\'reading\',\'mathlit\'].map(k=>\'<option value="\'+k+\'">\'+names[k]+([\'math\',\'informatics\'].includes(k)?\'\':\' · міндетті\')+\'</option>\').join(\'\');$(\'folder-paths\').innerHTML=meta.folders.map(f=>\'<option value="\'+esc(folderPath(f.id))+\'"></option>\').join(\'\');$(\'upload-state\').textContent=\'\'}\nasync function createFolder(){try{const path=$(\'upload-path\').value.trim();if(!path)return toast(\'Бөлім атауын жазыңыз\');await api(\'create_folder\',{path,scope:$(\'upload-scope\').value});await refresh();toast(\'Бөлім қосылды\')}catch(e){toast(e.message)}}\nfunction bytes64(buf){let text=\'\';const a=new Uint8Array(buf);for(let i=0;i<a.length;i+=32768)text+=String.fromCharCode(...a.subarray(i,i+32768));return btoa(text)}\n$(\'upload-form\').onsubmit=async e=>{e.preventDefault();if(uploading)return;const files=[...$(\'upload-files\').files];if(!files.length)return;uploading=true;const b=e.submitter;b.disabled=true;$(\'upload-progress\').hidden=false;$(\'upload-progress\').value=0;let done=0,total=files.reduce((n,f)=>n+f.size,0),ident=null;try{for(const file of files){if(file.size>1024**3)throw Error(file.name+\': 1 ГБ-тан асады\');$(\'upload-state\').textContent=file.name+\' — жүктелуде…\';const r=await api(\'upload_begin\',{scope:$(\'upload-scope\').value,subject:$(\'upload-subject\').value,path:$(\'upload-path\').value,name:file.name,size:file.size});ident=r.id;for(let off=0;off<file.size;off+=r.chunk){const buf=await file.slice(off,off+r.chunk).arrayBuffer();await api(\'upload_chunk\',{id:ident,offset:off,bytes:bytes64(buf)});$(\'upload-progress\').value=Math.floor(90*(done+off+buf.byteLength)/total)}$(\'upload-state\').textContent=file.name+\' — тексеріліп, сақталуда…\';await api(\'upload_finish\',{id:ident});let saved;for(;;){saved=await api(\'upload_status\',{id:ident});if(saved.phase===\'done\')break;if(saved.phase===\'error\')throw Error(saved.error||\'Сақтау сәтсіз\');$(\'upload-state\').textContent=file.name+\' — \'+(saved.msg||\'Сақталуда…\')+\' \'+(saved.scanned||0)+\' сұрақ\';$(\'upload-progress\').value=Math.min(99,Math.max(Number($(\'upload-progress\').value)||0,90+Math.min(8,(saved.scanned||0)/5000)));await new Promise(resolve=>setTimeout(resolve,800))}ident=null;done+=file.size;toast(file.name+\': \'+saved.count+\' сұрақ базаға толық қосылды\')}await refresh();$(\'upload-files\').value=\'\';$(\'upload-state\').textContent=\'100% — Базаға толық қосылды.\';$(\'upload-progress\').value=100}catch(err){$(\'upload-state\').textContent=err.message;if(ident)try{await api(\'upload_cancel\',{id:ident})}catch(e){}}finally{uploading=false;b.disabled=false}};\nasync function publishFile(file){const path=prompt(\'Жария бөлім жолы (мысалы: 1 бөлім/1.1):\',\'\');if(path===null)return;try{await api(\'publish_file\',{file,path});await refresh();library(\'public\');toast(\'Файл жарияланды\')}catch(e){toast(e.message)}}\nfunction startFolder(folder){startExam({folder,scope:currentScope})}\nasync function exam140(){if(!user)return;await startExam({mode:\'140\'})}\nasync function startExam(data){if(active&&!confirm(\'Аяқталмаған тест бар. Оның орнына жаңасын бастайсыз ба?\'))return;try{const r=await api(\'start\',{...data,replace:!!active});exam=r.exam;active=exam;review=false;marked=new Set();localStorage.removeItem(\'ubt_marks\');loadExam()}catch(e){toast(e.message)}}\nasync function resumeExam(){try{await refresh();if(!active)return toast(\'Белсенді тест жоқ\');exam=active;review=false;try{marked=new Set(JSON.parse(localStorage.getItem(\'ubt_marks_\'+exam.id)||\'[]\'))}catch(e){marked=new Set()}loadExam()}catch(e){toast(e.message)}}\nfunction loadExam(){show(\'s-exam\');qIndex=0;navOffset=0;$(\'exam-title\').textContent=exam.title;$(\'exam-sections\').innerHTML=exam.sections.map(s=>\'<option value="\'+s.start+\'">\'+esc(s.title)+\' · \'+s.count+\'</option>\').join(\'\');goQuestion(0);tick()}\nfunction drawNav(){const count=Math.min(100,exam.count-navOffset);$(\'nav-window\').textContent=(navOffset+1)+\'–\'+(navOffset+count)+\' / \'+exam.count;$(\'qnav\').innerHTML=Array.from({length:count},(_,j)=>{const i=navOffset+j;return \'<button class="qn \'+(i===qIndex?\'current \':\'\')+(marked.has(i)?\'marked \':Object.hasOwn(exam.answers,String(i))?\'answered \':\'\')+\'" data-q="\'+i+\'">\'+(i+1)+\'</button>\'}).join(\'\');$(\'qnav\').querySelectorAll(\'button\').forEach(b=>b.onclick=()=>goQuestion(Number(b.dataset.q)));$(\'exam-progress\').textContent=Object.keys(exam.answers).length+\' / \'+exam.count+\' жауап\'}\nfunction navPage(delta){navOffset=Math.max(0,Math.min(Math.floor((exam.count-1)/100)*100,navOffset+delta*100));drawNav()}\nasync function goQuestion(i){if(!exam||i<0||i>=exam.count)return;const job=++loadJob;qIndex=i;navOffset=Math.floor(i/100)*100;drawNav();$(\'question\').textContent=\'Жүктелуде…\';$(\'options\').replaceChildren();$(\'explanation\').hidden=true;try{const r=await api(\'question\',{exam:exam.id,index:i});if(job!==loadJob)return;qNow=r.question;$(\'q-number\').textContent=(i+1)+\' / \'+exam.count+\' · \'+(names[qNow.subject]||\'\')+\' · \'+qNow.points+\' ұпай\';$(\'question\').innerHTML=questionHTML(qNow);drawOptions();$(\'previous-q\').disabled=i===0;$(\'next-q\').disabled=i===exam.count-1;$(\'mark-button\').textContent=marked.has(i)?\'⚑ Белгіленген\':\'⚑ Белгілеу\';const sec=[...exam.sections].reverse().find(s=>i>=s.start);if(sec)$(\'exam-sections\').value=sec.start;if(review&&qNow.explanation){$(\'explanation\').textContent=qNow.explanation;$(\'explanation\').hidden=false}height()}catch(e){if(job===loadJob)$(\'question\').textContent=e.message}}\nfunction drawOptions(){const selected=exam.answers[String(qIndex)];$(\'options\').innerHTML=qNow.options.map((v,i)=>\'<button class="option \'+(i===selected?\'selected \':\'\')+(review&&i===qNow.correct?\'right \':review&&i===selected&&i!==qNow.correct?\'wrong \':\'\')+\'" data-option="\'+i+\'" \'+(review?\'disabled\':\'\')+\'><span class="option-letter">\'+String.fromCharCode(65+i)+\')</span><span>\'+esc(v)+\'</span></button>\').join(\'\');$(\'options\').querySelectorAll(\'button\').forEach(b=>b.onclick=()=>choose(Number(b.dataset.option)))}\nfunction choose(i){if(review||!exam||timeLeft()<=0)return;exam.answers[String(qIndex)]=i;drawOptions();drawNav();saveAnswers()}\nfunction saveAnswers(){if(!exam||review)return saving;const eid=exam.id,answers={...exam.answers};saving=saving.catch(()=>{}).then(()=>api(\'save_answers\',{exam:eid,answers})).catch(e=>{toast(\'Жауап сақталмады: \'+e.message);throw e});saving.catch(()=>{});return saving}\nfunction markQuestion(){if(marked.has(qIndex))marked.delete(qIndex);else marked.add(qIndex);localStorage.setItem(\'ubt_marks_\'+exam.id,JSON.stringify([...marked]));$(\'mark-button\').textContent=marked.has(qIndex)?\'⚑ Белгіленген\':\'⚑ Белгілеу\';drawNav()}\nfunction timeLeft(){return Math.max(0,Math.ceil((exam?.deadline||0)-Date.now()/1000))}\nfunction tick(){if(screen!==\'s-exam\'||!exam)return;$(\'exam-time\').textContent=review?\'Жауаптарды қарау\':Math.floor(timeLeft()/3600)+\':\'+String(Math.floor(timeLeft()%3600/60)).padStart(2,\'0\')+\':\'+String(timeLeft()%60).padStart(2,\'0\');if(!review&&!timeLeft()&&!finishing)finishExam(true)}\nsetInterval(tick,1000);\nasync function pauseExam(){if(review)return home();try{await saveAnswers();active=exam;home()}catch(e){toast(\'Жауаптар сақталмады. Қайта көріңіз.\')}}\nasync function finishExam(automatic=false){if(!exam||finishing)return;if(review)return home();if(!automatic&&!confirm(\'Тестті аяқтайсыз ба? Жауап берілгені: \'+Object.keys(exam.answers).length+\' / \'+exam.count))return;finishing=true;try{await saving.catch(()=>{});const r=await api(\'finish\',{exam:exam.id,answers:exam.answers});lastResult=r.result;exam=r.exam;active=null;showResult(r.result)}catch(e){toast(e.message)}finally{finishing=false}}\nfunction showResult(r){active=null;$(\'header\').hidden=false;show(\'s-result\');$(\'result-card\').innerHTML=\'<span class="badge">\'+esc(r.title)+\'</span><div class="score" style="margin:20px 0">\'+r.score+\' <span style="font-size:23px;color:var(--m)">/ \'+r.max+\'</span></div><p class="sub">Дұрыс жауап: \'+r.correct+\' / \'+r.count+\' · Жауап берілгені: \'+r.answered+\'</p>\'+Object.entries(r.subjects).map(([s,v])=>\'<div class="result-row"><span>\'+esc(names[s]||s)+\'</span><b>\'+v.score+\' / \'+v.max+\'</b></div>\').join(\'\')}\nfunction reviewExam(){if(!exam)return;review=true;loadExam()}\nasync function historyScreen(){show(\'s-history\');$(\'history-list\').textContent=\'Жүктелуде…\';try{const r=await api(\'history\');$(\'history-list\').innerHTML=r.items.map(v=>\'<div class="card"><div class="row"><b>\'+esc(v.title)+\'</b><span class="spacer"></span><b style="color:var(--p)">\'+v.score+\' / \'+v.max+\'</b></div><p class="tiny" style="margin-top:10px">\'+new Date(v.at*1000).toLocaleString(\'kk-KZ\')+\' · \'+v.answered+\' / \'+v.count+\' жауап</p></div>\').join(\'\')||\'<div class="empty">Әзірге нәтиже жоқ.</div>\'}catch(e){$(\'history-list\').textContent=e.message}}\nasync function adminScreen(){if(!user?.admin)return;show(\'s-admin\');try{const r=await api(\'admin_users\');$(\'users-list\').innerHTML=r.users.map(u=>\'<div class="result-row"><div><b>\'+esc(u.name)+\'</b><p class="tiny">\'+esc(u.login)+\'</p></div>\'+(u.id===\'admin\'?\'<span class="badge">Админ</span>\':\'<button class="btn btn-d btn-sm" data-delete-user="\'+esc(u.id)+\'">Өшіру</button>\')+\'</div>\').join(\'\');$(\'users-list\').querySelectorAll(\'[data-delete-user]\').forEach(b=>b.onclick=()=>deleteUser(b.dataset.deleteUser));const date=v=>v?new Date(v*1000).toLocaleString(\'kk-KZ\'):\'—\';$(\'access-list\').innerHTML=r.logs.map(l=>\'<div class="result-row"><div><b>\'+esc(l.name)+\'</b><p class="tiny">\'+esc(l.login)+\'</p></div><div class="tiny">Кірді: \'+date(l.entered)+\'<br>Шықты: \'+date(l.exited)+(l.reason===\'deleted\'?\' · аккаунт өшірілді\':\'\')+\'<br>Соңғы белсенділік: \'+date(l.lastSeen)+\'<br>\'+(l.exited?\'Сессия жабылды\':Date.now()/1000-l.lastSeen<120?\'Белсенді\':\'Белсенділігі тоқтады\')+\'</div></div>\').join(\'\')||\'<p class="sub">Әзірге жазба жоқ.</p>\'}catch(e){toast(e.message)}}\nasync function deleteUser(uid){if(!confirm(\'Бұл адамның аккаунтын өшіресіз бе? Қайта кіру мүмкіндігі жабылады.\'))return;try{await api(\'delete_user\',{uid});await refresh();await adminScreen();toast(\'Адам өшірілді\')}catch(e){toast(e.message)}}\nfunction subjectScreen(){if(!user)return;show(\'s-subject\');$(\'subject-pick\').innerHTML=Object.entries(names).map(([k,v])=>\'<option value="\'+k+\'">\'+esc(v)+\'</option>\').join(\'\');$(\'subject-pick\').value=\'math\'}\nfunction startSubject(){const value=$(\'subject-count\').value;startExam({mode:\'subject\',subject:$(\'subject-pick\').value,count:value===\'all\'?\'all\':Number(value)})}\nlet flashItems=[],flashOffset=0,flashIndex=0,flashTotal=0;\nasync function flashScreen(){if(!user)return;if(active)return toast(\'Алдымен тестті аяқтаңыз\');show(\'s-flash\');$(\'flash-subject\').innerHTML=\'<option value="">Барлық пән</option>\'+Object.entries(names).map(([k,v])=>\'<option value="\'+k+\'">\'+esc(v)+\'</option>\').join(\'\');await loadFlash(0)}\nasync function loadFlash(offset){try{const r=await api(\'flashcards\',{subject:$(\'flash-subject\').value,offset});flashItems=r.items;flashOffset=offset;flashTotal=r.total;flashIndex=0;drawFlash()}catch(e){toast(e.message)}}\nfunction drawFlash(){$(\'flash-back\').hidden=true;if(!flashItems.length){$(\'flash-front\').textContent=\'Бұл пәнде сұрақ жоқ.\';$(\'flash-number\').textContent=\'\';return}$(\'flash-number\').textContent=(flashOffset+flashIndex+1)+\' / \'+flashTotal;$(\'flash-front\').innerHTML=questionHTML(flashItems[flashIndex].front);$(\'flash-back\').textContent=flashItems[flashIndex].back+(flashItems[flashIndex].explanation?\'\\n\\n\'+flashItems[flashIndex].explanation:\'\')}\nfunction flipFlash(){if(flashItems.length)$(\'flash-back\').hidden=!$(\'flash-back\').hidden}\nfunction flashMove(delta){const next=flashOffset+flashIndex+delta;if(next<0||next>=flashTotal)return;if(next<flashOffset){loadFlash(Math.max(0,flashOffset-20));return}if(next>=flashOffset+flashItems.length){loadFlash(flashOffset+20);return}flashIndex+=delta;drawFlash()}\n$(\'user-form\').onsubmit=async e=>{e.preventDefault();if(!user?.admin)return;const b=e.submitter;b.disabled=true;try{await api(\'create_user\',{name:$(\'new-name\').value,login:$(\'new-login\').value,password:$(\'new-pass\').value});$(\'new-pass\').value=\'\';$(\'user-state\').textContent=\'Қолданушы қосылды.\';await refresh();adminScreen()}catch(err){$(\'user-state\').textContent=err.message}finally{b.disabled=false}};\nsetInterval(async()=>{if(!user||uploading||pending.size||screen===\'s-exam\'||document.hidden)return;try{const changed=await refresh();if(changed&&screen===\'s-library\')drawLibrary();if(screen===\'s-home\')home()}catch(e){}},15000);\n</script></body></html>\n'

st.set_page_config(page_title='ҰБТ PLUS · Инфо–мат',page_icon='📘',layout='wide')

try:
    _rt=runtime()
except Exception as exc:
    st.error(str(exc));st.stop()
_front=os.path.join(_HERE,'ubt_files_frontend')
os.makedirs(_front,exist_ok=True)
_index=os.path.join(_front,'index.html')
try:
    with open(_index,encoding='utf-8')as f:_previous=f.read()
except OSError:_previous=''
if _previous!=HTML:
    with open(_index,'w',encoding='utf-8')as f:f.write(HTML)
_component=components.declare_component('ubt_files_infomat',path=_front)
def _process_transport(payload):
    if not isinstance(payload,dict):return False
    changed=False;cache=st.session_state.setdefault('_files_rpc_cache',{})
    for req in payload.get('reqs',[])[:20]:
        if not isinstance(req,dict)or not isinstance(req.get('id'),str)or len(req['id'])>180:continue
        ident=req['id']
        if ident in cache:continue
        try:
            if not isinstance(req.get('data',{}),dict):raise ValueError('Сұраныс жарамсыз')
            data=dict(req.get('data',{}))
            if req.get('action')=='login':data['_client']=st.session_state.setdefault('_files_login_client',secrets.token_hex(16))
            cache[ident]=dispatch(_rt,str(req.get('token')or''),str(req.get('action')or''),data)
        except (ValueError,KeyError,TypeError,binascii.Error)as exc:
            cache[ident]={'ok':False,'msg':str(exc),'code':'AUTH_REQUIRED'if str(exc)=='Алдымен аккаунтқа кіріңіз'else'INVALID'}
        except Exception:
            cache[ident]={'ok':False,'msg':'Сервер деректі сақтай алмады. Қосылым мен сервер баптауын тексеріңіз.'}
        result=cache[ident]
        if req.get('action')=='view':
            st.session_state['_files_manage_visible']=bool(result.get('ok')and result.get('manage'))
            st.session_state['_files_dark']=bool(result.get('ok')and result.get('dark'))
        elif req.get('action')in('login','logout'):
            st.session_state['_files_manage_visible']=False
        changed=True
    # Bound the response cache; incoming requests are replay-safe until acknowledged.
    keep={r.get('id')for r in payload.get('reqs',[])if isinstance(r,dict)}
    for key in list(cache):
        if len(cache)<=64:break
        if key not in keep:cache.pop(key,None)
    return changed
_incoming=st.session_state.get('ubt_files_component')
_process_transport(_incoming)
st.markdown(_chrome_css(bool(st.session_state.get('_files_manage_visible')),bool(st.session_state.get('_files_dark',True))),unsafe_allow_html=True)
_pending=_incoming.get('reqs',[])if isinstance(_incoming,dict)else[]
_cache=st.session_state.get('_files_rpc_cache',{})
_replies={r['id']:_cache[r['id']]for r in _pending if isinstance(r,dict)and r.get('id')in _cache}
_value=_component(responses=_replies,key='ubt_files_component',default=None)
if _process_transport(_value):st.rerun()
