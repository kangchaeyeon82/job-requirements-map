CSS = r'''
.ai-btn{flex:none;font:inherit;font-size:14px;font-weight:800;border:0;border-radius:999px;padding:9px 16px;background:var(--ink);color:#fff;cursor:pointer;display:inline-flex;align-items:center;gap:6px}
.ai-btn:hover{background:#333d4b}
.ai-btn[aria-expanded="true"]{background:var(--accent-soft);color:var(--accent-ink)}
.ai-dot{width:8px;height:8px;border-radius:50%;background:var(--badge)}
.top-right{display:flex;align-items:center;gap:8px;flex-wrap:wrap;min-width:0}
.chat{position:fixed;z-index:40;right:0;top:0;bottom:0;width:400px;max-width:100%;background:var(--card);border-left:1px solid var(--line);display:flex;flex-direction:column;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px);box-shadow:-12px 0 32px rgba(25,31,40,.06)}
.chat-h{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:16px 18px 12px;border-bottom:1px solid var(--line)}
.chat-h b{font-size:17px;font-weight:800}
.chat-h small{display:block;font-size:12px;color:var(--sub);font-weight:500;margin-top:2px}
.chat-h .acts{display:flex;gap:6px}
.icon-btn{font:inherit;font-size:13px;font-weight:700;border:0;border-radius:10px;padding:7px 10px;background:var(--page);color:var(--ink2);cursor:pointer}
.icon-btn:hover{background:var(--line)}
.ctx{margin:12px 18px 0;padding:10px 12px;border-radius:12px;background:var(--accent-soft);color:var(--accent-ink);font-size:12.5px;font-weight:600;line-height:1.5}
.msgs{flex:1;overflow-y:auto;padding:14px 18px;display:flex;flex-direction:column;gap:12px}
.msg{max-width:92%;font-size:14px;line-height:1.7;word-break:keep-all;overflow-wrap:anywhere}
.msg.u{align-self:flex-end;background:var(--accent);color:#fff;border-radius:16px 16px 4px 16px;padding:10px 14px;white-space:pre-wrap}
.msg.a{align-self:flex-start;background:var(--page);color:var(--ink);border-radius:16px 16px 16px 4px;padding:12px 14px}
.msg.a p{margin:0 0 6px}.msg.a p:last-child{margin:0}
.msg.a ul,.msg.a ol{margin:2px 0 8px;padding-left:18px}
.msg.a li{margin:2px 0}
.msg.a a{color:var(--accent-ink);font-weight:700}
.msg.a .h{font-weight:800;margin-top:6px}
.msg.think{color:var(--sub);font-style:normal}
.msg.err{background:var(--red-soft);color:var(--red)}
.tool-note{font-size:12px;color:var(--sub);align-self:flex-start;padding-left:4px}
.hello{background:var(--page);border-radius:16px;padding:16px;font-size:14px;line-height:1.7;color:var(--ink2)}
.hello b{display:block;font-size:15px;color:var(--ink);margin-bottom:4px}
.sugs{display:flex;flex-wrap:wrap;gap:6px;padding:0 18px 10px}
.sug{font:inherit;font-size:13px;font-weight:600;border:1px solid var(--line);background:var(--card);color:var(--ink2);border-radius:999px;padding:7px 12px;cursor:pointer;text-align:left}
.sug:hover{border-color:var(--accent);color:var(--accent-ink)}
.compose{display:flex;gap:8px;align-items:flex-end;padding:12px 18px 16px;border-top:1px solid var(--line)}
.compose textarea{flex:1;min-width:0;resize:none;font:inherit;font-size:14px;line-height:1.5;border:0;border-radius:14px;background:var(--page);padding:11px 14px;color:var(--ink);max-height:140px}
.compose textarea::placeholder{color:var(--faint)}
.send{flex:none;font:inherit;font-size:14px;font-weight:800;border:0;border-radius:14px;padding:11px 16px;background:var(--accent);color:#fff;cursor:pointer}
.send:disabled{background:var(--accent-mid);cursor:default}
.send.stop{background:var(--ink)}
.chat-note{font-size:11.5px;color:var(--faint);padding:0 18px 12px;margin-top:-8px}
@media (min-width:1180px){body.chat-open{padding-right:400px}}
@media (max-width:1179px){.chat{width:100%;max-width:440px}}
@media (max-width:520px){.chat{max-width:100%;border-left:0}.ai-btn .lbl{display:none}}
'''

BTN = '''<div class="top-right"><nav class="fields" id="fields" aria-label="직무 분야"></nav><button class="ai-btn" id="ai-toggle" type="button" aria-expanded="false" aria-controls="chat" hidden><span class="ai-dot"></span><span class="lbl">AI에게 묻기</span><span class="sm-lbl" aria-hidden="true"></span></button></div>'''

PANEL = '''<aside class="chat" id="chat" aria-label="AI 취업 상담" hidden>
  <div class="chat-h">
    <div><b>AI 취업 상담</b><small>지금 보고 있는 통계를 근거로 답해요</small></div>
    <div class="acts"><button class="icon-btn" id="chat-new" type="button">새 대화</button><button class="icon-btn" id="chat-close" type="button" aria-label="상담 닫기">닫기</button></div>
  </div>
  <div class="ctx" id="chat-ctx"></div>
  <div class="msgs" id="msgs" aria-live="polite"></div>
  <div class="sugs" id="sugs"></div>
  <form class="compose" id="compose">
    <textarea id="ask" rows="1" placeholder="예: 신입이면 뭐부터 공부해야 해?" aria-label="질문 입력"></textarea>
    <button class="send" id="send" type="submit">보내기</button>
  </form>
  <p class="chat-note">답변은 내 Claude 사용량을 써요. 통계는 2026-10-15 원티드 공고 기준이에요.</p>
</aside>'''

JS = r'''<script>
(() => {
  const FIELD_NAME = {engineer:'엔지니어(임베디드·하드웨어)', dev:'개발', marketing:'마케팅', design:'디자인'};
  const btn = $('ai-toggle'), panel = $('chat'), msgs = $('msgs'), ask = $('ask'), send = $('send'), sugs = $('sugs');
  let sample = null, turns = [], busy = null, toolsOk = false;

  const isWide = () => window.matchMedia('(min-width:1180px)').matches;
  function setOpen(open) {
    panel.hidden = !open; btn.setAttribute('aria-expanded', String(open));
    document.body.classList.toggle('chat-open', open);
    try { localStorage.setItem('jobmap-chat', open ? '1' : '0'); } catch (e) {}
    if (open) { updateCtx(); if (isWide()) ask.focus({preventScroll: true}); }
  }
  btn.addEventListener('click', () => setOpen(panel.hidden));
  $('chat-close').addEventListener('click', () => setOpen(false));
  $('chat-new').addEventListener('click', () => { if (busy) busy.abort(); turns = []; msgs.replaceChildren(); hello(); });

  const p0 = (a, b) => b ? Math.round(a / b * 100) + '%' : '0%';
  function trackLine(t, T) {
    const top = T.skills.slice().sort((a, b) => b.must - a.must).slice(0, 6).map(s => `${s.skill} ${p0(s.must, T.n)}`).join(', ');
    return `- ${t === '전체' ? '전체' : LABEL[t]}: 공고 ${T.n}건, 신입 가능 ${p0(T.newbie, T.n)}, 2년 이하 ${p0(T.junior, T.n)}, 필수 상위 ${top}`;
  }
  function context() {
    const T = D.tracks[cur], n = T.n, L = [];
    L.push(`분야: ${FIELD_NAME[field]} / 지금 보는 직군: ${LABEL[cur]} / 원티드 공고 ${n}건, 회사 ${T.companies}곳 (수집 ${D.collected})`);
    L.push(`신입 가능 ${p0(T.newbie, n)}, 2년 이하 지원 가능 ${p0(T.junior, n)}, 최소 경력 중앙값 ${T.median_years}년, 서울·경기 ${p0(T.capital, n)}, ${D.meta.kpi5[0]} ${p0(T.kpi5, n)}`);
    L.push(`\n[${NOUN} 언급 상위 25개: 이름 | 분류 | 필수 비율 | 우대사항에만 비율]`);
    T.skills.slice().sort((a, b) => (b.must + b.nice) - (a.must + a.nice)).slice(0, 25).forEach(s => L.push(`${s.skill} | ${s.group} | ${p0(s.must, n)} | ${p0(s.nice, n)}`));
    L.push(`\n[경력 구간별 필수 상위]`);
    T.stages.forEach(s => L.push(`${s.stage}(공고 ${s.n}건): ` + s.top.map(([k, v]) => `${k} ${p0(v, s.n)}`).join(', ')));
    L.push(`\n[최소 경력 분포] ` + T.years.map(([b, v]) => `${b} ${v}건`).join(', '));
    L.push(`[학력·전공 언급] ` + T.edu.map(([k, v]) => `${k} ${p0(v, n)}`).join(', '));
    L.push(`[공통 역량 언급] ` + T.soft.map(([k, v]) => `${k} ${p0(v, n)}`).join(', '));
    L.push(`[근무지] ` + T.locations.map(([k, v]) => `${k} ${p0(v, n)}`).join(', '));
    L.push(`\n[같은 분야의 세부 직군 비교]`);
    ORDER.forEach(t => L.push(trackLine(t, D.tracks[t])));
    L.push(`\n[사이트가 정리한 해석]`);
    L.push(`${T.ins.hero[0]}: ${T.ins.hero[1]}`);
    T.ins.items.forEach(x => L.push(`${x[2]}: ${x[3]}`));
    Object.values(T.sec).forEach(x => L.push(x));
    return L.join('\n');
  }
  const RULES = () => `너는 '직무 채용 지도' 사이트 오른쪽에 붙은 취업 상담 도우미야. 사용자는 이 분야로 취업하려는 사람이야.
아래 통계는 원티드 채용 공고의 자격요건·우대사항을 분석한 결과야. 이 데이터를 근거로 답해.
- 한국어로, 친근하고 정중한 '~요' 말투로 답해. 6~12줄 정도로 짧고 구체적으로.
- 숫자는 아래 데이터에 있는 값만 인용하고, 데이터에 없는 내용(학습 자료, 일반 조언)은 일반적인 조언이라고 밝혀.
- 목록이 필요하면 '- ' 나 '1. ' 로 시작하는 줄을 써. 표와 제목 기호(#)는 쓰지 마.
- ${toolsOk ? '구체적인 공고를 추천하거나 찾을 때는 searchJobs 도구로 찾아서 회사·포지션·경력과 링크를 알려 줘.' : '개별 공고 목록은 페이지 아래 공고별 요건 표에서 검색하라고 안내해.'}
- 다른 분야(${Object.values(FIELD_NAME).filter(v => v !== FIELD_NAME[field]).join(', ')})는 사이트 상단 버튼으로 바꿔 볼 수 있다고 안내해.

${context()}`;

  const makeSearchTool = () => ({
    name: 'searchJobs',
    description: '지금 분야의 원티드 공고를 검색해요. 키워드(회사·포지션·기술), 세부 직군, 최대 최소경력(년)으로 거르고 최대 8건을 돌려줘요. 각 항목: company, position, track, experience, location, must(필수 키워드), url.',
    inputSchema: {type: 'object', properties: {
      query: {type: 'string', description: '회사·포지션·기술 키워드. 비우면 전체'},
      track: {type: 'string', description: '세부 직군 이름. 생략하면 사용자가 지금 보는 직군. 가능한 값: ' + ORDER.join(', ')},
      maxYears: {type: 'number', description: '최소 경력 상한(년). 신입만이면 0'}}},
    execute(input) {
      const q = String(input.query || '').trim().toLowerCase();
      let t = String(input.track || cur); if (!ORDER.includes(t)) { const hit = ORDER.find(k => LABEL[k] === t || k === t); t = hit || cur; }
      const my = input.maxYears === undefined || input.maxYears === null || input.maxYears === '' ? null : Number(input.maxYears);
      let rows = D.jobs.filter(j => t === '전체' || j.t === t);
      if (my !== null && !Number.isNaN(my)) rows = rows.filter(j => j.y <= my);
      if (q) { const words = q.split(/\s+/); rows = rows.filter(j => { const s = (j.c + ' ' + j.p + ' ' + j.ms + ' ' + j.k.join(' ')).toLowerCase(); return words.every(w => s.includes(w)); }); }
      note(`공고 검색: ${q || '전체'}${my !== null ? ` · ${my}년 이하` : ''} → ${rows.length}건`);
      return {total: rows.length, jobs: rows.slice(0, 8).map(j => ({company: j.c, position: j.p, track: LABEL[j.t] || j.t, experience: j.yl, location: j.l, must: j.m.slice(0, 6), url: `https://www.wanted.co.kr/wd/${j.id}`}))};
    }
  });

  function inline(parent, text) {
    const re = /(\*\*[^*]+\*\*|https?:\/\/[^\s)）\]]+)/g; let last = 0, m;
    while ((m = re.exec(text))) {
      if (m.index > last) parent.appendChild(document.createTextNode(text.slice(last, m.index)));
      if (m[0].startsWith('**')) parent.appendChild(el('strong', null, m[0].slice(2, -2)));
      else { const a = el('a', null, m[0].replace(/[.,]$/, '')); a.href = a.textContent; a.target = '_blank'; a.rel = 'noopener'; parent.appendChild(a); }
      last = m.index + m[0].length;
    }
    if (last < text.length) parent.appendChild(document.createTextNode(text.slice(last)));
  }
  function renderMd(box, text) {
    box.replaceChildren(); let list = null;
    text.split('\n').forEach(raw => {
      const line = raw.trimEnd();
      const ul = line.match(/^\s*[-*•]\s+(.*)$/), ol = line.match(/^\s*\d+[.)]\s+(.*)$/), hd = line.match(/^#{1,4}\s+(.*)$/);
      if (ul || ol) {
        const kind = ul ? 'ul' : 'ol';
        if (!list || list.tagName.toLowerCase() !== kind) { list = el(kind); box.appendChild(list); }
        const li = el('li'); inline(li, (ul || ol)[1]); list.appendChild(li); return;
      }
      list = null;
      if (!line.trim()) return;
      const p = el('p', hd ? 'h' : null); inline(p, hd ? hd[1] : line); box.appendChild(p);
    });
  }
  const scrollDown = () => { msgs.scrollTop = msgs.scrollHeight; };
  function note(t) { msgs.appendChild(el('div', 'tool-note', t)); scrollDown(); }
  const SUGS = () => [`${LABEL[cur]} 신입이면 뭐부터 공부해야 해?`, '가산점이 되는 건 뭐야?', '신입 지원 가능한 공고 5개 추천해 줘', '다른 세부 직군이랑 비교해 줘'];
  function hello() {
    const h = el('div', 'hello'); h.append(el('b', null, '무엇이든 물어보세요'), document.createTextNode('지금 보고 있는 분야와 직군의 공고 통계를 바탕으로 무엇을 공부하고 어디에 지원할지 함께 정리해 드려요.'));
    msgs.appendChild(h); buildSugs();
  }
  function buildSugs() {
    sugs.replaceChildren();
    if (turns.length) return;
    SUGS().forEach(s => { const b = el('button', 'sug', s); b.type = 'button'; b.addEventListener('click', () => { ask.value = s; submit(); }); sugs.appendChild(b); });
  }
  window.updateCtx = function updateCtx() {
    if (!D) return;
    $('chat-ctx').textContent = `지금 기준: ${FIELD_NAME[field]} · ${LABEL[cur]} (공고 ${D.tracks[cur].n.toLocaleString('ko-KR')}건)`;
    buildSugs();
  };
  const COPY = {not_granted: 'AI 사용이 허용되지 않았어요. 이 페이지에서는 상담을 쓸 수 없어요.', sampling_disabled: '이 계정에서는 AI 상담을 쓸 수 없어요.', rate_limited: '요청이 많아요. 잠시 뒤에 다시 보내 주세요.', session_expired: '로그인이 만료됐어요. 다시 로그인한 뒤 보내 주세요.', prompt_too_large: '대화가 너무 길어졌어요. 새 대화를 시작해 주세요.', refused: '이 질문에는 답할 수 없어요. 질문을 바꿔 주세요.', empty_completion: '답이 비어 있어요. 질문을 조금 바꿔 다시 보내 주세요.'};
  const HIDE = ['not_granted', 'sampling_disabled', 'not_declared', 'capability_disabled', 'capability_removed'];

  async function submit() {
    const q = ask.value.trim(); if (!q || busy || !sample) return;
    ask.value = ''; ask.style.height = ''; sugs.replaceChildren();
    msgs.appendChild(el('div', 'msg u', q));
    turns.push({role: 'user', content: q});
    if (turns.length > 12) turns = turns.slice(-12);
    while (turns.length && turns[0].role !== 'user') turns.shift();
    const box = el('div', 'msg a think', '생각하는 중이에요…'); msgs.appendChild(box); scrollDown();
    busy = new AbortController(); send.textContent = '멈추기'; send.classList.add('stop');
    const opts = {cache: false, signal: busy.signal, onText: ({text}) => { box.classList.remove('think'); renderMd(box, text); scrollDown(); }};
    if (toolsOk) opts.tools = [makeSearchTool()];
    try {
      const r = await sample([{role: 'user', content: RULES()}, ...turns], opts);
      box.classList.remove('think'); renderMd(box, r.text); msgs.appendChild(box);
      turns.push({role: 'assistant', content: r.text});
      if (r.truncated) note('답이 길어서 중간에 끊겼어요. 나눠서 물어봐 주세요.');
    } catch (e) {
      box.classList.remove('think');
      if (e && e.text) { renderMd(box, e.text); } else { box.remove(); }
      if (e && e.code !== 'cancelled') { const err = el('div', 'msg a err', COPY[e.code] || '연결이 잠시 끊겼어요. 다시 보내 주세요.'); msgs.appendChild(err); }
      if (e && HIDE.includes(e.code)) { ask.disabled = true; send.disabled = true; }
      turns.pop();
    } finally {
      busy = null; send.textContent = '보내기'; send.classList.remove('stop'); scrollDown();
    }
  }
  $('compose').addEventListener('submit', (e) => { e.preventDefault(); if (busy) { busy.abort(); return; } submit(); });
  ask.addEventListener('keydown', (e) => { if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) { e.preventDefault(); if (!busy) submit(); } });
  ask.addEventListener('input', () => { ask.style.height = ''; ask.style.height = Math.min(ask.scrollHeight, 140) + 'px'; });

  const _render = render;
  render = function () { _render(); if (!panel.hidden) updateCtx(); };

  hello();
  (async () => {
    if (!window.claude || !claude.use) return;
    sample = await claude.use('sample');
    if (!sample) return;
    try { const lim = await sample.limits(); toolsOk = !!(lim && lim.tools); } catch (e) { toolsOk = false; }
    btn.hidden = false;
    let pref = null; try { pref = localStorage.getItem('jobmap-chat'); } catch (e) {}
    setOpen(pref === '1' || (pref === null && isWide()));
  })();
})();
</script>'''
