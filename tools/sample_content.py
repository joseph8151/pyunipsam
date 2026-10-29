"""샘플 문제·해설 (편입샘 해설집 구조 시연용).

- 지문·문항·해설은 모두 편입샘이 새로 쓴 독창 내용이다(타 교재·기출 복제 아님).
- 아직 전문가 검수 전인 '제작 방식 시연용 샘플'이다. 화면과 PDF에 그 사실을 명시한다.
태그: 어휘(v) / 문법(g) / 연결사(c) / 빈칸(b)
"""
import html

E = html.escape

QNO = "Q.01"
QTYPE = "다음 빈칸에 들어갈 말로 가장 적절한 것은?"
TIME_GUIDE = "권장 풀이 시간 1분 30초 (설계 기준)"

CHOICES = [
    "decorations that make a city more attractive to tourists",
    "infrastructure that quietly supports public health",
    "obstacles to the efficient use of urban land",
    "private amenities reserved for wealthy neighborhoods",
    "temporary solutions to long-term medical problems",
]
ANSWER = 2

# (영문 문장 조각 리스트, 번역, 분석 노트 리스트)
# 조각: str 또는 (텍스트, 태그문자열) — 태그는 'v','g','c','b' 조합
SENTENCES = [
    ([("Many cities have ", ""), ("invested", "v"), (" in public parks on the ", ""), ("assumption", "v"), (" ", ""), ("that", "g"),
      (" green space is simply a pleasant extra.", "")],
     "많은 도시들이 녹지는 단지 기분 좋은 덤일 뿐이라는 가정 아래 공원에 투자해 왔다.",
     ["invest in ~ : ~에 투자하다 / assumption : 가정, 추정",
      "that : 동격 접속사 — assumption의 내용을 이끌며 뒤에 완전한 절(green space is ...)이 온다"]),
    ([("", ""), ("However", "c"), (", researchers who ", ""), ("track", "v"), (" residents over several years report a more concrete benefit.", "")],
     "그러나 몇 해에 걸쳐 주민들을 추적 조사하는 연구자들은 보다 구체적인 이점을 보고한다.",
     ["However : 앞 문장의 통념(공원 = 덤)과 대조 → 글의 방향이 '구체적 이점'으로 전환",
      "who : 주격 관계대명사, 선행사 researchers가 복수이므로 동사는 track(수일치)"]),
    ([("People who live within a short walk of a park ", ""), ("tend to", "v"), (" exercise more often, and they also ", ""),
      ("recover from", "v"), (" everyday stress more quickly.", "")],
     "공원에서 걸어서 가까운 거리에 사는 사람들은 더 자주 운동하는 경향이 있고, 일상적인 스트레스에서도 더 빨리 회복한다.",
     ["tend to ~ : ~하는 경향이 있다 / recover from ~ : ~에서 회복하다",
      "more often, more quickly : 비교급 — 비교 대상은 '공원 근처에 살지 않는 사람들'(생략)"]),
    ([("This does not mean ", ""), ("that", "g"), (" a park, ", ""), ("by itself", "v"), (", cures anything.", "")],
     "이것이 공원 자체만으로 무엇이든 치료한다는 뜻은 아니다.",
     ["mean that + 절 : ~라는 것을 의미하다 / by itself : 그 자체만으로",
      "과잉 해석 차단 문장 — 공원이 '치료'한다는 선택지(⑤의 solutions)는 이 문장과 충돌한다"]),
    ([("", ""), ("Rather", "c"), (", it ", ""), ("lowers", "v"), (" the effort ", ""), ("required", "g"), (" to build healthy habits, because a place to walk is already available ",
      ""), ("at no cost", "v"), (".", "")],
     "오히려 공원은 건강한 습관을 만드는 데 필요한 노력을 줄여 주는데, 걸을 수 있는 장소가 이미 무료로 이용 가능하기 때문이다.",
     ["Rather : 앞의 부정(치료하지 않는다)을 받아 올바른 설명을 제시 / at no cost : 무료로",
      "required : 과거분사의 후치 수식 — the effort (which is) required ... / because : 이유절"]),
    ([("", ""), ("Seen", "g"), (" this way, public parks are best understood ", ""), ("not as ", ""), ("luxuries", "v"), (" but as ", ""), ("________", "b"), (".", "")],
     "이렇게 보면, 공공 공원은 사치품이 아니라 ________로 이해하는 것이 가장 적절하다.",
     ["Seen this way : 분사구문(수동) = When they are seen this way / luxury : 사치(품)",
      "not A but B : 빈칸 B는 luxuries(사치)와 대조되는 개념 → 앞 문장들의 '비용을 낮추는 공통 기반'과 연결"]),
]

STRUCTURE = [
    ("서론", "도시들이 공원을 단순한 덤으로 여겨 투자해 왔다는 통념을 제시한다."),
    ("본론", "그러나 연구에 따르면 공원 근처 거주자는 운동량이 많고 스트레스 회복이 빠르다. 다만 공원이 직접 치료하는 것은 아니며, 건강한 습관을 만드는 데 드는 노력을 낮추는 것이다."),
    ("결론", "따라서 공원은 사치가 아니라 공공 건강을 뒷받침하는 기반시설로 이해해야 한다."),
]

META = [
    ("제목", "Public Parks as Quiet Health Infrastructure", "공공 공원, 조용한 건강 기반시설"),
    ("주제", "The practical health role of public green space", "공공 녹지의 실질적인 건강 기능"),
    ("요지", "Public parks matter not as luxuries but because they make healthy habits easier for everyone.",
     "공원은 사치품이 아니라, 누구에게나 건강한 습관을 쉽게 만들어 주기 때문에 중요하다."),
    ("요약", "The passage argues that parks do not cure illness directly but lower the cost of healthy behavior, so they should be seen as public health infrastructure.",
     "이 글은 공원이 질병을 직접 치료하지는 않지만 건강한 행동의 비용을 낮추므로 공공 보건 기반시설로 보아야 한다고 주장한다."),
]

ANALYSIS = [
    ("논리 구조", "통념(공원 = 덤) → However 반전(구체적 이점) → 한정(직접 치료는 아님) → Rather 원리(진입 비용 감소) → 결론(not 사치 but 기반시설)"),
    ("핵심 단서", "빈칸 문장의 not A but B 대조 구문 + 앞 문장의 'lowers the effort', 'at no cost' → 사회가 공통으로 제공하는 기반"),
]

# 선택지별 오답 분석 (번호는 1부터)
CHOICE_NOTES = [
    ("①", "관광객 유치용 장식", "✕", "관광 효과는 지문에 없고 'not luxuries'와 정면으로 충돌한다. 장식(decorations) = 사치의 다른 표현."),
    ("②", "건강을 조용히 뒷받침하는 기반시설", "○", "lowers the effort / no cost / 건강한 습관 → 공공 건강을 떠받치는 기반이라는 뜻으로 수렴한다. 정답."),
    ("③", "도시 토지 효율을 해치는 장애물", "✕", "토지 이용 효율은 논의된 적이 없다. 긍정적 이점을 말하는 글의 방향과도 반대."),
    ("④", "부유한 동네 전용 사설 편의시설", "✕", "지문은 public parks, 무료(at no cost)를 말한다. 'private', 'wealthy'는 근거 없는 반대 방향."),
    ("⑤", "장기 질환에 대한 임시 해결책", "✕", "S4가 '치료'를 부정했다. 'solutions'와 'temporary'는 모두 지문에 없는 과잉 해석 — 오답 원인 태그: 근거 없는 선택."),
]

TAGS = {"v": ("어휘", "tg-v"), "g": ("문법", "tg-g"), "c": ("연결사", "tg-c"), "b": ("빈칸", "tg-b")}
CIRC = "①②③④⑤"


def frag(parts):
    out = []
    for text, tag in parts:
        t = E(text)
        if tag:
            tg = "".join(f'<sup class="tg {TAGS[k][1]}">[{TAGS[k][0]}]</sup>' for k in tag)
            t = f"<b>{t}</b>{tg}"
        out.append(t)
    return "".join(out)


def passage_plain():
    return "".join("".join(t for t, _ in parts) for parts, _, _ in SENTENCES).replace("  ", " ")


def passage_text():
    """문제 페이지용 본문(빈칸 포함)."""
    texts = []
    for parts, _, _ in SENTENCES:
        texts.append("".join(t for t, _ in parts).strip())
    return " ".join(texts)


def problem_sheet():
    ch = "".join(f'<li><span class="cn">{CIRC[i]}</span>{E(c)}</li>' for i, c in enumerate(CHOICES))
    return f"""<section class="sheet" aria-label="문제 페이지 샘플">
<div class="sx-hd"><span class="sx-n">{QNO}</span><h3>{QTYPE}</h3><span class="sx-m">{TIME_GUIDE}</span></div>
<div class="sx-box">{E(passage_text())}</div>
<ol class="sx-ch">{ch}</ol>
<div class="sx-ft"><span>편입샘 · 편입영어 빈칸 추론</span><span>샘플 · 전문가 검수 전 시안</span></div></section>"""


def solution_sheets():
    meta = "".join(f'<div class="sx-r"><h4>{E(k)}</h4><p class="en">{E(en)}</p><p class="ko">{E(ko)}</p></div>' for k, en, ko in META)
    struct = "".join(f'<div class="sx-r"><h4>{E(k)}</h4><p class="ko">{E(v)}</p></div>' for k, v in STRUCTURE)
    trans = " ".join(ko for _, ko, _ in SENTENCES)
    ana = "".join(f'<p class="sx-hl"><b>{E(k)}:</b> {E(v)}</p>' for k, v in ANALYSIS)
    sheet1 = f"""<section class="sheet" aria-label="해설 페이지 샘플 1">
<div class="sx-hd"><span class="sx-n sol">해설</span><h3>{QNO} 본문·구성·핵심 정리</h3><span class="sx-m">정답 ② · 빈칸 추론</span></div>
<div class="sx-sec"><h4>■ 본문 번역</h4><p class="ko">{E(trans.replace('________', '(빈칸)'))}</p></div>
<div class="sx-sec"><h4>■ 글의 구성</h4>{struct}</div>
{''.join(f'<div class="sx-sec"><h4>■ {E(k)}</h4><p class="en">{E(en)}</p><p class="ko">{E(ko)}</p></div>' for k, en, ko in META)}
<div class="sx-sec accent"><h4>[지문 분석 요약]</h4>{ana}</div>
<div class="sx-ft"><span>편입샘 · 해설집</span><span>샘플 · 전문가 검수 전 시안</span></div></section>"""
    sents = ""
    for i, (parts, ko, notes) in enumerate(SENTENCES, 1):
        nt = "".join(f"<li>{E(n)}</li>" for n in notes)
        sents += f'<div class="sx-s"><span class="sn">S{i}</span><p class="en">{frag(parts)}</p><p class="ko">{E(ko)}</p><ul class="nt">{nt}</ul></div>'
    cn = "".join(f'<tr><th>{n}</th><td>{E(t)}</td><td class="{"ok" if m == "○" else "no"}">{m}</td><td>{E(d)}</td></tr>' for n, t, m, d in CHOICE_NOTES)
    sheet2 = f"""<section class="sheet" aria-label="해설 페이지 샘플 2">
<div class="sx-hd"><span class="sx-n sol">해설</span><h3>{QNO} 문장별 분석·선택지 해부</h3><span class="sx-m">태그: 어휘 · 문법 · 연결사 · 빈칸</span></div>
<div class="sx-sents">{sents}</div>
<div class="sx-sec"><h4>■ 선택지 해부</h4><div class="tw"><table class="sx-tb"><thead><tr><th>번호</th><th>선택지(요지)</th><th>정오</th><th>근거</th></tr></thead><tbody>{cn}</tbody></table></div></div>
<div class="sx-ft"><span>편입샘 · 해설집</span><span>샘플 · 전문가 검수 전 시안</span></div></section>"""
    return sheet1 + sheet2


def weapon_snippet():
    """메인 페이지용 해설 미리보기(S4~S5)."""
    s = ""
    for i in (3, 4):
        parts, ko, notes = SENTENCES[i]
        s += f'<div class="sx-s"><span class="sn">S{i+1}</span><p class="en">{frag(parts)}</p><p class="ko">{E(ko)}</p></div>'
    return s


# ═════════════ 수학·대학별 샘플 (독창 문항, 정답은 직접 계산으로 검증) ═════════════
# 문항 필드: no, kind(객관식/단답형), unit(단원), stem(HTML), choices(list|None), ans(str), intent, std(list), fast, verify,
#           notes(list[(번호/라벨, 설명)]), tag(오답 원인 태그), time

MATH_ITEMS = [
    dict(no="Q.01", kind="객관식", unit="미분법 · 곱의 미분과 합성함수", time="1분 30초",
         stem="함수 f(x) = x<sup>2</sup>e<sup>3x</sup> 에 대하여 f′(1)의 값은?",
         choices=["e<sup>3</sup>", "2e<sup>3</sup>", "3e<sup>3</sup>", "5e<sup>3</sup>", "6e<sup>3</sup>"], ans="④",
         intent="곱의 미분법과 합성함수의 미분(연쇄법칙)을 동시에 적용하는지 확인한다.",
         std=["곱의 미분: f′(x) = (x²)′·e<sup>3x</sup> + x²·(e<sup>3x</sup>)′",
              "(e<sup>3x</sup>)′ = 3e<sup>3x</sup> (연쇄법칙) 이므로 f′(x) = 2x·e<sup>3x</sup> + 3x²·e<sup>3x</sup> = e<sup>3x</sup>(2x + 3x²)",
              "x = 1 대입: f′(1) = e<sup>3</sup>(2 + 3) = 5e<sup>3</sup>"],
         fast="로그미분: ln f = 2 ln x + 3x → f′/f = 2/x + 3 → f′(1) = f(1)·(2+3) = e<sup>3</sup>·5 = 5e<sup>3</sup>",
         verify="f′(x)/f(x) = 2/x + 3 에서 x=1: 5 → f(1)=e³ 이므로 5e³. 두 방법의 결과가 일치한다.",
         notes=[("①", "e³ = f(1). 미분하지 않고 함숫값을 고른 경우"), ("②", "2e³ = 첫 항 (x²)′e<sup>3x</sup>만 계산하고 둘째 항 누락"),
                ("③", "3e³ = 연쇄법칙의 3을 곱하지 않고 2x·e<sup>3x</sup> + x²·e<sup>3x</sup> 로 계산"),
                ("④", "정답"), ("⑤", "6e³ = 곱의 미분을 '미분의 곱'(x²)′·(e<sup>3x</sup>)′ = 2x·3e<sup>3x</sup> 으로 착각")],
         tag="연쇄법칙 누락 / 곱의 미분 항 누락"),
    dict(no="Q.02", kind="객관식", unit="적분법 · 부분적분", time="1분 30초",
         stem="정적분 ∫<sub>0</sub><sup>1</sup> x·e<sup>x</sup> dx 의 값은?",
         choices=["0", "1", "e − 1", "e", "2e − 1"], ans="②",
         intent="부분적분의 부호와 상·하한 대입 순서를 정확히 처리하는지 확인한다.",
         std=["u = x, dv = e<sup>x</sup>dx 로 두면 du = dx, v = e<sup>x</sup>",
              "∫ x e<sup>x</sup> dx = x e<sup>x</sup> − ∫ e<sup>x</sup> dx = (x − 1)e<sup>x</sup> + C",
              "[(x − 1)e<sup>x</sup>]<sub>0</sub><sup>1</sup> = (0) − (−1) = 1"],
         fast="결과 꼴을 알고 있으면 (x − 1)e<sup>x</sup> 를 미분해 x e<sup>x</sup> 임을 확인하고 바로 대입한다.",
         verify="d/dx[(x − 1)e<sup>x</sup>] = e<sup>x</sup> + (x − 1)e<sup>x</sup> = x e<sup>x</sup> ✓. 피적분함수가 구간에서 양수이므로 값도 양수(1)이다.",
         notes=[("①", "0 = 상한 값(x=1)만 취하고 하한 값(−1)을 빼지 않음"), ("②", "정답"),
                ("③", "e − 1 = x를 무시하고 ∫e<sup>x</sup>dx 로 계산"), ("④", "e = x e<sup>x</sup> 자체를 원시함수로 착각 ([x e<sup>x</sup>] = e)"),
                ("⑤", "2e − 1 = 부분적분 부호 실수 ((x + 1)e<sup>x</sup> 를 원시함수로 사용)")],
         tag="부호 실수 / 하한 대입 누락"),
    dict(no="Q.03", kind="객관식", unit="선형대수 · 고유값과 대각합", time="2분",
         stem="행렬 A = [[4, 1], [2, 3]] 에 대하여 A<sup>2</sup>의 모든 고유값의 합은?",
         choices=["7", "10", "29", "49", "100"], ans="③",
         intent="고유값의 거듭제곱 성질과 대각합(trace)·행렬식 관계를 활용해 계산량을 줄이는지 확인한다.",
         std=["특성방정식: λ² − (4+3)λ + (4·3 − 1·2) = λ² − 7λ + 10 = 0 → λ = 2, 5",
              "A²의 고유값은 λ² = 4, 25 → 합은 4 + 25 = 29"],
         fast="tr(A²) = (tr A)² − 2 det A = 49 − 20 = 29 (고유값을 구하지 않고 바로 계산)",
         verify="A² = [[18, 7], [14, 11]] 을 직접 계산하면 대각합 18 + 11 = 29 ✓.",
         notes=[("①", "7 = A의 고유값의 합(제곱하지 않음)"), ("②", "10 = det A (고유값의 곱)"), ("③", "정답"),
                ("④", "49 = (tr A)². '제곱의 합'과 '합의 제곱'을 혼동"), ("⑤", "100 = det(A²). 고유값의 곱의 제곱을 계산")],
         tag="개념 혼동(합 vs 곱)"),
]

UNIV_ITEMS = [
    dict(no="01", kind="객관식", unit="극한 · 테일러 전개", time="1분 30초",
         stem="lim<sub>x→0</sub> (e<sup>2x</sup> − 1 − 2x) / x<sup>2</sup> 의 값은?",
         choices=["0", "1", "2", "4", "∞"], ans="③",
         intent="0/0 꼴에서 테일러 전개 또는 로피탈 정리를 선택해 빠르게 계산하는지 확인한다.",
         std=["e<sup>2x</sup> = 1 + 2x + (2x)²/2! + … = 1 + 2x + 2x² + …",
              "분자 = 2x² + (고차항) → 극한 = 2"],
         fast="로피탈 2회: (2e<sup>2x</sup> − 2)/(2x) → 4e<sup>2x</sup>/2 → x=0에서 2",
         verify="x = 0.01 대입: (e<sup>0.02</sup> − 1.02)/0.0001 ≈ (1.0202013 − 1.02)/0.0001 ≈ 2.01 → 2에 근접한다.",
         notes=[("①", "0 = 1차항이 소거되는 것만 보고 0으로 판단"), ("②", "1 = e<sup>x</sup> 전개 계수를 그대로 사용(2x → x)"),
                ("③", "정답"), ("④", "4 = (2x)² 에서 1/2! 을 누락"), ("⑤", "∞ = 분모가 0이라 발산으로 오판")],
         tag="전개 계수 실수 / 부정형 오판"),
    dict(no="02", kind="객관식", unit="급수 · 부분분수와 망원급수", time="2분",
         stem="급수 Σ<sub>n=1</sub><sup>∞</sup> 1 / (n(n + 2)) 의 값은?",
         choices=["1/2", "2/3", "3/4", "5/6", "1"], ans="③",
         intent="부분분수 분해로 망원급수(telescoping)를 인식하는지 확인한다.",
         std=["1/(n(n+2)) = (1/2)(1/n − 1/(n+2))",
              "부분합 S<sub>N</sub> = (1/2)[(1 + 1/2) − (1/(N+1) + 1/(N+2))]",
              "N → ∞ 이면 (1/2)(3/2) = 3/4"],
         fast="남는 항은 처음 두 항(1, 1/2)뿐이다. (1/2)(1 + 1/2) = 3/4",
         verify="S₁ = 1/3, S₂ ≈ 0.458, S₃ ≈ 0.525, S₄ ≈ 0.567, S₅ ≈ 0.595 … 가 0.75에 접근한다.",
         notes=[("①", "1/2 = 앞의 계수 1/2만 남기고 괄호 안을 1로 계산"), ("②", "2/3 = 부분합이 접근하는 값이 아님(부분합 검산으로 배제)"),
                ("③", "정답"), ("④", "5/6 = 부분합이 접근하는 값이 아님(부분합 검산으로 배제)"), ("⑤", "1 = 1/n − 1/(n+1) 꼴의 망원급수로 착각")],
         tag="분해 오류 / 남는 항 계산 실수"),
    dict(no="03", kind="단답형", unit="적분 · 삼각함수의 거듭제곱", time="2분",
         stem="정적분 ∫<sub>0</sub><sup>π/2</sup> sin<sup>3</sup>x dx = p/q (p, q는 서로소인 자연수) 일 때, p + q 의 값을 구하시오.",
         choices=None, ans="5",
         intent="홀수 거듭제곱의 치환 적분(sin 한 개를 떼어 cos로 치환)을 정확히 수행하는지 확인한다.",
         std=["sin³x = (1 − cos²x) sin x, t = cos x 로 치환하면 dt = −sin x dx",
              "∫<sub>0</sub><sup>π/2</sup> sin³x dx = ∫<sub>0</sub><sup>1</sup> (1 − t²) dt = 1 − 1/3 = 2/3",
              "p = 2, q = 3 → p + q = 5"],
         fast="월리스 공식: ∫<sub>0</sub><sup>π/2</sup> sin³x dx = (2/3)·1 = 2/3 (홀수 차수: (n−1)!!/n!!)",
         verify="정적분 값 2/3 ≈ 0.667. sin³x ≤ sin x 이고 ∫<sub>0</sub><sup>π/2</sup> sin x dx = 1 이므로 값은 1보다 작다 ✓.",
         notes=[("답안 작성", "단답형은 보기가 없으므로 값을 직접 도출해야 한다. 답은 p+q = 5 (2/3 자체를 쓰지 않도록 주의)."),
                ("흔한 실수", "치환 후 상·하한을 바꾸지 않거나 부호(−)를 처리하지 않아 −2/3 또는 1/3 이 나오는 경우")],
         tag="치환 한계 실수 / 부호"),
]

SAMPLE_SETS = {
    "eng": dict(label="편입영어", sub="빈칸 추론 · 독해/논리", file_q="eng-problem.pdf", file_s="eng-solution.pdf"),
    "math": dict(label="편입수학", sub="미분·적분·선형대수", file_q="math-problem.pdf", file_s="math-solution.pdf"),
    "univ": dict(label="대학별 모의고사", sub="한양대 자연계 수학 형식", file_q="univ-problem.pdf", file_s="univ-solution.pdf"),
}


def _stem_block(it):
    ch = ""
    if it["choices"]:
        ch = '<ol class="sx-ch">' + "".join(f'<li><span class="cn">{CIRC[i]}</span>{c}</li>' for i, c in enumerate(it["choices"])) + "</ol>"
    else:
        ch = '<p class="sx-sa">답: ______________</p>'
    return f'<div class="sx-q"><div class="sx-qh"><span class="sx-n">{it["no"]}</span><span class="tag">{it["kind"]}</span><span class="sx-m">{E(it["unit"])} · 권장 {it["time"]}</span></div><div class="sx-box">{it["stem"]}</div>{ch}</div>'


def math_problem_sheets(items, title, extra_head=""):
    body = "".join(_stem_block(i) for i in items)
    return (f'<section class="sheet prob" aria-label="{E(title)} 문제집 샘플"><div class="sx-hd"><span class="sx-n">문제집</span><h3>{E(title)}</h3>'
            f'<span class="sx-m">샘플 · 전문가 검수 전 시안</span></div>{extra_head}{body}'
            f'<div class="sx-ft"><span>편입샘 · 문제집</span><span>샘플 · 독창 문항</span></div></section>')


def math_solution_sheets(items, title):
    out = ""
    for it in items:
        std = "".join(f"<li>{s}</li>" for s in it["std"])
        notes = "".join(f'<tr><th>{n}</th><td>{d}</td></tr>' for n, d in it["notes"])
        out += (f'<div class="sx-sol"><div class="sx-qh"><span class="sx-n sol">{it["no"]}</span><span class="tag">정답 {it["ans"]}</span>'
                f'<span class="sx-m">{E(it["unit"])}</span></div>'
                f'<div class="sx-sec"><h4>■ 문제</h4><p>{it["stem"]}</p></div>'
                f'<div class="sx-sec"><h4>■ 출제 의도</h4><p class="ko">{E(it["intent"])}</p></div>'
                f'<div class="sx-sec"><h4>■ 정석 풀이</h4><ol class="sx-steps">{std}</ol></div>'
                f'<div class="sx-sec accent"><h4>[단축 풀이]</h4><p class="sx-hl">{it["fast"]}</p></div>'
                f'<div class="sx-sec"><h4>■ 계산 검증</h4><p class="ko">{it["verify"]}</p></div>'
                f'<div class="sx-sec"><h4>■ 선택지·오답 분석</h4><div class="tw"><table class="sx-tb"><tbody>{notes}</tbody></table></div></div>'
                f'<p class="sx-tag">오답 원인 태그: {E(it["tag"])}</p></div>')
    return (f'<section class="sheet sol" aria-label="{E(title)} 해설집 샘플"><div class="sx-hd"><span class="sx-n sol">해설집</span><h3>{E(title)} 해설</h3>'
            f'<span class="sx-m">샘플 · 전문가 검수 전 시안</span></div>{out}'
            f'<div class="sx-ft"><span>편입샘 · 해설집</span><span>샘플 · 독창 문항</span></div></section>')


UNIV_EXAM_INFO = ('<div class="sx-info"><b>시험 형식 기준</b> · 2026학년도 한양대학교 서울캠퍼스 자연계 필기시험(수험생 유의사항): 수학 25문항(객관식 20 + 단답형 5), 70분. '
                  '이 샘플은 위 형식에 맞춰 편입샘이 새로 만든 문항이며 한양대 실제 문항이 아닙니다. 대학과 무관한 비공식 자료입니다.</div>')


def eng_sheets():
    """영어 샘플: (문제집 시트, 해설집 시트)"""
    prob = problem_sheet().replace('<section class="sheet"', '<section class="sheet prob"')
    sol = solution_sheets().replace('<section class="sheet"', '<section class="sheet sol"')
    return prob, sol


def math_sheets():
    return (math_problem_sheets(MATH_ITEMS, "편입수학 샘플 문제 (미분·적분·선형대수)"),
            math_solution_sheets(MATH_ITEMS, "편입수학 샘플"))


def univ_sheets():
    return (math_problem_sheets(UNIV_ITEMS, "한양대학교 자연계 수학 모의고사 형식 · 샘플", UNIV_EXAM_INFO),
            math_solution_sheets(UNIV_ITEMS, "한양대학교 자연계 수학 모의고사 형식 · 샘플"))


def sheets_for(key):
    return {"eng": eng_sheets, "math": math_sheets, "univ": univ_sheets}[key]()
