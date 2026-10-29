"""문제집 표지 시안(SVG 스프라이트) 생성기.

모든 표지는 '디자인 시안'이다. 대학 공식 로고·엠블럼은 사용하지 않고 대학명을 타이포그래피로만 표기한다.
"""
import html
from catalog_products import PRODUCTS, SUBS

W, H = 300, 400
FONT = "'Pretendard Variable',Pretendard,'Apple SD Gothic Neo','Noto Sans KR','Malgun Gothic',sans-serif"
SUB_COLOR = {"vocab": "#6FA8A0", "grammar": "#D08C60", "reading": "#8E9BD6", "logic": "#B58DB6", "eng_all": "#E6DFCB"}
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
    elif p["unit"] in ("구성",):
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


def cover_english(p):
    c = SUB_COLOR.get(p["sub"], "#E6DFCB")
    lines = wrap(clean_title(p), 8)[:4]
    s = f'<rect width="{W}" height="{H}" fill="#16263D"/>'
    s += f'<rect x="0" y="0" width="14" height="{H}" fill="#0C192B"/>'
    s += f'<rect x="14" y="0" width="1" height="{H}" fill="#F8F7F3" opacity=".18"/>'
    s += f'<text x="40" y="52" font-size="11" font-weight="600" fill="#F8F7F3" letter-spacing=".32em" opacity=".85">편입샘</text>'
    s += f'<text x="40" y="70" font-size="8.5" fill="#F8F7F3" letter-spacing=".24em" opacity=".5">TRANSFER ENGLISH</text>'
    s += f'<rect x="40" y="104" width="26" height="3" fill="{c}"/>'
    s += text_block(lines, 40, 150, 31, 40, "#F8F7F3")
    s += f'<text x="40" y="296" font-size="9" font-weight="600" fill="{c}" letter-spacing=".2em">{SUB_EN.get(p["sub"], "")}</text>'
    if p.get("series"):
        s += f'<text x="40" y="314" font-size="10" fill="#F8F7F3" opacity=".7">{html.escape(p["series"])} SERIES</text>'
    s += f'<line x1="40" y1="346" x2="270" y2="346" stroke="#F8F7F3" stroke-opacity=".22"/>'
    s += f'<text x="40" y="368" font-size="11" fill="#F8F7F3" opacity=".78">{html.escape(info_line(p))}</text>'
    return s


def cover_math(p):
    lines = wrap(clean_title(p), 8)[:4]
    s = f'<rect width="{W}" height="{H}" fill="url(#mg)"/>'
    # 미세한 수학적 그래픽: 격자, 축, 곡선, 적분 기호
    for i in range(1, 8):
        s += f'<line x1="{i*38}" y1="0" x2="{i*38}" y2="{H}" stroke="#9FB3CC" stroke-opacity=".07"/>'
    for i in range(1, 11):
        s += f'<line x1="0" y1="{i*38}" x2="{W}" y2="{i*38}" stroke="#9FB3CC" stroke-opacity=".07"/>'
    s += '<path d="M0 300 C60 300 80 180 150 200 S 240 330 300 250" fill="none" stroke="#9FB3CC" stroke-opacity=".35" stroke-width="1.4"/>'
    s += '<path d="M0 330 C70 330 110 250 170 262 S 250 340 300 300" fill="none" stroke="#7B93B5" stroke-opacity=".25" stroke-width="1"/>'
    s += f'<text x="250" y="140" font-size="120" fill="#9FB3CC" fill-opacity=".09" font-weight="300">∫</text>'
    s += f'<text x="34" y="52" font-size="11" font-weight="600" fill="#E2E8F0" letter-spacing=".32em">편입샘</text>'
    s += f'<text x="34" y="70" font-size="8.5" fill="#CBD5E1" letter-spacing=".24em" opacity=".6">TRANSFER MATHEMATICS</text>'
    s += '<rect x="34" y="104" width="26" height="2" fill="#9FB3CC"/>'
    s += text_block(lines, 34, 150, 31, 40, "#F1F5F9")
    s += f'<text x="34" y="300" font-size="9" font-weight="600" fill="#9FB3CC" letter-spacing=".2em">{SUB_EN.get(p["sub"], "")}</text>'
    if p.get("series"):
        s += f'<text x="34" y="318" font-size="10" fill="#CBD5E1" opacity=".7">{html.escape(p["series"])} SERIES</text>'
    s += '<line x1="34" y1="346" x2="266" y2="346" stroke="#CBD5E1" stroke-opacity=".25"/>'
    s += f'<text x="34" y="368" font-size="11" fill="#CBD5E1" opacity=".85">{html.escape(info_line(p))}</text>'
    return s


def cover_univ(p):
    from catalog_univ import UNIV_BY_SLUG
    u = UNIV_BY_SLUG[p["univ"]]["name"]
    short = u.replace("학교", "")
    track = p.get("track", "")
    subj = p["title"].replace(u, "").strip()
    s = f'<rect width="{W}" height="{H}" fill="#F3EEE2"/>'
    s += f'<rect x="14" y="14" width="{W-28}" height="{H-28}" fill="none" stroke="#16263D" stroke-opacity=".55"/>'
    s += f'<rect x="19" y="19" width="{W-38}" height="{H-38}" fill="none" stroke="#16263D" stroke-opacity=".18"/>'
    s += '<text x="40" y="58" font-size="11" font-weight="600" fill="#16263D" letter-spacing=".32em">편입샘</text>'
    s += f'<text x="260" y="58" font-size="10" font-weight="700" fill="#16263D" letter-spacing=".18em" text-anchor="end">{html.escape(p.get("series") or "SERIES")}</text>'
    s += '<line x1="40" y1="74" x2="260" y2="74" stroke="#16263D" stroke-opacity=".3"/>'
    s += text_block(wrap(short, 5)[:3], 40, 150, 46, 54, "#16263D", ls="-0.05em")
    s += f'<text x="40" y="262" font-size="15" font-weight="600" fill="#16263D">{html.escape(subj)}</text>'
    s += f'<text x="40" y="284" font-size="10" fill="#16263D" opacity=".6" letter-spacing=".08em">{html.escape(track)} · {html.escape(p.get("spec", ""))[:26]}</text>'
    s += '<line x1="40" y1="338" x2="260" y2="338" stroke="#16263D" stroke-opacity=".3"/>'
    s += f'<text x="40" y="362" font-size="11" fill="#16263D" opacity=".8">{html.escape(info_line(p))}</text>'
    return s


def cover_major(p):
    lines = wrap(p["title"], 8)[:4]
    s = f'<rect width="{W}" height="{H}" fill="#2B2D31"/>'
    s += f'<rect x="0" y="0" width="{W}" height="6" fill="#B7AEA0" opacity=".6"/>'
    for i in range(0, 12):
        s += f'<line x1="40" y1="{250+i*6}" x2="{260-i*10}" y2="{250+i*6}" stroke="#CFC8BD" stroke-opacity=".07"/>'
    s += '<text x="40" y="52" font-size="11" font-weight="600" fill="#E8E2D8" letter-spacing=".32em">편입샘</text>'
    s += '<text x="40" y="70" font-size="8.5" fill="#CFC8BD" letter-spacing=".24em" opacity=".6">MAJOR EXAM SERIES</text>'
    s += '<rect x="40" y="104" width="26" height="2" fill="#B7AEA0"/>'
    s += text_block(lines, 40, 150, 30, 40, "#EEE9DF")
    s += '<line x1="40" y1="346" x2="260" y2="346" stroke="#CFC8BD" stroke-opacity=".25"/>'
    s += f'<text x="40" y="368" font-size="11" fill="#CFC8BD" opacity=".85">{html.escape(info_line(p))}</text>'
    return s


def cover_interview(p):
    lines = wrap(p["title"].replace("편입 ", ""), 8)[:4]
    s = f'<rect width="{W}" height="{H}" fill="#E9E4D9"/>'
    s += f'<rect x="0" y="0" width="{W}" height="{H}" fill="none" stroke="#16263D" stroke-opacity=".12"/>'
    s += f'<circle cx="250" cy="90" r="84" fill="none" stroke="#16263D" stroke-opacity=".08"/><circle cx="250" cy="90" r="56" fill="none" stroke="#16263D" stroke-opacity=".08"/>'
    s += '<text x="36" y="52" font-size="11" font-weight="600" fill="#16263D" letter-spacing=".32em">편입샘</text>'
    s += '<text x="36" y="70" font-size="8.5" fill="#16263D" letter-spacing=".24em" opacity=".55">INTERVIEW &amp; DOCUMENTS</text>'
    s += '<rect x="36" y="104" width="26" height="2" fill="#16263D"/>'
    s += text_block(lines, 36, 150, 30, 40, "#16263D")
    s += '<line x1="36" y1="346" x2="264" y2="346" stroke="#16263D" stroke-opacity=".25"/>'
    s += f'<text x="36" y="368" font-size="11" fill="#16263D" opacity=".8">{html.escape(info_line(p))}</text>'
    return s


def cover_complete(p):
    G = "#C9B27C"
    lines = wrap(p["title"].replace("편입영어 ", "").replace("편입수학 ", ""), 12)[:4]
    kind = "ENGLISH" if "pk_eng" == p["sub"] else "MATHEMATICS" if "pk_math" == p["sub"] else "ALL IN ONE"
    s = f'<rect width="{W}" height="{H}" fill="#0C192B"/>'
    s += f'<rect x="12" y="12" width="{W-24}" height="{H-24}" fill="none" stroke="{G}" stroke-width="1.2"/>'
    s += f'<rect x="18" y="18" width="{W-36}" height="{H-36}" fill="none" stroke="{G}" stroke-opacity=".35"/>'
    s += f'<text x="150" y="62" font-size="11" font-weight="600" fill="{G}" letter-spacing=".4em" text-anchor="middle">편입샘</text>'
    s += f'<text x="150" y="82" font-size="8.5" fill="{G}" letter-spacing=".3em" text-anchor="middle" opacity=".7">COMPLETE COLLECTION</text>'
    s += f'<line x1="120" y1="102" x2="180" y2="102" stroke="{G}"/>'
    pre = p["title"].split(" ")[0] if p["title"].startswith("편입") else ""
    if pre:
        s += f'<text x="150" y="132" font-size="12" fill="#F8F7F3" opacity=".7" text-anchor="middle" letter-spacing=".1em">{html.escape(pre)}</text>'
    s += text_block(wrap(p["title"].replace("편입영어 ", "").replace("편입수학 ", ""), 11)[:4], 150, 178, 26, 36, "#F4EFE2", ls="-0.02em", anchor="middle")
    s += f'<text x="150" y="304" font-size="9" fill="{G}" letter-spacing=".3em" text-anchor="middle">{kind}</text>'
    s += f'<line x1="40" y1="340" x2="260" y2="340" stroke="{G}" stroke-opacity=".4"/>'
    s += f'<text x="150" y="364" font-size="11" fill="#F4EFE2" opacity=".85" text-anchor="middle">{html.escape(info_line(p))}</text>'
    return s


MAKERS = {"english": cover_english, "math": cover_math, "univ": cover_univ, "major": cover_major,
          "interview": cover_interview, "complete": cover_complete}


def sprite_file():
    syms = []
    for p in PRODUCTS:
        body = MAKERS[p["cat"]](p)
        syms.append(f'<symbol id="c-{p["id"]}" viewBox="0 0 {W} {H}"><g font-family="{FONT}">{body}</g></symbol>')
    defs = '<defs><linearGradient id="mg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1F2937"/><stop offset="1" stop-color="#2E3F57"/></linearGradient></defs>'
    return ('<svg xmlns="http://www.w3.org/2000/svg">' + defs + "".join(syms) + "</svg>")
