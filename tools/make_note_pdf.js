// 오답노트 양식 PDF 생성: node tools/make_note_pdf.js  → site/samples/ohdap-note.pdf
const { chromium } = require("playwright");
const path = require("path");
const rows = Array.from({ length: 8 }, (_, i) => `<tr><td class="n">${i + 1}</td><td></td><td></td><td></td><td></td><td></td></tr>`).join("");
const html = `<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>
@page{size:A4;margin:14mm}
body{font-family:"Pretendard Variable",Pretendard,"Apple SD Gothic Neo","Noto Sans KR","Noto Sans CJK KR","Malgun Gothic",sans-serif;color:#172338;font-size:10pt}
h1{font-size:18pt;margin:0 0 4px;color:#0C192B;letter-spacing:-.03em}.sub{color:#667085;font-size:9pt;margin-bottom:14px}
.meta{display:flex;gap:16px;margin-bottom:12px;font-size:9pt}.meta span{flex:1;border-bottom:1px solid #16263D;padding-bottom:14px}
table{width:100%;border-collapse:collapse}th{background:#16263D;color:#fff;font-size:8.5pt;padding:6px 4px;font-weight:600}
td{border:1px solid #C9CED6;height:24mm}td.n{width:7mm;text-align:center;color:#667085;font-size:8.5pt}
th:nth-child(2){width:30mm}th:nth-child(3){width:26mm}th:nth-child(5){width:44mm}
.tags{margin-top:12px;font-size:8.5pt;color:#3C4A60;line-height:1.7}.ft{margin-top:10px;font-size:8pt;color:#667085;display:flex;justify-content:space-between}
</style></head><body>
<h1>편입샘 오답노트</h1><div class="sub">틀린 문제를 '왜 틀렸는지'까지 기록하는 양식 · 인쇄해서 사용하세요</div>
<div class="meta"><span>교재 / 회차</span><span>날짜</span><span>시간 기록</span></div>
<table><thead><tr><th>#</th><th>문제 위치(쪽·번호)</th><th>오답 원인 태그</th><th>내가 고른 답 / 정답</th><th>다시 풀 때 확인할 점 (근거 문장·공식·규칙)</th><th>복습일 ✓</th></tr></thead><tbody>${rows}</tbody></table>
<div class="tags"><b>오답 원인 태그 예시</b> · 뜻 오해 / 문맥 놓침 / 단서 무시 / 구조 분석 실패 / 개념 부족 / 계산 실수 / 부호·조건 누락 / 시간 부족 / 찍음<br>※ 태그는 스스로 정하세요. 같은 태그가 반복되면 그 원인을 먼저 고치는 것이 효율적입니다.</div>
<div class="ft"><span>편입샘 — 필요한 문제만, 정확하게.</span><span>무료 양식 · 재배포 금지</span></div>
</body></html>`;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.setContent(html, { waitUntil: "networkidle" });
  await p.pdf({ path: path.join(__dirname, "..", "site", "samples", "ohdap-note.pdf"), format: "A4", printBackground: true, preferCSSPageSize: true });
  await b.close(); console.log("ok");
})();
