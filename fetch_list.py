import json, urllib.request, time
base="https://www.wanted.co.kr/api/chaos/navigation/v1/results?job_group_id=518&job_ids=658&job_ids=672&country=all&job_sort=job.popularity_order&years=-1&locations=all&limit=100&offset=%d"
allj=[];off=0
while True:
    req=urllib.request.Request(base%off,headers={"User-Agent":"Mozilla/5.0"})
    d=json.load(urllib.request.urlopen(req))
    allj+=d['data']
    if not d['links'].get('next') or not d['data']: break
    off+=100; time.sleep(0.5)
json.dump(allj,open('data/list.json','w',encoding='utf-8'),ensure_ascii=False)
print(len(allj))
from collections import Counter
print(Counter(j['category_tag']['id'] for j in allj))
