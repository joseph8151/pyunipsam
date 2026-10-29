"""편입샘 정적 홈페이지 생성기. 실행: python3 tools/build_site.py (결과: site/)"""
import html, pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "site"
CONTACT = "mailto:yorkboy@gmail.com?subject=" + "편입샘 출시 알림 신청"

MENU = [
    ("english.html", "편입영어"), ("math.html", "편입수학"), ("univ.html", "대학별 모의고사"),
    ("major.html", "전공 필기"), ("interview.html", "면접·서류"), ("complete.html", "COMPLETE 패키지"),
    ("free.html", "무료 샘플"), ("guide.html", "이용 안내"),
]

# (이름, 설명, 구성) — 모두 출시 예정. 가격은 확정 전이라 표시하지 않는다.
ENGLISH = {
    "어휘": [("고난도 어휘 300제", "상위권 대학 대비 어휘 문제. 오답 선지의 의미까지 해설", "300문항 · 약 120쪽")],
    "문법": [("핵심 문법 300제", "시제·수일치·준동사·관계사·가정법 유형별 문제와 1쪽 개념 요약", "300문항 · 약 200쪽"),
             ("문법 오류 찾기 200제", "밑줄형 오류 문항. 틀린 이유와 맞는 선지가 맞는 이유를 함께 해설", "200문항 · 약 130쪽")],
    "독해": [("중급 독해 200제", "지문 약 250~350어. 오답 선지마다 근거 문장을 표시", "200문항 · 약 200쪽")],
    "논리": [("논리완성 200제", "빈칸·연결어 논리 문제와 연결어 논리 지도", "200문항 · 약 150쪽")],
    "종합·모의고사": [("영어 파이널 100제", "시험 직전 핵심 점검용 100문항", "100문항 · 약 100쪽")],
}
MATH = {
    "미적분학": [("미분법 200제", "극한·미분·응용. 정석 풀이와 단축 풀이를 함께 제공", "200문항 · 약 200쪽"),
               ("적분법 200제", "부정·정적분·응용 문제", "200문항 · 약 200쪽")],
    "선형대수": [("선형대수 200제", "행렬·고유값·벡터공간. 정답 유일성과 계산 검증을 거친 문항", "200문항 · 약 200쪽")],
}
UNIV = [
    ("한양대 자연계 수학 모의고사", "2026학년도 요강 기준: 수학만 25문항(객관식 20 + 단답형 5), 70분. 영어 필기는 폐지된 형식입니다.", "25문항 × 3회", "한양대 공식 유의사항"),
    ("한양대 인문계 영어 모의고사", "2026학년도 요강 기준: 영어 40문항, 70분.", "40문항 × 3회", "한양대 공식 유의사항"),
    ("중앙대 영어 모의고사", "2026학년도 요강 기준: 영어 40문항, 60분, 4지선다. (수학은 문항 수 확인 후 별도 안내)", "40문항 × 3회", "중앙대 2026 모집요강"),
    ("한국외대 인문계 영어 모의고사", "인문계 영어 50문항, 60분 (공식 요강 재확인 후 출시).", "50문항 × 3회", "한국외대 2026 모집요강"),
]

CSS = """
@import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css");
:root{--bg:#fbfbfd;--fg:#0f172a;--mu:#64748b;--ac:#2f4bff;--ac2:#6a5cff;--bd:#e6e9f0;--sf:#ffffff;--tint:#eef1ff;--sh:0 1px 2px rgba(15,23,42,.04),0 8px 24px rgba(15,23,42,.06)}
@media (prefers-color-scheme:dark){:root{--bg:#0b0f1a;--fg:#e9edf6;--mu:#94a0b8;--ac:#7f95ff;--ac2:#a79bff;--bd:#222a3b;--sf:#121827;--tint:#19213a;--sh:0 1px 2px rgba(0,0,0,.3),0 8px 24px rgba(0,0,0,.35)}}
*{box-sizing:border-box}
html{scroll-behavior:smooth}html,body{overflow-x:clip}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.75 "Pretendard Variable",Pretendard,-apple-system,"Noto Sans KR","Apple SD Gothic Neo",sans-serif;letter-spacing:-.01em;-webkit-font-smoothing:antialiased}
a{color:var(--ac)}
.w{max-width:1080px;margin:0 auto;padding:0 20px}
header{position:sticky;top:0;z-index:10;background:color-mix(in srgb,var(--bg) 82%,transparent);backdrop-filter:saturate(1.6) blur(14px);border-bottom:1px solid var(--bd)}
.top{display:flex;align-items:center;justify-content:space-between;gap:16px;padding-block:14px}
.logo{display:flex;align-items:center;gap:10px;font-weight:800;font-size:19px;text-decoration:none;color:var(--fg);letter-spacing:-.03em}
.mark{width:28px;height:28px;border-radius:9px;background:linear-gradient(135deg,var(--ac),var(--ac2));display:grid;place-items:center;color:#fff;font-size:15px;font-weight:800}
nav{display:flex;gap:2px;flex-wrap:wrap;font-size:14px;font-weight:500}
nav a{text-decoration:none;color:var(--mu);padding:6px 11px;border-radius:99px;transition:.15s}
nav a:hover{color:var(--fg);background:var(--tint)}nav a.on{color:var(--ac);background:var(--tint)}
@media(max-width:820px){.top{flex-direction:column;align-items:flex-start;gap:8px}nav{margin-inline:-11px}}
.hero{position:relative;padding:84px 0 64px}
.hero:before{content:"";position:absolute;inset:-10% -12% auto auto;width:640px;height:640px;background:radial-gradient(closest-side,color-mix(in srgb,var(--ac2) 28%,transparent),transparent);z-index:-1;filter:blur(10px)}
.hero:after{content:"";position:absolute;inset:0;background-image:linear-gradient(var(--bd) 1px,transparent 1px),linear-gradient(90deg,var(--bd) 1px,transparent 1px);background-size:44px 44px;mask-image:radial-gradient(ellipse at 75% 20%,#000,transparent 65%);-webkit-mask-image:radial-gradient(ellipse at 75% 20%,#000,transparent 65%);opacity:.55;z-index:-2}
.eyebrow{display:inline-block;font-size:13px;font-weight:600;color:var(--ac);background:var(--tint);padding:5px 12px;border-radius:99px;margin-bottom:18px}
.hero h1{font-size:clamp(34px,6vw,60px);line-height:1.15;letter-spacing:-.04em;margin:0 0 18px;font-weight:800}
.hero h1 em{font-style:normal;background:linear-gradient(120deg,var(--ac),var(--ac2));-webkit-background-clip:text;background-clip:text;color:transparent}
.hero p{color:var(--mu);font-size:18px;max-width:560px;margin:0 0 30px}
.btn{display:inline-flex;align-items:center;gap:6px;padding:12px 22px;border-radius:12px;background:linear-gradient(135deg,var(--ac),var(--ac2));color:#fff;text-decoration:none;font-weight:600;box-shadow:0 6px 18px color-mix(in srgb,var(--ac) 35%,transparent);transition:transform .15s}
.btn:hover{transform:translateY(-1px)}
.btn.o{background:var(--sf);border:1px solid var(--bd);color:var(--fg);box-shadow:none}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px;margin:20px 0 40px}
.card{display:block;position:relative;border:1px solid var(--bd);background:var(--sf);border-radius:18px;padding:22px;box-shadow:var(--sh);transition:transform .18s,border-color .18s}
a.card{text-decoration:none;color:inherit}a.card h3{color:var(--fg)}
a.card:hover{transform:translateY(-3px);border-color:color-mix(in srgb,var(--ac) 45%,var(--bd))}
.card h3{margin:0 0 8px;font-size:18px;letter-spacing:-.025em}
.card p{margin:0 0 10px;color:var(--mu);font-size:14.5px;line-height:1.65}
.card .go{color:var(--ac);font-size:14px;font-weight:600;text-decoration:none}
.num{font-size:13px;font-weight:700;color:var(--ac);letter-spacing:.04em;margin-bottom:10px;display:block}
.tag{display:inline-block;font-size:12px;font-weight:600;padding:3px 10px;border-radius:99px;background:var(--tint);color:var(--ac);margin-bottom:12px}
.meta{font-size:13px;color:var(--mu)}
main h1{font-size:clamp(28px,4vw,40px);letter-spacing:-.035em;margin:56px 0 8px;font-weight:800}
main h1+p{color:var(--mu);font-size:17px;max-width:680px;margin:0 0 8px}
h2{font-size:24px;letter-spacing:-.03em;margin:52px 0 4px;font-weight:700}
h2+p{margin-top:0;color:var(--mu)}
.note{display:flex;gap:10px;border:1px solid var(--bd);border-radius:14px;padding:16px 20px;background:var(--tint);margin:24px 0;font-size:14.5px}
.cta{margin:64px 0 8px;padding:40px;border-radius:24px;background:linear-gradient(135deg,var(--ac),var(--ac2));color:#fff}
.cta h2{margin:0 0 6px;color:#fff}.cta p{margin:0 0 20px;color:rgba(255,255,255,.82)}
.cta .btn{background:#fff;color:#2f2fb8;box-shadow:none}
details{border:1px solid var(--bd);background:var(--sf);border-radius:14px;padding:4px 20px;margin:10px 0}
summary{cursor:pointer;font-weight:600;padding:14px 0}details p{margin-top:0;color:var(--mu)}
footer{border-top:1px solid var(--bd);margin-top:72px;padding:36px 0 48px;color:var(--mu);font-size:13.5px}
.fl{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap}.fl b{color:var(--fg)}
footer a{color:var(--mu)}
"""

def page(fname, title, body, desc="대학 편입시험 전문 PDF 문제집. 필요한 문제만, 정확하게."):
    nav = "".join(f'<a href="{h}"{" class=on" if h==fname else ""}>{t}</a>' for h, t in MENU)
    doc = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}">
<link rel="stylesheet" href="style.css"></head><body>
<header><div class="w top"><a class="logo" href="index.html"><span class="mark">편</span>편입샘</a><nav>{nav}</nav></div></header>
<main class="w">{body}</main>
<footer><div class="w fl"><div><b>편입샘</b> — 대학 편입시험 전문 문제집<br>필요한 문제만, 정확하게.</div><div style="max-width:520px">편입샘은 학원·과외·컨설팅이 아닌 PDF 문제집 브랜드입니다. 합격을 보장하지 않으며, 대학별 시험 정보는 해당 연도 공식 모집요강이 우선합니다.<br><a href="guide.html">이용 안내</a> · <a href="plan/index.html">기획서</a></div></div></footer></body></html>"""
    (OUT / fname).write_text(doc, encoding="utf-8")

def card(name, desc, meta, extra=""):
    return (f'<div class="card"><span class="tag">출시 예정</span><h3>{html.escape(name)}</h3>'
            f'<p>{html.escape(desc)}</p><div class="meta">{html.escape(meta)}{extra}</div>'
            f'<a class="go" href="{CONTACT}">출시 알림 신청 →</a></div>')

def section_page(fname, title, lead, groups):
    b = f"<h1>{title}</h1><p>{lead}</p>"
    for g, items in groups.items():
        b += f"<h2>{g}</h2><div class='grid'>" + "".join(card(*i) for i in items) + "</div>"
    b += '<div class="note">상품은 AI 초안 제작 후 정답·해설·출제 범위 검수를 마친 뒤 출시합니다. 가격은 출시 시 공지합니다.</div>'
    page(fname, f"{title} | 편입샘", b)

def build():
    OUT.mkdir(exist_ok=True)
    (OUT / "style.css").write_text(CSS, encoding="utf-8")

    cats = [("english.html", "편입영어", "어휘·문법·독해·논리, 정답과 오답 선지까지 해설"),
            ("math.html", "편입수학", "미적분·선형대수, 계산 검증을 거친 풀이"),
            ("univ.html", "대학별 모의고사", "실제 모집요강의 문항 수·시간·형식 기준"),
            ("free.html", "무료 샘플", "진단 테스트·샘플 해설·오답노트")]
    principles = [("정확성", "문항마다 정답이 하나인지 독립 풀이와 전문가 검수로 확인한 뒤 판매합니다."),
                  ("요강 기준", "해당 연도 모집요강의 문항 수·시간·형식 기준으로 제작합니다. 존재하지 않는 시험은 만들지 않습니다."),
                  ("오답 중심 해설", "정답 근거뿐 아니라 오답 선지가 틀린 이유까지 설명합니다."),
                  ("독창 문항", "대학 기출문제를 복제하지 않고 새로 제작합니다.")]
    home = """<section class="hero"><span class="eyebrow">대학 편입시험 전문 PDF 문제집</span>
<h1>필요한 문제만,<br><em>정확하게.</em></h1>
<p>편입영어·편입수학·대학별 모의고사를 AI 초안과 전문가 검수로 만듭니다. 시험 형식에 맞는 문제와 오답까지 설명하는 해설을 제공합니다.</p>
<a class="btn" href="free.html">무료 샘플 보기 →</a> <a class="btn o" href="univ.html">대학별 모의고사</a></section>
<h2>카테고리</h2><p>준비 중인 문제집을 영역별로 확인하세요.</p><div class="grid">""" + "".join(
        f'<a class="card" href="{h}"><span class="num">0{i+1}</span><h3>{t}</h3><p>{d}</p><span class="go">자세히 보기 →</span></a>' for i,(h,t,d) in enumerate(cats)) + """</div>
<h2>편입샘이 지키는 기준</h2><p>과장 없이, 확인된 것만 만듭니다.</p><div class="grid">""" + "".join(
        f'<div class="card"><span class="num">0{i+1}</span><h3>{t}</h3><p>{d}</p></div>' for i,(t,d) in enumerate(principles)) + """</div>
<section class="cta"><h2>첫 문제집 출시 알림</h2><p>제작·검수를 마치는 대로 가장 먼저 안내해 드립니다.</p><a class="btn" href=\"""" + CONTACT + """\">출시 알림 신청</a></section>"""
    page("index.html", "편입샘 — 대학 편입시험 전문 문제집", home)

    section_page("english.html", "편입영어", "어휘·문법·독해·논리 영역별 문제집", ENGLISH)
    section_page("math.html", "편입수학", "미적분학·선형대수 문제집. 모든 정답은 독립 계산으로 검증합니다.", MATH)

    b = "<h1>대학별 모의고사</h1><p>해당 대학의 실제 시험 구성에 맞춘 모의고사입니다. 영어만 보는 대학, 수학만 보는 대학, 병행하는 대학을 구분해 제작합니다.</p><div class='grid'>"
    for n, d, m, src in UNIV:
        b += card(n, d, m, f" · 기준: {src}")
    b += """</div><div class="note"><b>다른 대학은요?</b> 건국·성균관·서강·경희·동국·홍익 등은 최신 공식 모집요강으로 시험 과목과 형식을 확인한 뒤 순차적으로 추가합니다. 확인되지 않은 시험 유형은 판매하지 않습니다.
원하는 대학이 있으면 <a href=\"""" + CONTACT + """\">알려 주세요</a>.</div>"""
    page("univ.html", "대학별 모의고사 | 편입샘", b)

    page("major.html", "전공 필기 | 편입샘",
         "<h1>전공 필기</h1><p>컴퓨터공학·경영학·경제학·생명과학·일반화학·일반물리학 등 전공 필기 자료는 실제로 전공시험을 시행하는 대학과 모집단위를 확인하고, 해당 분야 전문가 검수가 가능할 때만 오픈합니다.</p><div class='note'>현재 준비 중입니다. <a href=\"" + CONTACT + "\">오픈 알림 신청</a></div>")
    page("interview.html", "편입 면접·서류 | 편입샘",
         "<h1>편입 면접·서류</h1><p>면접 예상질문, 학업계획서·자기소개서 작성 워크북을 준비합니다. 대학별 면접 시행 여부와 제출 서류를 확인한 뒤 구성합니다. 문제집을 보조하는 자료입니다.</p><div class='note'>현재 준비 중입니다. <a href=\"" + CONTACT + "\">알림 신청</a></div>")
    page("complete.html", "COMPLETE 패키지 | 편입샘",
         "<h1>COMPLETE 패키지</h1><p>영역별 문제집을 한 권으로 묶은 종합 패키지(편입영어 COMPLETE, 편입수학 COMPLETE, 실전 모의고사 10회)를 준비 중입니다. 영역 균형 진단표와 오답노트가 포함됩니다.</p><div class='note'>개별 문제집 출시 이후 순차 구성합니다. <a href=\"" + CONTACT + "\">알림 신청</a></div>")
    page("free.html", "무료 샘플 | 편입샘",
         """<h1>무료 샘플</h1><p>구매 전에 문제와 해설의 품질을 확인하세요.</p><div class='grid'>
<div class="card"><span class="tag">준비 중</span><h3>영역 진단 테스트 30문항</h3><p>어휘·문법·독해·논리 약점 영역을 확인합니다.</p></div>
<div class="card"><span class="tag">준비 중</span><h3>샘플 PDF (문제 5 + 해설 3)</h3><p>상품별 샘플로 해설 방식을 미리 봅니다.</p></div>
<div class="card"><span class="tag">준비 중</span><h3>오답노트·학습 플래너</h3><p>인쇄해서 쓰는 양식입니다.</p></div></div>
<div class="note">샘플 파일이 공개되면 이 페이지에서 내려받으실 수 있습니다. <a href=\"""" + CONTACT + """\">공개 알림 신청</a></div>""")
    page("guide.html", "이용 안내 | 편입샘",
         """<h1>이용 안내</h1>
<details open><summary>편입샘은 어떤 곳인가요?</summary><p>대학 편입시험 대비 PDF 문제집을 제작·판매하는 곳입니다. 학원, 과외, 컨설팅은 하지 않습니다.</p></details>
<details><summary>문항은 어떻게 만드나요?</summary><p>AI로 초안을 만들고, 독립 풀이로 정답을 확인한 뒤 영어·수학 전문가가 정답·해설·출제 범위를 검수합니다. 검수를 마치지 않은 문항은 판매하지 않습니다.</p></details>
<details><summary>기출문제를 사용하나요?</summary><p>대학 기출문제를 복제하지 않고 독창 문항으로 제작합니다.</p></details>
<details><summary>대학별 모의고사의 기준은 무엇인가요?</summary><p>해당 학년도 대학 공식 모집요강의 문항 수·시간·형식입니다. 상품 표지에 기준 연도와 요강 출처를 표기하며, 요강이 바뀌면 개정합니다.</p></details>
<details><summary>구매·환불은 어떻게 되나요?</summary><p>현재 판매 전 준비 단계입니다. 결제 방식, 다운로드 방법, 환불·청약철회 규정은 판매 시작 전에 이곳에 공지합니다.</p></details>
<details><summary>정오표는 어디서 보나요?</summary><p>오류가 확인되면 이곳에 정오표를 공개하고 구매자에게 개정본을 안내합니다.</p></details>
<details><summary>재배포가 가능한가요?</summary><p>PDF의 복제·재배포·공유는 금지됩니다.</p></details>
<p>문의: <a href=\"""" + CONTACT + """\">yorkboy@gmail.com</a></p>""")

if __name__ == "__main__":
    build()
