import json, re, os, statistics
from collections import Counter

L = json.load(open('data/list.json', encoding='utf-8'))
TRACKS = {597: 'UI·GUI', 594: '웹', 602: '영상·모션', 10532: '콘텐츠', 599: 'UX'}
SEL = list(TRACKS)
TAX = {
 "디자인 툴": {"Figma": r"figma|피그마", "Photoshop": r"photoshop|포토샵", "Illustrator": r"illustrator|일러스트레이터", "Adobe 툴 전반": r"adobe|어도비",
   "Sketch": r"\bsketch\b|스케치 ?툴", "Adobe XD": r"\bxd\b", "InDesign": r"indesign|인디자인", "ProtoPie·Framer": r"protopie|프로토파이|framer|프레이머|principle"},
 "영상·3D 툴": {"After Effects": r"after ?effects|애프터 ?이펙트|\bae\b", "Premiere": r"premiere|프리미어", "Cinema 4D": r"cinema ?4d|\bc4d\b|시네마 ?4d", "Blender": r"blender|블렌더",
   "DaVinci·Final Cut": r"davinci|다빈치|final ?cut|파이널 ?컷", "3D 툴 전반": r"\b3d\b|3차원|keyshot|키샷|spline|unreal|언리얼|unity|유니티", "CapCut": r"capcut|캡컷|vrew"},
 "디자인 분야": {"UI 디자인": r"\bui\b|gui|인터페이스", "UX 디자인": r"\bux\b|사용자 ?경험|user experience", "웹 디자인": r"웹 ?(디자인|사이트|페이지)|web ?design|랜딩 ?페이지|landing",
   "앱 디자인": r"앱 ?(디자인|서비스)|모바일 ?(앱|ui)|\bapp\b", "브랜딩·BX": r"브랜딩|\bbx\b|브랜드 ?(디자인|아이덴티티|경험)|\bbi\b|\bci\b|branding",
   "그래픽·편집 디자인": r"그래픽|편집 ?디자인|graphic|타이포|typograph|레이아웃", "상세페이지·배너": r"상세 ?페이지|배너|banner|프로모션 ?디자인|기획전",
   "일러스트": r"일러스트(?!레이터)|illustration|드로잉|캐릭터", "패키지 디자인": r"패키지|package", "인쇄물": r"인쇄|print|굿즈|리플렛|브로슈어|포스터"},
 "UX 방법론": {"사용자 리서치": r"리서치|research|인터뷰|사용자 ?조사", "사용성 테스트": r"사용성|usability|유저 ?테스트|user test", "와이어프레임·IA": r"와이어 ?프레임|wireframe|\bia\b|정보 ?구조|user ?flow|유저 ?플로우|스토리보드",
   "프로토타이핑": r"프로토 ?타입|prototyp", "데이터 기반 개선": r"데이터|data|a/b|지표|ga4?\b|amplitude", "UX 라이팅": r"ux ?라이팅|ux ?writing|마이크로 ?카피"},
 "디자인 시스템·협업": {"디자인 시스템": r"디자인 ?시스템|design ?system|컴포넌트|component|가이드 ?라인|guideline", "개발자 협업": r"개발자와?|개발 ?(팀|직군)과|engineer|핸드 ?오프|hand-?off|zeplin|제플린",
   "반응형·멀티 디바이스": r"반응형|responsive|멀티 ?디바이스|다양한 ?(기기|디바이스)", "접근성": r"접근성|accessibility", "Jira·Notion 협업": r"jira|지라|notion|노션|slack|confluence"},
 "개발 이해": {"HTML/CSS": r"html|css", "JavaScript": r"javascript|자바스크립트|jquery|제이쿼리", "퍼블리싱": r"퍼블리싱|publishing|코딩", "노코드(Webflow 등)": r"webflow|웹플로우|노코드|no-?code|아임웹|카페24|cafe24|wix|윅스"},
 "영상·모션": {"모션 그래픽": r"모션 ?(그래픽|디자인)?|motion|애니메이션|animation|인터랙션|interaction", "영상 편집": r"영상 ?(편집|제작)|video edit|편집 ?툴", "촬영": r"촬영|shooting|카메라|사진",
   "숏폼": r"숏폼|short[- ]?form|릴스|reels|쇼츠|shorts|틱톡|tiktok", "로티(Lottie)": r"lottie|로티"},
 "콘텐츠·마케팅": {"SNS 콘텐츠": r"sns|인스타|instagram|소셜|유튜브|youtube|썸네일", "광고 소재": r"광고 ?(소재|디자인|배너)|퍼포먼스|소재 ?(제작|디자인)|\bcreative\b", "이커머스": r"이커머스|e-?commerce|커머스|쇼핑몰|자사몰",
   "트렌드 감각": r"트렌드|trend|감각|센스", "마케팅 이해": r"마케팅|marketing"},
 "AI 활용": {"생성형 AI 활용": r"생성형|midjourney|미드저니|stable diffusion|firefly|파이어플라이|runway|chat ?gpt|\bgpt\b|ai ?(툴|도구|이미지|활용|생성)|나노 ?바나나|higgsfield|kling|sora|veo", "AI 영상 생성": r"(ai|인공지능) ?영상|runway|kling|sora|veo|higgsfield"},
}
EDU = {"학사 이상": r"학사|bachelor|4년제|대졸", "석사 이상": r"석사|master", "디자인 관련 전공": r"디자인 ?(관련 )?전공|디자인학|시각 ?디자인|산업 ?디자인|관련 ?전공|미술", "전공 무관": r"전공 ?무관|학력 ?무관"}
SOFT = {"커뮤니케이션/협업": r"커뮤니케이션|소통|협업|communication|collaborat", "문제 해결·주도성": r"주도|문제 ?해결|ownership|오너십|자기 ?주도", "논리적 설명": r"논리|설득|근거|설명할 수",
        "트렌드·미적 감각": r"트렌드|trend|감각|센스|미적|심미", "빠른 실행력": r"빠르게|실행력|스타트업|startup|빠른 ?속도", "영어": r"영어|english|영문"}
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
                  req=req, pref=pref, must=must, nice=nice, edu=find(EDU, req), soft=find(SOFT, req + '\n' + pref),
                  pf=bool(re.search(r'포트폴리오|portfolio', req + pref + (d.get('main_tasks') or '') + (d.get('intro') or '') + (d.get('benefits') or ''), re.I))))
print(len(J), Counter(j['track'] for j in J))

def bucket(y): return '신입' if y == 0 else '1–2년' if y <= 2 else '3–4년' if y <= 4 else '5–6년' if y <= 6 else '7–9년' if y <= 9 else '10년+'
BK = ['신입', '1–2년', '3–4년', '5–6년', '7–9년', '10년+']
ORDER = ['전체', 'UI·GUI', '웹', '영상·모션', '콘텐츠', 'UX']
DATA = None  # set below
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
        kpi5=sum(1 for j in S if j['pf']),
        skills=skills, years=[[b, bc[b]] for b in BK], locations=Counter(j['loc2'] for j in S).most_common(),
        edu=Counter(e for j in S for e in j['edu']).most_common(), soft=Counter(e for j in S for e in j['soft']).most_common(),
        stages=stages, topco=Counter(j['co'] for j in S).most_common(8))
for j in J:
    yt = None if (j['yt'] or 0) >= 100 else j['yt']
    out['jobs'].append(dict(id=j['id'], c=j['co'], p=j['pos'], t=j['track'], l=j['loc2'], y=j['yf'],
        yl=(f"{j['yf']}년 이상" if yt is None else f"{j['yf']}–{yt}년") if j['yf'] else ('신입 가능' if yt is None or yt == 0 else f"신입–{yt}년"),
        m=j['must'], k=j['nice'], r=j['req'], q=j['pref']))
json.dump(out, open('data_dsn.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))

for tr in ORDER:
    t = out['tracks'][tr]; n = t['n']
    print('\n##', tr, 'n', n, 'co', t['companies'], 'newbie', t['newbie'], round(t['newbie']/n*100), 'junior', t['junior'], round(t['junior']/n*100), 'med', t['median_years'], 'cap', round(t['capital']/n*100), 'seoul', round(t['seoul']/n*100), 'data', t['kpi5'], round(t['kpi5']/n*100))
    print(' MUST', [(s['skill'], s['must'], round(s['must']/n*100)) for s in sorted(t['skills'], key=lambda s: -s['must'])[:16]])
    print(' NICE', [(s['skill'], s['nice'], s['must']) for s in sorted(t['skills'], key=lambda s: -s['nice'])[:14]])
    print(' YEARS', t['years']); print(' LOC', t['locations']); print(' EDU', [(a, b, round(b/n*100)) for a, b in t['edu']]); print(' SOFT', [(a, b, round(b/n*100)) for a, b in t['soft']])
    for st in t['stages']: print(' ', st['stage'], st['n'], [(k, v, round(v/max(st['n'],1)*100)) for k, v in st['top']])
    print(' TOPCO', t['topco'])
