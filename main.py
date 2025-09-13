import streamlit as st
st.title('나의 첫 웹앱!')
st.write('이걸 내가 만들었다고?!')
# app.py
import streamlit as st
import random

# ----------------------------
# 기본 설정
# ----------------------------
st.set_page_config(page_title="학생 기질 맞춤 양육 가이드", page_icon="🎯", layout="centered")
st.title("👩‍👧‍👦 학생 기질 유형 맞춤 양육 가이드")
st.markdown("#### 기질을 선택하면 과학적 연구 기반 양육 전략을 추천해드려요 🎉")

# ----------------------------
# 기질 유형 데이터
# ----------------------------
parenting_tips = {
    "다혈질 (🔥 활발하고 사교적)": {
        "설명": "활발하고 감정 표현이 풍부하며, 친구를 잘 사귀고 새로운 경험을 좋아하는 아이입니다.",
        "추천": [
            "✨ **칭찬을 아낌없이** 해주어 자존감을 높여주세요.",
            "🎨 **다양한 활동**을 경험하게 하여 호기심을 충족시켜 주세요.",
            "📏 짧고 **명확한 규칙**을 제공해 집중할 수 있도록 지도하세요.",
            "🤝 또래와의 협력 활동을 자주 경험하게 해주세요."
        ]
    },
    "우울질 (🍂 신중하고 감성적인)": {
        "설명": "내향적이고 세심하며, 감정이 풍부하고 완벽주의 성향을 가진 아이입니다.",
        "추천": [
            "💌 **감정을 표현**할 수 있는 글쓰기, 미술 활동을 권장하세요.",
            "🗓️ **충분한 시간**을 주고 서두르지 않도록 지도하세요.",
            "🤗 비판보다는 **공감과 지지**로 안정감을 주세요.",
            "🌱 실수와 실패를 성장의 기회로 바라볼 수 있게 도와주세요."
        ]
    },
    "담즙질 (⚡ 목표지향적이고 리더십 강함)": {
        "설명": "목표가 뚜렷하고 추진력이 강하며, 주도적으로 행동하는 아이입니다.",
        "추천": [
            "🏆 리더십을 발휘할 수 있는 **역할과 책임**을 주세요.",
            "🛠️ 스스로 **문제를 해결**할 기회를 제공하세요.",
            "⚖️ 단호하지만 **일관된 규칙**으로 균형을 잡아주세요.",
            "🌟 성취와 노력의 과정을 함께 **성찰**하게 도와주세요."
        ]
    },
    "점액질 (🌊 차분하고 온화한)": {
        "설명": "차분하고 안정적이며, 갈등을 싫어하고 인내심이 강한 아이입니다.",
        "추천": [
            "🌿 차분함과 인내심을 **구체적으로 칭찬**해주세요.",
            "🐢 작은 변화부터 서서히 **적응할 기회**를 제공하세요.",
            "🏡 안정된 환경에서 **스스로 결정**하도록 기회를 주세요.",
            "🤝 갈등 상황에서 **중재자 역할**을 경험하게 하세요."
        ]
    }
}

# ----------------------------
# 사용자 입력
# ----------------------------
temperament = st.selectbox(
    "학생의 기질 유형을 선택하세요",
    options=list(parenting_tips.keys()),
    index=0
)

# ----------------------------
# 버튼 클릭 시 결과 출력
# ----------------------------
if st.button("양육 전략 확인하기 🚀"):
    selected = parenting_tips[temperament]
    st.subheader(f"✨ {temperament} ✨")
    st.write(f"**특징 설명:** {selected['설명']}")
    
    st.markdown("---")
    st.markdown("### 💡 맞춤 양육 전략")
    
    for tip in selected["추천"]:
        st.write(f"- {tip}")
    
    # 랜덤 재미 요소
    effect = random.choice(["balloons", "snow"])
    if effect == "balloons":
        st.balloons()
    else:
        st.snow()
    
    st.success("양육의 즐거움이 가득하길 바랍니다 🌈💖")

# ----------------------------
# 푸터
# ----------------------------
st.markdown("---")
st.caption("출처: Thomas & Chess 기질 연구, 한국 아동·청소년 기질 및 성격검사 연구(KPRC, CBCL 등)")
# streamlit_app.py
import streamlit as st
import pandas as pd
import altair as alt
import os

st.set_page_config(page_title="MBTI 유형별 Top 10 국가", layout="wide")

st.title("MBTI 유형별 비율이 가장 높은 국가 Top 10 📊")
st.caption("같은 폴더에 CSV가 있으면 기본적으로 그 파일을 사용하고, 없을 경우 업로드한 파일을 사용합니다.")

# ---- Sidebar ----
st.sidebar.header("설정")
uploaded = st.sidebar.file_uploader("CSV 업로드", type=["csv"])
top_n = st.sidebar.slider("Top N", min_value=5, max_value=20, value=10, step=1)
as_percent = st.sidebar.checkbox("값을 %로 보기", value=True)
show_table = st.sidebar.checkbox("표도 함께 보기", value=False)

# 16개 MBTI 유형
MBTI_TYPES = [
    "INTJ","INTP","ENTJ","ENTP",
    "INFJ","INFP","ENFJ","ENFP",
    "ISTJ","ISFJ","ESTJ","ESFJ",
    "ISTP","ISFP","ESTP","ESFP"
]

def normalize_columns(cols):
    return [c.strip() for c in cols]

def detect_country_col(df):
    # 국가 컬럼 추정
    candidates = ["country", "Country", "COUNTRY", "국가", "나라"]
    for c in df.columns:
        if c in candidates or "country" in c.lower():
            return c
    return df.columns[0]  # 기본적으로 첫 번째 열을 국가로 가정

def prepare_long(df, country_col):
    # MBTI 열만 추출
    col_map = {}
    for c in df.columns:
        if c.strip().upper() in MBTI_TYPES:
            col_map[c] = c.strip().upper()
    if not col_map:
        st.error("MBTI 유형 열을 찾지 못했어요. 열 이름이 16개 유형과 일치하는지 확인해 주세요.")
        st.stop()

    use_cols = [country_col] + list(col_map.keys())
    skinny = df[use_cols].copy()
    skinny = skinny.rename(columns={country_col: "country", **col_map})

    long_df = skinny.melt(id_vars=["country"], var_name="type", value_name="value")
    long_df["value"] = pd.to_numeric(long_df["value"], errors="coerce")
    long_df = long_df.dropna(subset=["value"])
    return long_df

def detect_scale_hint(long_df):
    # 국가별 합계의 중앙값으로 스케일 추정
    sums = long_df.pivot_table(index="country", columns="type", values="value", aggfunc="first").sum(axis=1)
    med = sums.median()
    if 0.9 <= med <= 1.1:
        return "proportion"  # 0~1 비율
    elif 95 <= med <= 105:
        return "percentage"  # 0~100 퍼센트
    else:
        return "unknown"

def top_n_countries_for_type(long_df, mbti_type, n):
    sub = long_df[long_df["type"] == mbti_type].dropna(subset=["value"]).copy()
    sub = sub.sort_values("value", ascending=False).head(n)
    return sub

# ---- CSV 로드 ----
default_path = "countriesMBTI_16types.csv"

if os.path.exists(default_path):
    # 기본 폴더에 CSV 파일이 있을 경우 우선 사용
    st.success(f"기본 파일을 사용합니다: {default_path}")
    df = pd.read_csv(default_path)
elif uploaded is not None:
    st.success("업로드한 파일을 사용합니다.")
    try:
        df = pd.read_csv(uploaded)
    except Exception:
        uploaded.seek(0)
        df = pd.read_csv(uploaded, encoding="utf-8", engine="python")
else:
    st.error("CSV 파일이 필요합니다. 폴더에 기본 파일을 두거나 업로드해 주세요.")
    st.stop()

df.columns = normalize_columns(df.columns)
country_col = detect_country_col(df)
long_df = prepare_long(df, country_col)
scale_hint = detect_scale_hint(long_df)

# ---- 유형 선택 ----
available_types = sorted(long_df["type"].unique().tolist(), key=lambda x: MBTI_TYPES.index(x) if x in MBTI_TYPES else 999)
sel_type = st.selectbox("MBTI 유형 선택", options=available_types, index=available_types.index("INFP") if "INFP" in available_types else 0)

# Top N 데이터 추출
top_df = top_n_countries_for_type(long_df, sel_type, top_n).copy()

# 값 스케일링
def format_value(v):
    if as_percent:
        if scale_hint == "percentage":
            return v
        else:
            return v * 100.0
    else:
        if scale_hint == "percentage":
            return v / 100.0
        else:
            return v

top_df["display_value"] = top_df["value"].apply(format_value)

value_title = f"{sel_type} 비율" + (" (%)" if as_percent else " (0~1)")

# ---- Altair 그래프 ----
base = alt.Chart(top_df).encode(
    x=alt.X("display_value:Q", title=value_title),
    y=alt.Y("country:N", sort="-x", title="국가"),
    tooltip=[
        alt.Tooltip("country:N", title="국가"),
        alt.Tooltip("display_value:Q", title=value_title, format=".2f"),
    ]
)

bars = base.mark_bar().encode()
text = base.mark_text(
    align="left",
    baseline="middle",
    dx=3
).encode(
    text=alt.Text("display_value:Q", format=".2f")
)

chart = (bars + text).properties(
    width=800,
    height=40 * len(top_df),
    title=f"{sel_type} 비율이 가장 높은 국가 Top {len(top_df)}"
).interactive()

st.altair_chart(chart, use_container_width=True)

# ---- 표 출력 옵션 ----
if show_table:
    pretty = top_df[["country", "type", "display_value"]].rename(columns={
        "country": "국가",
        "type": "유형",
        "display_value": "값" + ("(%)" if as_percent else "")
    })
    st.dataframe(pretty.reset_index(drop=True))

# ---- 품질 진단 ----
with st.expander("데이터 스케일 및 품질 진단"):
    st.write(
        f"- 감지된 스케일: **{('0~1 비율' if scale_hint=='proportion' else ('0~100 퍼센트' if scale_hint=='percentage' else '불명확'))}**"
    )
    sums = long_df.pivot_table(index="country", columns="type", values="value", aggfunc="first").sum(axis=1)
    st.write(f"- 국가별 합계 중앙값: **{sums.median():.3f}**")

