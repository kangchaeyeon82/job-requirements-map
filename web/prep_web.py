import json, statistics
from collections import Counter

J = json.load(open('jobs_raw.json', encoding='utf-8'))
TRACKS = {872: '서버', 669: '프론트엔드', 10110: '소프트웨어 엔지니어', 873: '웹', 876: '프로덕트 매니저'}
ORDER = ['전체', '서버', '프론트엔드', '소프트웨어 엔지니어', '웹', '프로덕트 매니저']
for j in J:
    j['track'] = TRACKS[j['cat']]
    j['loc2'] = {'서울': '서울', '경기': '경기'}.get(j['loc'], '해외' if j['loc'] in ('Tokyo', 'Kanagawa', 'Osaka') else ('기타 지역' if j['loc'] else '미기재'))
    j['must'] = sorted({k for g, k in j['rk']})
    j['nice'] = sorted({k for g, k in j['pk']} - set(j['must']))
GROUP = {k: g for j in J for g, k in j['rk'] + j['pk']}

def bucket(y):
    return '신입' if y == 0 else '1–2년' if y <= 2 else '3–4년' if y <= 4 else '5–6년' if y <= 6 else '7–9년' if y <= 9 else '10년+'
BK = ['신입', '1–2년', '3–4년', '5–6년', '7–9년', '10년+']
STAGES = [(0, 2, '2년 이하'), (3, 4, '3–4년'), (5, 99, '5년 이상')]

out = {'tracks': {}, 'jobs': []}
for tr in ORDER:
    S = [j for j in J if tr == '전체' or j['track'] == tr]; n = len(S)
    rc = Counter(k for j in S for k in j['must']); pc = Counter(k for j in S for k in j['nice'])
    skills = sorted([dict(skill=k, group=GROUP[k], must=rc[k], nice=pc[k]) for k in set(rc) | set(pc)], key=lambda d: -(d['must'] + d['nice']))
    mins = [j['yf'] for j in S]
    bc = Counter(bucket(y) for y in mins)
    stages = []
    for lo, hi, lab in STAGES:
        G = [j for j in S if lo <= j['yf'] <= hi]
        c = Counter(k for j in G for k in j['must'])
        stages.append(dict(stage=lab, n=len(G), top=[[k, v] for k, v in c.most_common(6)]))
    out['tracks'][tr] = dict(
        n=n, companies=len({j['co'] for j in S}),
        newbie=sum(1 for y in mins if y == 0), junior=sum(1 for y in mins if y <= 2),
        median_years=statistics.median(mins),
        capital=sum(1 for j in S if j['loc2'] in ('서울', '경기')),
        seoul=sum(1 for j in S if j['loc2'] == '서울'),
        skills=skills,
        years=[[b, bc[b]] for b in BK],
        locations=Counter(j['loc2'] for j in S).most_common(),
        edu=Counter(e for j in S for e in j['edu']).most_common(),
        soft=Counter(e for j in S for e in j['soft']).most_common(),
        stages=stages,
        topco=Counter(j['co'] for j in S).most_common(8),
    )
for j in J:
    yt = None if (j['yt'] or 0) >= 100 else j['yt']
    out['jobs'].append(dict(id=j['id'], c=j['co'], p=j['pos'], t=j['track'], l=j['loc2'], y=j['yf'],
        yl=(f"{j['yf']}년 이상" if yt is None else f"{j['yf']}–{yt}년") if j['yf'] else ('신입 가능' if yt is None or yt == 0 else f"신입–{yt}년"),
        m=j['must'], k=j['nice'], r=j['req'], q=j['pref']))
json.dump(out, open('data_web.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
import os; print(os.path.getsize('data_web.json'))
for tr in ORDER:
    t = out['tracks'][tr]
    print('\n##', tr, 'n', t['n'], 'co', t['companies'], 'newbie', t['newbie'], round(t['newbie']/t['n']*100), 'junior', t['junior'], round(t['junior']/t['n']*100), 'med', t['median_years'], 'cap', round(t['capital']/t['n']*100), 'seoul', round(t['seoul']/t['n']*100))
    print(' MUST', [(s['skill'], s['must'], round(s['must']/t['n']*100)) for s in sorted(t['skills'], key=lambda s: -s['must'])[:15]])
    print(' NICE', [(s['skill'], s['nice'], s['must']) for s in sorted(t['skills'], key=lambda s: -s['nice'])[:12]])
    print(' YEARS', t['years']); print(' LOC', t['locations']); print(' EDU', [(a, b, round(b/t['n']*100)) for a, b in t['edu']]); print(' SOFT', [(a, b, round(b/t['n']*100)) for a, b in t['soft']])
    for st in t['stages']: print(' ', st['stage'], st['n'], [(k, v, round(v/st['n']*100)) for k, v in st['top']])
    print(' TOPCO', t['topco'])
