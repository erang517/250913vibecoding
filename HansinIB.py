import streamlit as st
st.title('한신초 IB 탐구설계 도우미')
st.write('탐구설계 도우미!')
# streamlit_app.py
import streamlit as st
import textwrap

st.set_page_config(page_title="IB 수업 설계 프롬프트 생성기", layout="wide")

st.title("🌐 IB 수업 설계 프롬프트 생성기")
st.caption("교사가 입력한 정보를 기반으로 ChatGPT에 바로 넣을 수 있는 완성형 프롬프트를 생성합니다.")

# ---- 입력 영역 ----
st.header("1. 기본 정보 입력")

col1, col2 = st.columns(2)
with col1:
    theme = st.text_input("초학문적 주제", placeholder="예: 우리가 속한 공간과 시간 (Where we are in place and time)")
    grade = st.text_input("학년", placeholder="예: 4학년")

with col2:
    subject_unit = st.text_area("교과목과 단원명", placeholder="예: 국어 - 인물에게 마음을 전해요\n사회 - 지도로 만나는 우리 지역")
    standards = st.text_area("성취기준", placeholder="[4국03-04] 목적과 주제를 고려하여 독자에게 마음을 전하는 글을 쓴다.\n[4사06-01] 지역의 문화유산의 가치를 탐색한다.")

# ---- 프롬프트 생성 버튼 ----
st.header("2. 프롬프트 생성")
if st.button("프롬프트 만들기 ✏️"):
    if not theme or not grade or not subject_unit or not standards:
        st.error("⚠️ 모든 항목을 입력해 주세요.")
    else:
        # 프롬프트 템플릿
        prompt_template = f"""
교사들이 제공하는 정보를 기반으로 IB PYP 수업 설계 결과를 생성합니다.

[입력정보]
- 초학문적 주제: {theme}
- 학년: {grade}
- 교과목과 단원명: {subject_unit}
- 성취기준: {standards}

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

        # 들여쓰기 정리
        final_prompt = textwrap.dedent(prompt_template).strip()

        st.subheader("📋 생성된 프롬프트")
        st.code(final_prompt, language="markdown")

        # 다운로드 기능
        st.download_button(
            label="프롬프트 다운로드",
            data=final_prompt,
            file_name="IB_prompt.txt",
            mime="text/plain"
        )

        st.success("프롬프트가 생성되었습니다! ChatGPT나 다른 LLM에 그대로 붙여넣어 사용하세요.")
