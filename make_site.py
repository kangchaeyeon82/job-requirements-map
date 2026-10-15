import json, re, importlib.util, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def load_mod(path):
    spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

# ---------- data files ----------
def write(key, D, META, INS, SEC, kpi=None):
    for k in D['tracks']:
        D['tracks'][k]['ins'] = INS[k]; D['tracks'][k]['sec'] = SEC[k]
        if kpi: D['tracks'][k]['kpi5'] = kpi[k]
    D['meta'] = META; D['collected'] = '2026-10-15'
    json.dump(D, open(f'site/data/{key}.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print(key, os.path.getsize(f'site/data/{key}.json'))

e = load_mod('ins_emb.py'); write('engineer', json.load(open('emb_data.json', encoding='utf-8')), e.META, e.INS, e.SEC)

src = open('web/insights_web.py', encoding='utf-8').read()
ns = {}; exec(src[src.index('INS = {'):src.index('\nfrom sections_web')], ns)
sw = load_mod('web/sections_web.py')
dev_meta = dict(title='개발 채용 지도', logo1='개발', h1='개발 직군 채용 요건 지도', ph='회사, 포지션, 기술로 검색 (예: Spring, React)', noun='기술',
    order=['전체', '서버', '프론트엔드', '소프트웨어 엔지니어', '웹', '프로덕트 매니저'],
    labels={'전체': '개발 직군 전체', '서버': '서버 개발자', '프론트엔드': '프론트엔드 개발자', '소프트웨어 엔지니어': '소프트웨어 엔지니어', '웹': '웹 개발자', '프로덕트 매니저': '프로덕트 매니저'},
    kpi5=['AI 언급', 'LLM·AI 모델·AI 도구'],
    foot='원티드 개발 직군 중 서버 개발자, 프론트엔드 개발자, 웹 개발자, 소프트웨어 엔지니어, 프로덕트 매니저 필터에 걸린 공고 1,258건을 2026-10-15에 모두 열어 정리했어요. 공고마다 대표 직군 하나로 나눴어요. 기술은 자격요건과 우대사항 원문을 미리 정한 기술 목록과 대조해 찾았기 때문에, 표기가 특이하거나 이미지로 올린 요건은 빠질 수 있어요.')
dd = json.load(open('web/data_web.json', encoding='utf-8'))
dd['groups'] = ["언어", "프레임워크", "데이터베이스·메시징", "인프라·클라우드", "프론트엔드", "설계·품질", "AI", "기획·PM", "협업 도구·방식"]
write('dev', dd, dev_meta, ns['INS'], sw.SEC, sw.AI)

m = load_mod('mkt/ins_mkt.py'); write('marketing', json.load(open('mkt/data_mkt.json', encoding='utf-8')), m.META, m.INS, m.SEC)
d = load_mod('dsn/ins_dsn.py'); write('design', json.load(open('dsn/data_dsn.json', encoding='utf-8')), d.META, d.INS, d.SEC)

# ---------- page ----------
s = open('page_shared.tpl.html', encoding='utf-8').read()
def rep(a, b, count=1):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b, count)

rep('<title>__TITLE__</title>', '<title>직무 채용 지도</title>')
rep('''<header class="top">
  <div class="top-in">
    <p class="logo">__LOGO1__ <span>채용 지도</span></p>
    <nav class="tabs" id="tabs" role="tablist" aria-label="직군 선택"></nav>
  </div>
</header>''', '''<header class="top">
  <div class="top-in">
    <p class="logo">직무 <span>채용 지도</span></p>
    <nav class="fields" id="fields" aria-label="직무 분야"></nav>
  </div>
  <div class="top-in sub"><nav class="tabs" id="tabs" role="tablist" aria-label="세부 직군"></nav></div>
</header>''')
rep('''@media (prefers-reduced-motion''', '''.fields{display:flex;gap:4px;background:var(--card);border-radius:999px;padding:4px;overflow-x:auto;scrollbar-width:none;max-width:100%}
.fields::-webkit-scrollbar{display:none}
.fld{flex:none;font:inherit;font-size:14px;font-weight:800;border:0;border-radius:999px;padding:8px 16px;background:transparent;color:var(--sub);cursor:pointer;transition:background .15s,color .15s}
.fld:hover{color:var(--ink)}
.fld[aria-pressed="true"]{background:var(--accent);color:#fff}
.top-in.sub{padding-block:0 10px}
body.loading .wrap{opacity:.45;transition:opacity .2s}
@media (prefers-reduced-motion''')
rep('<h1>__H1__</h1>', '<h1 id="h1"></h1>')
rep('placeholder="__PH__"', 'placeholder=""')
main_a = s.index('<main class="wrap">'); main_b = s.index('</main>')
s = s[:main_a] + s[main_a:main_b].replace('기술', '<span class="nn">기술</span>') + s[main_b:]

old_head = s[s.index('const D = /*__DATA__*/null;'):s.index('function barRow(')]
new_head = '''const FIELDS = [{key:'engineer', name:'엔지니어'}, {key:'dev', name:'개발'}, {key:'marketing', name:'마케팅'}, {key:'design', name:'디자인'}];
const CACHE = {};
let D = null, ORDER = [], LABEL = {}, NOUN = '기술', field = null;
const TONE = {'채널':'blue','데이터':'blue','언어':'blue','툴':'blue','포트폴리오':'green','핵심':'violet','기본':'blue','가산점':'earth','신입':'green','트렌드':'red','참고':'earth','지역':'blue','경력':'earth'};
const $ = (id) => document.getElementById(id);
const el = (tag, cls, txt) => { const e = document.createElement(tag); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; };
const pc = (a, b) => b ? Math.round(a / b * 100) : 0;
const pct = (a, b) => pc(a, b) + '%';
const fmt = (n) => n.toLocaleString('ko-KR');
const nn = (t) => NOUN === '기술' ? t : t.replace(/프로젝트로/g, '포트폴리오로').replace(/기술/g, NOUN);

let cur = '전체';
const tabs = $('tabs'), fieldsNav = $('fields');
FIELDS.forEach(f => {
  const b = el('button', 'fld', f.name); b.type = 'button'; b.dataset.f = f.key;
  b.addEventListener('click', () => { if (f.key !== field) { go(f.key); window.scrollTo(0, 0); } });
  fieldsNav.appendChild(b);
});
function buildTabs() {
  tabs.replaceChildren();
  ORDER.forEach(t => {
    const b = el('button', 'tab', t === '전체' ? '전체' : LABEL[t]); b.type = 'button'; b.setAttribute('role', 'tab'); b.dataset.t = t;
    b.addEventListener('click', () => { cur = t; selected = null; render(); });
    tabs.appendChild(b);
  });
}
async function go(key) {
  field = key;
  try { localStorage.setItem('jobmap-field', key); } catch (e) {}
  try { if (location.hash.slice(1) !== key) history.replaceState(null, '', '#' + key); } catch (e) {}
  fieldsNav.querySelectorAll('.fld').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.f === key)));
  if (!CACHE[key]) {
    document.body.classList.add('loading'); $('h-track').textContent = '데이터를 불러오는 중이에요';
    try {
      const r = await fetch(`data/${key}.json`); if (!r.ok) throw new Error(r.status);
      const data = await r.json(); data.jobs.forEach(j => { j.ms = j.m.join(', '); }); CACHE[key] = data;
    } catch (e) {
      document.body.classList.remove('loading'); $('h-track').textContent = '데이터를 불러오지 못했어요. 새로고침해 보세요.'; return;
    }
    document.body.classList.remove('loading');
  }
  if (field !== key) return;
  D = CACHE[key]; ORDER = D.meta.order; LABEL = D.meta.labels; NOUN = D.meta.noun || '기술';
  cur = '전체'; selected = null; sortKey = null; $('q').value = '';
  $('h1').textContent = D.meta.h1; $('q').placeholder = D.meta.ph;
  document.querySelectorAll('.nn').forEach(x => { x.textContent = NOUN; });
  buildTabs(); render();
}

'''
s = s.replace(old_head, new_head)
for a in ["add('에서 가장 자주 필수로 요구하는 기술은 ')", "'없으면 서류에서 걸러지기 쉬운 기술'", "'핵심 기술'", "'방향에 맞춰 2–3개를 골라 프로젝트로 증명'", "'우대사항에 더 자주 나오는 기술'", "'해당 기술 없음'"]:
    inner = a[a.index("'"):a.rindex("'") + 1]
    rep(a, a.replace(inner, f'nn({inner})'))
tail = s.rindex('render();\n</script>')
s = s[:tail] + '''{ const h = location.hash.slice(1); let start = FIELDS.some(f => f.key === h) ? h : null;
  if (!start) { try { const v = localStorage.getItem('jobmap-field'); if (FIELDS.some(f => f.key === v)) start = v; } catch (e) {} }
  go(start || 'engineer'); }
</script>''' + s[tail + len('render();\n</script>'):]

import chat_snippet as CH
rep('@media (prefers-reduced-motion', CH.CSS + '@media (prefers-reduced-motion')
rep('<nav class="fields" id="fields" aria-label="직무 분야"></nav>', CH.BTN)
rep('</main>', '</main>\n\n' + CH.PANEL)
s = s.rstrip() + '\n' + CH.JS + '\n'
assert '__' not in s.replace('__proto__', ''), re.findall(r'__\w+__', s)
open('site/index.html', 'w', encoding='utf-8').write(s)
print('page', len(s))
