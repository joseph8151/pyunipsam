"""네이버·검색엔진 최적화(SEO) 데이터.

원칙
- 키워드를 본문에 억지로 반복하지 않는다(네이버는 과도한 반복을 감점하고, 편입샘 블로그 원칙과도 어긋난다).
- 제공하지 않는 것을 검색어로 쓰지 않는다. 예: '기출' — 편입샘은 기출을 복제하지 않으므로 '기출문제집'을 키워드로 쓰지 않는다.
- 판매 중이 아닌 상품에 '구매' 의도를 암시하지 않는다.
"""
import html, json
from catalog_univ import UNIV_BY_SLUG, YEAR

E = html.escape

GENERIC = ["편입 문제집", "편입 PDF 문제집", "편입 해설집", "대학 편입시험", "일반편입", "학사편입", "편입샘"]

# 분류별 대표 검색 구문
PK = {
    "vocab": "편입영어 어휘", "grammar": "편입영어 문법", "reading": "편입영어 독해", "logic": "편입영어 논리",
    "eng_all": "편입영어 모의고사", "eng_tool": "편입영어 학습 도구",
    "base": "편입수학 기초", "calc": "편입수학 미적분", "linear": "편입수학 선형대수", "eng_math": "편입수학 공학수학",
    "math_all": "편입수학 모의고사", "math_tool": "편입수학 학습 도구",
    "major": "편입 전공 필기", "interview": "편입 면접", "docs": "편입 학업계획서·자기소개서",
    "pk_eng": "편입영어 패키지", "pk_math": "편입수학 패키지", "pk_all": "편입 패키지",
}
EXTRA = {
    "vocab": ["편입 영어 단어", "편입영어 어휘 문제집", "편입 영어 어휘"],
    "grammar": ["편입 영어 문법 문제집", "편입영어 문법 오류", "편입 영어 문법"],
    "reading": ["편입 영어 독해 문제집", "편입영어 독해 해설", "편입 영어 독해"],
    "logic": ["편입영어 논리완성", "편입 영어 논리 문제", "편입영어 빈칸"],
    "eng_all": ["편입영어 실전 모의고사", "편입영어 파이널", "편입 영어 모의고사"],
    "eng_tool": ["편입영어 오답노트", "편입 학습 플래너", "편입영어 요약집"],
    "base": ["편입수학 기초수학", "편입수학 입문"],
    "calc": ["편입수학 미분", "편입수학 적분", "편입수학 문제집"],
    "linear": ["편입수학 행렬", "편입수학 고유값", "편입 선형대수"],
    "eng_math": ["편입수학 미분방정식", "편입 공학수학", "편입수학 벡터해석"],
    "math_all": ["편입수학 실전 모의고사", "편입수학 파이널", "편입 수학 모의고사"],
    "math_tool": ["편입수학 공식", "편입수학 오답노트", "편입 학습 플래너"],
    "major": ["편입 전공 시험", "편입 전공기초"],
    "interview": ["편입 면접 질문", "편입 면접 준비", "편입 면접 예상질문"],
    "docs": ["편입 학업계획서", "편입 자기소개서", "편입 서류 준비"],
    "pk_eng": ["편입영어 문제집 세트", "편입영어 30일"], "pk_math": ["편입수학 문제집 세트", "편입수학 30일"],
    "pk_all": ["편입 문제집 세트", "편입 파이널"],
}


def short(u):
    return u["name"].replace("학교", "")


def subj_of(p):
    spec = p.get("spec", "")
    return "영어·수학" if ("영어" in spec and "수학" in spec) else ("수학" if "수학" in spec else "영어")


def pk_of(p):
    if p["cat"] == "univ":
        u = UNIV_BY_SLUG[p["univ"]]
        return f"{short(u)} 편입 {subj_of(p)}"
    return PK.get(p["sub"], "편입 문제집")


def product_keywords(p):
    kw = [p["title"], pk_of(p)]
    if p["cat"] == "univ":
        s = short(UNIV_BY_SLUG[p["univ"]])
        kw += [f"{s} 편입 모의고사", f"{s} 편입 시험", f"{s} 편입 필기시험 {YEAR}", f"{s} 편입 {p.get('track', '')}".strip(), "대학별 편입 모의고사"]
    else:
        kw += EXTRA.get(p["sub"], [])
        kw += [f"편입 {t}" if not t.startswith("편입") else t for t in p["types"][:3]]
    kw += ["편입 PDF 문제집", "편입 해설집", "편입샘"]
    return dedupe(kw)[:16]


def product_title(p):
    return f"{p['title']} | {pk_of(p)} PDF 문제집 · 편입샘" if p["cat"] != "univ" else f"{p['title']} | {pk_of(p)} 모의고사 · 편입샘"


def product_desc(p, meta):
    status = {"coming_soon": "출시 예정", "draft": "기획 중", "sample_ready": "샘플 공개", "on_sale": "판매 중", "discontinued": "판매 종료"}[p["status"]]
    base = p["summary"].rstrip(".")
    return f"{base}. {meta} · PDF 문제집·해설집 · {status}. 편입샘"


def dedupe(items):
    seen, out = set(), []
    for i in items:
        i = i.strip()
        if i and i not in seen:
            seen.add(i); out.append(i)
    return out


PAGE_KW = {
    "index.html": ["편입 문제집", "편입영어 문제집", "편입수학 문제집", "편입 PDF", "편입 모의고사", "대학별 편입 모의고사", "일반편입", "학사편입",
                   "편입 해설집", "편입 독학", "편입 셀프스터디", "편입영어", "편입수학", "편입샘"],
    "products.html": ["편입 문제집 전체", "편입영어 문제집", "편입수학 문제집", "편입 모의고사", "편입 PDF 문제집", "편입샘"],
    "english.html": ["편입영어", "편입영어 문제집", "편입영어 어휘", "편입영어 문법", "편입영어 독해", "편입영어 논리", "편입영어 해설집", "편입영어 독학", "편입영어 모의고사", "편입 영어 PDF"],
    "math.html": ["편입수학", "편입수학 문제집", "편입수학 미적분", "편입수학 선형대수", "편입수학 공학수학", "편입수학 해설집", "편입수학 독학", "편입수학 모의고사", "편입 수학 PDF"],
    "univ.html": ["대학별 편입 모의고사", "편입 모의고사", "대학 편입 시험 형식", "한양대 편입", "중앙대 편입", "건국대 편입", "한국외대 편입", "동국대 편입", "세종대 편입", "홍익대 편입"],
    "major.html": ["편입 전공 필기", "편입 전공 시험", "편입 전공기초", "컴퓨터공학 편입", "경영학 편입", "경제학 편입", "편입 일반화학", "편입 일반물리", "편입 생명과학"],
    "interview.html": ["편입 면접", "편입 면접 질문", "편입 학업계획서", "편입 자기소개서", "편입 서류", "편입 면접 준비"],
    "complete.html": ["편입 패키지", "편입영어 패키지", "편입수학 패키지", "편입 30일 완성", "편입 파이널 패키지", "편입 문제집 세트"],
    "free.html": ["편입 무료 샘플", "편입 문제집 샘플", "편입 해설집 샘플", "편입 오답노트 양식", "편입 샘플 PDF"],
    "sample.html": ["편입 샘플 문제집", "편입 샘플 해설집", "편입영어 샘플", "편입수학 샘플", "편입 모의고사 샘플"],
    "info.html": ["대학별 편입 정보", "편입 모집요강", "편입 시험 과목", "편입 필기시험", "일반편입 학사편입 차이", "편입 공인영어", "편입 면접 여부", f"{YEAR} 편입"],
    "learn.html": ["편입 학습법", "편입 정보", "편입 시험 정보", "일반편입 학사편입 안내"],
    "guide.html": ["편입샘 이용 안내", "편입 PDF 문제집 구매", "편입 해설집", "편입 문제집 환불"],
    "contact.html": ["편입샘 문의", "편입 문제집 문의"], "privacy.html": ["편입샘 개인정보 처리방침"],
}


def page_keywords(path, extra=None):
    kw = list(PAGE_KW.get(path, []))
    if path.startswith("u/"):
        slug = path[2:-5]
        u = UNIV_BY_SLUG.get(slug)
        if u:
            s = short(u)
            kw = [f"{s} 편입", f"{s} 편입 시험", f"{s} 편입 필기시험", f"{s} 편입 모집요강", f"{s} 편입 영어", f"{s} 편입 수학", f"{YEAR} {s} 편입", f"{s} 일반편입", f"{s} 학사편입", f"{s} 편입 모의고사"]
    if path.startswith("learn/"):
        kw = ["편입 학습 정보", "편입 시험 정보"]
    kw += extra or []
    return dedupe(kw + ["편입샘"])[:16]


# ───────────── FAQ (사실만) ─────────────
FAQ_EN = [
    ("편입영어는 어떤 영역으로 나뉘나요?", "대체로 어휘·문법·독해·논리 영역으로 나누어 준비합니다. 다만 대학마다 출제 영역과 문항 수가 다르므로 지원 대학의 모집요강을 먼저 확인해야 합니다. 편입샘 '대학별 편입정보'에 확인된 대학의 시험 형식을 정리해 두었습니다."),
    ("편입영어 문제집은 어떤 순서로 푸는 것이 좋은가요?", "개념과 어휘를 정리한 뒤 영역별 문제집으로 약한 영역을 보강하고, 시험 직전에는 대학 형식에 맞춘 모의고사와 FINAL REVIEW로 점검하는 순서를 권합니다. 영역별 정답률을 기록하면 약한 곳을 찾기 쉽습니다."),
    ("편입샘 해설집은 무엇이 다른가요?", "정답만 알려 주지 않고 본문 번역, 글의 구성, 제목·주제·요지·요약, 문장별 어휘·문법·연결사 분석, 오답 선지가 틀린 이유까지 담는 것을 목표로 설계합니다. 무료 샘플에서 같은 구성을 미리 볼 수 있습니다."),
    ("혼자 공부(독학)해도 되나요?", "셀프스터디를 전제로 해설을 촘촘하게 설계합니다. 다만 개별 질의응답과 첨삭은 제공하지 않으며 합격이나 점수 향상을 보장하지 않습니다."),
]
FAQ_MATH = [
    ("편입수학의 출제 범위는 어떻게 되나요?", "주로 미적분학과 선형대수학이며 대학에 따라 공학수학(미분방정식 등)이 포함될 수 있습니다. 출제 범위는 대학마다 다르므로 모집요강으로 확인하세요."),
    ("편입수학 문제집은 문항 수에 비해 쪽수가 많은 이유가 있나요?", "수학은 풀이가 길어 문항당 해설 분량이 영어보다 큽니다. 편입샘은 정석 풀이와 단축 풀이, 계산 검증, 오답 선지 분석을 함께 담기 위해 문항당 쪽수를 넉넉하게 설계합니다."),
    ("편입수학 정답은 어떻게 검증하나요?", "AI 초안을 독립 계산으로 검증하고 전문가가 정답과 풀이를 확인하는 것을 원칙으로 합니다. 검수를 마치지 않은 문항은 판매하지 않으며, 검수를 마친 상품에만 '검수 완료'를 표시합니다."),
    ("단답형 문항도 준비할 수 있나요?", "단답형 출제 여부는 대학마다 다릅니다. 예를 들어 2026학년도 한양대 자연계 수학은 객관식 20문항과 단답형 5문항으로 안내되었습니다. 단답형 집중 문제집을 별도로 기획하고 있습니다."),
]
FAQ_UNIV = [
    ("대학별 모의고사는 실제 시험과 같은 문제인가요?", "아닙니다. 대학 공식 모집요강으로 확인된 문항 수·시간·형식에 맞춰 편입샘이 새로 만든 독창 문항입니다. 대학 기출문제를 복제하지 않으며 해당 대학과 무관한 비공식 자료입니다."),
    ("모든 대학의 모의고사가 있나요?", "아니요. 모든 대학이 같은 편입시험을 치르지 않으므로 공식 자료로 시험 형식이 확인된 대학부터 기획합니다. 확인하지 못한 대학은 상품이 아닌 정보 페이지로만 제공합니다."),
    ("시험 정보는 얼마나 정확한가요?", "각 대학 정보에 기준 학년도와 마지막 확인일, 확인 수준(공식 문서·공식 공지 일부·2차 자료·미확인)을 표시합니다. 2차 자료 기준 항목은 공식 모집요강과 대조해 확정합니다."),
    ("한양대 자연계는 영어 시험이 있나요?", "2026학년도 한양대 서울캠퍼스 자연계 필기시험은 수학 25문항 70분으로 안내되었고 영어 필기는 폐지되었습니다. 매년 바뀔 수 있으니 지원 시점의 모집요강을 확인하세요."),
]


def faq_section(items, title="자주 묻는 질문"):
    rows = "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in items)
    return f'<section class="w pdsec faq"><h2>{E(title)}</h2>{rows}</section>'


def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def org_ld(site_url):
    return {"@context": "https://schema.org", "@type": "Organization", "name": "편입샘", "url": site_url,
            "logo": site_url + "/assets/favicon.svg", "description": "대학 편입시험 전문 PDF 문제집·해설집 브랜드"}


# ───────────── 관련 검색어(내부 링크) ─────────────
def related_chips(p, R):
    links = []
    sub = p["sub"]
    if p["cat"] == "english":
        links.append((PK.get(sub, "편입영어") + " 문제집", f"english.html#{sub}"))
        links.append(("편입영어 모의고사", "english.html#eng_all"))
    elif p["cat"] == "math":
        links.append((PK.get(sub, "편입수학") + " 문제집", f"math.html#{sub}"))
        links.append(("편입수학 모의고사", "math.html#math_all"))
    elif p["cat"] == "univ":
        u = UNIV_BY_SLUG[p["univ"]]
        links.append((f"{short(u)} 편입 시험 정보", f"u/{u['slug']}.html"))
        links.append(("대학별 편입 모의고사", "univ.html"))
    elif p["cat"] == "complete":
        links.append(("편입 패키지 전체", "complete.html"))
    elif p["cat"] == "major":
        links.append(("편입 전공 필기 안내", "major.html"))
    else:
        links.append(("편입 면접·서류 자료", "interview.html"))
    links += [("대학별 편입정보", "info.html"), ("편입 샘플 문제집·해설집", "sample.html"), ("편입 PDF 문제집 전체", "products.html")]
    chips = "".join(f'<a class="chip" href="{R}{h}">{E(t)}</a>' for t, h in links)
    return f'<section class="w pdsec"><h2>함께 보는 페이지</h2><div class="chips">{chips}</div></section>'
