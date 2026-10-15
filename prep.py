import json,os,statistics
from collections import Counter
J=json.load(open('jobs.json',encoding='utf-8'))
os.makedirs('out',exist_ok=True)
def track(x):
    tags=[t['id'] for t in json.load(open(f"data/d/{x['id']}.json",encoding='utf-8'))['job']['category_tags']]
    a,b=658 in tags,672 in tags
    return '임베디드' if a and not b else '하드웨어' if b and not a else '임베디드' if x['cat']==658 else '하드웨어' if x['cat']==672 else ('임베디드' if a else '하드웨어')
both=0
for x in J:
    x['track']=track(x)
print(Counter(x['track'] for x in J))
def norm(lst):
    out=[]
    for k in lst:
        k='C/C++' if k in('C','C++') else k
        if k not in out: out.append(k)
    return out
GROUPS=["언어","OS·플랫폼","프로세서·칩","통신·인터페이스","HW 설계·검증","개발 도구·방법론","AI·비전","로보틱스·제어","차량·안전 표준"]
def bucket(y):
    if y is None or y==0: return '0년 (신입 가능)'
    if y<=2: return '1–2년'
    if y<=4: return '3–4년'
    if y<=6: return '5–6년'
    if y<=9: return '7–9년'
    return '10년 이상'
BK=['0년 (신입 가능)','1–2년','3–4년','5–6년','7–9년','10년 이상']
LOCMAP={'서울':'서울','경기':'경기','Tokyo':'해외(도쿄)'}
jobs=[];skills=[];years=[];locs=[];edu=[];soft=[];summ=[]
for x in J:
    x['req_set']={(g,k) for g in GROUPS for k in norm(x['rk'].get(g,[]))}
    x['pref_set']={(g,k) for g in GROUPS for k in norm(x['pk'].get(g,[]))}
    loc=LOCMAP.get(x['loc'],'기타 지역') if x['loc'] else '미기재'
    x['loc2']=loc
    yt=None if (x['yt'] or 0)>=100 else x['yt']
    jobs.append(dict(id=str(x['id']),company=x['co'],position=x['pos'],track=x['track'],location=loc,district=x['dist'] or '',
       years_min=x['yf'] or 0, years_max=yt, years_label=(f"{x['yf'] or 0}년 이상" if yt is None else f"{x['yf'] or 0}–{yt}년"),
       must=", ".join(k for g,k in sorted(x['req_set'],key=lambda t:(GROUPS.index(t[0]),t[1]))),
       nice=", ".join(k for g,k in sorted(x['pref_set']-x['req_set'],key=lambda t:(GROUPS.index(t[0]),t[1]))),
       requirements=x['req'],preferred=x['pref'],url=f"https://www.wanted.co.kr/wd/{x['id']}"))
for tr in ['전체','임베디드','하드웨어']:
    S=[x for x in J if tr=='전체' or x['track']==tr]; n=len(S)
    rc=Counter(t for x in S for t in x['req_set']); pc=Counter(t for x in S for t in x['pref_set']-x['req_set'])
    for (g,k) in set(rc)|set(pc):
        skills.append(dict(track=tr,group=g,skill=k,must=rc[(g,k)],nice_only=pc[(g,k)],total=rc[(g,k)]+pc[(g,k)],must_share=round(rc[(g,k)]/n,4),total_share=round((rc[(g,k)]+pc[(g,k)])/n,4)))
    bc=Counter(bucket(x['yf']) for x in S)
    for i,b in enumerate(BK): years.append(dict(track=tr,order=i,bucket=b,jobs=bc[b]))
    lc=Counter(x['loc2'] for x in S)
    for l,c in lc.most_common(): locs.append(dict(track=tr,location=l,jobs=c))
    ec=Counter(e for x in S for e in x['edu'])
    for e,c in ec.most_common(): edu.append(dict(track=tr,item=e,jobs=c,share=round(c/n,4)))
    sc=Counter(e for x in S for e in x['soft'])
    for e,c in sc.most_common(): soft.append(dict(track=tr,item=e,jobs=c,share=round(c/n,4)))
    mins=[x['yf'] or 0 for x in S]
    summ.append(dict(track=tr,jobs=n,companies=len({x['co'] for x in S}),newbie_ok=sum(1 for m in mins if m==0),
       newbie_share=round(sum(1 for m in mins if m==0)/n,4),median_min_years=statistics.median(mins),
       capital_share=round(sum(1 for x in S if x['loc2'] in('서울','경기'))/n,4),
       cpp_share=round(sum(1 for x in S if ('언어','C/C++') in x['req_set'])/n,4)))
for name,rows in dict(jobs=jobs,skills=skills,years=years,locations=locs,education=edu,soft_skills=soft,summary=summ).items():
    json.dump(rows,open(f'out/{name}.json','w',encoding='utf-8'),ensure_ascii=False)
    print(name,len(rows),os.path.getsize(f'out/{name}.json'))
print(summ)
