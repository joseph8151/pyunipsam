"""샘플 문제집·해설집 v2 — 과목별 10문항, 해설은 2단으로 빽빽하게.

- 모든 지문·문항·해설은 편입샘이 새로 쓴 독창 내용이다(타 교재·기출 복제 아님).
- 수학·대학별 문항의 정답은 수치 계산으로 검증했다. 영어는 직접 검증했으나 전문가 검수 전이다.
- 해설 구성(영어): 본문 번역 · (글의 구성/제목·주제·요지·요약) · 문장별 분석[어휘/문법/연결사/빈칸] · 어휘 정리 · 핵심 개념 · 선택지 해부 · 함정 · 변형 출제
- 해설 구성(수학): 출제 의도 · 핵심 개념 · 정석 풀이 · 단축 풀이 · 계산 검증 · 선택지 분석 · 함정 · 변형 출제
"""
import html
import sample_content as base
from sample_content import frag, CIRC, MATH_ITEMS, UNIV_ITEMS, UNIV_EXAM_INFO

E = html.escape
TIME_GUIDE = base.TIME_GUIDE


def P(*pairs):
    """('text','tags') 조각 리스트를 간단히 만든다. 문자열만 주면 태그 없음."""
    return [(x, "") if isinstance(x, str) else x for x in pairs]


# ═════════════ 영어 10문항 ═════════════
ENG = []

# Q.01 빈칸 추론 (공원 지문) — sample_content 의 기존 해설 데이터를 재사용하고 설명을 추가
ENG.append(dict(
    no="Q.01", type="빈칸 추론", q=base.QTYPE, time="1분 30초", choices=base.CHOICES, ans=2,
    sents=base.SENTENCES, meta=base.META, structure=base.STRUCTURE, analysis=base.ANALYSIS, notes=base.CHOICE_NOTES,
    vocab=[("invest in", "~에 투자하다"), ("assumption", "가정, 추정 (assume의 명사형)"), ("track", "추적 조사하다 (= monitor, follow)"),
           ("tend to", "~하는 경향이 있다"), ("recover from", "~에서 회복하다"), ("at no cost", "무료로 (= free of charge)"),
           ("luxury", "사치(품) ↔ necessity 필수품"), ("infrastructure", "기반시설 (도로·상하수도처럼 사회를 떠받치는 시설)")],
    concept=["not A but B: A를 부정하고 B를 강조한다. 빈칸이 B이면 A(luxuries)와 의미상 대조되는 단어가 정답 후보다.",
             "However → Rather 는 글의 방향 전환 신호다. However(통념 반박) 뒤에 연구 결과, Rather 뒤에 올바른 설명이 온다.",
             "한정 문장('치료하지는 않는다', S4)은 과잉 해석 선지(⑤)를 걸러내는 결정적 근거다."],
    trap="①은 luxuries와 같은 계열(장식·사치)이라 단어 모양이 끌리지만 'not luxuries'와 정면 충돌한다. 빈칸 문제에서는 빈칸 주변 대조 구문을 먼저 확인하라.",
    variant="선지를 'essential services that cities should provide for everyone' 으로 바꿔도 같은 근거(no cost, 건강한 습관의 진입 비용 감소)로 정답이 된다.",
    tag="근거 없는 선택 / 대조 구문 무시"))

ENG.append(dict(
    no="Q.02", type="어휘 · 동의어", q="밑줄 친 ephemeral 과 의미가 가장 가까운 것은?", time="30초",
    stem_html="The popularity of the trend proved <u>ephemeral</u>; within a year, nobody mentioned it.",
    choices=["lasting", "short-lived", "harmful", "controversial", "gradual"], ans=2,
    sents=[(P("The popularity of the trend proved ", ("ephemeral", "v"), "; within a year, ", ("nobody", "g"), " mentioned it."),
            "그 유행의 인기는 덧없는 것으로 드러났다. 1년 안에 아무도 그것을 언급하지 않았다.",
            ["ephemeral : 덧없는, 단명하는 (= short-lived, transient, fleeting)",
             "단서: within a year, nobody mentioned it → 오래 지속되지 않았다는 결과가 세미콜론 뒤에서 설명된다",
             "nobody : 부정 대명사 — 자체로 부정이므로 not 을 함께 쓰지 않는다 (nobody didn't ✕)"])],
    vocab=[("ephemeral", "덧없는, 하루살이 같은"), ("transient", "일시적인"), ("fleeting", "순식간의, 잠깐인"), ("enduring", "오래 지속되는 (반의어)"), ("trend", "유행, 추세")],
    concept=["어원: epi(~위에) + hemera(날) → '하루만 가는' → 덧없는.", "세미콜론(;) 뒤는 앞 문장을 구체화한다. 뒤 문장이 의미 단서가 된다.",
             "시간 관련 어휘는 '길이(short/long)'와 '속도(slow/fast)'를 구분해서 판단한다."],
    notes=[("①", "lasting", "✕", "반의어. 'nobody mentioned it' 과 충돌한다."), ("②", "short-lived", "○", "정답. 오래 가지 못하고 금방 잊혔다는 뜻과 일치한다."),
           ("③", "harmful", "✕", "해로움은 문맥 어디에도 없다. 뜻을 모를 때 부정적 어감만 보고 고르는 실수."),
           ("④", "controversial", "✕", "논쟁적이면 오히려 언급이 많아야 한다. 단서와 반대."),
           ("⑤", "gradual", "✕", "속도(점진적) 개념이라 '짧게 지속'과 다르다. 시간 어휘끼리의 혼동을 노린 선지.")],
    trap="ephemeral 을 모르면 'trend'(유행) 때문에 positive/negative 로만 판단하게 된다. 어휘 문제는 뜻을 몰라도 세미콜론·콜론 뒤의 풀이 문장으로 정답을 좁힐 수 있다.",
    variant="'The beauty of cherry blossoms is ephemeral' 처럼 자연 현상 문장으로 바뀌어도 정답 개념(short-lived)은 같다.",
    tag="어휘 뜻 미숙지 / 단서 문장 무시"))

ENG.append(dict(
    no="Q.03", type="어휘 · 동의어", q="밑줄 친 exacerbate 와 의미가 가장 가까운 것은?", time="30초",
    stem_html="Skipping meals will only <u>exacerbate</u> your fatigue.",
    choices=["relieve", "worsen", "disguise", "measure", "postpone"], ans=2,
    sents=[(P("Skipping meals will ", ("only", "g"), " ", ("exacerbate", "v"), " your fatigue."),
            "식사를 거르는 것은 피로를 악화시킬 뿐이다.",
            ["exacerbate : 악화시키다 (= aggravate, worsen)", "Skipping meals : 동명사 주어 — 단수 취급하므로 will + 동사원형이 이어진다",
             "only : '~할 뿐' — 부정적 방향을 강조하는 신호, 기대와 반대되는 결과를 암시한다"])],
    vocab=[("exacerbate", "악화시키다"), ("aggravate", "악화시키다, 화나게 하다"), ("alleviate", "완화하다 (반의어)"), ("fatigue", "피로"), ("skip", "건너뛰다, 거르다")],
    concept=["exacerbate는 '상황·증상을 더 나쁘게' 만드는 동사로 목적어가 pain, tension, fatigue 같은 부정적 명사일 때 자주 쓰인다.",
             "동명사 주어(Skipping meals)는 단수 취급한다.", "only + 동사: '~하는 것은 ~을 더할 뿐'이라는 한정 부사 용법."],
    notes=[("①", "relieve", "✕", "반의어(완화하다). only 가 만드는 부정적 방향과 반대다."), ("②", "worsen", "○", "정답. 피로가 더 심해진다는 뜻."),
           ("③", "disguise", "✕", "'위장하다'. 피로를 숨기는 것이 아니라 키우는 문장."), ("④", "measure", "✕", "'측정하다'. 문맥에 측정 행위가 없다."),
           ("⑤", "postpone", "✕", "'미루다'. 목적어 fatigue(피로)와 호응하지 않는다.")],
    trap="접두사 ex- 때문에 '밖으로 내보내다'(relieve)로 오해하기 쉽다. 목적어가 부정적 명사일 때는 악화 계열 동사를 우선 고려한다.",
    variant="exacerbate 를 aggravate / compound 로 바꾼 동의어 문항, 또는 alleviate 를 고르는 반의어 문항으로 변형된다.",
    tag="접두사 오해 / 방향성(+/−) 미판단"))

ENG.append(dict(
    no="Q.04", type="문법 · 오류 찾기", q="다음 중 어법상 틀린 부분은?", time="40초",
    stem_html="The number of students who <u>① applies</u> for the scholarship <u>② has increased</u> <u>③ since</u> the university <u>④ introduced</u> the new policy.",
    choices=["applies", "has increased", "since", "introduced"], ans=1,
    sents=[(P("The number of students ", ("who", "g"), " ", ("applies", "g"), " for the scholarship ", ("has increased", "g"), " ", ("since", "g"),
              " the university introduced the new policy."),
            "새 정책을 도입한 이후 장학금에 지원하는 학생의 수가 증가해 왔다.",
            ["who 의 선행사는 students(복수) → 동사는 applies ✕, apply ○ (관계절 안의 수일치는 선행사에 맞춘다)",
             "The number of + 복수명사 + 단수동사 : 주어는 number 이므로 has increased ○ (A number of + 복수명사는 복수 취급)",
             "since + 과거 시점의 절(introduced) ↔ 주절은 현재완료(has increased) 가 호응한다 ○"])],
    vocab=[("scholarship", "장학금"), ("apply for", "~에 지원하다"), ("introduce a policy", "정책을 도입하다"), ("the number of", "~의 수 (단수 취급)"), ("a number of", "많은 ~ (복수 취급)")],
    concept=["the number of vs a number of: the number 는 단수, a number of 는 복수 취급.", "관계절 속 동사의 수는 주절의 주어가 아니라 관계대명사의 선행사에 일치한다.",
             "since 절은 과거형, 주절은 현재완료가 호응한다."],
    notes=[("①", "applies", "○(오류)", "정답. who 의 선행사 students 가 복수이므로 apply 여야 한다."), ("②", "has increased", "✕", "주어가 The number(단수)이므로 has 가 맞다."),
           ("③", "since", "✕", "'~한 이후로' 의 접속사 — 현재완료와 호응해 맞다."), ("④", "introduced", "✕", "since 절의 동사는 과거형이 맞다.")],
    trap="가까이 있는 명사(students)에 끌려 ②를 고치거나, number 에 끌려 ①을 건드리지 못하는 함정. 관계절 → 선행사, 주절 → 핵심 주어를 분리해서 확인하라.",
    variant="'A number of students who applies...' 로 바꾸면 주절의 동사가 have increased 로 달라진다는 점까지 묻는 변형이 가능하다.",
    tag="수일치 대상 오인"))

ENG.append(dict(
    no="Q.05", type="문법 · 가정법 빈칸", q="다음 빈칸에 들어갈 말로 가장 적절한 것은?", time="40초",
    stem_html="Had the manager been more attentive, the error ________ unnoticed.",
    choices=["would not have gone", "would not go", "had not gone", "will not have gone", "did not go"], ans=1,
    sents=[(P(("Had", "g"), " the manager been more ", ("attentive", "v"), ", the error ", ("________", "b"), " ", ("unnoticed", "v"), "."),
            "관리자가 더 주의를 기울였더라면, 그 오류는 눈에 띄지 않은 채 넘어가지 않았을 것이다.",
            ["Had + S + p.p. = If + S + had p.p. (if 생략 도치) → 가정법 과거완료의 조건절",
             "주절: S + would(not) have p.p. → would not have gone", "go unnoticed : 눈에 띄지 않고 지나가다 (go + 형용사 : ~한 상태가 되다)"])],
    vocab=[("attentive", "주의 깊은"), ("go unnoticed", "눈에 띄지 않고 지나가다"), ("error", "오류"), ("manager", "관리자"), ("inversion", "도치")],
    concept=["가정법 과거완료: If + S + had p.p., S + would/could/might + have p.p. (과거 사실의 반대)", "If 생략 시 Had + S + p.p. 로 도치한다. (Were + S ~ / Should + S ~ 도 같은 원리)",
             "go + 형용사(unnoticed, wrong, bad)는 '~한 상태로 되다' 라는 연결동사 용법이다."],
    notes=[("①", "would not have gone", "○", "정답. 과거완료 조건절 → would not have p.p. 주절."), ("②", "would not go", "✕", "가정법 과거의 주절 형태 — 조건절이 과거완료이므로 시제 불일치."),
           ("③", "had not gone", "✕", "과거완료는 조건절의 형태이지 주절에 쓰지 않는다."), ("④", "will not have gone", "✕", "미래완료. 가정법이 아니다."),
           ("⑤", "did not go", "✕", "직설법 과거. 'Had ... attentive' 가 만드는 가정의 의미가 사라진다.")],
    trap="도치 구문(Had the manager been)을 의문문으로 오해하면 문장 구조가 흔들린다. 문두의 Had/Were/Should 는 if 생략 도치부터 의심하라.",
    variant="'Were the manager more attentive, the error would not go unnoticed' 처럼 가정법 과거로 바뀌면 정답은 would not go 가 된다.",
    tag="if 생략 도치 미인식 / 시제 호응"))

ENG.append(dict(
    no="Q.06", type="논리완성 · 양보", q="다음 빈칸에 들어갈 말로 가장 적절한 것은?", time="1분",
    stem_html="Although the new policy was ________ at first, it soon won over most of its critics.",
    choices=["enthusiastically embraced", "met with skepticism", "widely praised", "quietly ignored", "unanimously adopted"], ans=2,
    sents=[(P(("Although", "c"), " the new policy was ", ("________", "b"), " at first, it soon ", ("won over", "v"), " most of its ", ("critics", "v"), "."),
            "비록 그 새 정책이 처음에는 ________ 이었지만, 곧 대부분의 비판자들을 설득해 냈다.",
            ["Although : 양보 접속사 → 앞 절과 뒤 절의 방향이 반대 (처음: 부정 ↔ 나중: 긍정)", "win over : (~을) 설득해 자기편으로 만들다 — 뒤에 긍정적 변화가 온다는 신호",
             "critics : 비판자가 존재했다는 것은 처음에 부정적 반응이 있었음을 뜻한다"])],
    vocab=[("skepticism", "회의론, 의심"), ("embrace", "받아들이다, 포옹하다"), ("win over", "설득해 지지를 얻다"), ("critic", "비판자"), ("unanimously", "만장일치로")],
    concept=["양보(Although/Though/While) 문제는 '앞 = 부정이면 뒤 = 긍정, 앞 = 긍정이면 뒤 = 부정' 으로 방향을 먼저 정한다.",
             "win over 의 대상(critics)이 곧 초반 상황의 단서다.", "'be met with + 반응' 은 '~한 반응에 부딪히다' 의 관용 표현이다."],
    notes=[("①", "enthusiastically embraced", "✕", "긍정. Although 가 요구하는 반대 방향이 아니다."), ("②", "met with skepticism", "○", "정답. 처음엔 회의적 → 나중엔 설득 (양보 관계 성립)."),
           ("③", "widely praised", "✕", "긍정. 비판자(critics)를 설득할 필요가 없다."), ("④", "quietly ignored", "✕", "무시되었다면 비판자가 생길 수 없어 critics 와 모순."),
           ("⑤", "unanimously adopted", "✕", "만장일치 채택이면 설득할 비판자가 없다.")],
    trap="④ quietly ignored 는 '부정적' 어감만으로 고르기 쉽다. 비판자가 있었다는 사실(critics)과 모순됨을 확인해야 한다.",
    variant="Although 를 Because 로 바꾸면 방향이 같아져 enthusiastically embraced 계열이 정답이 되는 반전 문제로 변형된다.",
    tag="양보 방향 미판단 / 부정 어감만 선택"))

ENG.append(dict(
    no="Q.07", type="논리완성 · 인과", q="다음 빈칸에 들어갈 말로 가장 적절한 것은?", time="1분",
    stem_html="Because the data were collected from only fifty participants, the researchers cautioned that the results should not be ________ to the general population.",
    choices=["generalized", "compared", "restricted", "reported", "delayed"], ans=1,
    sents=[(P(("Because", "c"), " the ", ("data were", "g"), " collected from only fifty participants, the researchers ", ("cautioned", "v"),
              " that the results should not be ", ("________", "b"), " to the general population."),
            "데이터가 단지 50명의 참가자에게서 수집되었기 때문에, 연구자들은 그 결과를 일반 모집단에 ________ 해서는 안 된다고 주의를 주었다.",
            ["Because : 이유절 — 표본이 작다는 이유가 '주의(cautioned)'의 근거", "data were : data 는 datum 의 복수형 (현대 영어에서 단수 취급도 허용되나 시험에서는 복수 취급을 기본으로 본다)",
             "generalize A to B : A 를 B 로 일반화하다 — to the general population 과 호응"])],
    vocab=[("generalize", "일반화하다"), ("participant", "참가자"), ("caution", "경고하다, 주의를 주다"), ("population", "모집단, 인구"), ("sample size", "표본 크기")],
    concept=["표본이 작다 → 결과를 전체에 적용(일반화)하기 어렵다는 인과 구조.", "be generalized to + 대상 : ~에 일반화되다. 전치사 to 와 호응하는 동사를 고른다.",
             "cautioned that ... should not be p.p. : 주의의 내용이 부정 명령이므로 빈칸 동사는 '적용·확대' 계열이다."],
    notes=[("①", "generalized", "○", "정답. 작은 표본의 결과를 전체에 일반화하지 말라는 뜻."), ("②", "compared", "✕", "compared to 는 가능하지만 '표본이 작다'는 이유와 인과가 이어지지 않는다."),
           ("③", "restricted", "✕", "restricted to 는 '~에 한정되다' — 일반 모집단에 한정하라는 의미가 되어 어색하다."), ("④", "reported", "✕", "보고 여부는 표본 크기와 무관하다."),
           ("⑤", "delayed", "✕", "지연은 근거가 없다.")],
    trap="②와 ③은 문법적으로 to 와 결합 가능해 보인다. 이유절(only fifty participants)과 논리가 이어지는지로 판단하라.",
    variant="'..., the findings cannot be extended to larger groups' 처럼 동의어 표현으로 바꿔도 같은 논리다.",
    tag="인과 연결 미확인 / 전치사 호응만으로 선택"))

ENG.append(dict(
    no="Q.08", type="독해 · 주제", q="윗글의 주제로 가장 적절한 것은?", time="1분 30초",
    stem_html=("Many students believe that typing notes is the more efficient choice because it allows them to record nearly every word a lecturer says. "
               "However, this speed can become a disadvantage. When students copy lectures word for word, they often process the material only superficially. "
               "Handwriting, by contrast, is slower, which forces writers to listen closely, decide what matters, and rephrase ideas in their own words. "
               "In other words, the limits of handwriting push learners toward deeper understanding."),
    choices=["Typing allows students to record lectures faster than handwriting.", "Slower note-taking can promote deeper processing of lecture content.",
             "Students should avoid recording lectures word for word in any form.", "Lecturers should speak more slowly during classes.",
             "Rephrasing ideas is unnecessary when notes are typed."], ans=2,
    sents=[(P("Many students ", ("believe", "v"), " ", ("that", "g"), " typing notes is the more efficient choice because it ", ("allows", "g"), " them ", ("to record", "g"), " nearly every word a lecturer says."),
             "많은 학생들은 강사가 하는 거의 모든 말을 기록할 수 있기 때문에 필기를 타이핑하는 것이 더 효율적인 선택이라고 믿는다.",
             ["allow + O + to V : O 가 ~하도록 허용하다/가능하게 하다", "the more efficient choice : 두 대상 중 하나를 가리키는 the + 비교급 (타이핑 vs 손글씨)"]),
            (P(("However", "c"), ", this ", ("speed", "v"), " can become a disadvantage."), "그러나 이 속도는 단점이 될 수 있다.",
             ["However : 통념(타이핑이 효율적)을 뒤집는 전환 — 이 지점부터 필자의 주장이 시작된다", "this speed : 앞 문장의 '기록 속도'를 받는 지시어 → 필자는 속도 자체를 문제로 삼는다"]),
            (P("When students copy lectures ", ("word for word", "v"), ", they often process the material only ", ("superficially", "v"), "."),
             "학생들이 강의를 한 마디 한 마디 베껴 쓸 때, 그들은 종종 내용을 피상적으로만 처리한다.",
             ["word for word : 한 마디 한 마디, 그대로", "superficially : 피상적으로 ↔ deeply — 뒤에 나올 deeper understanding 과 대비되는 핵심 어휘"]),
            (P("Handwriting, ", ("by contrast", "c"), ", is slower, ", ("which", "g"), " ", ("forces", "g"), " writers to listen closely, decide what matters, and rephrase ideas in their own words."),
             "이와 대조적으로 손글씨는 더 느려서, 필기하는 사람이 주의 깊게 듣고, 무엇이 중요한지 결정하고, 아이디어를 자신의 말로 바꿔 쓰도록 만든다.",
             ["by contrast : 타이핑 ↔ 손글씨의 대조", "which : 계속적 용법 관계대명사 — 앞 절 전체(손글씨가 느리다는 사실)를 선행사로 받는다",
              "force + O + to V : O 가 ~하도록 강제하다 / listen, decide, rephrase 가 병렬(to 가 하나로 묶임)"]),
            (P(("In other words", "c"), ", the limits of handwriting push learners toward deeper understanding."), "다시 말해, 손글씨의 한계가 학습자를 더 깊은 이해로 이끈다.",
             ["In other words : 앞 내용을 한 문장으로 환언 → 이 문장이 사실상 주제문", "limits (한계) 가 오히려 장점으로 연결되는 역설적 표현"])],
    meta=[("제목", "Why Slower Note-Taking Can Teach More", "느린 필기가 더 많이 가르치는 이유"), ("주제", "The cognitive benefit of handwritten notes", "손글씨 필기의 인지적 이점"),
          ("요지", "Typing is faster, but handwriting's slowness encourages deeper processing of ideas.", "타이핑은 더 빠르지만 손글씨의 느림이 아이디어를 더 깊이 처리하게 만든다."),
          ("요약", "The passage argues that copying lectures verbatim leads to shallow processing, whereas the effort of handwriting encourages selection and rephrasing.",
           "이 글은 강의를 그대로 베끼면 피상적으로 처리하게 되지만, 손글씨의 수고는 선별과 재진술을 유도한다고 주장한다.")],
    structure=[("도입", "타이핑이 더 효율적이라는 통념을 제시한다."), ("전개", "속도가 오히려 단점이 되며, 그대로 베끼면 피상적 처리에 그친다고 반박한다."),
               ("전환·근거", "손글씨는 느려서 듣기·선별·재진술을 강제한다."), ("결론", "손글씨의 한계가 더 깊은 이해로 이어진다.")],
    analysis=[("논리 구조", "통념(타이핑 효율) → However 반박(속도의 단점) → 원인(그대로 베낌 → 피상적 처리) → By contrast 대안(손글씨의 강제 효과) → In other words 결론"),
              ("핵심 단서", "However, by contrast, In other words 가 만드는 3단 전환. 주제는 마지막 환언 문장(in other words)에 집약된다.")],
    vocab=[("efficient", "효율적인"), ("lecturer", "강사"), ("superficially", "피상적으로"), ("rephrase", "다시 표현하다"), ("push A toward B", "A를 B로 이끌다"), ("disadvantage", "단점")],
    concept=["주제 찾기: 전환어(However/By contrast/In other words)가 연결하는 문장을 모아 공통 개념(slower → deeper)을 뽑는다.",
             "세부 정보 선지는 '글에 나온 사실'이지만 주제는 아니다 — ①은 첫 문장의 전제일 뿐 필자는 반박한다.",
             "과잉 일반화 선지(in any form, unnecessary)는 지문에 없는 단정을 포함한다."],
    notes=[("①", "타이핑이 손글씨보다 더 빠르게 기록할 수 있다", "✕", "S1의 전제일 뿐 However 이후 필자가 반박하는 내용이다."),
           ("②", "느린 필기가 강의 내용의 깊은 처리를 촉진할 수 있다", "○", "정답. By contrast, In other words 문장과 일치한다."),
           ("③", "어떤 형태로든 받아쓰기를 피해야 한다", "✕", "'in any form' 은 과잉 일반화. 지문은 베껴 쓰기가 피상적 처리로 이어질 수 있다고만 말한다."),
           ("④", "강사는 더 천천히 말해야 한다", "✕", "강사의 말 속도는 언급이 없다."), ("⑤", "타이핑하면 아이디어를 바꿔 쓸 필요가 없다", "✕", "지문은 타이핑 시 재진술이 줄 수 있다고 시사할 뿐 '필요 없다'고 단정하지 않는다.")],
    trap="①은 지문에 있는 문장이라 안전해 보인다. 하지만 'However' 앞의 내용은 반박 대상이다. 주제는 필자가 마지막에 강조한 방향에서 찾는다.",
    variant="'윗글의 제목' 문제로 바뀌면 정답은 Why Slower Note-Taking Can Teach More 계열이 되며 같은 근거를 쓴다.",
    tag="통념(반박 대상) 선택 / 과잉 일반화"))

ENG.append(dict(
    no="Q.09", type="독해 · 문장 순서", q="주어진 글 다음에 이어질 글의 순서로 가장 적절한 것은?", time="1분",
    stem_html=("<b>Given:</b> Bees are often described as simple insects, yet their communication is surprisingly sophisticated.<br>"
               "<b>(A)</b> For example, a forager that finds a rich flower patch returns to the hive and performs a &ldquo;waggle dance.&rdquo;<br>"
               "<b>(B)</b> The angle and length of the dance indicate the direction and distance of the food.<br>"
               "<b>(C)</b> This behavior shows that bees can share precise information about locations."),
    choices=["(A) - (B) - (C)", "(A) - (C) - (B)", "(B) - (A) - (C)", "(B) - (C) - (A)", "(C) - (A) - (B)"], ans=1,
    sents=[(P("Bees are often described as simple insects, ", ("yet", "c"), " their communication is surprisingly ", ("sophisticated", "v"), "."),
            "벌은 흔히 단순한 곤충으로 묘사되지만, 그들의 의사소통은 놀랄 만큼 정교하다.", ["yet : 양보·대조 접속사(= but) — '단순하다 ↔ 정교하다' 대조가 글의 화제를 설정한다", "sophisticated : 정교한, 세련된"]),
           (P(("For example", "c"), ", a ", ("forager", "v"), " that finds a rich flower patch returns to the hive and performs a \"waggle dance.\""),
            "예를 들어, 풍부한 꽃밭을 발견한 채집벌은 벌집으로 돌아와 '8자 춤'을 춘다.", ["For example : 주어진 글의 '정교한 의사소통'을 구체화하는 첫 예시 → (A) 가 가장 먼저 온다", "forager : 먹이를 찾아 모으는 개체(채집벌)"]),
           (P("", ("The", "g"), " angle and length of the dance indicate the direction and distance of the food."), "춤의 각도와 길이는 먹이의 방향과 거리를 나타낸다.",
            ["the dance : 정관사 — (A) 에서 처음 소개한 waggle dance 를 다시 가리킨다 → (B) 는 (A) 뒤", "angle ↔ direction, length ↔ distance 가 대응하는 구체적 설명"]),
           (P(("This behavior", "g"), " shows that bees can share precise information about locations."), "이 행동은 벌이 위치에 대한 정확한 정보를 공유할 수 있음을 보여 준다.",
            ["This behavior : 지시어 — 앞에서 서술한 행동(춤 + 정보 전달)을 가리키므로 마지막 (C)", "shows that ~ : 앞 내용을 일반화하는 결론 문장"])],
    vocab=[("sophisticated", "정교한"), ("forager", "채집하는 개체"), ("hive", "벌집"), ("patch", "(작은) 구역, 밭"), ("indicate", "나타내다"), ("waggle dance", "(꿀벌의) 8자 춤")],
    concept=["순서 배열 3원칙: ① 지시어/정관사는 선행 정보 뒤 ② 예시(For example)는 주장 뒤 ③ 결론(This shows)은 마지막.",
             "첫 문장 후보를 먼저 확정하면 나머지 순서가 연쇄적으로 정해진다.", "(B)의 The dance 처럼 정관사 + 앞에서 소개된 명사는 소개 문장(A) 뒤에 온다."],
    notes=[("①", "(A) - (B) - (C)", "○", "정답. 사례 제시 → 세부 설명 → 일반화 결론."), ("②", "(A) - (C) - (B)", "✕", "(C)의 결론이 (B)의 세부 정보보다 먼저 와 흐름이 뒤집힌다."),
           ("③", "(B) - (A) - (C)", "✕", "(B)의 The dance 가 (A)에서 소개되기 전에 쓰였다."), ("④", "(B) - (C) - (A)", "✕", "③과 같은 이유 + 결론이 사례보다 앞선다."),
           ("⑤", "(C) - (A) - (B)", "✕", "(C)의 This behavior 가 가리킬 선행 대상이 없다.")],
    trap="(A)(B)(C) 가운데 (B)를 먼저 읽으면 'The angle and length' 가 자연스러워 보인다. 하지만 정관사(the dance)의 선행 소개가 없다는 점이 결정적 근거다.",
    variant="Given 문장이 'This ...' 로 시작하는 문장 삽입형으로 바뀌어도 지시어 추적 원리는 같다.",
    tag="정관사·지시어 추적 실패"))

ENG.append(dict(
    no="Q.10", type="논리 · 연결사 빈칸", q="다음 빈칸에 들어갈 말로 가장 적절한 것은?", time="40초",
    stem_html="Public libraries are often seen as quiet places for borrowing books. ________, many of them now offer job-training workshops, language classes, and free internet access.",
    choices=["However", "Similarly", "Consequently", "For instance", "Likewise"], ans=1,
    sents=[(P("Public libraries are often ", ("seen as", "g"), " quiet places for borrowing books."), "공공도서관은 흔히 책을 빌리는 조용한 장소로 여겨진다.",
            ["be seen as ~ : ~로 여겨지다 (통념·인식을 나타내는 표현) — 뒤에 통념을 뒤집는 전환이 올 가능성이 높다"]),
           (P(("________", "b"), ", many of them now ", ("offer", "v"), " job-training workshops, language classes, and free internet access."),
            "________, 현재 많은 도서관이 직업 훈련 워크숍, 어학 수업, 무료 인터넷 이용을 제공한다.",
            ["now : 시간 부사 — 과거의 통념과 현재의 실제 모습을 대비한다", "offer A, B, and C : 병렬 구조 / many of them : them = public libraries"])],
    vocab=[("public library", "공공도서관"), ("borrow", "빌리다"), ("workshop", "워크숍"), ("access", "접근, 이용"), ("however", "그러나 (역접)"), ("consequently", "결과적으로")],
    concept=["연결사 문제는 앞·뒤 문장의 '방향 관계'(대조/예시/인과/추가)를 기호(+, −, =)로 먼저 적는다.", "통념(often seen as) 뒤에는 대조 연결사(However, In fact)가 오는 경우가 많다.",
             "대조(However) ≠ 예시(For instance) ≠ 인과(Consequently) ≠ 유사(Similarly/Likewise) 의 관계 표를 암기하라."],
    notes=[("①", "However", "○", "정답. 통념(조용한 장소)과 현재의 실제(다양한 서비스)가 대조된다."), ("②", "Similarly", "✕", "유사 관계. 두 문장은 같은 내용이 아니다."),
           ("③", "Consequently", "✕", "인과 관계. 조용해서 프로그램을 제공한다는 논리는 성립하지 않는다."), ("④", "For instance", "✕", "앞 문장은 사례가 필요한 주장이 아니라 통념이다."),
           ("⑤", "Likewise", "✕", "Similarly 와 같은 유사 관계.")],
    trap="'many of them now offer ...' 만 읽고 For instance 를 고르기 쉽다. 반드시 앞 문장과의 관계를 먼저 판정하라.",
    variant="두 문장의 순서가 바뀌면(서비스를 먼저 제시) For instance 나 In fact 계열로 정답이 달라질 수 있다.",
    tag="연결사 관계 미판정"))


# ═════════════ 수학·대학별: 새 문항 추가 (정답은 수치로 검증 완료) ═════════════
def _it(**k):
    return k


# 기존 3문항에 설명 보강
_EXTRA_OLD = {
    "Q.01": dict(concept=["곱의 미분: (uv)′ = u′v + uv′ — 두 함수의 변화를 모두 반영한다.", "합성함수의 미분: (e^{g(x)})′ = g′(x)e^{g(x)} — 지수 위 함수의 도함수를 곱한다.", "로그미분: 곱·거듭제곱이 섞인 함수는 ln 을 취하면 합으로 바뀌어 계산이 단순해진다."],
                 trap="체인룰의 3 을 빼먹거나 곱의 미분 두 항 중 하나를 놓치는 실수가 가장 빈번하다. 오답 ①②③⑤ 가 모두 이 실수에서 나온다.",
                 variant="f(x)=x³e^{−x} 처럼 지수의 부호·차수를 바꿔도 로그미분 f′/f = 3/x − 1 로 같은 방식이 통한다."),
    "Q.02": dict(concept=["부분적분: ∫u dv = uv − ∫v du, u 는 미분하면 단순해지는 함수(x)를 택한다.", "정적분은 원시함수를 먼저 구한 뒤 상한 − 하한으로 대입한다(하한 값 누락 주의).", "피적분함수가 양수이면 정적분도 양수 — 부호로 오답을 1차 필터링한다."],
                 trap="[(x−1)e^x]₀¹ 에서 상한 값 0 만 남기고 하한 값 −1 을 빼지 않아 0 을 고르는 실수가 빈번하다.",
                 variant="구간을 [0,2] 로 바꾸면 [(x−1)e^x]₀² = e² + 1 이 된다."),
    "Q.03": dict(concept=["A 의 고유값이 λ 이면 A² 의 고유값은 λ² 이다 (Ax = λx → A²x = λ²x).", "tr(A) = 고유값의 합, det(A) = 고유값의 곱.", "tr(A²) = (tr A)² − 2 det A (2×2 행렬의 항등식)."],
                 trap="‘제곱의 합’(Σλ²)과 ‘합의 제곱’((Σλ)²)을 혼동해 49 를 고르거나, det 를 고유값의 합으로 착각한다.",
                 variant="A 가 대칭행렬이면 고유값이 모두 실수이므로 tr(A²) = Σλ² ≥ 0 임을 이용하는 변형이 가능하다."),
}
for it in MATH_ITEMS:
    it.update(_EXTRA_OLD.get(it["no"], {}))

MATH_ITEMS += [
    _it(no="Q.04", kind="객관식", unit="극한 · 무리식의 유리화", time="1분 30초",
        stem="lim<sub>x→∞</sub> ( √(x<sup>2</sup> + 3x) − x ) 의 값은?", choices=["0", "1", "3/2", "3", "∞"], ans="③",
        intent="∞ − ∞ 꼴을 유리화로 해소하고 최고차항으로 나누어 극한을 구하는지 확인한다.",
        std=["∞ − ∞ 부정형이므로 켤레식 √(x²+3x) + x 를 분자·분모에 곱한다", "분자: (x² + 3x) − x² = 3x, 분모: √(x²+3x) + x",
             "분모를 x 로 나누면 √(1 + 3/x) + 1 → x→∞ 에서 2", "극한 = 3x / (x·2) = 3/2"],
        fast="√(x²+ax) ≈ x + a/2 (x 가 매우 클 때) 이므로 차는 a/2 = 3/2",
        verify="x = 10⁸ 대입: √(10¹⁶ + 3·10⁸) − 10⁸ ≈ 1.49999999… → 3/2 ✓.",
        concept=["∞ − ∞ 는 유리화(켤레식)로 분수 꼴로 바꾼다.", "x→∞ 에서 √(x²+ax) = x√(1+a/x) ≈ x(1 + a/(2x)) (이항근사).", "분모·분자를 최고차항 x 로 나눠 극한을 정리한다."],
        notes=[("①", "0 = ∞ − ∞ 를 ‘같은 크기’로 보고 0 으로 판단"), ("②", "1 = 분모를 계산하며 √ 안의 계수를 잘못 처리(3/2 를 정수로 반올림)"),
               ("③", "정답"), ("④", "3 = 분모의 + x 를 누락하고 3x/x 로 계산"), ("⑤", "∞ = 부정형을 발산으로 오판")],
        trap="분모의 + x 를 빼먹거나, ∞ − ∞ 를 0 으로 단정하는 실수. 유리화 후 반드시 분모의 두 항을 모두 x 로 나눠야 한다.",
        variant="√(x²+ax) − x → a/2 로 일반화되므로 a 를 바꾼 문항은 계산 없이 풀 수 있다.", tag="부정형 판단 / 분모 항 누락"),
    _it(no="Q.05", kind="객관식", unit="미분 응용 · 최대·최소", time="2분",
        stem="구간 [0, 4] 에서 함수 f(x) = x<sup>3</sup> − 6x<sup>2</sup> + 9x + 1 의 최댓값은?", choices=["1", "4", "5", "6", "9"], ans="③",
        intent="임계점과 구간 끝점의 함숫값을 모두 비교하는 최대·최소 문제의 절차를 확인한다.",
        std=["f′(x) = 3x² − 12x + 9 = 3(x − 1)(x − 3) → 임계점 x = 1, 3 (모두 구간 안)", "후보 : f(0) = 1, f(1) = 5, f(3) = 1, f(4) = 64 − 96 + 36 + 1 = 5", "최댓값 = 5 (x = 1 과 x = 4 에서 동시에 도달)"],
        fast="f(x) − 1 = x(x − 3)² 로 인수분해되므로 [0,4] 에서 x(x−3)² 의 최댓값을 보면 x=1 (4) 과 x=4 (4) 가 같다 → f 의 최댓값 5",
        verify="x(x−3)² 를 전개하면 x³ − 6x² + 9x ✓. x=1: 1·4 = 4, x=4: 4·1 = 4 ✓ → f = 4 + 1 = 5.",
        concept=["닫힌구간 최대·최소 정리: 최댓값·최솟값은 임계점 또는 구간 끝점에서 나온다.", "극값이 구간 내부에 있어도 끝점 값을 반드시 함께 비교한다.", "함수를 인수분해해 두면 극값의 구조를 계산 없이 파악할 수 있다."],
        notes=[("①", "1 = 최솟값 (f(0) = f(3) = 1)"), ("②", "4 = 구간 끝점의 x 좌표(4)를 값으로 착각"), ("③", "정답"), ("④", "6 = 임계점 함숫값의 합 f(1) + f(3) = 5 + 1"),
               ("⑤", "9 = 도함수의 값 f′(0) = 9 와 혼동")],
        trap="x = 4 (끝점)의 함숫값을 비교하지 않고 극대값 f(1) = 5 만 보고 풀 수 있어 정답은 우연히 맞더라도 절차 점검이 중요하다. 끝점이 더 크면 답이 달라진다.",
        variant="구간이 [−1, 4] 이면 f(−1) = −15 이므로 최솟값 후보가 바뀌지만 최댓값 5 는 그대로다.", tag="끝점 누락 / 값과 좌표 혼동"),
    _it(no="Q.06", kind="객관식", unit="적분 응용 · 넓이", time="1분 30초",
        stem="곡선 y = x<sup>2</sup> 과 직선 y = 2x 로 둘러싸인 부분의 넓이는?", choices=["2/3", "1", "4/3", "2", "8/3"], ans="③",
        intent="교점을 구해 적분 구간을 정하고 위·아래 함수를 구분해 넓이를 계산하는지 확인한다.",
        std=["교점: x² = 2x → x = 0, 2", "구간 [0, 2] 에서 2x ≥ x² (위: 직선, 아래: 포물선)", "넓이 = ∫₀² (2x − x²) dx = [x² − x³/3]₀² = 4 − 8/3 = 4/3"],
        fast="포물선과 현으로 둘러싸인 넓이 공식: (|a|/6)(β − α)³ , a = 1, β−α = 2 → 8/6 = 4/3",
        verify="구간을 1/N 로 쪼개 수치적분하면 ≈ 1.3333 ✓.",
        concept=["두 곡선 사이의 넓이: ∫(위쪽 함수 − 아래쪽 함수)dx, 구간은 교점에서 정한다.", "이차함수와 직선(현) 사이 넓이 = |a|(β−α)³/6 (1/6 공식).", "위·아래를 뒤집으면 음수가 나오므로 부호로 오류를 검산한다."],
        notes=[("①", "2/3 = 구간을 [0, 1] 로 잘못 잡음"), ("②", "1 = 유사 값 방지용 선지 (수치적분으로 배제)"), ("③", "정답"), ("④", "2 = 유사 값 방지용 선지 (수치적분으로 배제)"),
               ("⑤", "8/3 = ∫₀² x² dx = 8/3 로 포물선 아래 면적만 계산")],
        trap="교점을 구하지 않고 [0, 1] 에서 계산하거나, 한 곡선 아래 넓이만 구하는 실수. 먼저 그림을 그려 위·아래를 정하라.",
        variant="y = x² 과 y = x 로 바꾸면 ∫₀¹ (x − x²)dx = 1/6.", tag="구간 설정 오류 / 위아래 혼동"),
    _it(no="Q.07", kind="객관식", unit="급수 · 수렴반경", time="1분 30초",
        stem="멱급수 Σ<sub>n=1</sub><sup>∞</sup> n·x<sup>n</sup> / 2<sup>n</sup> 의 수렴반경은?", choices=["1/2", "1", "2", "4", "∞"], ans="③",
        intent="비율판정법으로 수렴반경을 구하고 계수 n 이 반경에 영향을 주지 않음을 이해하는지 확인한다.",
        std=["a<sub>n</sub> = n x<sup>n</sup>/2<sup>n</sup> 에 비율판정법: |a<sub>n+1</sub>/a<sub>n</sub>| = ((n+1)/n)·|x|/2", "n → ∞ 에서 (n+1)/n → 1 이므로 극한은 |x|/2",
             "|x|/2 < 1 ⟺ |x| < 2 → 수렴반경 R = 2"],
        fast="Σ(x/2)ⁿ 의 공비 x/2 에 다항 계수 n 이 붙어도 수렴반경은 바뀌지 않는다 → R = 2",
        verify="((n+1)/n)·(1/2) 를 n = 10⁶ 에서 계산하면 ≈ 0.5000005 → 극한 1/2 = 1/R ✓.",
        concept=["수렴반경 R = 1 / lim |a<sub>n+1</sub>/a<sub>n</sub>| (계수 기준) 또는 비율판정법으로 |x| < R.", "다항식 계수(n, n², …)는 수렴반경을 바꾸지 않는다 (경계점 수렴 여부만 달라질 수 있다).", "수렴반경과 수렴구간은 다르다 — 경계점은 따로 확인한다."],
        notes=[("①", "1/2 = 극한값(1/R)을 반경으로 착각"), ("②", "1 = 계수 n 때문에 반경이 줄어든다고 오판"), ("③", "정답"), ("④", "4 = 2² (분모의 제곱)"), ("⑤", "∞ = 지수함수 급수와 혼동")],
        trap="비율의 극한이 1/2 로 나오면 그것이 반경이 아니라 1/R 이다. R = 2 로 뒤집는 마지막 단계를 빼먹기 쉽다.",
        variant="분모를 3ⁿ 으로 바꾸면 R = 3. 분자를 n! 로 바꾸면 R = 0 이 된다.", tag="역수 처리 누락"),
    _it(no="Q.08", kind="객관식", unit="다변수 · 방향도함수", time="2분",
        stem="함수 f(x, y) = x<sup>2</sup>y + y<sup>2</sup> 의 점 (1, 2) 에서 벡터 u = (3/5, 4/5) 방향의 방향도함수 D<sub>u</sub>f 의 값은?", choices=["4", "5", "9", "32/5", "32"], ans="④",
        intent="기울기 벡터와 단위벡터의 내적으로 방향도함수를 구하는지 확인한다.",
        std=["f<sub>x</sub> = 2xy → (1, 2) 에서 4 / f<sub>y</sub> = x² + 2y → 1 + 4 = 5 → ∇f = (4, 5)", "u = (3/5, 4/5) 는 크기 1 인 단위벡터 (9/25 + 16/25 = 1)", "D<sub>u</sub>f = ∇f · u = 4·3/5 + 5·4/5 = 12/5 + 20/5 = 32/5"],
        fast="단위벡터 확인 후 ∇f·u 를 한 줄로 계산: (12 + 20)/5 = 32/5",
        verify="수치 미분으로 (f(1 + 0.6h, 2 + 0.8h) − f(1,2))/h (h → 0) ≈ 6.4 = 32/5 ✓.",
        concept=["D<sub>u</sub>f = ∇f · u (u 는 반드시 단위벡터).", "기울기 ∇f 는 f 가 가장 빠르게 증가하는 방향이고, 그 크기가 방향도함수의 최댓값이다.", "단위벡터가 아니면 크기로 나눠 정규화한 뒤 내적한다."],
        notes=[("①", "4 = f<sub>x</sub> 만 사용"), ("②", "5 = f<sub>y</sub> 만 사용"), ("③", "9 = f<sub>x</sub> + f<sub>y</sub> 의 합"), ("④", "정답"), ("⑤", "32 = 단위벡터화 없이 (3, 4) 를 그대로 사용 (4·3 + 5·4)")],
        trap="방향 벡터를 정규화하지 않아 32 를 고르는 실수가 가장 흔하다. 문제의 u 가 이미 단위벡터인지 크기를 먼저 확인하라.",
        variant="u 를 (3, 4) 로 주면 |u| = 5 로 나눠 같은 값 32/5 를 얻는 문제로 변형된다.", tag="정규화 누락 / 편미분 항 선택"),
    _it(no="Q.09", kind="객관식", unit="미분방정식 · 1계 선형", time="2분 30초",
        stem="y′ + 2y = e<sup>−x</sup>, y(0) = 2 를 만족하는 해 y(x) 에 대하여 y(1) 의 값은?", choices=["2/e<sup>2</sup>", "1/e", "1/e + 1/e<sup>2</sup>", "1/e + 2/e<sup>2</sup>", "2/e"], ans="③",
        intent="적분인자법으로 일반해를 구하고 초기조건으로 상수를 정확히 결정하는지 확인한다.",
        std=["적분인자 μ = e<sup>2x</sup> → (y·e<sup>2x</sup>)′ = e<sup>2x</sup>·e<sup>−x</sup> = e<sup>x</sup>", "y·e<sup>2x</sup> = e<sup>x</sup> + C → y = e<sup>−x</sup> + C e<sup>−2x</sup>",
             "y(0) = 1 + C = 2 → C = 1 → y = e<sup>−x</sup> + e<sup>−2x</sup>", "y(1) = 1/e + 1/e²"],
        fast="미정계수법: 특수해 y<sub>p</sub> = A e<sup>−x</sup> 를 대입하면 −A + 2A = 1 → A = 1, 제차해 C e<sup>−2x</sup> 를 더한다",
        verify="y = e^{−x} + e^{−2x} 를 방정식에 대입하면 y′ + 2y = −e^{−x} − 2e^{−2x} + 2e^{−x} + 2e^{−2x} = e^{−x} ✓, y(0) = 2 ✓.",
        concept=["1계 선형 y′ + P y = Q 의 적분인자: μ = e^{∫P dx}.", "일반해 = 특수해 + 제차해 (y<sub>h</sub> = C e<sup>−2x</sup>).", "초기조건은 일반해 전체에 대입해 C 를 구한다 — 특수해만 대입하지 않는다."],
        notes=[("①", "2/e² = 제차해만 사용 (y = 2e<sup>−2x</sup>)"), ("②", "1/e = 특수해만 사용 (초기조건 무시, C = 0)"), ("③", "정답"),
               ("④", "1/e + 2/e² = y(0) = 2 를 C 에 그대로 대입 (C = 2)"), ("⑤", "2/e = 유사 값 방지용 선지 (대입 검산으로 배제)")],
        trap="y(0) = 2 를 일반해 y = e<sup>−x</sup> + C e<sup>−2x</sup> 의 C 에 그대로 넣는 실수. 1 + C = 2 로 C = 1 임을 거쳐야 한다.",
        variant="우변을 e<sup>−2x</sup> 로 바꾸면 제차해와 겹쳐 공명이 일어나 특수해가 x e<sup>−2x</sup> 꼴이 된다.", tag="초기조건 처리 / 일반해 구성"),
    _it(no="Q.10", kind="객관식", unit="선형대수 · 계수와 영공간", time="1분 30초",
        stem="행렬 A = [[1, 2, 3], [2, 4, 6], [1, 0, 1]] 에 대하여 동차연립방정식 Ax = 0 의 해공간의 차원은?", choices=["0", "1", "2", "3", "해가 없다"], ans="②",
        intent="행의 일차종속성을 찾아 rank 를 구하고 계수-영공간 정리(rank + nullity = n)를 적용하는지 확인한다.",
        std=["R₂ = 2R₁ 이므로 두 번째 행은 첫 번째 행의 상수배 (일차종속)", "R₁ 과 R₃ 는 서로 상수배가 아니므로 일차독립 → rank A = 2", "rank + nullity = 3 (열의 수) → nullity = 3 − 2 = 1"],
        fast="행 하나가 다른 행의 배수임을 눈으로 확인하면 rank 2, nullity 1 로 바로 결정된다 (det A = 0 도 같은 신호).",
        verify="수치 계산으로 rank(A) = 2 를 확인했다. 해공간 기저: (−1, −1, 1)ᵗ → A(−1,−1,1)ᵗ = (−1−2+3, −2−4+6, −1+0+1) = (0,0,0) ✓.",
        concept=["계수-영공간 정리: rank(A) + nullity(A) = (열의 수).", "행이 서로 일차종속이면 rank 가 줄어든다 — det = 0 은 정사각행렬의 신호.", "동차연립방정식 Ax = 0 은 항상 자명해 x = 0 을 가진다 — ‘해가 없음’은 불가능."],
        notes=[("①", "0 = A 가 가역(full rank)이라고 가정"), ("②", "정답"), ("③", "2 = rank 와 nullity 혼동"), ("④", "3 = 변수의 수(열의 수)를 해공간 차원으로 착각"), ("⑤", "동차계는 항상 자명해를 가지므로 해가 없을 수 없다")],
        trap="rank 와 nullity 를 혼동해 2 를 고르는 실수가 가장 많다. 질문이 묻는 것은 ‘해공간’(영공간)의 차원이다.",
        variant="세 번째 행을 (2, 0, 2) 로 바꿔도 rank 는 2, nullity 는 1 로 같다.", tag="rank/nullity 혼동"),
]

# ── 대학별(한양 자연계 수학 형식): 객관식 7 + 단답형 3 ──
_old = {it["no"]: it for it in UNIV_ITEMS}
_UEX = {
    "01": dict(concept=["e<sup>x</sup> = 1 + x + x²/2! + … 의 테일러 전개를 이용하면 ‘0/0’ 극한이 다항식 비교로 바뀐다.", "(e<sup>ax</sup> − 1 − ax)/x² → a²/2 (a = 2 이면 2).", "로피탈 정리는 분모·분자 모두 0 일 때 미분해서 다시 극한을 보는 방법이다 (2회 적용)."],
              trap="1/2! 계수를 빼먹어 4 를 고르거나, 1차항이 소거되는 것만 보고 0 으로 단정하는 실수가 빈번하다.",
              variant="(e^{ax} − 1 − ax)/x² → a²/2 로 일반화되어 a 만 바꾼 문항은 즉시 풀린다."),
    "02": dict(concept=["부분분수 분해 1/(n(n+2)) = ½(1/n − 1/(n+2)) 로 망원급수(telescoping)를 만든다.", "망원급수는 앞 두 항(1, ½)만 남고 뒤쪽은 0 으로 수렴한다.", "부분합 S<sub>N</sub> 의 극한이 급수의 합이다."],
              trap="괄호 안 계수 ½ 를 빼먹어 3/2 가 되거나, 1/n − 1/(n+1) 꼴로 착각해 1 을 고르는 실수.",
              variant="1/(n(n+3)) 이면 (1/3)(1 + 1/2 + 1/3) = 11/18."),
    "03": dict(concept=["홀수 거듭제곱은 sin 하나를 떼고 cos 로 치환하면 다항 적분이 된다.", "월리스 공식: ∫₀^{π/2} sinⁿx dx = (n−1)!!/n!! (n 홀수일 때 π/2 계수 없음).", "치환 시 상·하한도 함께 바꾼다 (x: 0→π/2, t = cos x: 1→0)."],
              trap="치환 후 상·하한을 바꾸지 않거나 −부호를 처리하지 않아 −2/3 또는 1/3 이 나오는 실수.",
              variant="sin⁵x 이면 8/15 (p + q = 23)."),
}
for k, v in _UEX.items():
    _old[k].update(v)

_old03 = _old["03"]  # 단답형 → 08 번으로 이동
_old03["no"] = "08"
_U_NEW = [
    _it(no="03", kind="객관식", unit="적분 · 부분적분(삼각함수)", time="1분 30초",
        stem="정적분 ∫<sub>0</sub><sup>π/2</sup> x cos x dx 의 값은?", choices=["π/2 − 1", "π/2", "π/2 + 1", "π − 1", "1 − π/2"], ans="①",
        intent="부분적분에서 삼각함수의 부호 처리와 경계값 대입을 정확히 하는지 확인한다.",
        std=["u = x, dv = cos x dx → du = dx, v = sin x", "∫ x cos x dx = x sin x − ∫ sin x dx = x sin x + cos x + C", "[x sin x + cos x]₀^{π/2} = (π/2 + 0) − (0 + 1) = π/2 − 1"],
        fast="d/dx(x sin x + cos x) = sin x + x cos x − sin x = x cos x 임을 확인하고 곧바로 대입한다.",
        verify="구간을 잘게 쪼갠 수치적분 값 ≈ 0.570796 = π/2 − 1 ✓.",
        concept=["부분적분에서 u 는 미분하면 단순해지는 함수(x), dv 는 적분이 쉬운 함수(cos x)를 택한다.", "(sin x)′ = cos x, (cos x)′ = −sin x 의 부호를 항상 확인한다.", "피적분함수가 [0, π/2] 에서 0 이상이므로 값은 양수 (π/2 − 1 ≈ 0.57)."],
        notes=[("①", "정답"), ("②", "π/2 = cos x 항(−1)을 누락"), ("③", "π/2 + 1 = 부호 실수 (+ cos 항을 반대로 대입)"), ("④", "π − 1 = x sin x 의 값을 π/2 가 아닌 π 로 계산"), ("⑤", "1 − π/2 = 전체 부호 반전 (음수 → 피적분함수가 양수이므로 불가능)")],
        trap="부호가 음수인 선지(⑤)는 피적분함수의 부호만으로 즉시 제거할 수 있다. 부호 검산을 습관화하라.",
        variant="∫₀^{π/2} x sin x dx = 1 로 바뀌며 같은 방식으로 풀린다.", tag="부호 실수 / 상수항 누락"),
    _it(no="04", kind="객관식", unit="선형대수 · 고유값과 행렬식", time="2분",
        stem="행렬 A = [[2, 0], [1, 3]] 에 대하여 det(A<sup>2</sup> + A) 의 값은?", choices=["18", "36", "60", "72", "144"], ans="④",
        intent="행렬 다항식의 고유값이 λ 의 다항식으로 변환됨을 이용해 계산량을 줄이는지 확인한다.",
        std=["A 는 하삼각행렬이므로 고유값은 대각성분 2, 3", "A² + A 의 고유값 = λ² + λ → 2² + 2 = 6, 3² + 3 = 12", "det(A² + A) = 6 × 12 = 72"],
        fast="det(A² + A) = det(A)·det(A + I) = 6 × 12 = 72 (A(A+I) 로 인수분해)",
        verify="A² = [[4, 0], [5, 9]], A² + A = [[6, 0], [6, 12]] → det = 6·12 − 0·6 = 72 ✓.",
        concept=["삼각행렬의 고유값은 대각성분이다.", "p(A) 의 고유값은 p(λ). 행렬식은 고유값의 곱이다.", "det(AB) = det(A)·det(B) — A² + A = A(A + I) 로 인수분해해 계산한다."],
        notes=[("①", "18 = tr(A² + A) = 6 + 12 (대각합과 행렬식 혼동)"), ("②", "36 = det(A)² = det(A²) 만 계산"), ("③", "60 = 유사 값 방지용 선지 (직접 계산으로 배제)"), ("④", "정답"), ("⑤", "144 = 12² (고유값 곱의 제곱 오류)")],
        trap="tr(대각합)과 det(행렬식)을 혼동해 18 을 고르거나, A² 의 행렬식만 구해 36 을 고르는 실수.",
        variant="고유값이 a, b 이면 det(A² + A) = (a² + a)(b² + b) 로 일반화된다.", tag="trace/det 혼동"),
    _it(no="05", kind="객관식", unit="다변수 · 이중적분", time="2분",
        stem="영역 D = {(x, y) : 0 ≤ y ≤ x ≤ 1} 에 대하여 ∬<sub>D</sub> xy dA 의 값은?", choices=["1/12", "1/8", "1/6", "1/4", "1/2"], ans="②",
        intent="삼각형 영역의 적분 순서를 정하고 안쪽 적분 후 바깥 적분을 정확히 수행하는지 확인한다.",
        std=["0 ≤ y ≤ x, 0 ≤ x ≤ 1 이므로 ∫₀¹ ( ∫₀ˣ x y dy ) dx", "안쪽: x · [y²/2]₀ˣ = x · x²/2 = x³/2", "바깥: ∫₀¹ x³/2 dx = 1/8"],
        fast="대칭성: 정사각형 [0,1]² 에서 ∬xy = 1/4 이고 y ≤ x 영역은 그 절반 → 1/8",
        verify="수치적분 ≈ 0.12500 = 1/8 ✓.",
        concept=["적분 영역을 먼저 그림으로 확인하고 안쪽 적분의 변수 범위를 결정한다.", "피적분함수 xy 가 x, y 에 대해 대칭이므로 y ≤ x 와 x ≤ y 영역의 적분 값은 같다.", "정사각형 영역에서는 ∬xy = (∫x)(∫y) = ¼ (분리 가능)."],
        notes=[("①", "1/12 = 유사 값 방지용 선지 (직접 계산으로 배제)"), ("②", "정답"), ("③", "1/6 = 안쪽 적분 후 x 인수를 곱하지 않고 ∫ x²/2 계산"), ("④", "1/4 = 영역을 정사각형 [0,1]² 로 착각"), ("⑤", "1/2 = 유사 값 방지용 선지")],
        trap="영역을 정사각형으로 착각해 1/4 를 고르거나 안쪽 적분 결과에 곱해야 할 x 를 빠뜨려 1/6 이 나온다.",
        variant="영역이 0 ≤ x ≤ y ≤ 1 이어도 대칭성으로 값은 1/8 로 같다.", tag="영역 오인 / 적분 순서 오류"),
    _it(no="06", kind="객관식", unit="급수 · 등비급수의 변형", time="1분 30초",
        stem="급수 Σ<sub>n=0</sub><sup>∞</sup> (n + 1) / 3<sup>n</sup> 의 값은?", choices=["3/2", "2", "9/4", "3", "9/2"], ans="③",
        intent="Σ(n+1)rⁿ = 1/(1−r)² 공식을 알고 있는지, 또는 등비급수를 미분해 유도할 수 있는지 확인한다.",
        std=["Σ<sub>n≥0</sub> r<sup>n</sup> = 1/(1 − r) 의 양변을 r 로 미분하면 Σ n r<sup>n−1</sup> = 1/(1 − r)²", "Σ<sub>n≥0</sub> (n + 1) r<sup>n</sup> = 1/(1 − r)²", "r = 1/3 → 1/(2/3)² = 9/4"],
        fast="공식 Σ(n+1)rⁿ = 1/(1 − r)² 에 r = 1/3 을 바로 대입한다.",
        verify="처음 200 항의 합을 계산하면 2.25 = 9/4 ✓.",
        concept=["등비급수 Σrⁿ = 1/(1−r) (|r| < 1) 를 항별 미분하면 계수 n 이 붙은 급수의 합이 나온다.", "Σ(n+1)rⁿ = 1/(1−r)² 는 공식으로 외워 둘 가치가 있다.", "수렴 조건 |r| < 1 을 먼저 확인한다."],
        notes=[("①", "3/2 = 계수 n + 1 을 무시한 등비급수 Σ(1/3)ⁿ = 3/2"), ("②", "2 = 유사 값 방지용 선지 (부분합 검산으로 배제)"), ("③", "정답"), ("④", "3 = 유사 값 방지용 선지"), ("⑤", "9/2 = 정답에 2를 곱한 값 (미분 시 계수 오류)")],
        trap="(n+1) 계수를 무시한 3/2 를 고르는 실수. 계수 n 이 붙으면 반드시 미분 공식을 떠올려야 한다.",
        variant="r = 1/2 이면 1/(1/2)² = 4.", tag="계수 무시 / 공식 미암기"),
    _it(no="07", kind="객관식", unit="미분 응용 · 극값", time="1분 30초",
        stem="함수 f(x) = x e<sup>−x</sup> (x ≥ 0) 의 최댓값은?", choices=["0", "1/e<sup>2</sup>", "1/e", "2/e", "e"], ans="③",
        intent="도함수의 부호 변화로 극대점을 찾고 극댓값을 계산하는지 확인한다.",
        std=["f′(x) = e<sup>−x</sup> − x e<sup>−x</sup> = (1 − x) e<sup>−x</sup>", "f′ = 0 → x = 1 이고, x < 1 에서 f′ > 0, x > 1 에서 f′ < 0 → x = 1 에서 극대(최대)", "f(1) = 1·e<sup>−1</sup> = 1/e"],
        fast="e<sup>−x</sup> > 0 이므로 f′ 의 부호는 (1 − x) 의 부호와 같다. 극대점이 x = 1 로 즉시 결정된다.",
        verify="x 를 0 에서 5 까지 0.001 간격으로 대입하면 최댓값 0.36788 = 1/e (x = 1) ✓.",
        concept=["도함수가 0 이 되는 점의 좌우 부호 변화로 극대·극소를 판정한다.", "e<sup>−x</sup> 는 항상 양수이므로 부호 분석에서 소거해도 된다.", "x → ∞ 에서 f → 0 이므로 극대점이 최대점이 된다."],
        notes=[("①", "0 = f(0) = 0 (경계값)"), ("②", "1/e² = f(2) = 2/e² 와 혼동하거나 지수만 계산"), ("③", "정답"), ("④", "2/e = 분모 처리 오류"), ("⑤", "e = e<sup>x</sup> 를 e<sup>−x</sup> 로 착각해 f(1) = e 로 계산")],
        trap="e<sup>−x</sup> 의 지수 부호를 놓치면 e 를 고른다. f(1) = 1·e<sup>−1</sup> 에서 지수 −1 을 반드시 대입하라.",
        variant="f(x) = x² e<sup>−x</sup> 이면 극댓값은 x = 2 에서 4/e².", tag="지수 부호 실수"),
    _old03,
    _it(no="09", kind="단답형", unit="선형대수 · 고유값", time="1분 30초",
        stem="행렬 A = [[5, 2], [2, 2]] 의 두 고유값 중 큰 값을 λ 라 할 때, λ<sup>2</sup> 의 값을 구하시오.", choices=None, ans="36",
        intent="특성방정식으로 고유값을 구하고 큰 값을 정확히 선택하는지 확인한다.",
        std=["특성방정식: λ² − (5 + 2)λ + (5·2 − 2·2) = λ² − 7λ + 6 = 0", "(λ − 1)(λ − 6) = 0 → λ = 1, 6", "큰 값 6 이므로 λ² = 36"],
        fast="tr = 7, det = 6 → 합이 7, 곱이 6 인 두 수는 1 과 6 (바로 판별)",
        verify="고유값을 수치로 계산하면 (6, 1) ✓. A(2,1)ᵗ = (12, 6)ᵗ = 6(2,1)ᵗ 로 λ = 6 의 고유벡터를 확인했다.",
        concept=["2×2 행렬의 특성방정식: λ² − (tr A)λ + det A = 0.", "tr 과 det 만 알면 고유값의 합과 곱을 바로 알 수 있다.", "단답형은 ‘구하는 대상’(λ² 인지 λ 인지)을 마지막에 다시 확인한다."],
        notes=[("답안 작성", "단답형이므로 보기가 없다. 구하는 값은 λ² = 36 이다 (λ = 6 이라고 쓰지 않도록 주의)."), ("흔한 실수", "큰 고유값 6 만 쓰고 제곱을 빠뜨리거나, 1 + 36 = 37 처럼 두 고유값을 모두 제곱해 더하는 경우")],
        trap="문제가 묻는 것이 λ 가 아니라 λ² 임을 놓치는 실수. 마지막에 질문을 다시 읽어라.",
        variant="고유값이 1, 6 이므로 det A = 6, tr A = 7. 값을 거꾸로 주는 역문제로도 출제된다.", tag="요구값 재확인 누락"),
    _it(no="10", kind="단답형", unit="적분 · 절댓값 정적분", time="2분",
        stem="정적분 ∫<sub>0</sub><sup>2</sup> |x<sup>2</sup> − 2x| dx = p/q (p, q는 서로소인 자연수) 일 때, p + q 의 값을 구하시오.", choices=None, ans="7",
        intent="절댓값 안의 부호를 구간별로 판단해 정적분을 정확히 계산하는지 확인한다.",
        std=["x² − 2x = x(x − 2) ≤ 0 (0 ≤ x ≤ 2) → |x² − 2x| = 2x − x²", "∫₀² (2x − x²) dx = [x² − x³/3]₀² = 4 − 8/3 = 4/3", "p = 4, q = 3 → p + q = 7"],
        fast="그림으로 보면 y = x² − 2x 는 [0, 2] 에서 x 축 아래이므로 넓이 = 포물선·x 축 넓이 (1/6 공식: 8/6 = 4/3)",
        verify="구간을 쪼개 수치적분하면 1.33333 = 4/3 ✓.",
        concept=["절댓값 안의 식의 부호가 바뀌는 지점(영점)을 먼저 찾아 구간을 나눈다.", "[0, 2] 에서 x(x − 2) ≤ 0 이므로 부호를 뒤집어 적분한다.", "단답형 답안은 p + q 처럼 묻는 형식에 맞춰 마지막에 변환한다."],
        notes=[("답안 작성", "정적분 값은 4/3 이고 요구하는 답은 p + q = 4 + 3 = 7 이다."), ("흔한 실수", "절댓값을 무시하고 ∫(x² − 2x) = −4/3 을 계산해 음수 값이 나오는 경우 / 4/3 자체를 답으로 쓰는 경우")],
        trap="절댓값을 벗길 때 부호를 판단하지 않으면 −4/3 이 나온다. 정적분 값이 면적이므로 양수여야 한다.",
        variant="구간이 [0, 3] 이면 4/3 + 4/3 = 8/3 (p + q = 11).", tag="절댓값 부호 / 요구 형식 변환"),
]
# 순서: 01,02,03,04,05,06,07,08(단답 sin³),09,10
UNIV_ITEMS[:] = [_old["01"], _old["02"], _U_NEW[0], _U_NEW[1], _U_NEW[2], _U_NEW[3], _U_NEW[4], _old03, _U_NEW[6], _U_NEW[7]]

for it in MATH_ITEMS + UNIV_ITEMS:
    it.setdefault("variant", "")
    it.setdefault("concept", [])
    it.setdefault("trap", "")


# ═════════════ 렌더러 ═════════════
SAMPLE_SETS = base.SAMPLE_SETS


def _plain_stem(it):
    return it.get("stem_html") or E(" ".join("".join(t for t, _ in parts).strip() for parts, _, _ in it["sents"]))


def _eng_problem(it):
    stem = _plain_stem(it)
    ch = "".join(f'<li><span class="cn">{CIRC[i]}</span>{E(c)}</li>' for i, c in enumerate(it["choices"]))
    return (f'<div class="sx-q"><div class="sx-qh"><span class="sx-n">{it["no"]}</span><span class="tag">{E(it["type"])}</span><span class="sx-m">권장 {it["time"]}</span></div>'
            f'<p class="sx-ins">{E(it["q"])}</p><div class="sx-box">{stem}</div><ol class="sx-ch">{ch}</ol></div>')


def _eng_solution(it):
    sents = ""
    for i, (parts, ko, notes) in enumerate(it["sents"], 1):
        nt = "".join(f"<li>{E(n)}</li>" for n in notes)
        sents += f'<div class="sx-s"><span class="sn">S{i}</span><p class="en">{frag(parts)}</p><p class="ko">{E(ko)}</p><ul class="nt">{nt}</ul></div>'
    trans = " ".join(ko for _, ko, _ in it["sents"]).replace("________", "(빈칸)")
    structure = ""
    if it.get("structure"):
        structure = "<div class=\"sx-sec\"><h4>■ 글의 구성</h4>" + "".join(f'<p class="ko"><b>{E(k)}</b> · {E(v)}</p>' for k, v in it["structure"]) + "</div>"
    meta = ""
    if it.get("meta"):
        meta = "".join(f'<div class="sx-sec"><h4>■ {E(k)}</h4><p class="en">{E(en)}</p><p class="ko">{E(ko)}</p></div>' for k, en, ko in it["meta"])
    analysis = ""
    if it.get("analysis"):
        analysis = '<div class="sx-sec accent"><h4>[지문 분석 요약]</h4>' + "".join(f'<p class="sx-hl"><b>{E(k)}:</b> {E(v)}</p>' for k, v in it["analysis"]) + "</div>"
    vocab = "".join(f"<li><b>{E(w)}</b> {E(m)}</li>" for w, m in it["vocab"])
    concept = "".join(f"<li>{E(c)}</li>" for c in it["concept"])
    rows = ""
    for n, t, m, d in it["notes"]:
        cls = "ok" if m.startswith("○") else "no"
        rows += f'<tr><th>{n}</th><td>{E(t)}</td><td class="{cls}">{E(m)}</td><td>{E(d)}</td></tr>'
    return (f'<div class="sx-sol"><div class="sx-qh"><span class="sx-n sol">{it["no"]}</span><span class="tag">정답 {CIRC[it["ans"]-1]}</span><span class="sx-m">{E(it["type"])}</span></div>'
            f'<div class="sx-sec"><h4>■ 문제</h4><p class="sx-ins">{E(it["q"])}</p><div class="sx-box small">{_plain_stem(it)}</div></div>'
            f'<div class="sx-sec"><h4>■ 본문 번역</h4><p class="ko">{E(trans)}</p></div>{structure}{meta}'
            f'<div class="sx-sec"><h4>■ 문장별 분석 <span class="mm">[어휘] [문법] [연결사] [빈칸]</span></h4><div class="sx-sents">{sents}</div></div>{analysis}'
            f'<div class="sx-sec"><h4>■ 어휘 정리</h4><ul class="sx-vt">{vocab}</ul></div>'
            f'<div class="sx-sec"><h4>■ 핵심 개념</h4><ul class="nt big">{concept}</ul></div>'
            f'<div class="sx-sec"><h4>■ 선택지 해부</h4><div class="tw"><table class="sx-tb"><thead><tr><th>번호</th><th>선택지</th><th>정오</th><th>근거</th></tr></thead><tbody>{rows}</tbody></table></div></div>'
            f'<div class="sx-sec warn"><h4>■ 함정 포인트</h4><p>{E(it["trap"])}</p></div>'
            f'<div class="sx-sec"><h4>■ 변형 출제</h4><p>{E(it["variant"])}</p></div><p class="sx-tag">오답 원인 태그: {E(it["tag"])}</p></div>')


def _math_stem(it):
    return base._stem_block(it)


def _math_solution(it):
    std = "".join(f"<li>{s}</li>" for s in it["std"])
    concept = "".join(f"<li>{c}</li>" for c in it["concept"])
    notes = "".join(f"<tr><th>{n}</th><td>{d}</td></tr>" for n, d in it["notes"])
    return (f'<div class="sx-sol"><div class="sx-qh"><span class="sx-n sol">{it["no"]}</span><span class="tag">정답 {it["ans"]}</span><span class="sx-m">{E(it["unit"])}</span></div>'
            f'<div class="sx-sec"><h4>■ 문제</h4><div class="sx-box small mathbox">{it["stem"]}</div></div>'
            f'<div class="sx-sec"><h4>■ 출제 의도</h4><p class="ko">{E(it["intent"])}</p></div>'
            + (f'<div class="sx-sec"><h4>■ 핵심 개념</h4><ul class="nt big">{concept}</ul></div>' if concept else "")
            + f'<div class="sx-sec"><h4>■ 정석 풀이</h4><ol class="sx-steps">{std}</ol></div>'
            f'<div class="sx-sec accent"><h4>[단축 풀이]</h4><p class="sx-hl">{it["fast"]}</p></div>'
            f'<div class="sx-sec"><h4>■ 계산 검증</h4><p class="ko">{it["verify"]}</p></div>'
            f'<div class="sx-sec"><h4>■ 선택지·오답 분석</h4><div class="tw"><table class="sx-tb"><tbody>{notes}</tbody></table></div></div>'
            + (f'<div class="sx-sec warn"><h4>■ 함정 포인트</h4><p>{it["trap"]}</p></div>' if it["trap"] else "")
            + (f'<div class="sx-sec"><h4>■ 변형 출제</h4><p>{it["variant"]}</p></div>' if it["variant"] else "")
            + f'<p class="sx-tag">오답 원인 태그: {E(it["tag"])}</p></div>')


def _sheet(cls, label, title, body, foot, head_extra=""):
    return (f'<section class="sheet {cls}" aria-label="{E(title)}"><div class="sx-hd"><span class="sx-n{" sol" if cls == "sol" else ""}">{label}</span><h3>{E(title)}</h3>'
            f'<span class="sx-m">샘플 · 전문가 검수 전 시안</span></div>{head_extra}<div class="sx-body">{body}</div><div class="sx-ft"><span>{foot}</span><span>샘플 · 독창 문항</span></div></section>')


def eng_sheets():
    prob = _sheet("prob", "문제집", "편입영어 샘플 문제 (어휘·문법·논리·독해 10문항)", "".join(_eng_problem(i) for i in ENG), "편입샘 · 문제집")
    sol = _sheet("sol", "해설집", "편입영어 샘플 해설", "".join(_eng_solution(i) for i in ENG), "편입샘 · 해설집")
    return prob, sol


def math_sheets():
    prob = _sheet("prob", "문제집", "편입수학 샘플 문제 (미적분·선형대수·미분방정식 10문항)", "".join(_math_stem(i) for i in MATH_ITEMS), "편입샘 · 문제집")
    sol = _sheet("sol", "해설집", "편입수학 샘플 해설", "".join(_math_solution(i) for i in MATH_ITEMS), "편입샘 · 해설집")
    return prob, sol


def univ_sheets():
    title = "한양대학교 자연계 수학 모의고사 형식 · 샘플 (10문항: 객관식 7 + 단답형 3)"
    prob = _sheet("prob", "문제집", title, "".join(_math_stem(i) for i in UNIV_ITEMS), "편입샘 · 문제집", UNIV_EXAM_INFO)
    sol = _sheet("sol", "해설집", "한양대학교 자연계 수학 모의고사 형식 · 샘플 해설", "".join(_math_solution(i) for i in UNIV_ITEMS), "편입샘 · 해설집")
    return prob, sol


def sheets_for(key):
    return {"eng": eng_sheets, "math": math_sheets, "univ": univ_sheets}[key]()


def weapon_snippet():
    return base.weapon_snippet()
