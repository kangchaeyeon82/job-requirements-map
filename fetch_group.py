"""원티드 목록 API에서 한 직군 그룹의 공고 목록을 받아 data/list.json에 저장합니다.
사용: python ../fetch_group.py <그룹 id> <직군 id> [<직군 id> ...]
예:   python ../fetch_group.py 523 1635 1030 950 707 710
"""
import json, os, sys, time, urllib.request
group, ids = sys.argv[1], sys.argv[2:]
base = (f"https://www.wanted.co.kr/api/chaos/navigation/v1/results?job_group_id={group}"
        + "".join(f"&job_ids={i}" for i in ids)
        + "&country=all&job_sort=job.popularity_order&years=-1&locations=all&limit=100&offset=%d")
os.makedirs('data/d', exist_ok=True)
allj, off = [], 0
while True:
    d = json.load(urllib.request.urlopen(urllib.request.Request(base % off, headers={"User-Agent": "Mozilla/5.0"})))
    allj += d['data']
    if not d['links'].get('next') or not d['data']: break
    off += 100; time.sleep(0.5)
json.dump(allj, open('data/list.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(allj))
