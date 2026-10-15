import json, urllib.request, time, os
from concurrent.futures import ThreadPoolExecutor
L=json.load(open('data/list.json',encoding='utf-8'))
os.makedirs('data/d',exist_ok=True)
def get(i):
    p=f'data/d/{i}.json'
    if os.path.exists(p): return
    for t in range(3):
        try:
            r=urllib.request.Request(f"https://www.wanted.co.kr/api/v4/jobs/{i}",headers={"User-Agent":"Mozilla/5.0"})
            open(p,'wb').write(urllib.request.urlopen(r,timeout=20).read()); return
        except Exception as e: time.sleep(2)
    print('fail',i)
with ThreadPoolExecutor(6) as ex: list(ex.map(get,[j['id'] for j in L]))
print(len(os.listdir('data/d')))
