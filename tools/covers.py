"""문제집 표지 시안(SVG 스프라이트) 생성기 — 차콜 × 웜 아이보리 × 샌드 베이지.

모든 표지는 '디자인 시안'이다. 대학 공식 로고·엠블럼은 사용하지 않고 대학명을 타이포그래피로만 표기한다.
컬렉션 구분은 보조 색상과 타이포그래피로 한다(블루 계열 미사용).
"""
import html
from catalog_products import PRODUCTS

W, H = 300, 400
FONT = "'Pretendard Variable',Pretendard,'Apple SD Gothic Neo','Noto Sans KR','Malgun Gothic',sans-serif"

CH, CHD, IV, SAND = "#33312F", "#242321", "#F4F1EB", "#BAA58C"
# 편입영어 영역별 보조 색상 (채도를 낮춘 웜 톤)
SUB_COLOR = {"vocab": "#9DAA8F", "grammar": "#C9967A", "reading": "#B59A9A", "logic": "#A8A27A", "eng_all": SAND}
SUB_EN = {"vocab": "VOCABULARY", "grammar": "GRAMMAR", "reading": "READING", "logic": "LOGIC", "eng_all": "COMPLETE &amp; MOCK",
          "base": "FOUNDATION", "calc": "CALCULUS", "linear": "LINEAR ALGEBRA", "eng_math": "ENGINEERING MATH", "math_all": "COMPLETE &amp; MOCK"}


def wrap(text, n):
    """한글 기준 줄바꿈 (공백 우선, 한 줄 최대 n자)."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) <= n:
            cur = f"{cur} {w}".strip()
        else:
            if cur:
                lines.append(cur)
            while len(w) > n:
                lines.append(w[:n]); w = w[n:]
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(lines, x, y, size, lh, fill, weight=700, ls="-0.04em", anchor="start"):
    out = [f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" letter-spacing="{ls}" text-anchor="{anchor}">']
    for i, l in enumerate(lines):
        out.append(f'<tspan x="{x}" dy="{0 if i == 0 else lh}">{html.escape(l)}</tspan>')
    out.append("</text>")
    return "".join(out)


def info_line(p):
    bits = [p["diff"]]
    if p["unit"] == "회":
        bits.append(f'{p["q"]}회')
    elif p["unit"] == "권":
        bits.append(f'{p["q"]}권 구성')
    elif p["unit"] == "구성":
        pass
    else:
        bits.append(f'{p["q"]:,}{p["unit"]}')
    if p.get("pages"):
        bits.append(f'약 {p["pages"]}쪽')
    return " · ".join(bits)


def clean_title(p):
    t = p["title"]
    for pre in ("편입영어 ", "편입수학 "):
        if t.startswith(pre) and p["cat"] in ("english", "math"):
            return t[len(pre):]
    return t


def brand(x, y, fill, sub, subfill, anchor="start"):
    s = f'<text x="{x}" y="{y}" font-size="11" font-weight="600" fill="{fill}" letter-spacing=".32em" text-anchor="{anchor}">편입샘</text>'
    s += f'<text x="{x}" y="{y+18}" font-size="8.5" fill="{subfill}" letter-spacing=".24em" text-anchor="{anchor}" opacity=".7">{sub}</text>'
    return s


def cover_english(p):
    c = SUB_COLOR.get(p["sub"], SAND)
    lines = wrap(clean_title(p), 8)[:4]
    s = f'<rect width="{W}" height="{H}" fill="{CH}"/>'
    s += f'<rect x="0" y="0" width="14" height="{H}" fill="{CHD}"/><rect x="14" y="0" width="1" height="{H}" fill="{IV}" opacity=".16"/>'
    s += brand(40, 52, IV, "TRANSFER ENGLISH", SAND)
    s += f'<rect x="40" y="104" width="28" height="3" fill="{c}"/>'
    s += text_block(lines, 40, 150, 31, 40, IV)
    s += f'<text x="40" y="296" font-size="9" font-weight="600" fill="{c}" letter-spacing=".2em">{SUB_EN.get(p["sub"], "")}</text>'
    if p.get("series"):
        s += f'<text x="40" y="314" font-size="10" fill="{IV}" opacity=".62">{html.escape(p["series"])} SERIES</text>'
    s += f'<line x1="40" y1="346" x2="270" y2="346" stroke="{IV}" stroke-opacity=".2"/>'
    s += f'<text x="40" y="368" font-size="11" fill="{IV}" opacity=".74">{html.escape(info_line(p))}</text>'
    return s


def cover_math(p):
    lines = wrap(clean_title(p), 9)[:4]
    s = f'<rect width="{W}" height="{H}" fill="url(#mg)"/>'
    for i in range(1, 8):
        s += f'<line x1="{i*38}" y1="0" x2="{i*38}" y2="{H}" stroke="{SAND}" stroke-opacity=".07"/>'
    for i in range(1, 11):
        s += f'<line x1="0" y1="{i*38}" x2="{W}" y2="{i*38}" stroke="{SAND}" stroke-opacity=".07"/>'
    s += f'<path d="M0 300 C60 300 80 180 150 200 S 240 330 300 250" fill="none" stroke="{SAND}" stroke-opacity=".45" stroke-width="1.3"/>'
    s += f'<path d="M0 330 C70 330 110 250 170 262 S 250 340 300 300" fill="none" stroke="{IV}" stroke-opacity=".16" stroke-width="1"/>'
    s += f'<text x="236" y="146" font-size="120" fill="{SAND}" fill-opacity=".10" font-weight="300">∫</text>'
    s += f'<rect x="{W-6}" y="0" width="6" height="{H}" fill="{SAND}" opacity=".55"/>'
    s += brand(34, 52, IV, "TRANSFER MATHEMATICS", SAND)
    s += f'<rect x="34" y="104" width="28" height="1.5" fill="{SAND}"/>'
    s += text_block(lines, 34, 150, 30, 40, IV, weight=500, ls="-0.03em")
    s += f'<text x="34" y="300" font-size="9" font-weight="500" fill="{SAND}" letter-spacing=".2em">{SUB_EN.get(p["sub"], "")}</text>'
    if p.get("series"):
        s += f'<text x="34" y="318" font-size="10" fill="{IV}" opacity=".6">{html.escape(p["series"])} SERIES</text>'
    s += f'<line x1="34" y1="346" x2="264" y2="346" stroke="{IV}" stroke-opacity=".2"/>'
    s += f'<text x="34" y="368" font-size="11" fill="{IV}" opacity=".78">{html.escape(info_line(p))}</text>'
    return s


def cover_univ(p):
    from catalog_univ import UNIV_BY_SLUG
    u = UNIV_BY_SLUG[p["univ"]]["name"]
    short = u.replace("학교", "")
    track = p.get("track", "")
    subj = p["title"].replace(u, "").strip()
    s = f'<rect width="{W}" height="{H}" fill="{IV}"/>'
    s += f'<rect x="14" y="14" width="{W-28}" height="{H-28}" fill="none" stroke="{CH}" stroke-opacity=".55"/>'
    s += f'<rect x="19" y="19" width="{W-38}" height="{H-38}" fill="none" stroke="{SAND}" stroke-opacity=".9"/>'
    s += f'<text x="40" y="58" font-size="11" font-weight="600" fill="{CH}" letter-spacing=".32em">편입샘</text>'
    s += f'<text x="260" y="58" font-size="10" font-weight="700" fill="{CH}" letter-spacing=".18em" text-anchor="end">{html.escape(p.get("series") or "SERIES")}</text>'
    s += f'<line x1="40" y1="74" x2="260" y2="74" stroke="{CH}" stroke-opacity=".3"/>'
    s += text_block(wrap(short, 5)[:3], 40, 150, 46, 54, CHD, ls="-0.05em", weight=800)
    s += f'<rect x="40" y="232" width="28" height="3" fill="{SAND}"/>'
    s += f'<text x="40" y="266" font-size="15" font-weight="600" fill="{CHD}">{html.escape(subj)}</text>'
    s += f'<text x="40" y="286" font-size="10" fill="{CH}" opacity=".6" letter-spacing=".06em">{html.escape(track)} · {html.escape(p.get("spec", ""))[:26]}</text>'
    s += f'<line x1="40" y1="338" x2="260" y2="338" stroke="{CH}" stroke-opacity=".3"/>'
    s += f'<text x="40" y="362" font-size="11" fill="{CH}" opacity=".8">{html.escape(info_line(p))}</text>'
    return s


def cover_major(p):
    lines = wrap(p["title"], 8)[:4]
    s = f'<rect width="{W}" height="{H}" fill="#4A4744"/>'
    s += f'<rect x="0" y="0" width="{W}" height="6" fill="#8F877D"/>'
    for i in range(0, 12):
        s += f'<line x1="40" y1="{250+i*6}" x2="{260-i*10}" y2="{250+i*6}" stroke="{IV}" stroke-opacity=".07"/>'
    s += brand(40, 52, IV, "MAJOR EXAM SERIES", "#CFC8BD")
    s += '<rect x="40" y="104" width="28" height="2" fill="#B7AEA0"/>'
    s += text_block(lines, 40, 150, 30, 40, IV)
    s += f'<line x1="40" y1="346" x2="260" y2="346" stroke="{IV}" stroke-opacity=".22"/>'
    s += f'<text x="40" y="368" font-size="11" fill="#E4DFD6" opacity=".85">{html.escape(info_line(p))}</text>'
    return s


def cover_interview(p):
    lines = wrap(p["title"].replace("편입 ", ""), 8)[:4]
    s = f'<rect width="{W}" height="{H}" fill="{SAND}"/>'
    s += f'<circle cx="250" cy="90" r="84" fill="none" stroke="{CHD}" stroke-opacity=".10"/><circle cx="250" cy="90" r="56" fill="none" stroke="{CHD}" stroke-opacity=".10"/>'
    s += brand(36, 52, CHD, "INTERVIEW &amp; DOCUMENTS", CHD)
    s += f'<rect x="36" y="104" width="28" height="2" fill="{CHD}"/>'
    s += text_block(lines, 36, 150, 30, 40, CHD)
    s += f'<line x1="36" y1="346" x2="264" y2="346" stroke="{CHD}" stroke-opacity=".3"/>'
    s += f'<text x="36" y="368" font-size="11" fill="{CHD}" opacity=".85">{html.escape(info_line(p))}</text>'
    return s


def cover_complete(p):
    G = SAND
    title = p["title"].replace("편입영어 ", "").replace("편입수학 ", "")
    pre = "편입영어" if p["title"].startswith("편입영어") else "편입수학" if p["title"].startswith("편입수학") else ""
    kind = "ENGLISH" if p["sub"] == "pk_eng" else "MATHEMATICS" if p["sub"] == "pk_math" else "ALL IN ONE"
    s = f'<rect width="{W}" height="{H}" fill="{CHD}"/>'
    s += f'<rect x="12" y="12" width="{W-24}" height="{H-24}" fill="none" stroke="{G}" stroke-width="1.2"/>'
    s += f'<rect x="18" y="18" width="{W-36}" height="{H-36}" fill="none" stroke="{G}" stroke-opacity=".35"/>'
    s += f'<text x="150" y="62" font-size="11" font-weight="600" fill="{G}" letter-spacing=".4em" text-anchor="middle">편입샘</text>'
    s += f'<text x="150" y="82" font-size="8.5" fill="{G}" letter-spacing=".3em" text-anchor="middle" opacity=".7">COMPLETE COLLECTION</text>'
    s += f'<line x1="120" y1="102" x2="180" y2="102" stroke="{G}"/>'
    if pre:
        s += f'<text x="150" y="132" font-size="12" fill="{IV}" opacity=".7" text-anchor="middle" letter-spacing=".1em">{pre}</text>'
    s += text_block(wrap(title, 11)[:4], 150, 178, 26, 36, IV, ls="-0.02em", anchor="middle")
    s += f'<text x="150" y="304" font-size="9" fill="{G}" letter-spacing=".3em" text-anchor="middle">{kind}</text>'
    s += f'<line x1="40" y1="340" x2="260" y2="340" stroke="{G}" stroke-opacity=".4"/>'
    s += f'<text x="150" y="364" font-size="11" fill="{IV}" opacity=".85" text-anchor="middle">{html.escape(info_line(p))}</text>'
    return s


MAKERS = {"english": cover_english, "math": cover_math, "univ": cover_univ, "major": cover_major,
          "interview": cover_interview, "complete": cover_complete}


def sprite_file():
    syms = []
    for p in PRODUCTS:
        body = MAKERS[p["cat"]](p)
        syms.append(f'<symbol id="c-{p["id"]}" viewBox="0 0 {W} {H}"><g font-family="{FONT}">{body}</g></symbol>')
    defs = ('<defs><linearGradient id="mg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2A2927"/>'
            '<stop offset="1" stop-color="#3D3A36"/></linearGradient></defs>')
    return '<svg xmlns="http://www.w3.org/2000/svg">' + defs + "".join(syms) + "</svg>"
