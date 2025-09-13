import streamlit as st
st.title('한신초 IB 탐구설계 도우미')
st.write('탐구설계 도우미!')
# streamlit_app.py
import streamlit as st
import openai
import textwrap
import os

# --- 기본 설정 ---
st.set_page_config(page_title="IB 수업 설계 도우미", layout="wide")
st.title("🌐 IB 수업 설계 도우미")
st.caption("교사가 입력한 정보를 기반으로 AI가 IB PYP 수업 설계안을 자동 생성합니다.")

# --- OpenAI API 키 설정 ---
api_key = st.sidebar.text_input("🔑 OpenAI API Key 입력", type="password")
if api_key:
    openai.api_key = api_key

# --- 입력 영역 ---
st.header("1. 기본 정보 입력")

col1, col2 = st.columns(2)
with col1:
    theme = st.text_input("초학문적 주제", placeholder="예: 우리가 속한 공간과 시간 (Where we are in place and time)")
    grade = st.text_input("학년", placeholder="예: 4학년")

with col2:
    subject_unit = st.text_area("교과목과 단원명", placeholder="예: 국어 - 인물에게 마음을 전해요\n사회 - 지도로 만나는 우리 지역")
    standards = st.text_area("성취기준", placeholder="[4국03-04] 목적과 주제를 고려하여 독자에게 마음을 전하는 글을 쓴다.\n[4사06-01] 지역의 문화유산의 가치를 탐색한다.")

# --- 프롬프트 자동 생성 ---
def build_prompt(theme, grade, subject_unit, standards):
    return textwrap.dedent(f"""
    당신은 IB PYP 교육과정 설계 전문가입니다.
    교사가 제공한 정보를 바탕으로 아래의 출력사항을 포함하여 완성형 IB 수업 설계안을 작성하세요.

    [입력정보]
    - 초학문적 주제: {theme}
    - 학년: {grade}
    - 교과목과 단원명: {subject_unit}
    - 성취기준: {standards}

    [출력사항] 아래 내용을 반드시 포함하여 제시합니다.
    1. 중심 아이디어(Central Idea)
    2. 명시된 개념 3개와 그에 따른 배움 내용 또는 탐구질문 1개
    3. 추가개념: 관련 교과의 주요 용어 포함
    4. 학습접근방법: 각 방법에 학생활동 2개 이내 포함. 평가요소와 연계
    5. 학습자상
    6. 탐구목록 LOI(List of Inquiries) 3개 설계
    7. 탐구목록 내 탐구질문(Inquiry Questions):
       - 탐구시작 질문, 개념적 질문, 토론 질문, 성찰 질문 각각 2개씩
       - 반드시 성취기준과 연계, 교과내용 포함 최소 1개
       - 연계된 성취기준을 명시
       - LOI 3개와 탐구질문을 **표 형식**으로 제시 (가로축=LOI, 세로축=탐구질문 종류)
    8. LOI별 산출물 또는 수행과제 제안 (평가루브릭 반영 가능)
    9. 교사용 안내 문장 (수업 운영 포인트 + 학부모 안내용)
    10. 관련된 IB 학습자상
    11. 평가루브릭: 학습접근방법에 포함된 내용을 기반으로 작성

    [작성 조건]
    - 모든 내용은 제공된 성취기준과 주제를 반드시 반영해야 합니다.
    - 결과물은 한국어로 작성합니다.
    """)

# --- AI 실행 ---
st.header("2. AI 수업 설계 생성")

if st.button("수업 설계안 생성 🚀"):
    if not api_key:
        st.error("⚠️ OpenAI API Key를 입력해주세요.")
    elif not theme or not grade or not subject_unit or not standards:
        st.error("⚠️ 모든 입력 정보를 작성해주세요.")
    else:
        with st.spinner("AI가 수업 설계안을 생성하고 있습니다..."):
            prompt = build_prompt(theme, grade, subject_unit, standards)

            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "당신은 IB PYP 교육과정 설계 전문가입니다."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )

            ai_output = response["choices"][0]["message"]["content"]

        st.subheader("📘 AI가 생성한 IB 수업 설계안")
        st.write(ai_output)

        # 다운로드 버튼
        st.download_button(
            label="💾 결과 다운로드",
            data=ai_output,
            file_name=f"IB_수업설계_{grade}.txt",
            mime="text/plain"
        )
