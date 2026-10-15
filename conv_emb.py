import json, statistics
from collections import Counter
J = json.load(open('jobs.json', encoding='utf-8'))
GROUPS = ["언어","OS·플랫폼","프로세서·칩","통신·인터페이스","HW 설계·검증","개발 도구·방법론","AI·비전","로보틱스·제어","차량·안전 표준"]
def track(x):
    tags = [t['id'] for t in json.load(open(f"data/d/{x['id']}.json", encoding='utf-8'))['job']['category_tags']]
    a, b = 658 in tags, 672 in tags
    return '임베디드' if a and not b else '하드웨어' if b and not a else '임베디드' if x['cat'] == 658 else '하드웨어' if x['cat'] == 672 else ('임베디드' if a else '하드웨어')
def norm(d):
    out = {}
    for g in GROUPS:
        for k in d.get(g, []):
            out['C/C++' if k in ('C', 'C++') else k] = g
    return out
GROUP = {}
for x in J:
    x['track'] = track(x)
    m = norm(x['rk']); p = norm(x['pk']); GROUP.update(m); GROUP.update(p)
    x['must'] = sorted(m); x['nice'] = sorted(set(p) - set(m))
    x['yf'] = x['yf'] or 0
    x['loc2'] = {'서울': '서울', '경기': '경기', 'Tokyo': '해외(도쿄)'}.get(x['loc'], '기타 지역' if x['loc'] else '미기재')
def bucket(y): return '신입' if y == 0 else '1–2년' if y <= 2 else '3–4년' if y <= 4 else '5–6년' if y <= 6 else '7–9년' if y <= 9 else '10년+'
BK = ['신입', '1–2년', '3–4년', '5–6년', '7–9년', '10년+']
out = {'tracks': {}, 'jobs': [], 'groups': GROUPS}
for tr in ['전체', '임베디드', '하드웨어']:
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
        kpi5=sum(1 for j in S if 'C/C++' in j['must']), skills=skills, years=[[b, bc[b]] for b in BK], locations=Counter(j['loc2'] for j in S).most_common(),
        edu=Counter(e for j in S for e in j['edu']).most_common(), soft=Counter(e for j in S for e in j['soft']).most_common(), stages=stages)
    t = out['tracks'][tr]; print(tr, n, t['companies'], t['newbie'], t['junior'], t['median_years'], round(t['capital']/n*100), round(t['kpi5']/n*100), [(s['skill'],s['must']) for s in sorted(skills,key=lambda s:-s['must'])[:5]])
    for st in stages: print('  ', st['stage'], st['n'], st['top'][:4])
for j in J:
    yt = None if (j['yt'] or 0) >= 100 else j['yt']
    out['jobs'].append(dict(id=j['id'], c=j['co'], p=j['pos'], t=j['track'], l=j['loc2'], y=j['yf'],
        yl=(f"{j['yf']}년 이상" if yt is None else f"{j['yf']}–{yt}년") if j['yf'] else ('신입 가능' if yt is None or yt == 0 else f"신입–{yt}년"),
        m=j['must'], k=j['nice'], r=j['req'], q=j['pref']))
json.dump(out, open('emb_data.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
