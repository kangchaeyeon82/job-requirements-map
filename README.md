# 직무 채용 지도

원티드 채용 공고 3,702건의 자격요건과 우대사항을 분석해, 직무마다 무엇을 요구하는지 보여 주는 사이트입니다. 엔지니어, 개발, 마케팅, 디자인 네 분야를 한곳에 모았고, 오른쪽 사이드바에서 AI에게 취업 상담을 받을 수 있습니다.

- 🌐 사이트: https://claude.ai/artifact/Mhvc6SB4fQWqpz3KvusJGz
- 📘 학습 로드맵 보고서 (마케팅·디자인): https://claude.ai/code/artifact/229d250d-cd85-47db-8cca-4b11c58937d8

> 수집 시점: 2026-10-15

## 분야와 공고 수

| 분야 | 세부 직군 | 공고 | 회사 |
|---|---|---|---|
| 엔지니어 | 임베디드 개발자, 하드웨어 엔지니어 | 263 | 154 |
| 개발 | 서버, 프론트엔드, 소프트웨어 엔지니어, 웹, 프로덕트 매니저 | 1,258 | 652 |
| 마케팅 | 콘텐츠, 디지털, 글로벌, 브랜드 마케터, 마케터 | 1,687 | 843 |
| 디자인 | UI·GUI, 웹, 영상·모션, 콘텐츠, UX 디자이너 | 494 | 371 |

## 사이트 구성

상단 버튼으로 분야를 고르고, 그 아래 탭에서 세부 직군을 고릅니다. 주소 끝에 `#engineer`, `#dev`, `#marketing`, `#design`을 붙이면 그 분야로 바로 열립니다.

1. **요약**: 한 줄 요약과 핵심 지표 6개(공고 수, 기업 수, 경력 중앙값, 신입 가능 비율, 분야별 지표, 수도권 비율)
2. **핵심 인사이트** 4개
3. **가장 많이 요구하는 기술·역량 Top 20**: 필수와 우대를 구분
4. **경력 단계별 요구 기술**: 2년 이하, 3–4년, 5년 이상
5. **준비 체크리스트**: 기본기, 핵심, 가산점
6. **분야별 상세 요건**
7. **경력·학력·근무지**
8. **공고별 요건 표**: 검색과 정렬이 되고, 원문을 볼 수 있습니다
9. **AI 취업 상담 사이드바**: 지금 보는 직군의 통계를 근거로 답하고, 조건에 맞는 공고를 찾아 줍니다

### 주요 결과

- **엔지니어**: C/C++을 필수로 요구하는 공고가 47%입니다(임베디드 64%).
- **개발**: 공고의 50%가 LLM, AI 모델, AI 코딩 도구 중 하나를 언급합니다.
- **마케팅**: 2년 이하도 지원할 수 있는 공고가 53%로 진입 문턱이 가장 낮습니다.
- **디자인**: Figma를 48%가 언급하고, 39%는 포트폴리오를 직접 요구합니다.

## 폴더 구조

```
site/                 배포용 사이트
  index.html          페이지 (분야 전환, 대시보드, AI 사이드바)
  data/*.json         분야별 집계 데이터와 공고 목록
fetch_group.py        원티드 목록 API → data/list.json (그룹·직군 id를 인자로 받음)
fetch_detail.py       공고 상세 API → data/d/{id}.json
fetch_list.py         엔지니어 분야 목록 수집 (fetch_group.py의 고정 버전)
analyze.py, prep.py   엔지니어 분야 키워드 분석
conv_emb.py, ins_emb.py   엔지니어 데이터를 사이트 형식으로 변환, 해석 문장
web/                  개발 분야 (analyze_web.py, prep_web.py, insights_web.py, sections_web.py)
mkt/                  마케팅 분야 (analyze_mkt.py, ins_mkt.py)
dsn/                  디자인 분야 (analyze_dsn.py, ins_dsn.py)
web/page.tpl.html     대시보드 템플릿 원본
mk_shared.py          템플릿을 분야 공용으로 바꿔 page_shared.tpl.html 생성
chat_snippet.py       AI 사이드바 HTML·CSS·JS
make_site.py          site/ 전체를 만드는 빌드 스크립트
```

## 다시 만들기

Python 3.9 이상이 필요하고 표준 라이브러리만 씁니다. Windows 콘솔에서 한글이 깨지면 `PYTHONIOENCODING=utf-8`을 설정하세요.

```bash
# 엔지니어 (저장소 루트에서)
python fetch_list.py && python fetch_detail.py && python analyze.py && python conv_emb.py

# 개발
cd web && python ../fetch_group.py 518 872 669 873 10110 876 && python ../fetch_detail.py && python analyze_web.py && python prep_web.py && cd ..

# 마케팅
cd mkt && python ../fetch_group.py 523 1635 1030 950 707 710 && python ../fetch_detail.py && python analyze_mkt.py && cd ..

# 디자인
cd dsn && python ../fetch_group.py 511 594 599 597 602 10532 && python ../fetch_detail.py && python analyze_dsn.py && cd ..

# 사이트 빌드
python mk_shared.py && python make_site.py
```

해석 문장(`ins_*.py`, `web/insights_web.py`, `web/sections_web.py`)에는 2026-10-15 수치가 직접 적혀 있습니다. 데이터를 새로 받으면 숫자를 다시 확인해서 고쳐야 합니다.

## 사용한 외부 도구·서비스

| 도구 / 서비스 | 용도 |
|---|---|
| 원티드 공개 API | 공고 목록(`/api/chaos/navigation/v1/results`)과 상세(`/api/v4/jobs/{id}`) 수집. 인증 없음 |
| Claude Code | 수집·분석 스크립트 작성과 실행 |
| Claude Artifacts | 사이트 호스팅. AI 사이드바는 아티팩트의 `sample` 기능을 씁니다 |
| Claude Docs | 학습 로드맵 보고서 |
| GitHub CLI | 저장소 업로드 |

## 알아 둘 점

- **AI 사이드바**: Claude 아티팩트 안에서만 작동합니다. `site/`를 GitHub Pages 같은 다른 곳에 올리면 대시보드는 그대로 쓸 수 있지만 사이드바 버튼은 나타나지 않습니다. 질문할 때는 보는 사람 본인의 Claude 사용량을 씁니다.
- **원본 데이터**: 수집한 원본(`data/`)은 원티드 콘텐츠라 저장소에 넣지 않았습니다. 다만 `site/data/*.json`에는 공고별 자격요건·우대사항 원문이 들어 있으니, 저장소를 공개할 때는 이 점을 고려하세요.
- **키워드 정확도**: 키워드는 정규식으로 찾았기 때문에 문맥은 반영하지 못하고, 이미지로 올린 요건은 빠집니다.
- **분류 기준**: 공고마다 대표 직군 하나로 나눴습니다. 디자인의 10532번 직군은 공식 이름을 확인하지 못해, 공고 제목을 보고 "콘텐츠 디자이너"로 붙였습니다.
