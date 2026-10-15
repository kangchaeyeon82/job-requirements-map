s = open('web/page.tpl.html', encoding='utf-8').read()
R = [
 ('<title>개발 채용 지도</title>', '<title>__TITLE__</title>'),
 ('<p class="logo">개발 <span>채용 지도</span></p>', '<p class="logo">__LOGO1__ <span>채용 지도</span></p>'),
 ('<h1>개발 직군 채용 요건 지도</h1>', '<h1>__H1__</h1>'),
 ('placeholder="회사, 포지션, 기술로 검색 (예: Spring, React)"', 'placeholder="__PH__"'),
 ("const ORDER = ['전체','서버','프론트엔드','소프트웨어 엔지니어','웹','프로덕트 매니저'];", "const ORDER = D.meta.order;"),
 ("const LABEL = {'전체':'개발 직군 전체','서버':'서버 개발자','프론트엔드':'프론트엔드 개발자','소프트웨어 엔지니어':'소프트웨어 엔지니어','웹':'웹 개발자','프로덕트 매니저':'프로덕트 매니저'};", "const LABEL = D.meta.labels;"),
 ("['AI 언급', pct(T.ai, n), 'LLM·AI 모델·AI 도구']", "[D.meta.kpi5[0], pct(T.kpi5, n), D.meta.kpi5[1]]"),
 ("const b = el('button', 'tab', t);", "const b = el('button', 'tab', t === '전체' ? '전체' : LABEL[t]);"),
 ("const TONE = {", "const TONE = {'채널':'blue','데이터':'blue','언어':'blue','툴':'blue','포트폴리오':'green',"),
]
for a, b in R:
    assert a in s, a
    s = s.replace(a, b)
import re
i = s.index("  $('foot').textContent = `"); j = s.index("`;", i) + 2
s = s[:i] + "  $('foot').textContent = D.meta.foot;" + s[j:]
s = s.replace("const D = /*__DATA__*/null;\n", "const D = /*__DATA__*/null;\n")
open('page_shared.tpl.html', 'w', encoding='utf-8').write(s)
print('ok')
