"""편입샘 V2.0 정적 사이트 생성기.  실행: python3 tools/build_site.py  (결과물: site/)

- 상품 정적 데이터: tools/catalog_products.py, tools/catalog_univ.py
- 판매 데이터(관리자 설정): data/prices.json, data/status_overrides.json, data/samples.json
"""
import html, json, pathlib, shutil, subprocess, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from catalog_products import PRODUCTS, BY_ID, CATS, SUBS, DIFF, LEGACY_MERGE
from catalog_univ import UNIVS, UNIV_BY_SLUG, ARTICLES, ARTICLE_PENDING, CHECKED, YEAR, LEVEL_LABEL, CAND_TYPES
import covers
import sample_content as sc

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "site"
DATA = ROOT / "data"
SITE_URL = "https://pyunipsam.yorkboy.workers.dev"
CONTACT_MAIL = "yorkboy@gmail.com"

STATUS = {
    "draft": ("기획 중", "s-draft"), "coming_soon": ("출시 예정", "s-soon"), "sample_ready": ("샘플 공개", "s-sample"),
    "on_sale": ("판매 중", "s-sale"), "discontinued": ("판매 종료", "s-end"),
}
MENU = [("english.html", "편입영어"), ("math.html", "편입수학"), ("univ.html", "대학별 모의고사"), ("major.html", "전공 필기"),
        ("interview.html", "면접·서류"), ("complete.html", "COMPLETE 패키지"), ("free.html", "무료 샘플"), ("info.html", "대학별 편입정보")]
E = html.escape


def esc(s):
    return E(str(s), quote=True)


# ───────────────────────── 판매 데이터 병합 ─────────────────────────
def load_json(name, default):
    f = DATA / name
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    return default


def merge_sales():
    prices = load_json("prices.json", {})
    overrides = load_json("status_overrides.json", {})
    samples = load_json("samples.json", {"products": {}, "free": {}})
    problems = []
    for p in PRODUCTS:
        pr = prices.get(p["id"], {})
        p["price"] = pr.get("price")
        p["sale_price"] = pr.get("salePrice")
        if p["id"] in overrides:
            p["status"] = overrides[p["id"]]
        sm = samples["products"].get(p["id"])
        p["sample"] = None
        if sm and (OUT / sm["file"]).exists() and (OUT / sm.get("solution", sm["file"])).exists():
            p["sample"] = sm
        if p["status"] == "on_sale":
            if not p["price"]:
                problems.append(f'{p["id"]}: on_sale 상태이지만 price 가 없습니다.')
            if p["sale_price"] and p["price"] and p["sale_price"] >= p["price"]:
                problems.append(f'{p["id"]}: salePrice 가 price 이상입니다(가짜 할인 방지).')
        if p["status"] == "sample_ready" and not p["sample"]:
            problems.append(f'{p["id"]}: sample_ready 이지만 샘플 파일이 없습니다.')
    if problems:
        raise SystemExit("데이터 검증 실패:\n" + "\n".join(problems))
    return samples


def won(n):
    return f"{n:,}원"


def qlabel(p):
    u, q = p["unit"], p["q"]
    if u == "회":
        return f"모의고사 {q}회"
    if u == "권":
        return f"{q}권 구성"
    if u == "구성":
        return "선택 대학 구성"
    if u == "쪽":
        return f"워크북 {q}쪽"
    if u == "어":
        return f"표제어 {q:,}개"
    return f"{q:,}{u}"


def meta_line(p):
    bits = [p["diff"], qlabel(p)]
    if p.get("pages"):
        bits.append(f'약 {p["pages"]}쪽')
    return " · ".join(bits)


def price_html(p, compact=False):
    if p["status"] == "on_sale" and p.get("price"):
        if p.get("sale_price"):
            pct = round((1 - p["sale_price"] / p["price"]) * 100)
            return (f'<span class="price"><del>{won(p["price"])}</del> <b>{won(p["sale_price"])}</b> '
                    f'<span class="pct">{pct}%</span></span>')
        return f'<span class="price"><b>{won(p["price"])}</b></span>'
    return '<span class="price none">가격 · 출시 시 공지</span>'


def badge(p):
    t, c = STATUS[p["status"]]
    return f'<span class="badge {c}">{t}</span>'


# ───────────────────────── 공통 레이아웃 ─────────────────────────
MARK_PATH = ('<path d="M7 8.5h6.2c.5 0 .8.3.8.8V20c-.5-.5-1.2-.8-2-.8H7z M21 8.5h-6.2c-.5 0-.8.3-.8.8V20c.5-.5 1.2-.8 2-.8H21z" '
             'fill="none" stroke="#242321" stroke-width="1.4" stroke-linejoin="round"/><rect x="7" y="22" width="14" height="1.3" fill="#F4F1EB"/>')
LOGO = ('<svg class="mark" viewBox="0 0 28 28" aria-hidden="true"><rect width="28" height="28" rx="3" fill="#BAA58C"/>' + MARK_PATH + '</svg>')

ICON_SEARCH = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="m16 16 4.5 4.5"/></svg>'
ICON_CART = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M3 4h2.5l2 11h10.5l2-8H6.5"/><circle cx="9" cy="19.5" r="1.3"/><circle cx="17" cy="19.5" r="1.3"/></svg>'
ICON_CMP = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M8 5H4v14h4M16 5h4v14h-4M12 3v18"/></svg>'
ICON_MENU = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'


def drawer(R):
    def group(label, href, subs):
        links = "".join(f'<a href="{R}{h}">{t}</a>' for t, h in subs)
        return f'<details class="dg"><summary>{label}</summary><a class="all" href="{R}{href}">{label} 전체 보기</a>{links}</details>'
    g = [
        group("편입영어", "english.html", [("어휘", "english.html#vocab"), ("문법", "english.html#grammar"), ("독해", "english.html#reading"), ("논리", "english.html#logic"), ("종합·실전", "english.html#eng_all")]),
        group("편입수학", "math.html", [("기초수학", "math.html#base"), ("미적분학", "math.html#calc"), ("선형대수학", "math.html#linear"), ("공학수학", "math.html#eng_math"), ("종합·실전", "math.html#math_all")]),
        group("대학별 모의고사", "univ.html", [("대학 검색", "univ.html"), ("모의고사 상품", "univ.html#products")]),
        group("전공 필기", "major.html", [("전공 필기 안내", "major.html")]),
        group("면접·서류", "interview.html", [("면접", "interview.html#interview"), ("서류", "interview.html#docs")]),
        group("COMPLETE 패키지", "complete.html", [("패키지 전체", "complete.html")]),
    ]
    rest = "".join(f'<a class="dl" href="{R}{h}">{t}</a>' for h, t in [("free.html", "무료 샘플"), ("info.html", "대학별 편입정보"), ("learn.html", "학습 콘텐츠"), ("products.html", "전체 문제집"), ("contact.html", "고객 문의"), ("guide.html", "이용 안내")])
    return f'<div class="drawer" id="drawer" hidden><div class="dr-in">{"".join(g)}<div class="dr-rest">{rest}</div></div></div>'


def header(R, active=""):
    gnb = "".join(f'<a href="{R}{h}"{" class=on aria-current=page" if h == active else ""}>{t}</a>' for h, t in MENU)
    return f"""<a class="skip" href="#main">본문 바로가기</a>
<header class="site">
 <div class="util"><div class="w"><span>대학 편입시험 전문 PDF 문제집</span><span class="ul"><a href="{R}guide.html">이용 안내</a><a href="{R}contact.html">고객 문의</a><a href="{R}learn.html">학습 콘텐츠</a></span></div></div>
 <div class="top w">
  <a class="logo" href="{R}index.html" aria-label="편입샘 홈">{LOGO}<span>편입샘</span></a>
  <form class="search" role="search" action="{R}products.html" method="get"><label class="sr" for="hq">문제집 검색</label>
   <input id="hq" name="q" type="search" placeholder="문제집·대학명을 검색하세요" autocomplete="off"><button type="submit" aria-label="검색">{ICON_SEARCH}</button></form>
  <div class="tools">
   <button class="ic" id="searchToggle" aria-label="검색 열기" aria-expanded="false">{ICON_SEARCH}</button>
   <a class="ic" href="{R}compare.html" aria-label="상품 비교">{ICON_CMP}<span class="cnt" data-count="compare" hidden>0</span></a>
   <a class="ic" href="{R}cart.html" aria-label="장바구니">{ICON_CART}<span class="cnt" data-count="cart" hidden>0</span></a>
   <button class="ic menu" id="menuToggle" aria-label="메뉴 열기" aria-expanded="false" aria-controls="drawer">{ICON_MENU}</button>
  </div>
 </div>
</header>
<nav class="gnb" aria-label="주요 메뉴"><div class="w">{gnb}</div></nav>
{drawer(R)}"""


def footer(R):
    return f"""<footer class="site"><div class="w">
 <div class="fgrid">
  <div><a class="logo" href="{R}index.html">{LOGO}<span>편입샘</span></a>
   <p class="fm">대학 편입시험 전문 문제집<br>필요한 문제만, 정확하게.</p></div>
  <div><h4>문제집</h4><a href="{R}english.html">편입영어</a><a href="{R}math.html">편입수학</a><a href="{R}univ.html">대학별 모의고사</a><a href="{R}major.html">전공 필기</a><a href="{R}interview.html">면접·서류</a><a href="{R}complete.html">COMPLETE 패키지</a></div>
  <div><h4>정보</h4><a href="{R}info.html">대학별 편입정보</a><a href="{R}learn.html">학습 콘텐츠</a><a href="{R}free.html">무료 샘플</a><a href="{R}products.html">전체 문제집</a></div>
  <div><h4>고객 지원</h4><a href="{R}guide.html">이용 안내</a><a href="{R}contact.html">고객 문의</a><a href="{R}privacy.html">개인정보 처리방침</a></div>
 </div>
 <p class="legal">편입샘은 학원·과외·컨설팅이 아닌 PDF 문제집 브랜드입니다. 합격을 보장하지 않으며, 대학별 시험 정보는 해당 연도 대학 공식 모집요강이 우선합니다. 표지 이미지는 디자인 시안이며 실제 제작본과 다를 수 있습니다. 대학 명칭은 시험 정보 표기를 위한 서술적 사용이며 해당 대학과 무관한 비공식 자료입니다. 사업자 정보와 결제·환불 규정은 판매 시작 전 공지합니다.</p>
</div></footer>
<div class="toast" id="toast" role="status" aria-live="polite" hidden></div>"""


def page(path, title, desc, body, active="", extra_head="", body_class="", jsonld=None, robots=None):
    depth = path.count("/")
    R = "../" * depth
    full_title = title if "편입샘" in title else f"{title} | 편입샘"
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    rb = f'<meta name="robots" content="{robots}">' if robots else ""
    doc = f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(full_title)}</title><meta name="description" content="{esc(desc)}">{rb}
<meta property="og:type" content="website"><meta property="og:site_name" content="편입샘"><meta property="og:title" content="{esc(full_title)}"><meta property="og:description" content="{esc(desc)}">
<meta name="theme-color" content="#33312F">
<link rel="icon" href="{R}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="stylesheet" href="{R}assets/style.css">{extra_head}{ld}
</head><body class="{body_class}" data-root="{R}">
{header(R, active)}
<main id="main">{body}</main>
{footer(R)}
<script src="{R}assets/app.js" defer></script>
</body></html>"""
    f = OUT / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(doc, encoding="utf-8")


def cover(p, R, cls="cv"):
    return (f'<svg class="{cls}" viewBox="0 0 300 400" role="img" aria-label="{esc(p["title"])} 표지 시안">'
            f'<use href="{R}assets/covers.svg#c-{p["id"]}"/></svg>')


def card(p, R, show_cat=False):
    sub = SUBS.get(p["sub"], "")
    cat = CATS[p["cat"]][0]
    univ = UNIV_BY_SLUG[p["univ"]]["name"] if p.get("univ") else ""
    hay = " ".join([p["title"], cat, sub, univ, " ".join(p["types"]), p["summary"]]).lower()
    return f"""<article class="pc" data-id="{p['id']}" data-cat="{p['cat']}" data-sub="{p['sub']}" data-diff="{p['diff']}" data-pages="{p.get('pages') or ''}" data-status="{p['status']}" data-univ="{p.get('univ') or ''}" data-hay="{esc(hay)}">
 <a class="pc-cv" href="{R}p/{p['id']}.html" tabindex="-1" aria-hidden="true">{cover(p, R)}</a>
 <div class="pc-b">
  <div class="pc-tags">{badge(p)}<span class="tag">{esc(sub if p['cat'] != 'univ' else univ)}</span></div>
  <h3><a href="{R}p/{p['id']}.html">{esc(p['title'])}</a></h3>
  <p class="pc-m">{esc(meta_line(p))}</p>
  <p class="pc-p">{price_html(p)}</p>
  <div class="pc-a"><a class="lk" href="{R}p/{p['id']}.html">상세 보기</a><button class="cmp" data-compare="{p['id']}" aria-pressed="false">비교 담기</button></div>
 </div></article>"""


def grid(items, R, cols=""):
    return f'<div class="pgrid {cols}">' + "".join(card(p, R) for p in items) + "</div>"


NOTE_SPEC = '<p class="fn">※ 문항 수·쪽수는 설계안이며 제작·검수 과정에서 조정될 수 있습니다. 표지는 디자인 시안입니다.</p>'


def by(cat=None, sub=None, status=None):
    return [p for p in PRODUCTS if (cat is None or p["cat"] == cat) and (sub is None or p["sub"] == sub)
            and (status is None or p["status"] == status)]


def sec_head(eyebrow, title, sub="", dark=False):
    return f'<div class="sh{" dk" if dark else ""}"><span class="eb">{eyebrow}</span><h2>{title}</h2>{f"<p>{sub}</p>" if sub else ""}</div>'


def crumbs(R, items):
    parts = [f'<a href="{R}index.html">홈</a>'] + [f'<a href="{R}{h}">{esc(t)}</a>' if h else f'<span aria-current="page">{esc(t)}</span>' for t, h in items]
    return '<nav class="bc w" aria-label="현재 위치">' + '<span class="sep">/</span>'.join(parts) + "</nav>"


# ───────────────────────── 홈 ─────────────────────────
SUBJ = {  # 대학별 시험 과목/계열 (필터용, 확인 수준은 대학 정보 표 참고)
    "konkuk": ("인문·자연", "영어·수학"), "khu": ("인문·자연", "영어"), "korea": ("인문·자연", "영어·수학"),
    "kookmin": ("인문·자연", "영어·수학"), "dankook": ("미확인", "미확인"), "dongguk": ("인문", "영어"),
    "sogang": ("미확인", "미확인"), "skku": ("인문·자연", "영어·수학"), "sejong": ("인문·자연", "영어·수학"),
    "soongsil": ("인문·자연", "영어·수학"), "yonsei": ("인문·자연", "전공·논술(미확인)"), "cau": ("인문·자연", "영어·수학"),
    "hufs": ("인문·자연", "영어·수학"), "hanyang": ("인문·자연", "영어·수학"), "hongik": ("인문·자연", "영어·수학"),
}


def sample_cards(R, samples, free_page=False):
    """과목별 샘플 카드: 문제집·해설집 두 권 세트 + 오답노트."""
    fr = samples["free"]
    def ok(k):
        s_ = fr.get(k)
        return s_ if (s_ and (OUT / s_["file"]).exists()) else None
    out = ""
    desc = {"eng": "빈칸 추론 1문항 — 문제집 1쪽과 해설집 2쪽(본문 번역·구성·제목·주제·요지·요약·문장별 분석·선택지 해부)",
            "math": "미분·적분·선형대수 3문항 — 문제집과 해설집(정석 풀이·단축 풀이·계산 검증·오답 선지 분석)",
            "univ": "한양대 자연계 수학 형식(25문항·70분 기준)의 3문항 — 객관식 2 + 단답형 1"}
    for key, meta in sc.SAMPLE_SETS.items():
        q, so = ok(key + "-q"), ok(key + "-s")
        bq = f'<a class="btn pri" href="{R}{q["file"]}" download>문제집 PDF</a>' if q else '<button class="btn dis" disabled>문제집 준비 중</button>'
        bs = f'<a class="btn" href="{R}{so["file"]}" download>해설집 PDF</a>' if so else '<button class="btn dis" disabled>해설집 준비 중</button>'
        out += (f'<div class="fc sc"><span class="badge {"s-sample" if (q and so) else "s-draft"}">{"문제집 + 해설집" if (q and so) else "준비 중"}</span>'
                f'<h3>{meta["label"]} 샘플</h3><p>{desc[key]}</p>'
                f'<div class="sc-b">{bq}{bs}</div><a class="lk" href="{R}sample/{key}.html">화면으로 미리 보기 →</a></div>')
    n = ok("free-note")
    bn = f'<a class="btn pri" href="{R}{n["file"]}" download>PDF 다운로드</a>' if n else '<button class="btn dis" disabled>준비 중</button>'
    out += f'<div class="fc sc"><span class="badge {"s-sample" if n else "s-draft"}">{"다운로드 가능" if n else "준비 중"}</span><h3>오답노트 양식</h3><p>오답 원인 태그를 적어 두는 인쇄용 A4 양식입니다. 해설집을 읽은 뒤 바로 기록하세요.</p><div class="sc-b">{bn}</div></div>'
    return out


def build_home():
    R = ""
    hero_ids = ["p13", "p27", "u01", "p58"]
    hero_cov = "".join(f'<a class="hc hc{i}" href="p/{pid}.html" tabindex="-1" aria-hidden="true">{cover(BY_ID[pid], R, "cv")}</a>' for i, pid in enumerate(hero_ids))
    onsale = by(status="on_sale")
    feat_ids = ["p12", "p27", "u01", "u02", "p17", "p06", "p23", "p41"]
    feat = onsale[:8] if onsale else [BY_ID[i] for i in feat_ids]
    feat_note = ("판매 중인 상품입니다." if onsale else
                 "현재 판매 중인 상품은 없습니다. 아래는 제작 준비 중인 <b>출시 예정</b> 상품이며, 출시 알림을 신청할 수 있습니다.")

    eng_cols = [("vocab", "어휘", covers.SUB_COLOR["vocab"], "p02", "뜻을 아는 단어와 문맥에서 구분하는 단어는 다릅니다."),
                ("grammar", "문법", covers.SUB_COLOR["grammar"], "p06", "개념 요약과 오답 원인 태그로 약한 영역을 찾습니다."),
                ("reading", "독해", covers.SUB_COLOR["reading"], "p12", "오답 선지마다 지문의 근거 문장을 표시합니다."),
                ("logic", "논리", covers.SUB_COLOR["logic"], "p17", "빈칸 전후의 관계를 먼저 읽는 순서를 익힙니다.")]
    eng = "".join(f'''<a class="col" href="english.html#{k}" style="--c:{c}"><div class="cvw">{cover(BY_ID[pid], R)}</div>
<span class="bar"></span><h3>{t}</h3><p>{d}</p><span class="more">{len(by("english", k))}종 보기 →</span></a>''' for k, t, c, pid, d in eng_cols)
    math_cols = [("base", "기초수학", "p25", "함수·방정식·삼각함수 등 선수 개념을 정리합니다."),
                 ("calc", "미적분학", "p27", "극한부터 다변수까지, 정석 풀이와 단축 풀이를 비교합니다."),
                 ("linear", "선형대수학", "p32", "행렬·벡터공간·고유값을 계산 검증과 함께 연습합니다."),
                 ("eng_math", "공학수학", "p37", "대학별 출제 범위를 확인하고 필요한 영역만 학습합니다.")]
    mth = "".join(f'''<a class="col" href="math.html#{k}"><div class="cvw">{cover(BY_ID[pid], R)}</div><h3>{t}</h3><p>{d}</p><span class="more">{len(by("math", k))}종 보기 →</span></a>''' for k, t, pid, d in math_cols)

    ulinks = "".join(f'<a class="chip" href="u/{u["slug"]}.html">{esc(u["name"].replace("학교",""))}</a>' for u in UNIVS)
    comp_ids = [("p55", "편입영어 COMPLETE"), ("p58", "편입수학 COMPLETE"), ("p56", "READING & LOGIC"), ("p59", "CALCULUS"), ("p61", "대학별 FINAL")]
    comp = "".join(f'<a class="cc" href="p/{pid}.html"><div class="cvw">{cover(BY_ID[pid], R)}</div><h3>{esc(BY_ID[pid]["title"])}</h3><p>{esc(BY_ID[pid]["summary"])}</p></a>' for pid, _ in comp_ids)

    fcards = sample_cards(R, load_json("samples.json", {"free": {}, "products": {}}))

    crit = [("출제 범위 확인", "대학별 모의고사는 해당 연도 모집요강의 문항 수·시간·형식을 근거로 설계합니다. 확인하지 못한 시험은 상품으로 만들지 않습니다."),
            ("독창 문항 제작", "대학 기출문제를 복제하지 않고 새로 제작합니다."),
            ("정답 및 풀이 검증", "AI 초안을 독립 풀이와 계산 검증으로 점검하고, 전문가가 정답을 확인합니다."),
            ("상세 해설 구성", "본문 번역, 문장별 분석, 정답 근거, 오답 선지가 틀린 이유까지 해설집에 담습니다.")]
    crit_h = "".join(f'<li><span class="n">0{i+1}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(crit))
    reviewed = sum(1 for p in PRODUCTS if p.get("reviewed"))

    arts = "".join(f'<a class="ac" href="learn/{a["slug"]}.html"><span class="tag">{esc(a["tag"])}</span><h3>{esc(a["title"])}</h3><p>{esc(a["desc"])}</p><time datetime="{a["date"]}">{a["date"]}</time></a>' for a in sorted(ARTICLES, key=lambda a: a["date"], reverse=True))
    arts += "".join(f'<div class="ac pend"><span class="tag">{esc(a["tag"])}</span><h3>{esc(a["title"])}</h3><p>{esc(a["desc"])}</p><span class="soon">준비 중</span></div>' for a in ARTICLE_PENDING)

    cats = [("편입영어", "english.html", "p13", "어휘·문법·독해·논리, 영역별 24종"),
            ("편입수학", "math.html", "p27", "미적분·선형대수·공학수학, 19종"),
            ("대학별 모의고사", "univ.html", "u01", "실제 시험 형식에 맞춘 모의고사"),
            ("전공 필기", "major.html", "p43", "대학별 시험과 연결될 때만 활성화"),
            ("면접·서류", "interview.html", "p50", "면접 예상질문과 서류 작성 워크북"),
            ("COMPLETE 패키지", "complete.html", "p58", "영역을 묶은 프리미엄 컬렉션")]
    cat_h = "".join(f'<a class="cat" href="{h}"><div class="cvw">{cover(BY_ID[pid], R)}</div><div><h3>{t}</h3><p>{d}</p></div></a>' for t, h, pid, d in cats)

    body = f"""
<section class="hero"><div class="w hg">
 <div class="hl"><span class="eb">TRANSFER EXAM WORKBOOKS</span>
  <h1>목표 대학을 향한 준비,<br>문제의 수준부터 다르게.</h1>
  <p>편입영어·편입수학부터 대학별 실전 모의고사까지.<br>편입샘은 학습 단계에 맞는 전문 문제집을 제안합니다.</p>
  <div class="cta"><a class="btn pri" href="products.html">전체 문제집 보기</a><a class="btn" href="univ.html">대학별 모의고사 보기</a></div>
 </div>
 <div class="hr" aria-hidden="true">{hero_cov}</div>
</div>
<div class="facts"><div class="w">
  <div><b>{len(PRODUCTS)}종<i>기획·제작 준비</i></b>영어·수학·대학별·전공·면접·패키지</div>
  <div><b>{len(UNIVS)}개 대학<i>편입정보</i></b>확인 수준과 출처를 함께 표시</div>
  <div><b>{reviewed}종<i>검수 완료</i></b>검수를 마친 상품에만 표시합니다</div></div></div>
</section>

<section class="sec weapon"><div class="w wg">
 <div class="wl"><span class="eb">OUR WEAPON</span>
  <h2>해설집이 편입샘의 무기입니다.</h2>
  <p class="wlead">정답 한 줄로 끝나는 해설은 쓰지 않습니다. 본문 번역부터 문장별 어휘·문법·연결사 분석, 오답 선지가 틀린 이유까지 — <b>밀도 있게, 스파르타로</b> 해부합니다.</p>
  <ol class="layers">
   <li><b>본문 번역</b><span>문장 단위 직독직해 번역</span></li>
   <li><b>글의 구성</b><span>서론·본론·결론의 논리 흐름</span></li>
   <li><b>제목·주제·요지·요약</b><span>영문과 번역을 함께 제시</span></li>
   <li><b>문장별 분석</b><span>[어휘] [문법] [연결사] [빈칸] 태그</span></li>
   <li><b>선택지 해부</b><span>오답 선지마다 틀린 이유와 근거</span></li>
   <li><b>지문 분석 요약</b><span>논리 구조와 핵심 단서를 한 번에</span></li></ol>
  <p class="fn">해설편이 문제편보다 두껍게 설계됩니다(설계안). 아래 샘플은 편입샘이 새로 쓴 독창 문항이며 전문가 검수 전 시안입니다.</p>
  <div class="cta"><a class="btn pri" href="sample.html">샘플 문제집·해설집 보기</a><a class="btn" href="free.html">PDF 내려받기</a></div>
 </div>
 <div class="wr" aria-label="해설집 미리보기"><div class="paper"><div class="paper-h"><span>해설집 · 문장별 분석</span><span>샘플</span></div>{sc.weapon_snippet()}
  <p class="paper-f">정답 근거와 오답 선지까지 — 해설집 한 쪽의 모습</p></div></div>
</div></section>

<section class="sec dark selfstudy"><div class="w">{sec_head("SELF STUDY", "선생님 없이도 끝까지. 셀프스터디를 위해 만듭니다.", "혼자 공부하는 수험생이 해설집만 펴고도 막힌 곳을 스스로 찾아 고칠 수 있도록 설계합니다. 개별 질의응답과 첨삭은 제공하지 않습니다. 그래서 해설이 더 촘촘해야 한다고 생각합니다.", True)}
 <ol class="loop">
  <li><span>01</span><b>진단</b><p>영역별 정답률을 기록해 약한 곳부터 찾습니다.</p></li>
  <li><span>02</span><b>시간 재고 풀기</b><p>권장 풀이 시간을 기준으로 실제처럼 풉니다.</p></li>
  <li><span>03</span><b>해설 정독</b><p>정답이어도 선택지 해부까지 끝까지 읽습니다.</p></li>
  <li><span>04</span><b>오답노트</b><p>오답 원인 태그를 적어 같은 실수를 추적합니다.</p></li>
  <li><span>05</span><b>재풀이</b><p>복습일에 오답만 다시 풀고 기록을 비교합니다.</p></li></ol>
 <div class="cta"><a class="btn pri" href="sample.html">셀프스터디 샘플 해보기</a><a class="btn" href="free.html#note">오답노트 양식 받기</a></div></div></section>

<section class="sec w">{sec_head("CATEGORY", "나에게 필요한 편입 문제집", "영역을 고르면 세부 분류와 상품을 볼 수 있습니다.")}
 <div class="catgrid">{cat_h}</div></section>

<section class="sec soft"><div class="w">{sec_head("NOW PREPARING", "지금 준비할 문제집", feat_note)}
 {grid(feat, R)}{NOTE_SPEC}
 <p class="more-l"><a href="products.html">전체 문제집 {len(PRODUCTS)}종 보기 →</a></p></div></section>

<section class="sec w">{sec_head("ENGLISH", "편입영어 컬렉션", "어휘·문법·독해·논리, 네 영역을 따로 또 함께 준비합니다.")}
 <div class="cols">{eng}</div></section>

<section class="sec math"><div class="w">{sec_head("MATHEMATICS", "편입수학 컬렉션", "풀이가 길어지는 만큼 문항당 쪽수를 넉넉히 설계합니다. 모든 정답은 독립 계산으로 검증합니다.", True)}
 <div class="cols">{mth}</div></div></section>

<section class="sec w" id="univ-search">{sec_head("UNIVERSITY", "목표 대학을 선택하세요.", "계열, 시험 과목, 대학명으로 찾을 수 있습니다. 각 대학의 시험 정보에는 기준 학년도와 확인 수준을 함께 표시합니다.")}
 <form class="ubig" action="univ.html" method="get" role="search"><label class="sr" for="uq">대학명 검색</label>
  <input id="uq" name="q" type="search" placeholder="대학명을 입력하세요 (예: 한양대, 중앙대)"><button class="btn pri" type="submit">대학 찾기</button></form>
 <div class="chips">{ulinks}</div></section>

<section class="sec dark"><div class="w">{sec_head("COMPLETE COLLECTION", "COMPLETE COLLECTION", "영역별 문제집을 학습 순서에 맞게 묶은 프리미엄 컬렉션입니다.", True)}
 <div class="compgrid">{comp}</div>
 <div class="cmpnote"><div><h3>개별 상품과 무엇이 다른가요?</h3><p>개별 문제집은 한 영역을 깊게 다루고, 패키지는 영역 순서와 학습 흐름까지 설계한 묶음입니다. 패키지의 구성품은 상세페이지에서 확인할 수 있으며, 구성 문제집이 모두 완성·검수되기 전에는 판매하지 않습니다.</p></div>
 <a class="btn gold" href="complete.html">패키지 전체 보기</a></div></div></section>

<section class="sec w" id="free">{sec_head("FREE SAMPLE", "문제와 해설을 먼저 확인하세요.", "과목별로 문제집과 해설집을 한 세트로 확인할 수 있습니다. 실제 파일이 준비된 샘플만 내려받을 수 있습니다.")}
 <div class="fgrid2 sg">{fcards}</div></section>

<section class="sec soft"><div class="w">{sec_head("OUR STANDARD", "편입샘의 제작 기준", "")}
 <ol class="crit">{crit_h}</ol>
 <p class="fn strong">현재 검수가 완료된 상품: <b>{reviewed}종</b>. 검수를 마친 상품에만 '검수 완료'를 표시합니다.</p></div></section>

<section class="sec w">{sec_head("LEARN", "학습 콘텐츠", "대학별 시험 정보와 학습 자료를 정리합니다.")}
 <div class="acgrid">{arts}</div></section>
"""
    page("index.html", "편입샘 — 대학 편입시험 전문 문제집", "대학 편입시험 전문 PDF 문제집. 편입영어·편입수학·대학별 모의고사. 필요한 문제만, 정확하게.", body,
         jsonld={"@context": "https://schema.org", "@type": "WebSite", "name": "편입샘", "url": SITE_URL,
                 "potentialAction": {"@type": "SearchAction", "target": SITE_URL + "/products.html?q={q}", "query-input": "required name=q"}})


# ───────────────────────── 카테고리 페이지 ─────────────────────────
def build_cat_pages():
    # 편입영어
    secs = ""
    intro = {"vocab": "문맥 속 의미 구분과 유사 표현 판별 중심.", "grammar": "영역별 개념 요약과 오답 원인 분석.",
             "reading": "지문 구조와 근거 문장을 찾는 독해.", "logic": "연결어와 논리 관계로 정답을 판단하는 훈련.",
             "eng_all": "종합본과 실전 모의고사, 시험 직전 점검."}
    for k in ["vocab", "grammar", "reading", "logic", "eng_all"]:
        secs += f'<section class="sec w" id="{k}">{sec_head("ENGLISH · " + SUBS[k], SUBS[k], intro[k])}{grid(by("english", k), "")}</section>'
    page("english.html", "편입영어 문제집", "편입영어 어휘·문법·독해·논리·종합 문제집 24종. 오답 선지까지 해설하는 PDF 문제집.",
         crumbs("", [("편입영어", None)]) + f'<div class="phead w"><h1>편입영어</h1><p>어휘·문법·독해·논리 네 영역과 종합·실전 문제집. 현재 모든 상품은 제작 준비 중이며 출시 예정으로 표시됩니다.</p></div>' + secs + f'<div class="w">{NOTE_SPEC}</div>', active="english.html")
    # 편입수학
    secs = ""
    intro = {"base": "대학수학 계산에 필요한 선수 개념.", "calc": "극한·미분·적분·급수·다변수미적분.", "linear": "행렬·벡터공간·고유값.",
             "eng_math": "미분방정식과 공학수학. 출제 범위는 대학마다 다릅니다.", "math_all": "계산 훈련, 시간 단축, 종합 실전과 모의고사."}
    for k in ["base", "calc", "linear", "eng_math", "math_all"]:
        secs += f'<section class="sec w" id="{k}">{sec_head("MATH · " + SUBS[k], SUBS[k], intro[k])}{grid(by("math", k), "")}</section>'
    page("math.html", "편입수학 문제집", "편입수학 기초수학·미적분학·선형대수학·공학수학 문제집. 풀이 분량을 고려한 PDF 문제집.",
         crumbs("", [("편입수학", None)]) + '<div class="phead w"><h1>편입수학</h1><p>수학은 식과 풀이가 길어 문항 수에 비해 쪽수가 많습니다. 문항당 쪽수를 영어보다 넉넉하게 설계했습니다.</p></div>' + secs + f'<div class="w">{NOTE_SPEC}</div>', active="math.html")
    # 전공
    mj = by("major")
    page("major.html", "전공 필기 문제집", "편입 전공 필기 대비 문제집 기획. 실제 전공시험과 연결될 때만 판매 후보로 활성화합니다.",
         crumbs("", [("전공 필기", None)]) + f'<div class="phead w"><h1>전공 필기</h1><p>컴퓨터공학·경영학·경제학·일반화학·일반물리학·생명과학 전공기초와 FINAL REVIEW.</p></div><section class="sec w"><div class="note">전공 필기 상품은 <b>대학별 실제 전공시험과 연결되는 경우에만</b> 판매 후보로 활성화합니다. 시험 시행 대학·모집단위와 전문가 검수자가 확인되기 전까지는 <b>기획 중</b>으로 표시합니다.</div>{grid(mj, "")}{NOTE_SPEC}</section>', active="major.html")
    # 면접
    iv = by("interview")
    page("interview.html", "편입 면접·서류 자료", "편입 면접 예상질문과 학업계획서·자기소개서 작성 워크북.",
         crumbs("", [("면접·서류", None)]) + f'<div class="phead w"><h1>편입 면접·서류</h1><p>문제집을 보조하는 면접·서류 준비 자료입니다.</p></div><section class="sec w"><div class="note">대학마다 <b>면접 시행 여부와 제출 서류</b>가 다릅니다. 지원 대학의 모집요강에서 시행 여부를 먼저 확인한 뒤 필요한 자료만 준비하세요. <a href="info.html">대학별 편입정보 보기</a></div>'
         f'<div id="interview">{sec_head("INTERVIEW", "면접", "")}{grid([p for p in iv if p["sub"] == "interview"], "")}</div><div id="docs">{sec_head("DOCUMENTS", "서류", "")}{grid([p for p in iv if p["sub"] == "docs"], "")}</div>{NOTE_SPEC}</section>', active="interview.html")
    # COMPLETE
    pk = by("complete")
    rows = ""
    for p in pk:
        comp = "<br>".join(f'<a href="p/{c}.html">{esc(BY_ID[c]["title"])}</a>' for c in p["includes"])
        rows += f'<tr><th scope="row"><a href="p/{p["id"]}.html">{esc(p["title"])}</a></th><td>{esc(p["who"])}</td><td>{comp}</td></tr>'
    page("complete.html", "COMPLETE 패키지", "편입영어·편입수학 COMPLETE 패키지와 대학별 FINAL 패키지. 구성품과 개별 상품과의 차이.",
         '<div class="darkpage">' + crumbs("", [("COMPLETE 패키지", None)]).replace("bc w", "bc w dk") +
         f'<div class="phead w dk"><span class="eb">COMPLETE COLLECTION</span><h1>COMPLETE COLLECTION</h1><p>영역별 문제집을 학습 순서에 맞게 묶은 프리미엄 컬렉션입니다. 구성 문제집이 모두 완성·검수되기 전에는 판매하지 않습니다.</p></div>'
         f'<section class="sec w">{grid(pk, "")}</section>'
         f'<section class="sec w"><div class="sh dk"><h2>개별 상품과의 차이</h2><p>개별 문제집은 한 영역을 깊게, 패키지는 영역의 순서와 학습 흐름까지 설계합니다.</p></div>'
         f'<div class="tw"><table class="tb dk"><thead><tr><th>패키지</th><th>적합한 수험생</th><th>구성품</th></tr></thead><tbody>{rows}</tbody></table></div></section></div>', active="complete.html", body_class="dkbody")


# ───────────────────────── 전체 상품(검색·필터) ─────────────────────────
def build_products_page():
    R = ""
    cat_opts = "".join(f'<label class="ck"><input type="checkbox" name="cat" value="{k}"><span>{v[0]}</span></label>' for k, v in CATS.items())
    diff_opts = "".join(f'<label class="ck"><input type="checkbox" name="diff" value="{d}"><span>{d}</span></label>' for d in DIFF)
    st_opts = "".join(f'<label class="ck"><input type="checkbox" name="status" value="{k}"><span>{v[0]}</span></label>' for k, v in STATUS.items() if any(p["status"] == k for p in PRODUCTS))
    uni_opts = '<option value="">대학 전체</option>' + "".join(f'<option value="{u["slug"]}">{esc(u["name"])}</option>' for u in UNIVS if any(p.get("univ") == u["slug"] for p in PRODUCTS))
    body = f"""{crumbs(R, [("전체 문제집", None)])}
<div class="phead w"><h1>전체 문제집</h1><p>검색과 필터로 필요한 문제집을 찾고, 최대 3개까지 비교할 수 있습니다.</p></div>
<section class="w shop">
 <aside class="filters" aria-label="필터"><button class="fbtn" id="fToggle" aria-expanded="false" aria-controls="fBody">필터</button>
 <form id="fBody" onsubmit="return false">
  <div class="fgp"><label class="fl" for="pq">검색</label><input id="pq" type="search" placeholder="상품명·대학·유형" autocomplete="off"></div>
  <fieldset><legend>카테고리</legend>{cat_opts}</fieldset>
  <fieldset><legend>난도</legend>{diff_opts}</fieldset>
  <div class="fgp"><label class="fl" for="pu">대학</label><select id="pu">{uni_opts}</select></div>
  <fieldset><legend>상태</legend>{st_opts}</fieldset>
  <button type="reset" class="lk" id="fReset">필터 초기화</button>
 </form></aside>
 <div class="res"><div class="rbar"><p id="rcount" role="status" aria-live="polite">{len(PRODUCTS)}종</p>
   <label class="sr" for="psort">정렬</label><select id="psort"><option value="">기본 순서</option><option value="diff">난도 낮은 순</option><option value="pages">쪽수 적은 순</option></select></div>
  <div class="pgrid" id="plist">{"".join(card(p, R) for p in PRODUCTS)}</div>
  <p class="empty" id="pempty" hidden>조건에 맞는 문제집이 없습니다. 필터를 줄여 보세요.</p>{NOTE_SPEC}</div>
</section>"""
    page("products.html", "전체 문제집", f"편입샘 문제집 {len(PRODUCTS)}종. 카테고리·난도·대학별 필터와 상품 비교.", body)


# ───────────────────────── 상품 상세 ─────────────────────────
def toc_for(p):
    if p["cat"] == "univ":
        r = ["시험 정보와 기준 학년도 안내"]
        r += [f"모의고사 {i}회 ({p['spec']})" for i in (1, 2, 3)]
        return r + ["정답 및 상세 해설", "채점표와 시간 배분 기록표", "회차별 취약 영역 분석"]
    if p["cat"] == "complete":
        return [f"구성 {i+1}. {BY_ID[c]['title']}" for i, c in enumerate(p["includes"])] + ["통합 학습 플래너(설계안)"]
    r = ["이용 안내와 학습 플래너"]
    r += [f"Part {i+1}. {t}" for i, t in enumerate(p["types"])]
    return r + ["정답 및 상세 해설", "오답노트 양식", "부록(유형별 점검표)"]


FORMAT = {"english": "객관식(4~5지선다) 중심. 지원 대학의 문항 형식에 맞춰 조정(설계안)",
          "math": "객관식과 단답형 병행(설계안)",
          "major": "개념 문제와 계산 문제(설계안)", "interview": "질문·작성 양식 중심 워크북",
          "complete": "구성 문제집 묶음"}


def wire(kind):
    """PDF 구성 시안(실제 문항 아님)."""
    lines = "".join(f'<i style="width:{w}%"></i>' for w in (92, 80, 88, 62, 90, 76, 84, 58))
    if kind == "q":
        return f'<div class="wf" aria-hidden="true"><b>문제 페이지 구성 시안</b><span class="n">Q.01</span>{lines}<div class="ch"><i></i><i></i><i></i><i></i></div></div>'
    return f'<div class="wf" aria-hidden="true"><b>해설 페이지 구성 시안</b><span class="n">A.01</span><div class="ans">정답 · 근거</div>{lines}<div class="ans alt">오답 선지 분석</div>{lines[:160]}</div>'


def build_product_pages(samples):
    R = "../"
    for p in PRODUCTS:
        cat, catfile, _ = CATS[p["cat"]]
        sub = SUBS.get(p["sub"], "")
        univ = UNIV_BY_SLUG.get(p.get("univ"))
        rel = [x for x in PRODUCTS if x["id"] != p["id"] and x["sub"] == p["sub"] and x["cat"] == p["cat"]][:4]
        if len(rel) < 4:
            rel += [x for x in PRODUCTS if x["id"] != p["id"] and x["cat"] == p["cat"] and x not in rel][:4 - len(rel)]
        if p["cat"] == "univ":
            rel = [x for x in PRODUCTS if x["id"] != p["id"] and x["cat"] == "univ"][:4]
        buy = ""
        if p["status"] == "on_sale" and p.get("price"):
            buy = f'<button class="btn pri wide" data-cart="{p["id"]}">장바구니 담기</button>'
        else:
            lab = "출시 알림 신청" if p["status"] in ("coming_soon", "draft", "sample_ready") else "판매 종료"
            buy = f'<a class="btn pri wide" href="#notify">{lab}</a>' if p["status"] != "discontinued" else '<button class="btn wide dis" disabled>판매 종료</button>'
        if p["sample"]:
            sp = p["sample"]
            sample_btn = (f'<a class="btn wide" href="../{sp["file"]}" download>문제집 샘플 PDF</a>'
                          f'<a class="btn wide" href="../{sp.get("solution", sp["file"])}" download>해설집 샘플 PDF</a>')
        else:
            sample_btn = '<button class="btn wide dis" disabled>샘플 준비 중</button>'
        legacy = [k for k, v in LEGACY_MERGE.items() if v == p["id"]]
        spec_rows = [("분류", f"{cat} · {sub}"), ("예상 난도", p["diff"]), ("문항·구성", qlabel(p) + " (설계안)")]
        if p.get("pages"):
            spec_rows.append(("페이지 수", f'약 {p["pages"]}쪽 (설계안)'))
        if p["cat"] == "univ":
            spec_rows += [("대상 계열", p["track"]), ("시험 형식(기준)", p["spec"]), ("기준 학년도", f"{YEAR} · 마지막 확인 {CHECKED}"),
                          ("확인 수준", LEVEL_LABEL[p["level"]])]
        else:
            spec_rows.append(("문항 유형", FORMAT.get(p["cat"], "")))
        spec_rows += [("파일 형식", "PDF (A4 기준 설계안)"), ("공개 상태", STATUS[p["status"]][0])]
        spec = "".join(f"<tr><th scope='row'>{esc(a)}</th><td>{esc(b)}</td></tr>" for a, b in spec_rows)
        toc = "".join(f"<li>{esc(t)}</li>" for t in toc_for(p))
        types = "".join(f'<li>{esc(t)}</li>' for t in p["types"])
        inc = "".join(f'<li>{esc(t)}</li>' for t in p["inc"])
        note = f'<div class="note">{esc(p["note"])}</div>' if p.get("note") else ""
        univ_box = ""
        if univ:
            univ_box = f'<div class="note"><b>{esc(univ["name"])}</b> 시험 정보는 {YEAR} 기준 {LEVEL_LABEL[univ["level"]]}입니다. <a href="../u/{univ["slug"]}.html">대학별 편입정보에서 확인 수준과 출처 보기</a></div>'
        incl = ""
        if p["includes"]:
            incl = '<ul class="inc">' + "".join(f'<li><a href="../p/{c}.html">{esc(BY_ID[c]["title"])}</a> <span class="mm">{esc(meta_line(BY_ID[c]))}</span></li>' for c in p["includes"]) + "</ul>"
        legacy_note = f'<p class="fn">이전 홈페이지의 \'{esc(legacy[0])}\' 기획 상품을 이어받은 상품입니다.</p>' if legacy else ""
        preview = (f'<div class="sample-links"><p>이 상품과 같은 방식으로 구성한 샘플 문제집·해설집입니다. (독창 문항 · 전문가 검수 전 시안)</p><a class="btn pri" href="../{p["sample"].get("page", "sample.html")}">샘플 화면으로 보기</a> <a class="btn" href="../{p["sample"]["file"]}" download>문제집 PDF</a> <a class="btn" href="../{p["sample"].get("solution", p["sample"]["file"])}" download>해설집 PDF</a></div>' if p["sample"] else
                   f'<div class="wfs">{wire("q")}{wire("a")}</div><p class="fn">PDF 샘플은 제작·검수가 끝나면 이 자리에서 미리볼 수 있습니다. 위 그림은 페이지 구성 시안이며 실제 문항이 아닙니다.</p>')
        tabs = "".join(f'<a href="#{i}">{t}</a>' for i, t in [("intro", "소개"), ("spec", "구성"), ("toc", "목차"), ("preview", "미리보기"), ("guide", "구매 안내"), ("notify", "알림 신청")])
        body = f"""{crumbs(R, [(cat, catfile), (sub if p['cat'] != 'univ' else univ['name'], None)])}
<section class="w pd">
 <div class="pd-cv"><div class="cvbig">{cover(p, R)}</div><p class="cap">※ 표지는 디자인 시안이며 실제 제작본과 다를 수 있습니다.</p></div>
 <div class="pd-info">
  <div class="pc-tags">{badge(p)}<span class="tag">{esc(sub)}</span>{f'<span class="tag">{esc(p["series"])}</span>' if p.get('series') and p['cat'] != 'univ' and p['series'] not in sub else ''}</div>
  <h1>{esc(p['title'])}</h1>
  <p class="lead">{esc(p['summary'])}</p>
  <dl class="kv"><div><dt>난도</dt><dd>{p['diff']}</dd></div><div><dt>구성</dt><dd>{esc(qlabel(p))}</dd></div>{f'<div><dt>쪽수</dt><dd>약 {p["pages"]}쪽</dd></div>' if p.get('pages') else ''}<div><dt>형식</dt><dd>PDF</dd></div></dl>
  <div class="pbox"><div class="prow">{price_html(p)}</div>
   <div class="acts">{buy}{sample_btn}<button class="btn wide cmp" data-compare="{p['id']}" aria-pressed="false">비교 담기</button></div>
   <p class="fn">{('결제 시스템이 연결되기 전에는 구매할 수 없습니다.' if p['status'] != 'on_sale' else '결제는 주문 단계에서 안내됩니다.')}</p></div>
  {univ_box}{note}
 </div>
</section>
<div class="w"><nav class="tabs" aria-label="상세 페이지 목차">{tabs}</nav></div>
<section class="w pdsec" id="intro"><h2>이 문제집은</h2>
 <div class="story"><div><h3>해결하려는 문제</h3><p>{esc(p['problem'])}</p></div>
 <div><h3>이런 수험생에게</h3><p>{esc(p['who'])}</p></div>
 <div><h3>학습하는 유형</h3><ul class="chiplist">{types}</ul></div>
 <div><h3>활용 방법</h3><p>{esc(p['how'])}</p></div>
 <div><h3>포함 자료</h3><ul class="dots">{inc}</ul></div></div>{incl}{legacy_note}</section>
<section class="w pdsec" id="spec"><h2>구성 정보</h2><div class="tw"><table class="tb"><tbody>{spec}</tbody></table></div><p class="fn">문항 수와 쪽수는 설계안이며 제작·검수 과정에서 조정될 수 있습니다.</p></section>
<section class="w pdsec" id="toc"><h2>상세 목차 <span class="mm">설계안</span></h2><ol class="toc">{toc}</ol></section>
<section class="w pdsec" id="preview"><h2>문제·해설 샘플</h2>{preview}</section>
<section class="w pdsec" id="guide"><h2>구매·다운로드 및 이용 안내</h2>
 <div class="guidegrid"><div><h3>구매·다운로드</h3><p>판매가 시작되면 결제 완료 후 다운로드 방법을 이 페이지와 이메일로 안내합니다. 결제 시스템이 연결되기 전에는 구매할 수 없습니다.</p></div>
 <div><h3>파일 형식</h3><p>PDF 1종. 열람 환경과 인쇄 가능 여부는 판매 시작 전에 확정해 안내합니다.</p></div>
 <div><h3>이용·환불</h3><p>디지털 콘텐츠의 환불·청약철회 규정은 판매 시작 전에 공지합니다. 자세한 내용은 <a href="../guide.html">이용 안내</a>를 확인하세요.</p></div></div></section>
<section class="w pdsec" id="notify"><h2>출시 알림 신청</h2>
 <form class="nform" data-form="notify" data-product="{p['id']}" novalidate>
  <p class="fn" data-statusmsg>알림 신청 접수 상태를 확인하고 있습니다…</p>
  <label for="ne-{p['id']}">이메일 주소</label><input id="ne-{p['id']}" name="email" type="email" required autocomplete="email" placeholder="example@email.com">
  <input class="hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
  <label class="ck consent"><input type="checkbox" name="consent" required><span>[필수] 개인정보 수집·이용에 동의합니다. (이메일 주소 / 해당 상품 출시 안내 목적 / 신청일로부터 12개월 보관 후 파기, 요청 시 즉시 삭제) <a href="../privacy.html">자세히</a></span></label>
  <button class="btn pri" type="submit" disabled>알림 신청</button><p class="msg" role="status" aria-live="polite"></p>
 </form></section>
<section class="w pdsec"><h2>관련 상품</h2>{grid(rel, R)}{NOTE_SPEC}</section>
<div class="sticky" role="region" aria-label="구매 메뉴"><div class="sp">{price_html(p)}</div>
 <button class="btn cmp" data-compare="{p['id']}" aria-pressed="false">비교</button>
 {('<button class="btn pri" data-cart="%s">장바구니</button>' % p['id']) if (p['status'] == 'on_sale' and p.get('price')) else ('<a class="btn pri" href="#notify">출시 알림</a>' if p['status'] != 'discontinued' else '')}</div>"""
        ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "홈", "item": SITE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": cat, "item": f"{SITE_URL}/{catfile}"},
            {"@type": "ListItem", "position": 3, "name": p["title"]}]}
        page(f"p/{p['id']}.html", p["title"], p["summary"], body, active=catfile, body_class="detail", jsonld=ld)


# ───────────────────────── 대학 ─────────────────────────
def build_univ_pages():
    R = ""
    cards = ""
    for u in UNIVS:
        trk, subj = SUBJ[u["slug"]]
        prods = [p for p in PRODUCTS if p.get("univ") == u["slug"]]
        hay = f'{u["name"]} {u["name"].replace("학교", "")} {trk} {subj}'
        cards += f"""<a class="uc" href="u/{u['slug']}.html" data-hay="{esc(hay.lower())}" data-track="{esc(trk)}" data-subj="{esc(subj)}" data-level="{u['level']}">
 <div class="uh"><h3>{esc(u['name'])}</h3><span class="lv lv-{u['level']}">{LEVEL_LABEL[u['level']]}</span></div>
 <dl><div><dt>계열</dt><dd>{esc(trk)}</dd></div><div><dt>시험 과목</dt><dd>{esc(subj)}</dd></div><div><dt>모의고사</dt><dd>{f'{len(prods)}종 출시 예정' if prods else '상품 기획 전'}</dd></div></dl></a>"""
    prods = by("univ")
    body = f"""{crumbs(R, [("대학별 모의고사", None)])}
<div class="phead w"><h1>목표 대학을 선택하세요.</h1><p>모든 대학이 같은 편입시험을 치르지 않습니다. 편입샘은 대학 공식 자료로 확인된 시험 형식에 대해서만 모의고사를 기획하며, {YEAR} 기준 확인 수준을 함께 표시합니다.</p></div>
<section class="w usearch">
 <form class="ubig" role="search" onsubmit="return false"><label class="sr" for="uq2">대학명 검색</label><input id="uq2" type="search" placeholder="대학명을 입력하세요 (예: 한양대, 중앙대)" autocomplete="off"></form>
 <div class="ufil"><fieldset><legend>계열</legend><label class="ck"><input type="checkbox" name="track" value="인문"><span>인문</span></label><label class="ck"><input type="checkbox" name="track" value="자연"><span>자연</span></label></fieldset>
 <fieldset><legend>시험 과목</legend><label class="ck"><input type="checkbox" name="subj" value="영어"><span>영어</span></label><label class="ck"><input type="checkbox" name="subj" value="수학"><span>수학</span></label></fieldset>
 <fieldset><legend>확인 수준</legend><label class="ck"><input type="checkbox" name="level" value="official"><span>공식 문서</span></label><label class="ck"><input type="checkbox" name="level" value="partial"><span>공식 공지 일부</span></label><label class="ck"><input type="checkbox" name="level" value="secondary"><span>2차 자료</span></label><label class="ck"><input type="checkbox" name="level" value="none"><span>미확인</span></label></fieldset></div>
 <p id="ucount" role="status" aria-live="polite">{len(UNIVS)}개 대학</p>
 <div class="ugrid" id="ulist">{cards}</div><p class="empty" id="uempty" hidden>조건에 맞는 대학이 없습니다.</p>
 <div class="note">대학별 시험은 해마다 바뀝니다. 이 페이지의 정보는 {YEAR} 기준(마지막 확인 {CHECKED})이며, 공식 모집요강으로 확인된 수준에 따라 상품 기획 여부를 결정합니다. 연세대·고려대처럼 모집단위·캠퍼스별로 시험이 다른 대학은 공식 확인 전까지 정보 페이지로만 제공합니다. <a href="info.html">대학별 편입정보 표 보기</a></div>
</section>
<section class="sec w" id="products">{sec_head("MOCK EXAMS", "대학별 모의고사 상품", "공식 자료로 시험 형식이 확인된 대학부터 기획합니다.")}{grid(prods, R)}{NOTE_SPEC}</section>"""
    page("univ.html", "대학별 모의고사", "건국·한양·중앙·한국외대·동국대 등 대학별 편입 필기시험 형식에 맞춘 모의고사. 기준 학년도와 확인 수준 표시.", body, active="univ.html")

    # 개별 대학 페이지
    stlab = {"product": "출시 예정 상품 있음", "candidate": "상품 기획 후보 (공식 확인 후 결정)", "unconfirmed": "시험 정보 미확인", "none": "해당 시험 형식 없음/별도 구성 없음"}
    for u in UNIVS:
        R = "../"
        prods = [p for p in PRODUCTS if p.get("univ") == u["slug"]]
        links = "".join(f'<li><a href="{esc(h)}" rel="noopener" target="_blank">{esc(t)}</a> <span class="mm">{"공식" if k == "official" else "2차 자료"}</span></li>' for t, h, k in u["links"]) or "<li>공식 링크 미확인</li>"
        exam = "".join(f"<li>{esc(x)}</li>" for x in u["exam"])
        rows = ""
        for key, label in CAND_TYPES:
            st, v = u["cand"][key]
            extra = ""
            if st == "product":
                extra = f' · <a href="../p/{v}.html">{esc(BY_ID[v]["title"])}</a>'
            elif v:
                extra = f" · {esc(v)}"
            rows += f'<tr><th scope="row">{key}. {label}</th><td><span class="st st-{st}">{stlab[st]}</span>{extra}</td></tr>'
        info = [("기준 학년도", YEAR), ("일반·학사편입", u["types"]), ("모집단위", u["units"]), ("공인영어 반영", u["english"]),
                ("면접", u["interview"]), ("서류", u["docs"]), ("마지막 확인일", CHECKED), ("확인 수준", LEVEL_LABEL[u["level"]])]
        irows = "".join(f"<tr><th scope='row'>{a}</th><td>{esc(b)}</td></tr>" for a, b in info)
        warn = ("이 정보는 공식 문서에서 직접 확인했습니다. 그래도 지원 전에는 최신 모집요강을 다시 확인하세요." if u["level"] == "official" else
                "공식 공지의 일부만 확인한 정보입니다. 수치는 요약 자료 기준이므로 공식 원문과 대조가 필요합니다." if u["level"] == "partial" else
                "학원·입시 블로그 등 2차 자료만 확인했습니다. 공식 모집요강과 다를 수 있으므로 단정하지 마세요." if u["level"] == "secondary" else
                "시험 정보를 확인하지 못했습니다. 공식 모집요강 확인 전에는 상품 기획을 진행하지 않습니다.")
        body = f"""{crumbs(R, [("대학별 편입정보", "info.html"), (u['name'], None)])}
<div class="phead w"><span class="lv lv-{u['level']}">{LEVEL_LABEL[u['level']]}</span><h1>{esc(u['name'])} 편입 시험 정보</h1>
 <p>{YEAR} 기준 · 마지막 확인 {CHECKED}</p></div>
<section class="w pdsec"><div class="note lvl-{u['level']}"><b>확인 수준: {LEVEL_LABEL[u['level']]}.</b> {warn}</div>
 {f'<div class="note">{esc(u["note"])}</div>' if u.get("note") else ''}
 <h2>기본 정보</h2><div class="tw"><table class="tb"><tbody>{irows}</tbody></table></div>
 <h2>필기시험</h2><ul class="dots">{exam}</ul>
 <h2>공식 링크·출처</h2><ul class="dots">{links}</ul></section>
<section class="w pdsec"><h2>상품 유형별 상태</h2><div class="tw"><table class="tb"><tbody>{rows}</tbody></table></div>
 <p class="fn">실제로 존재하는 시험 형식에만 상품을 기획합니다. '후보' 표시는 판매 예정이 아니라 공식 확인 후 결정할 기획 후보입니다.</p></section>
{f'<section class="w pdsec"><h2>관련 문제집</h2>{grid(prods, R)}{NOTE_SPEC}</section>' if prods else ''}"""
        page(f"u/{u['slug']}.html", f"{u['name']} 편입 시험 정보", f"{u['name']} {YEAR} 편입 필기시험 정보와 확인 수준, 관련 모의고사.", body, active="info.html")

    # 정보센터
    rows = ""
    for u in UNIVS:
        prods = [p for p in PRODUCTS if p.get("univ") == u["slug"]]
        rel = "<br>".join(f'<a href="p/{p["id"]}.html">{esc(p["title"])}</a>' for p in prods) or "—"
        lk = "<br>".join(f'<a href="{esc(h)}" rel="noopener" target="_blank">{esc(t)}</a>' for t, h, k in u["links"]) or "공식 링크 미확인"
        trk, subj = SUBJ[u["slug"]]
        ex = "<br>".join(esc(x) for x in u["exam"][:2])
        rows += f"""<tr data-hay="{esc((u['name'] + ' ' + subj + ' ' + trk).lower())}">
<th scope="row" data-l="대학"><a href="u/{u['slug']}.html">{esc(u['name'])}</a></th><td data-l="학년도">{YEAR}</td><td data-l="일반·학사">{esc(u['types'])}</td><td data-l="모집단위">{esc(u['units'])}</td>
<td data-l="필기시험">{ex}</td><td data-l="공인영어">{esc(u['english'])}</td><td data-l="면접">{esc(u['interview'])}</td><td data-l="서류">{esc(u['docs'])}</td>
<td data-l="공식 링크">{lk}</td><td data-l="마지막 확인">{CHECKED}</td><td data-l="확인 수준"><span class="lv lv-{u['level']}">{LEVEL_LABEL[u['level']]}</span></td><td data-l="관련 문제집">{rel}</td></tr>"""
    body = f"""{crumbs("", [("대학별 편입정보", None)])}
<div class="phead w"><span class="eb">TRANSFER INFORMATION CENTER</span><h1>대학별 편입정보</h1>
<p>15개 대학의 {YEAR} 편입 필기시험 정보를 정리합니다. 공식 출처로 확인되지 않은 항목은 <b>미확인</b>으로 표시하며, 확인 수준(공식 문서 / 공식 공지 일부 / 2차 자료)을 함께 밝힙니다.</p></div>
<section class="w"><div class="note">대학별 시험은 해마다 바뀝니다. 이 정보는 참고용이며 지원 전에는 반드시 해당 대학의 최신 공식 모집요강을 확인하세요. 마지막 확인일: {CHECKED}</div>
 <form class="ubig" role="search" onsubmit="return false"><label class="sr" for="iq">대학명 검색</label><input id="iq" type="search" placeholder="대학명 또는 과목으로 검색" autocomplete="off"></form>
 <div class="tw wide"><table class="tb itb" id="itb"><thead><tr><th>대학</th><th>학년도</th><th>일반·학사</th><th>모집단위</th><th>필기시험</th><th>공인영어</th><th>면접</th><th>서류</th><th>공식 링크</th><th>마지막 확인</th><th>확인 수준</th><th>관련 문제집</th></tr></thead><tbody>{rows}</tbody></table></div></section>"""
    page("info.html", "대학별 편입정보", f"15개 대학 {YEAR} 편입 필기시험 정보. 공식 출처 링크와 확인 수준 표시, 미확인 항목 구분.", body, active="info.html")


# ───────────────────────── 학습 콘텐츠 ─────────────────────────
def build_learn():
    R = ""
    cards = "".join(f'<a class="ac" href="learn/{a["slug"]}.html"><span class="tag">{esc(a["tag"])}</span><h3>{esc(a["title"])}</h3><p>{esc(a["desc"])}</p><time datetime="{a["date"]}">{a["date"]}</time></a>' for a in sorted(ARTICLES, key=lambda a: a["date"], reverse=True))
    cards += "".join(f'<div class="ac pend"><span class="tag">{esc(a["tag"])}</span><h3>{esc(a["title"])}</h3><p>{esc(a["desc"])}</p><span class="soon">준비 중</span></div>' for a in ARTICLE_PENDING)
    page("learn.html", "학습 콘텐츠", "편입 학습법, 대학별 편입시험 정보, 일반편입·학사편입 안내.",
         crumbs(R, [("학습 콘텐츠", None)]) + f'<div class="phead w"><h1>학습 콘텐츠</h1><p>대학별 시험 정보와 학습 자료를 최신순으로 정리합니다.</p></div><section class="w"><div class="acgrid">{cards}</div></section>')
    for a in ARTICLES:
        R2 = "../"
        body = "".join(f"<h2>{esc(h)}</h2><p>{esc(t)}</p>" for h, t in a["body"])
        src = "".join(f'<li><a href="{R2 + h if not h.startswith("http") else h}" rel="noopener" target="_blank">{esc(t)}</a></li>' for t, h in a["sources"])
        page(f"learn/{a['slug']}.html", a["title"], a["desc"],
             crumbs(R2, [("학습 콘텐츠", "learn.html"), (a["tag"], None)]) +
             f'<article class="w art"><span class="tag">{esc(a["tag"])}</span><h1>{esc(a["title"])}</h1><time datetime="{a["date"]}">{a["date"]}</time>{body}<h2>출처</h2><ul class="dots">{src}</ul><p class="fn">모든 정보는 작성일 기준이며 2027학년도 모집요강 공개 후 달라질 수 있습니다.</p></article>')


# ───────────────────────── 보조 페이지 ─────────────────────────
def build_misc(samples):
    R = ""
    # 무료 샘플
    page("free.html", "무료 샘플", "과목별 문제집·해설집 샘플 PDF와 오답노트 양식. 실제 파일이 준비된 샘플만 다운로드할 수 있습니다.",
         crumbs(R, [("무료 샘플", None)]) + f'''<div class="phead w"><h1>문제와 해설을 먼저 확인하세요.</h1><p>과목마다 문제집과 해설집을 한 세트로 제공합니다. 모든 샘플은 편입샘이 새로 만든 독창 문항이며, 전문가 검수 전 제작 방식 시연용 시안입니다.</p></div>
<section class="w" id="note"><div class="fgrid2 sg">{sample_cards(R, samples)}</div>
<div class="note">샘플은 판매 상품의 문항이 아니라 <b>문제집과 해설집의 구성 방식</b>을 보여 주기 위한 것입니다. 판매 상품의 문항·해설은 검수를 마친 뒤에만 공개하며, 검수를 마친 상품에만 '검수 완료'를 표시합니다.</div></section>''', active="free.html")
    # 이용 안내
    qa = [("편입샘은 어떤 곳인가요?", "대학 편입시험 대비 PDF 문제집을 제작·판매하는 브랜드입니다. 학원, 과외, 컨설팅은 하지 않습니다."),
          ("문항은 어떻게 만드나요?", "AI로 초안을 만들고, 독립 풀이와 계산 검증을 거친 뒤 영어·수학 전문가가 정답·해설·출제 범위를 검수합니다. 검수를 마치지 않은 문항은 판매하지 않으며, 검수를 마친 상품에만 '검수 완료'를 표시합니다."),
          ("기출문제를 사용하나요?", "대학 기출문제를 복제하지 않고 독창 문항으로 제작합니다."),
          ("대학별 모의고사의 기준은 무엇인가요?", "해당 학년도 대학 공식 모집요강의 문항 수·시간·형식입니다. 상품 페이지에 기준 학년도와 확인 수준을 표시하며, 요강이 바뀌면 개정합니다. 공식 확인 전에는 상품이 아닌 정보 페이지로만 제공합니다."),
          ("혼자 공부해도 되나요?", "셀프스터디를 전제로 설계합니다. 해설집에 본문 번역, 문장별 분석, 정답 근거, 오답 선지 해부, 오답노트 양식을 담아 혼자서도 막힌 곳을 찾을 수 있게 합니다. 다만 개별 질의응답·첨삭은 제공하지 않으며, 합격이나 점수 향상을 보장하지 않습니다."),
          ("샘플은 어디서 보나요?", "무료 샘플 메뉴에서 과목별(편입영어·편입수학·대학별 모의고사) 문제집과 해설집 PDF를 내려받을 수 있습니다. 샘플은 독창 문항이며 전문가 검수 전 시안입니다."),
          ("상품 상태 표시는 무슨 뜻인가요?", "기획 중(draft) / 출시 예정(coming_soon) / 샘플 공개(sample_ready) / 판매 중(on_sale) / 판매 종료(discontinued)입니다. '판매 중'인 상품만 구매할 수 있습니다."),
          ("지금 구매할 수 있나요?", "아직 판매 중인 상품이 없습니다. 결제 시스템이 연결되고 상품이 검수를 마치면 판매를 시작하며, 출시 알림을 신청하실 수 있습니다."),
          ("구매·환불은 어떻게 되나요?", "결제 방식, 다운로드 방법, 환불·청약철회 규정은 판매 시작 전에 이곳에 공지합니다."),
          ("가격은 어떻게 정해지나요?", "가격은 판매가 확정되기 전에는 표시하지 않습니다. 임의의 정가나 할인율을 표시하지 않습니다."),
          ("정오표는 어디서 보나요?", "오류가 확인되면 이곳에 정오표를 공개하고 구매자에게 개정본을 안내합니다."),
          ("재배포가 가능한가요?", "PDF의 복제·재배포·공유는 금지됩니다.")]
    body = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in qa)
    page("guide.html", "이용 안내", "편입샘 이용 안내: 제작·검수 방식, 상품 상태, 구매·환불, 정오표.", crumbs(R, [("이용 안내", None)]) + f'<div class="phead w"><h1>이용 안내</h1></div><section class="w faq">{body}<p>문의: <a href="contact.html">고객 문의</a></p></section>', active="guide.html")
    # 문의
    page("contact.html", "고객 문의", "편입샘 고객 문의와 출시 알림 요청.",
         crumbs(R, [("고객 문의", None)]) + f"""<div class="phead w"><h1>고객 문의</h1><p>제작 중인 문제집, 대학별 시험 정보, 오류 신고 등을 남겨 주세요.</p></div>
<section class="w"><form class="nform wide" data-form="contact" novalidate>
 <p class="fn" data-statusmsg>접수 상태를 확인하고 있습니다…</p>
 <label for="cn">이름 (선택)</label><input id="cn" name="name" autocomplete="name">
 <label for="ce">답변받을 이메일</label><input id="ce" name="email" type="email" required autocomplete="email">
 <label for="cm">문의 내용</label><textarea id="cm" name="message" rows="6" required maxlength="2000"></textarea>
 <input class="hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
 <label class="ck consent"><input type="checkbox" name="consent" required><span>[필수] 개인정보 수집·이용에 동의합니다. (이메일·이름·문의 내용 / 문의 답변 목적 / 문의 처리 후 12개월 보관 후 파기, 요청 시 즉시 삭제) <a href="privacy.html">자세히</a></span></label>
 <button class="btn pri" type="submit" disabled>문의 보내기</button><p class="msg" role="status" aria-live="polite"></p></form>
 <p class="fn">접수 시스템이 연결되지 않은 경우 양식은 비활성화됩니다. 이 경우 <a href="mailto:{CONTACT_MAIL}?subject=편입샘 문의">{CONTACT_MAIL}</a> 로 직접 보내 주세요.</p></section>""")
    # 개인정보
    page("privacy.html", "개인정보 처리방침", "편입샘 개인정보 수집·이용·보관 정책.",
         crumbs(R, [("개인정보 처리방침", None)]) + """<div class="phead w"><h1>개인정보 처리방침</h1><p>시행 전 초안입니다. 사업자 정보와 법적 검토를 마친 뒤 확정·공지합니다.</p></div>
<section class="w art">
<h2>1. 수집 항목과 목적</h2><ul class="dots"><li>출시 알림 신청: 이메일 주소 — 신청한 상품의 출시 안내</li><li>고객 문의: 이메일 주소, 이름(선택), 문의 내용 — 문의 답변</li></ul>
<h2>2. 보관 기간</h2><p>신청일(문의 접수일)로부터 12개월 동안 보관한 뒤 파기합니다. 목적 달성(출시 안내 발송, 문의 답변 완료) 후에는 요청 시 즉시 삭제합니다.</p>
<h2>3. 동의 거부 권리</h2><p>동의를 거부할 수 있으며, 거부해도 사이트의 상품 열람은 제한되지 않습니다. 다만 출시 알림 신청과 문의 접수는 이용할 수 없습니다.</p>
<h2>4. 제3자 제공·위탁</h2><p>수집한 정보를 제3자에게 제공하지 않습니다. 저장은 Cloudflare 인프라에서 이루어집니다(해외 이전 포함 가능).</p>
<h2>5. 삭제·열람 요청</h2><p><a href="contact.html">고객 문의</a>로 요청하시면 확인 후 삭제합니다.</p>
<p class="fn">※ 사업자 상호·대표자·개인정보 보호책임자 정보는 판매 시작 전 이 문서에 추가합니다.</p></section>""")
    # 비교 / 장바구니
    page("compare.html", "상품 비교", "문제집 최대 3종을 나란히 비교합니다.",
         crumbs(R, [("상품 비교", None)]) + '<div class="phead w"><h1>상품 비교</h1><p>상품 카드의 \'비교 담기\'로 최대 3종까지 담을 수 있습니다.</p></div><section class="w"><div id="cmpbox" class="tw"></div><p class="empty" id="cmpempty" hidden>비교할 상품이 없습니다. <a href="products.html">전체 문제집 보기</a></p></section>', robots="noindex")
    page("cart.html", "장바구니", "장바구니와 주문 단계 안내.",
         crumbs(R, [("장바구니", None)]) + '<div class="phead w"><h1>장바구니</h1></div><section class="w"><div id="cartbox"></div><p class="empty" id="cartempty" hidden>장바구니가 비어 있습니다. 현재 판매 중인 상품이 없습니다. <a href="products.html">전체 문제집 보기</a></p><div class="note">결제 시스템이 연결되기 전에는 주문·결제를 할 수 없습니다. 결제가 연결되면 이 화면에서 주문이 진행됩니다.</div><button class="btn pri" disabled>결제 준비 중</button></section>', robots="noindex")


def build_sample_pages(samples):
    """샘플 문제집·해설집 화면. PDF 는 tools/make_sample_pdfs.js 가 이 화면에서 생성한다."""
    R = ""
    page("sample.html", "샘플 문제집·해설집", "편입영어·편입수학·대학별 모의고사 샘플. 과목마다 문제집과 해설집 한 세트.",
         crumbs(R, [("무료 샘플", "free.html"), ("샘플 문제집·해설집", None)]) +
         f'''<div class="phead w"><span class="eb">SAMPLE · PROBLEM BOOK &amp; SOLUTION BOOK</span><h1>샘플 문제집·해설집</h1>
<p>과목마다 문제집과 해설집을 한 세트로 준비했습니다. 문제를 먼저 풀고, 해설집으로 끝까지 확인하세요. 셀프스터디가 이렇게 진행됩니다.</p></div>
<section class="w"><div class="fgrid2 sg">{sample_cards(R, samples)}</div>
<div class="note">모든 샘플은 편입샘이 새로 만든 <b>독창 문항</b>이며, 타 교재·기출문제를 복제하지 않았습니다. 판매 상품이 아니라 구성 방식을 보여 주는 <b>전문가 검수 전 시안</b>입니다.</div></section>''', active="free.html")
    for key, meta in sc.SAMPLE_SETS.items():
        prob, sol = sc.sheets_for(key)
        q, so = samples["free"].get(key + "-q"), samples["free"].get(key + "-s")
        dl = ""
        if q and (OUT / q["file"]).exists():
            dl += f'<a class="btn pri" href="../{q["file"]}" download>문제집 PDF 내려받기</a>'
        if so and (OUT / so["file"]).exists():
            dl += f'<a class="btn" href="../{so["file"]}" download>해설집 PDF 내려받기</a>'
        dl = dl or '<span class="fn">PDF 파일 준비 중</span>'
        page(f"sample/{key}.html", f"{meta['label']} 샘플 문제집·해설집", f"{meta['label']} 샘플: 문제집과 해설집. 독창 문항, 전문가 검수 전 시안.",
             crumbs("../", [("무료 샘플", "free.html"), ("샘플 문제집·해설집", "sample.html"), (meta["label"], None)]) +
             f'''<div class="phead w"><span class="eb">SAMPLE · {meta["label"]}</span><h1>{meta["label"]} 샘플 — 문제집과 해설집</h1>
<p>{meta["sub"]}. 먼저 문제집을 풀고 해설집을 확인하세요. 아래는 PDF와 동일한 구성입니다.</p><div class="cta sdl">{dl}</div></div>
<section class="w sheets"><h2 class="sx-t">문제집</h2>{prob}<h2 class="sx-t">해설집</h2>{sol}
<div class="note">전문가 검수 전 제작 방식 시연용 샘플입니다. 판매 상품의 문항·해설은 검수를 마친 뒤에만 공개합니다. 대학 명칭은 시험 형식 표기를 위한 서술적 사용이며 해당 대학과 무관한 비공식 자료입니다.</div></section>''',
             active="free.html", robots="noindex" if False else None)


def build_data_files():
    pj = []
    for p in PRODUCTS:
        pj.append(dict(id=p["id"], title=p["title"], cat=CATS[p["cat"]][0], sub=SUBS.get(p["sub"], ""), diff=p["diff"], q=qlabel(p),
                       pages=p.get("pages"), status=p["status"], statusLabel=STATUS[p["status"]][0],
                       price=p.get("price"), sale=p.get("sale_price"), who=p["who"], inc=" · ".join(p["inc"]), url=f"p/{p['id']}.html"))
    (OUT / "assets").mkdir(exist_ok=True)
    (OUT / "assets" / "products.json").write_text(json.dumps(pj, ensure_ascii=False), encoding="utf-8")
    (OUT / "assets" / "covers.svg").write_text(covers.sprite_file(), encoding="utf-8")
    (OUT / "assets" / "favicon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 28 28"><rect width="28" height="28" rx="3" fill="#33312F"/><path d="M7 8.5h6.2c.5 0 .8.3.8.8V20c-.5-.5-1.2-.8-2-.8H7z M21 8.5h-6.2c-.5 0-.8.3-.8.8V20c.5-.5 1.2-.8 2-.8H21z" fill="none" stroke="#BAA58C" stroke-width="1.4" stroke-linejoin="round"/><rect x="7" y="22" width="14" height="1.3" fill="#F4F1EB"/></svg>', encoding="utf-8")
    urls = ["", "products.html", "english.html", "math.html", "univ.html", "major.html", "interview.html", "complete.html", "free.html", "sample.html", "sample/eng.html", "sample/math.html", "sample/univ.html", "info.html", "learn.html", "guide.html", "contact.html", "privacy.html"]
    urls += [f"p/{p['id']}.html" for p in PRODUCTS] + [f"u/{u['slug']}.html" for u in UNIVS] + [f"learn/{a['slug']}.html" for a in ARTICLES]
    sm = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{SITE_URL}/{u}</loc></url>" for u in urls) + "</urlset>"
    (OUT / "sitemap.xml").write_text(sm, encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /plan/\nDisallow: /cart.html\nDisallow: /compare.html\nDisallow: /api/\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")


def build_plan():
    """기획서(/plan) 재생성. pandoc 이 없으면 기존 파일을 유지한다."""
    src = ROOT / "pyunipsam_plan"
    if not shutil.which("pandoc") or not src.exists():
        return
    (OUT / "plan").mkdir(exist_ok=True)
    nav = '<nav><a href="../index.html">홈</a> · <a href="index.html">목차</a> · <a href="p1.html">Part1</a> · <a href="p2.html">Part2</a> · <a href="p3.html">Part3</a></nav>'
    nf = OUT / "plan" / "_nav.html"
    nf.write_text(nav, encoding="utf-8")
    hf = OUT / "plan" / "_head.html"
    hf.write_text('<meta name="robots" content="noindex"><link rel="stylesheet" href="../assets/plan.css">', encoding="utf-8")
    for i, f in enumerate(sorted(src.glob("0*.md")), 1):
        subprocess.run(["pandoc", str(f), "-f", "gfm", "-t", "html5", "-s", "--metadata", f"title=편입샘 기획서 Part {i}", "--metadata", "lang=ko",
                        "-H", str(hf), "-B", str(nf), "-o", str(OUT / "plan" / f"p{i}.html")], check=True, stderr=subprocess.DEVNULL)
    nf.unlink(); hf.unlink()
    (OUT / "plan" / "index.html").write_text('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>편입샘 기획서</title><link rel="stylesheet" href="../assets/plan.css"></head><body><h1>편입샘 사업 기획서</h1><p><a href="../index.html">홈</a></p><ul><li><a href="p1.html">Part 1. 브랜드·시장·경쟁</a></li><li><a href="p2.html">Part 2. 상품·목차·가격</a></li><li><a href="p3.html">Part 3. 제작·홈페이지·블로그·로드맵</a></li></ul></body></html>', encoding="utf-8")


def main():
    OUT.mkdir(exist_ok=True)
    samples = merge_sales()
    assets = ROOT / "tools" / "assets"
    (OUT / "assets").mkdir(exist_ok=True)
    for f in assets.iterdir():
        shutil.copy(f, OUT / "assets" / f.name)
    old = OUT / "style.css"
    if old.exists():
        old.unlink()
    build_data_files()
    build_home(); build_cat_pages(); build_products_page(); build_product_pages(samples)
    build_univ_pages(); build_learn(); build_misc(samples); build_sample_pages(samples); build_plan()
    print(f"products={len(PRODUCTS)} univ={len(UNIVS)} pages={len(list(OUT.rglob('*.html')))}")


if __name__ == "__main__":
    main()
