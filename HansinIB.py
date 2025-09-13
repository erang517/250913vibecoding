import streamlit as st
st.title('한신초 IB 탐구설계 도우미')
st.write('탐구설계 도우미!')
# streamlit_app.py
import streamlit as st
import textwrap

st.set_page_config(page_title="IB 수업 설계 프롬프트 생성기", layout="wide")

st.title("🌐 IB 수업 설계 프롬프트 생성기")
st.caption("교사가 입력한 정보를 기반으로 ChatGPT에 바로 넣을 수 있는 완성형 프롬프트를 생성합니다.")

# -----------------------------
# 0) Presets & helpers
# -----------------------------
PYP_THEMES = [
    "우리 자신(Who we are)",
    "장소와 시간 속의 우리(Where we are in place and time)",
    "자기표현의 방식(How we express ourselves)",
    "세상이 어떻게 작동하는가(How the world works)",
    "우리가 자신을 조직하는 방식(How we organize ourselves)",
    "지구를 공유하며 사는 방법(Sharing the planet)",
]
PYP_THEME_DESC = {
    "우리 자신(Who we are)":
        "정체성, 신념과 가치, 건강, 관계, 인간됨에 대한 탐구",
    "장소와 시간 속의 우리(Where we are in place and time)":
        "개인·집단의 역사, 가정과 공동체, 이동과 정착, 변천과 연속성",
    "자기표현의 방식(How we express ourselves)":
        "아이디어·감정·자연·문화의 표현과 해석, 창의적 커뮤니케이션",
    "세상이 어떻게 작동하는가(How the world works)":
        "자연 세계·물리 법칙·과학·기술·사회와 환경의 상호작용",
    "우리가 자신을 조직하는 방식(How we organize ourselves)":
        "인간 시스템·경제 활동·조직·권리·책임·의사결정",
    "지구를 공유하며 사는 방법(Sharing the planet)":
        "자원, 생태계, 갈등과 협력, 지속가능성, 공정성과 평등",
}

GRADES = ["초1", "초2", "초3", "초4", "초5", "초6"]

SUBJECTS = [
    "국어", "수학", "사회", "과학", "도덕",
    "영어", "체육", "미술", "음악", "실과/가정", "정보"
]

# (예시) 학년·교과별 단원 추천(학교/지역에 따라 다를 수 있어 어디까지나 샘플)
UNIT_SUGGESTIONS = {
    "국어": {
        "초3": ["대화의 즐거움", "이야기 속 인물의 마음 알기"],
        "초4": ["인물에게 마음을 전해요", "정보를 찾아 설명해요"],
        "초5": ["주장과 근거", "토의하고 해결해요"],
        "초6": ["비유적 표현", "매체로 소통해요"],
    },
    "사회": {
        "초3": ["지역의 생활", "우리 고장의 모습"],
        "초4": ["지도로 만나는 우리 지역", "우리 지역의 문화유산"],
        "초5": ["국가의 구성과 역할", "환경과 인간생활"],
        "초6": ["대한민국의 민주정치", "세계와 교류하는 우리나라"],
    },
    "과학": {
        "초3": ["물체의 길이와 무게", "식물의 한살이"],
        "초4": ["태양계와 별", "물의 상태 변화"],
        "초5": ["용해와 용액", "생물과 환경"],
        "초6": ["전기회로", "지구와 달"],
    },
    "도덕": {
        "초3": ["배려와 존중", "정직과 약속"],
        "초4": ["디지털 시민으로서의 책임", "공동체 구성원의 역할"],
        "초5": ["자유와 책임", "공익과 규칙"],
        "초6": ["정의와 공정", "인권과 존엄"],
    },
    "수학": {
        "초3": ["곱셈과 나눗셈의 기초", "시간과 길이"],
        "초4": ["분수의 덧셈과 뺄셈", "각도와 도형의 성질"],
        "초5": ["분수와 소수의 곱셈", "자료의 해석"],
        "초6": ["비와 비율", "원과 입체도형"],
    },
    "미술": {
        "초3": ["선과 색의 표현", "관찰과 상상"],
        "초4": ["시각문화와 이미지 읽기", "재료와 도구의 활용"],
        "초5": ["표현 주제 확장", "미디어 아트"],
        "초6": ["통합적 표현", "작품 감상과 비평"],
    },
    "음악": {
        "초3": ["리듬과 가락 익히기", "노래와 표현"],
        "초4": ["박과 장단", "합주와 감상"],
        "초5": ["화음과 형식", "국악과 세계음악"],
        "초6": ["창작과 편곡", "공연과 감상문"],
    },
    "영어": {
        "초3": ["기초 인사와 소개", "교실 영어"],
        "초4": ["일상 표현과 역할놀이", "읽기·쓰기 기초"],
        "초5": ["간단한 정보 찾기", "간단한 설명과 묘사"],
        "초6": ["의견 말하기", "간단한 글쓰기"],
    },
    "체육": {
        "초3": ["기초 체력과 협동", "놀이와 게임"],
        "초4": ["기초 구기활동", "표현운동"],
        "초5": ["기초 육상과 체력", "안전교육"],
        "초6": ["전략 게임 기초", "스포츠맨십"],
    },
    "실과/가정": {
        "초5": ["가정생활과 안전", "기초 요리와 위생"],
        "초6": ["의복과 생활", "간단한 발명·제작"],
    },
    "정보": {
        "초5": ["디지털 기기 이해", "문제해결과 알고리즘 기초"],
        "초6": ["정보윤리와 저작권", "자료수집·시각화"],
    }
}

# (예시) 성취기준 힌트(간단 샘플): "코드 - 설명" 형태
STANDARDS_HINT = {
    "국어": {
        "초4": [
            "[4국03-04] 목적과 주제를 고려하여 독자에게 마음을 전하는 글을 쓴다.",
            "[4국02-03] 글에서 인물의 마음과 행동을 파악한다."
        ]
    },
    "사회": {
        "초4": [
            "[4사06-01] 지역의 문화유산의 가치를 탐색한다.",
            "[4사05-01] 지도의 기본 요소와 정보를 활용하여 지역을 설명한다."
        ]
    },
    "과학": {
        "초4": [
            "[4과01-02] 태양계의 구성과 운동을 탐구한다.",
            "[4과02-01] 물의 상태 변화와 열을 관련지어 설명한다."
        ]
    },
    "도덕": {
        "초4": [
            "[4도03-02] 디지털 환경에서 책임 있는 시민의 태도를 지닌다.",
            "[4도02-01] 배려와 존중의 의미를 이해하고 실천한다."
        ]
    },
    "수학": {
        "초4": [
            "[4수03-02] 분수의 덧셈과 뺄셈의 원리를 이해하고 계산한다.",
            "[4수02-03] 각도와 도형의 성질을 탐구한다."
        ]
    }
}

def get_units(subjects, grade):
    """선택된 교과 리스트에서, 해당 학년에 맞는 추천 단원(중복 제거 후)"""
    out = []
    for s in subjects:
        if s in UNIT_SUGGESTIONS and grade in UNIT_SUGGESTIONS[s]:
            out.extend(UNIT_SUGGESTIONS[s][grade])
    # 중복 제거 + 정렬
    return sorted(list(dict.fromkeys(out)))

def get_standards_hints(subjects, grade):
    """선택된 교과 리스트에서, 해당 학년의 성취기준 예시 모음"""
    out = []
    for s in subjects:
        if s in STANDARDS_HINT and grade in STANDARDS_HINT[s]:
            out.extend(STANDARDS_HINT[s][grade])
    # 중복 제거 유지
    return list(dict.fromkeys(out))

# -----------------------------
# 1) 입력 영역
# -----------------------------
st.header("1. 기본 정보 입력")

col1, col2 = st.columns([1, 1])
with col1:
    theme = st.selectbox(
        "초학문적 주제 선택",
        options=PYP_THEMES,
        index=1,
        help="아래 ‘주제 설명 보기’를 열면 6개 주제의 간단한 설명을 볼 수 있어요."
    )
    grade = st.selectbox("학년 선택", options=GRADES, index=3)

with col2:
    subjects = st.multiselect(
        "교과 선택(복수 선택 가능)",
        options=SUBJECTS,
        default=["사회", "국어"],
        help="여러 교과를 융합해도 좋아요. 선택한 교과에 맞춰 추천 단원과 성취기준 힌트를 보여드려요."
    )

with st.expander("📚 초학문적 주제 설명 보기"):
    for t in PYP_THEMES:
        st.markdown(f"- **{t}**: {PYP_THEME_DESC.get(t.split(' (')[0], PYP_THEME_DESC.get(t, ''))}")

# ----- 단원명 쉽게 입력하기 -----
st.subheader("교과목과 단원명")
unit_suggestions = get_units(subjects, grade)
colu1, colu2 = st.columns([1,1])
with colu1:
    selected_units = st.multiselect(
        "추천 단원에서 선택",
        options=unit_suggestions,
        default=unit_suggestions[:1] if unit_suggestions else [],
        help="추천 단원은 예시입니다. 학교/지역/교과서에 따라 다를 수 있어요."
    )
with colu2:
    extra_units = st.text_input(
        "자유 입력 단원(쉼표로 구분)",
        placeholder="예: 디지털 시민 교육, 우리 지역 답사"
    )

# 교과/단원 조합 문자열 만들기 (자동 조합 버튼)
subject_unit_auto = ""
if st.button("교과/단원 자동 조합 ✨"):
    lines = []
    # 추천 단원 + 자유 입력 합치기
    extras = [u.strip() for u in extra_units.split(",")] if extra_units else []
    extras = [e for e in extras if e]
    combo = list(dict.fromkeys([*selected_units, *extras]))
    if not subjects:
        st.warning("교과를 최소 1개 이상 선택해 주세요.")
    else:
        # 교과별 한 줄씩 조합(단원은 전체 공통으로 붙여줌)
        # 필요 시 교과별로 다른 단원을 적용하도록 커스터마이징 가능
        units_str = " / ".join(combo) if combo else "(단원명 직접 입력)"
        for s in subjects:
            lines.append(f"{s} - {units_str}")
        subject_unit_auto = "\n".join(lines)
        st.success("교과/단원명이 자동 조합되었습니다. 아래 입력창에 반영해 주세요.")

# 최종 교과/단원 입력
subject_unit = st.text_area(
    "최종 교과·단원명 입력",
    value=subject_unit_auto if subject_unit_auto else "",
    placeholder="예: 국어 - 인물에게 마음을 전해요\n사회 - 지도로 만나는 우리 지역"
)

# ----- 성취기준 힌트 -----
st.subheader("성취기준")
std_hints = get_standards_hints(subjects, grade)
colstd1, colstd2 = st.columns([1,1])
with colstd1:
    picked_standards = st.multiselect(
        "성취기준 힌트에서 선택",
        options=std_hints,
        default=std_hints[:1] if std_hints else [],
        help="간단한 예시입니다. 실제 학교/교육과정 상황에 맞게 수정하세요."
    )
with colstd2:
    extra_std = st.text_area(
        "자유 입력 성취기준(여러 줄 가능)",
        placeholder="[코드] 설명 형태 권장\n예: [4국03-04] 목적과 주제를 고려하여 독자에게 마음을 전하는 글을 쓴다."
    )

standards_all = "\n".join([*picked_standards, extra_std]).strip()

# -----------------------------
# 2) 프롬프트 생성
# -----------------------------
st.header("2. 프롬프트 생성")
if st.button("프롬프트 만들기 ✏️"):
    if not theme or not grade or not subject_unit or not standards_all:
        st.error("⚠️ 초학문적 주제, 학년, 교과·단원, 성취기준을 모두 입력/선택해 주세요.")
    else:
        prompt_template = f"""
교사들이 제공하는 정보를 기반으로 IB PYP 수업 설계 결과를 생성합니다.

[입력정보]
- 초학문적 주제: {theme}
- 학년: {grade}
- 교과목과 단원명: {subject_unit}
- 성취기준: {standards_all}

[출력사항] 아래 9가지 항목을 반드시 포함하여 제시합니다.
1. 중심 아이디어(Central Idea)
2. 명시된 개념 3개와 그에 따른 배움 내용 또는 탐구질문 1개
3. 추가개념: 관련 교과의 주요 용어 포함
4. 학습접근방법: 각 방법에 학생활동 2개 이내 포함. 평가요소와 연계
5. 학습자상
6. 탐구목록 LOI(List of Inquiries) 3개를 설계
7. 탐구목록 내 탐구질문(Inquiry Questions) 제안:
   - 탐구시작 질문, 개념적 질문, 토론 질문, 성찰 질문 각각 2개씩
   - 교과 성취기준과 반드시 연계되며, 교과내용 반영 최소 1개 이상 포함
   - 연계된 성취기준을 표시
   - LOI 3개와 각 탐구질문을 모두 포함하는 표로 작성 (가로축=LOI, 세로축=탐구질문 순서)
8. 산출물 또는 수행과제 제안: LOI별 산출물과 수행과제를 제안하며 평가루브릭에 반영 가능하도록 작성
9. 교사용 안내 문장: 수업 운영 포인트와 학부모 안내에 활용 가능하게 작성. 
   예시 참고:
   '본 단원 ‘우리가 속한 공간과 시간’은 학생들이 자신이 살고 있는 지역을 다양한 시각에서 탐구하고, 공간과 시간 속에서 지역의 정체성과 공동체의 가치를 이해하는 것을 목표로 합니다. 
    1차 탐구활동(LOI.1)에서는 종이지도 및 디지털 지도를 활용해 우리 지역의 주요 장소를 조사하고, 지리정보 요소를 가지고 우리 지역과 다른 지역을 비교하여 설명하는 보고서를 제작합니다. 
    2차 탐구활동(LOI.2)에서는 지역의 문화유산을 중심으로 현장 답사를 계획하고 실행합니다.
    학생들은 점차 깊이 있는 질문을 통해 자신의 삶과 지역 사회를 연결하고 사고력을 키워 나갑니다.'

10. 관련된 IB 학습자상
11. 평가루브릭: 학습접근방법에 포함된 내용을 바탕으로 작성

[작성 조건]
- 모든 내용은 입력된 성취기준과 주제를 반영해야 합니다.
- 결과물은 한국어로 작성합니다.
"""
        final_prompt = textwrap.dedent(prompt_template).strip()

        st.subheader("📋 생성된 프롬프트")
        st.code(final_prompt, language="markdown")

        st.download_button(
            label="프롬프트 다운로드",
            data=final_prompt,
            file_name="IB_prompt.txt",
            mime="text/plain"
        )

        st.success("프롬프트가 생성되었습니다! ChatGPT나 다른 LLM에 그대로 붙여넣어 사용하세요.")
