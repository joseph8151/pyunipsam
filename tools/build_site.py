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
:root{--bg:#fff;--fg:#1c2330;--mu:#5d6778;--ac:#1a56db;--bd:#e3e7ee;--sf:#f5f7fb}
@media (prefers-color-scheme:dark){:root{--bg:#10141c;--fg:#e8ecf3;--mu:#98a2b3;--ac:#7aa2ff;--bd:#272e3b;--sf:#171c27}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.7 -apple-system,"Noto Sans KR","Apple SD Gothic Neo",sans-serif}
a{color:var(--ac)}
header{border-bottom:1px solid var(--bd);position:sticky;top:0;background:var(--bg);z-index:5}
.w{max-width:1040px;margin:0 auto;padding:0 16px}
.top{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;padding-block:12px}
.logo{font-weight:800;font-size:20px;text-decoration:none;color:var(--fg)}
nav{display:flex;gap:4px 14px;flex-wrap:wrap;font-size:14px}
nav a{text-decoration:none;color:var(--mu)}nav a:hover,nav a.on{color:var(--ac)}
.hero{padding:56px 0 40px}.hero h1{font-size:clamp(28px,5vw,44px);line-height:1.25;margin:0 0 12px}
.hero p{color:var(--mu);max-width:640px;margin:0 0 20px}
.btn{display:inline-block;padding:10px 18px;border-radius:8px;background:var(--ac);color:#fff;text-decoration:none;font-weight:600}
.btn.o{background:none;border:1px solid var(--bd);color:var(--fg)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px;margin:16px 0 32px}
.card{border:1px solid var(--bd);background:var(--sf);border-radius:12px;padding:16px}
.card h3{margin:0 0 6px;font-size:17px}.card p{margin:0 0 8px;color:var(--mu);font-size:14px}
.tag{display:inline-block;font-size:12px;padding:2px 8px;border-radius:99px;border:1px solid var(--bd);color:var(--mu)}
.meta{font-size:13px;color:var(--mu)}
h2{margin:36px 0 4px}h2+p{margin-top:0;color:var(--mu)}
.note{border-left:3px solid var(--ac);padding:8px 14px;background:var(--sf);margin:16px 0;font-size:14px}
footer{border-top:1px solid var(--bd);margin-top:48px;padding:24px 0;color:var(--mu);font-size:13px}
details{border:1px solid var(--bd);border-radius:8px;padding:8px 14px;margin:8px 0}summary{cursor:pointer;font-weight:600}
"""

def page(fname, title, body, desc="대학 편입시험 전문 PDF 문제집. 필요한 문제만, 정확하게."):
    nav = "".join(f'<a href="{h}"{" class=on" if h==fname else ""}>{t}</a>' for h, t in MENU)
    doc = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}">
<link rel="stylesheet" href="style.css"></head><body>
<header><div class="w top"><a class="logo" href="index.html">편입샘</a><nav>{nav}</nav></div></header>
<main class="w">{body}</main>
<footer><div class="w">편입샘 — 대학 편입시험 전문 문제집 · 필요한 문제만, 정확하게.<br>
편입샘은 학원·과외·컨설팅이 아닌 PDF 문제집 브랜드입니다. 합격을 보장하지 않으며, 대학별 시험 정보는 해당 연도 공식 모집요강이 우선합니다.<br>
<a href="plan/index.html">사업 기획서</a> · <a href="guide.html">이용 안내</a></div></footer></body></html>"""
    (OUT / fname).write_text(doc, encoding="utf-8")

def card(name, desc, meta, extra=""):
    return (f'<div class="card"><span class="tag">출시 예정</span><h3>{html.escape(name)}</h3>'
            f'<p>{html.escape(desc)}</p><div class="meta">{html.escape(meta)}{extra}</div>'
            f'<p style="margin-top:10px"><a href="{CONTACT}">출시 알림 신청</a></p></div>')

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
    home = f"""<section class="hero"><h1>대학 편입시험 전문 문제집</h1>
<p>필요한 문제만, 정확하게. 편입영어·편입수학·대학별 모의고사를 PDF 문제집으로 제작합니다.</p>
<a class="btn" href="free.html">무료 샘플 보기</a> <a class="btn o" href="univ.html">대학별 모의고사</a></section>
<h2>카테고리</h2><div class="grid">""" + "".join(
        f'<a class="card" href="{h}" style="text-decoration:none;color:inherit"><h3>{t}</h3><p>{d}</p></a>' for h, t, d in cats) + """</div>
<h2>편입샘이 지키는 기준</h2><div class="grid">
<div class="card"><h3>정확성</h3><p>문항마다 정답이 하나인지 독립 풀이와 전문가 검수로 확인한 뒤 판매합니다.</p></div>
<div class="card"><h3>요강 기준</h3><p>대학별 모의고사는 해당 연도 모집요강의 문항 수·시간·형식 기준으로 만듭니다. 존재하지 않는 시험은 만들지 않습니다.</p></div>
<div class="card"><h3>오답 중심 해설</h3><p>정답 근거뿐 아니라 오답 선지가 틀린 이유까지 설명합니다.</p></div>
<div class="card"><h3>독창 문항</h3><p>대학 기출문제를 복제하지 않고 새로 제작합니다.</p></div></div>
<div class="note">현재 첫 상품들을 제작·검수 중입니다. 출시 알림을 신청하시면 가장 먼저 안내해 드립니다. <a href=\"""" + CONTACT + """\">알림 신청</a></div>"""
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
