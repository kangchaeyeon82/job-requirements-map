import json, re, os, statistics
from collections import Counter

L = json.load(open('data/list.json', encoding='utf-8'))
SEL = [872, 669, 873, 10110, 876]

TAX = {
 "언어": {"Java": r"\bjava\b(?!\s*script)", "Kotlin": r"kotlin|코틀린", "Python": r"python|파이썬", "JavaScript": r"javascript|(?<!\.)\bjs\b|자바스크립트",
         "TypeScript": r"typescript|타입스크립트|\bts\b", "Go": r"\bgolang\b|\bgo\b(?= ?(언어|lang|,|/|\)))", "PHP": r"\bphp\b", "C#": r"c#", "C/C++": r"c\+\+|(?<![a-z#/+])c(?= ?(언어|/c\+\+))",
         "Ruby": r"\bruby\b", "Rust": r"\brust\b", "Scala": r"\bscala\b", "Dart": r"\bdart\b"},
 "프레임워크": {"Spring/Spring Boot": r"spring|스프링", "JPA/Hibernate": r"\bjpa\b|hibernate|querydsl", "Django": r"django|장고", "FastAPI": r"fastapi", "Flask": r"\bflask\b",
         "Node.js": r"node\.?js|\bnode\b", "NestJS": r"nest\.?js", "Express": r"express\.?js", "React": r"react(?!\s*native)|리액트", "Next.js": r"next\.?js", "Vue": r"vue|뷰\.?js", "Nuxt": r"nuxt",
         "Angular": r"angular", "Svelte": r"svelte", ".NET": r"\.net\b|asp\.net", "Laravel": r"laravel", "Rails": r"rails", "React Native": r"react\s*native", "Flutter": r"flutter"},
 "데이터베이스·메시징": {"MySQL": r"mysql|mariadb", "PostgreSQL": r"postgre", "Oracle": r"oracle", "MSSQL": r"mssql|sql server", "MongoDB": r"mongo", "Redis": r"redis",
         "Elasticsearch": r"elastic|opensearch", "Kafka": r"kafka", "RabbitMQ/SQS": r"rabbitmq|\bsqs\b|메시지 ?큐|message queue", "SQL·RDBMS": r"\bsql\b|rdb|관계형", "NoSQL": r"nosql"},
 "인프라·클라우드": {"AWS": r"\baws\b|amazon web", "GCP": r"\bgcp\b|google cloud", "Azure": r"azure", "Docker": r"docker|도커|컨테이너", "Kubernetes": r"kubernetes|\bk8s\b|쿠버네티스|\beks\b",
         "Terraform/IaC": r"terraform|\biac\b", "CI/CD": r"ci/cd|ci ?/ ?cd|jenkins|github actions|argocd|배포 자동화", "Linux": r"linux|리눅스", "MSA": r"\bmsa\b|마이크로 ?서비스|microservice",
         "Serverless": r"serverless|lambda|서버리스", "모니터링": r"모니터링|monitoring|datadog|grafana|prometheus|observability"},
 "프론트엔드": {"HTML/CSS": r"html|css", "상태관리(Redux 등)": r"redux|zustand|recoil|mobx|jotai|상태 ?관리", "React Query/SWR": r"react[- ]?query|tanstack|\bswr\b",
         "반응형·크로스브라우징": r"반응형|크로스 ?브라우|responsive|cross[- ]browser",
         "웹 접근성": r"접근성|accessibility|a11y", "빌드 도구(Webpack/Vite)": r"webpack|vite|babel|번들", "CSS 프레임워크": r"tailwind|styled[- ]components|emotion|scss|sass",
         "디자인 시스템": r"디자인 ?시스템|design system|storybook", "SSR·SEO": r"\bssr\b|서버 ?사이드 ?렌더링|\bseo\b"},
 "설계·품질": {"REST API": r"\brest(ful)?\b|api ?(설계|개발)", "성능 최적화": r"성능 ?(최적화|개선|튜닝)|web vitals|렌더링 최적화|performance (optimi|tuning)", "GraphQL": r"graphql", "gRPC": r"grpc", "대용량 트래픽": r"대용량|대규모 트래픽|high traffic|트래픽", "분산 시스템": r"분산|distributed",
         "테스트 코드/TDD": r"테스트 ?코드|단위 ?테스트|unit test|\btdd\b|jest|cypress|playwright|junit|testing", "DDD·객체지향 설계": r"\bddd\b|도메인 주도|객체 ?지향|oop|설계 패턴|design pattern|clean architecture|클린 아키텍처",
         "CS 기초": r"자료 ?구조|알고리즘|algorithm|data structure|운영 ?체제|컴퓨터 ?과학|cs 지식|cs 기초|네트워크 이해", "보안": r"보안|security|oauth|인증/인가"},
 "AI": {"LLM·생성형 AI": r"\bllm\b|생성형|gpt|langchain|openai|claude|gemini|프롬프트|prompt", "AI/ML": r"머신 ?러닝|machine learning|딥 ?러닝|deep learning|pytorch|tensorflow|mlops|(\bai\b|인공지능) ?(모델|서비스|기술|시스템|에이전트|agent|엔지니어|개발|플랫폼|솔루션|연구)|모델 ?(학습|서빙|개발|추론)", "RAG·벡터DB": r"\brag\b|벡터|vector",
         "AI 코딩 도구 활용": r"cursor|copilot|claude ?code|codex|ai ?(코딩|도구|툴|어시스턴트|assistant)|ai[- ]native|바이브 ?코딩|ai를 (적극|활용)|ai 활용"},
 "기획·PM": {"서비스 기획·요구사항 정의": r"서비스 ?기획|제품 ?기획|기획 ?(경험|역량|능력|업무)|요구 ?사항 ?(정의|분석|도출)|\bprd\b|스펙 ?정의|requirements? (definition|gathering)", "데이터 분석·지표": r"데이터 ?분석|지표|metric|kpi|a/b|amplitude|mixpanel|ga4|google analytics|태블로|tableau",
         "Figma·와이어프레임": r"figma|피그마|와이어프레임|wireframe|프로토타입", "프로젝트·일정 관리": r"일정 ?관리|프로젝트 ?관리|project manag|pmp|리소스 관리"},
 "협업 도구·방식": {"Git": r"\bgit\b|github|gitlab|형상 ?관리", "코드 리뷰": r"코드 ?리뷰|code review", "Agile/Scrum": r"agile|애자일|scrum|스크럼", "Jira/Confluence": r"jira|confluence"},
}
EDU = {"학사 이상": r"학사|bachelor|4년제|대졸|b\.?s\.?\b", "석사 이상": r"석사|master", "컴퓨터공학/관련 전공": r"컴퓨터|computer science|전산|소프트웨어 ?공학|관련 ?전공", "전공 무관": r"전공 ?무관|학력 ?무관"}
SOFT = {"커뮤니케이션/협업": r"커뮤니케이션|소통|협업|communication|collaborat", "문제 해결·주도성": r"주도|문제 ?해결|problem[- ]solving|ownership|오너십",
        "문서화": r"문서|documentation", "영어": r"영어|english|영문", "제품·사용자 관점": r"사용자 ?(경험|관점)|제품 ?(관점|마인드)|비즈니스 (이해|임팩트)|product mind", "빠른 실행·스타트업": r"스타트업|startup|빠르게"}

def find(dic, text):
    return [k for k, p in dic.items() if re.search(p, text, re.I)]

def track_of(it, tags):
    if it['category_tag']['id'] in SEL: return it['category_tag']['id']
    for t in tags:
        if t in SEL: return t
    return None

jobs = []
names = Counter()
for it in L:
    p = f"data/d/{it['id']}.json"
    if not os.path.exists(p): continue
    j = json.load(open(p, encoding='utf-8'))['job']; d = j['detail']
    tags = [t['id'] for t in j.get('category_tags', [])]
    tr = track_of(it, tags)
    req = d.get('requirements') or ''; pref = d.get('preferred_points') or ''
    rk, pk = [], []
    for g, dic in TAX.items():
        rk += [(g, k) for k in find(dic, req)]
        pk += [(g, k) for k in find(dic, pref)]
    addr = j.get('address') or {}
    loc = (addr.get('location') or '').strip()
    jobs.append(dict(id=it['id'], co=j['company']['name'], pos=j['position'], cat=tr,
        yf=it.get('annual_from') or 0, yt=it.get('annual_to'), loc=loc,
        req=req, pref=pref, rk=rk, pk=[x for x in pk if x not in rk],
        edu=find(EDU, req), soft=find(SOFT, req + '\n' + pref)))
json.dump(jobs, open('jobs_raw.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(jobs), Counter(j['cat'] for j in jobs))
for c in SEL:
    print(c, [j['pos'] for j in jobs if j['cat'] == c][:12])
print(Counter(j['loc'] for j in jobs).most_common(12))
