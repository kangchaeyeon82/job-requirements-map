import json, re, os, statistics
from collections import Counter

L = json.load(open('data/list.json', encoding='utf-8'))
TRACKS = {1635: '콘텐츠', 1030: '디지털', 950: '글로벌', 707: '브랜드', 710: '마케터'}
SEL = list(TRACKS)

TAX = {
 "채널·전략": {"퍼포먼스 마케팅": r"퍼포먼스|performance market|유료 ?광고|paid (media|ads)", "SNS 마케팅": r"sns|소셜 ?(미디어|마케팅)|social media",
   "인플루언서 마케팅": r"인플루언서|influencer|크리에이터 ?(협업|마케팅|섭외)|kol", "콘텐츠 마케팅": r"콘텐츠 ?마케팅|content marketing",
   "CRM 마케팅": r"crm|리텐션|retention|lifecycle|라이프사이클", "검색·SEO": r"\bseo\b|검색 ?(엔진 )?최적화|\bsem\b|\baeo\b|\bgeo\b",
   "PR·언론홍보": r"\bpr\b|언론|보도 ?자료|홍보", "제휴·파트너십": r"제휴|파트너십|partnership|co-?marketing|콜라보",
   "오프라인·이벤트": r"오프라인|팝업|행사|이벤트 ?(기획|운영)|전시회|박람회|event (planning|management)|offline", "커뮤니티": r"커뮤니티|community", "그로스 마케팅": r"그로스|growth"},
 "광고 플랫폼": {"Meta 광고": r"meta|페이스북|facebook|인스타그램 ?광고", "Google 광고": r"google ads|구글 ?(광고|애즈)|\bgdn\b|uac|\bpmax\b",
   "네이버 광고": r"네이버 ?(광고|검색광고|sa|gfa)|\bgfa\b|파워링크", "카카오 광고": r"카카오 ?(모먼트|광고|비즈보드)|비즈보드", "TikTok 광고": r"틱톡 ?광고|tiktok ads",
   "쿠팡·커머스 광고": r"쿠팡 ?광고|\bcpc\b 광고|마켓 ?광고", "미디어 플래닝": r"미디어 ?(플래닝|믹스|바잉|전략)|media (planning|buying|mix)|\batl\b|\bbtl\b"},
 "SNS·미디어": {"인스타그램": r"인스타|instagram", "유튜브": r"유튜브|youtube", "틱톡": r"틱톡|tiktok", "블로그": r"블로그|blog",
   "숏폼": r"숏폼|short[- ]?form|릴스|reels|쇼츠|shorts", "X·스레드": r"트위터|twitter|\bx\b ?\(|스레드|threads", "링크드인": r"링크드인|linkedin"},
 "데이터·분석": {"GA·GA4": r"\bga4?\b|google analytics|구글 ?애널리틱스", "GTM": r"\bgtm\b|tag manager|태그 ?매니저", "SQL": r"\bsql\b",
   "엑셀·스프레드시트": r"엑셀|excel|스프레드시트|spreadsheet|구글 ?시트", "Amplitude·Mixpanel": r"amplitude|mixpanel|앰플리튜드",
   "MMP(Appsflyer 등)": r"appsflyer|앱스플라이어|adjust|airbridge|에어브릿지|\bmmp\b", "A/B 테스트": r"a/b|ab ?테스트|실험 ?설계",
   "성과 지표(ROAS 등)": r"roas|\bcpa\b|\bctr\b|\bcac\b|\bltv\b|\bkpi\b|전환율", "BI 툴": r"tableau|태블로|looker|power ?bi|redash|metabase",
   "데이터 분석": r"데이터 ?(분석|기반|드리븐)|data[- ]driven|data analy", "Python": r"python|파이썬"},
 "콘텐츠 제작": {"카피라이팅": r"카피|copywrit|글쓰기|문장력|작문", "영상 기획·편집": r"영상 ?(기획|편집|제작|촬영)|premiere|프리미어|파이널 ?컷|final cut|캡컷|capcut|after effects|애프터 ?이펙트",
   "Photoshop·Illustrator": r"포토샵|photoshop|일러스트레이터|illustrator|adobe", "Figma": r"figma|피그마", "Canva·Miri": r"canva|캔바|미리캔버스",
   "상세페이지": r"상세 ?페이지", "뉴스레터": r"뉴스레터|newsletter|이메일 ?마케팅|email marketing", "콘텐츠 기획": r"콘텐츠 ?(기획|제작|전략)|content (strategy|creation|planning)"},
 "브랜드·캠페인": {"브랜딩·브랜드 전략": r"브랜딩|브랜드 ?(전략|아이덴티티|경험|빌딩|기획|관리)|branding|brand (strategy|identity|management)",
   "캠페인 기획": r"캠페인|campaign|\bimc\b", "에이전시 협업": r"에이전시|대행사|agency", "시장·소비자 조사": r"시장 ?조사|소비자 ?(조사|인사이트|분석)|market research|리서치|트렌드 ?분석|경쟁사 ?분석",
   "굿즈·팝업": r"굿즈|팝업 ?스토어|pop-?up"},
 "커머스": {"이커머스·D2C": r"이커머스|e-?commerce|d2c|온라인 ?(커머스|쇼핑몰)", "자사몰": r"자사몰|카페24|cafe24|쇼피파이|shopify|아임웹",
   "마켓플레이스": r"쿠팡|스마트스토어|올리브영|무신사|29cm|아마존|amazon|마켓플레이스|marketplace|큐텐|qoo10|라쿠텐|rakuten|쇼피|lazada|tmall|티몰",
   "앱 마케팅": r"앱 ?(마케팅|설치|다운로드)|app (marketing|install)|aso\b|앱스토어", "프로모션 기획": r"프로모션|promotion|할인 ?행사|기획전"},
 "언어·글로벌": {"영어": r"영어|english|영문|비즈니스 ?영어|toeic|토익|opic", "일본어": r"일본어|japanese|jlpt", "중국어": r"중국어|chinese|hsk",
   "해외 시장 경험": r"해외|글로벌|global|북미|미국 시장|일본 시장|동남아|overseas|international", "현지화": r"현지화|로컬라이|locali"},
 "협업 툴·AI": {"생성형 AI 활용": r"chat ?gpt|생성형|\bgpt\b|\bllm\b|midjourney|미드저니|ai ?(툴|도구|활용)|gemini|claude|프롬프트",
   "CRM 툴(Braze 등)": r"braze|브레이즈|hubspot|허브스팟|salesforce|세일즈포스|클레버탭|clevertap|moengage|iterable|channel ?talk|채널톡",
   "노션·협업 툴": r"notion|노션|jira|지라|slack|슬랙|confluence|asana|monday", "자동화(Zapier 등)": r"zapier|make\.com|n8n|자동화"},
}
EDU = {"학사 이상": r"학사|bachelor|4년제|대졸", "석사 이상": r"석사|master|mba", "관련 전공(경영·광고·미디어)": r"경영|마케팅 ?(전공|학과)|광고 ?홍보|신문 ?방송|미디어 ?(전공|학과)|커뮤니케이션 ?(전공|학과)|관련 ?전공",
       "전공 무관": r"전공 ?무관|학력 ?무관"}
SOFT = {"커뮤니케이션/협업": r"커뮤니케이션|소통|협업|communication|collaborat", "문제 해결·주도성": r"주도|문제 ?해결|ownership|오너십|자기 ?주도",
        "트렌드 감각": r"트렌드|trend|감각|센스|밈", "문서·보고서 작성": r"문서|보고서|리포트|report|기획서|제안서", "빠른 실행력": r"빠르게|실행력|스타트업|startup|애자일",
        "숫자·데이터 감각": r"숫자|수치|데이터에 (기반|근거)|데이터 ?감각|분석적 사고|논리적"}

def find(dic, text): return [k for k, p in dic.items() if re.search(p, text, re.I)]
GROUP = {k: g for g, d in TAX.items() for k in d}

J = []
for it in L:
    p = f"data/d/{it['id']}.json"
    if not os.path.exists(p): continue
    j = json.load(open(p, encoding='utf-8'))['job']; d = j['detail']
    tags = [t['id'] for t in j.get('category_tags', [])]
    cat = it['category_tag']['id'] if it['category_tag']['id'] in SEL else next((t for t in tags if t in SEL), None)
    if cat is None: continue
    req = d.get('requirements') or ''; pref = d.get('preferred_points') or ''
    must = sorted(set(find_all := [k for g, dic in TAX.items() for k in find(dic, req)]))
    nice = sorted(set(k for g, dic in TAX.items() for k in find(dic, pref)) - set(must))
    loc = ((j.get('address') or {}).get('location') or '').strip()
    J.append(dict(id=it['id'], co=j['company']['name'], pos=j['position'], track=TRACKS[cat], yf=it.get('annual_from') or 0, yt=it.get('annual_to'),
                  loc2={'서울': '서울', '경기': '경기'}.get(loc, '해외' if loc and not re.search(r'[가-힣]', loc) else ('기타 지역' if loc else '미기재')),
                  req=req, pref=pref, must=must, nice=nice, edu=find(EDU, req), soft=find(SOFT, req + '\n' + pref)))
print(len(J), Counter(j['track'] for j in J))

def bucket(y): return '신입' if y == 0 else '1–2년' if y <= 2 else '3–4년' if y <= 4 else '5–6년' if y <= 6 else '7–9년' if y <= 9 else '10년+'
BK = ['신입', '1–2년', '3–4년', '5–6년', '7–9년', '10년+']
ORDER = ['전체', '콘텐츠', '디지털', '글로벌', '브랜드', '마케터']
DATA = set(TAX['데이터·분석'])
out = {'tracks': {}, 'jobs': [], 'groups': list(TAX)}
for tr in ORDER:
    S = [j for j in J if tr == '전체' or j['track'] == tr]; n = len(S)
    rc = Counter(k for j in S for k in j['must']); pc = Counter(k for j in S for k in j['nice'])
    skills = sorted([dict(skill=k, group=GROUP[k], must=rc[k], nice=pc[k]) for k in set(rc) | set(pc)], key=lambda d: -(d['must'] + d['nice']))
    mins = [j['yf'] for j in S]; bc = Counter(bucket(y) for y in mins)
    stages = []
    for lo, hi, lab in [(0, 2, '2년 이하'), (3, 4, '3–4년'), (5, 99, '5년 이상')]:
        G = [j for j in S if lo <= j['yf'] <= hi]; c = Counter(k for j in G for k in j['must'])
        stages.append(dict(stage=lab, n=len(G), top=[[k, v] for k, v in c.most_common(6)]))
    out['tracks'][tr] = dict(n=n, companies=len({j['co'] for j in S}), newbie=sum(1 for y in mins if y == 0), junior=sum(1 for y in mins if y <= 2),
        median_years=statistics.median(mins), capital=sum(1 for j in S if j['loc2'] in ('서울', '경기')), seoul=sum(1 for j in S if j['loc2'] == '서울'),
        kpi5=sum(1 for j in S if DATA & set(j['must'] + j['nice'])),
        skills=skills, years=[[b, bc[b]] for b in BK], locations=Counter(j['loc2'] for j in S).most_common(),
        edu=Counter(e for j in S for e in j['edu']).most_common(), soft=Counter(e for j in S for e in j['soft']).most_common(),
        stages=stages, topco=Counter(j['co'] for j in S).most_common(8))
for j in J:
    yt = None if (j['yt'] or 0) >= 100 else j['yt']
    out['jobs'].append(dict(id=j['id'], c=j['co'], p=j['pos'], t=j['track'], l=j['loc2'], y=j['yf'],
        yl=(f"{j['yf']}년 이상" if yt is None else f"{j['yf']}–{yt}년") if j['yf'] else ('신입 가능' if yt is None or yt == 0 else f"신입–{yt}년"),
        m=j['must'], k=j['nice'], r=j['req'], q=j['pref']))
json.dump(out, open('data_mkt.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))

for tr in ORDER:
    t = out['tracks'][tr]; n = t['n']
    print('\n##', tr, 'n', n, 'co', t['companies'], 'newbie', t['newbie'], round(t['newbie']/n*100), 'junior', t['junior'], round(t['junior']/n*100), 'med', t['median_years'], 'cap', round(t['capital']/n*100), 'seoul', round(t['seoul']/n*100), 'data', t['kpi5'], round(t['kpi5']/n*100))
    print(' MUST', [(s['skill'], s['must'], round(s['must']/n*100)) for s in sorted(t['skills'], key=lambda s: -s['must'])[:16]])
    print(' NICE', [(s['skill'], s['nice'], s['must']) for s in sorted(t['skills'], key=lambda s: -s['nice'])[:14]])
    print(' YEARS', t['years']); print(' LOC', t['locations']); print(' EDU', [(a, b, round(b/n*100)) for a, b in t['edu']]); print(' SOFT', [(a, b, round(b/n*100)) for a, b in t['soft']])
    for st in t['stages']: print(' ', st['stage'], st['n'], [(k, v, round(v/max(st['n'],1)*100)) for k, v in st['top']])
    print(' TOPCO', t['topco'])
