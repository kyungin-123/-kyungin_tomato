import streamlit as st
import pandas as pd
import joblib

# ---------------- 페이지 설정 ----------------
st.set_page_config(
    page_title="Smart Farm AI",
    page_icon="🍅",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>

/* 전체 배경 */
.stApp {
    background:
        linear-gradient(to bottom,
        #6ec6ff 0%,
        #b3ecff 30%,
        #7ec850 30%,
        #5f9f3e 45%,
        #6b3f1d 45%,
        #4b2e14 100%);
    overflow: hidden;
}

/* 상단 제목 */
.main-title {
    text-align: center;
    font-size: 68px;
    font-weight: 900;
    color: white;
    letter-spacing: 3px;
    text-shadow: 4px 4px 20px rgba(0,0,0,0.45);
    margin-top: 10px;
}

/* 부제목 */
.sub-title {
    text-align: center;
    font-size: 24px;
    color: #f2f2f2;
    margin-bottom: 40px;
    text-shadow: 2px 2px 10px rgba(0,0,0,0.3);
}

/* 유리온실 카드 */
.glass-card {
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(15px);
    padding: 40px;
    border-radius: 30px;
    border: 1px solid rgba(255,255,255,0.3);
    box-shadow: 0px 10px 35px rgba(0,0,0,0.35);
}

/* 섹션 제목 */
.section-title {
    font-size: 32px;
    font-weight: bold;
    color: white;
    margin-bottom: 20px;
}

/* 슬라이더 */
.stSlider > div > div > div > div {
    background: linear-gradient(90deg,#00ff87,#60efff);
}

/* 버튼 */
.stButton>button {
    width: 100%;
    height: 75px;
    border-radius: 18px;
    border: none;
    background: linear-gradient(90deg,#00c853,#64dd17);
    color: white;
    font-size: 28px;
    font-weight: bold;
    box-shadow: 0px 8px 25px rgba(0,0,0,0.3);
    transition: all 0.3s ease;
}

/* 버튼 호버 */
.stButton>button:hover {
    transform: translateY(-3px) scale(1.02);
    background: linear-gradient(90deg,#00e676,#76ff03);
}

/* 결과 카드 */
.result-card {
    background: linear-gradient(135deg,#ff512f,#dd2476);
    border-radius: 30px;
    padding: 40px;
    text-align: center;
    color: white;
    margin-top: 35px;
    box-shadow: 0px 10px 35px rgba(0,0,0,0.4);
    animation: glow 2s infinite alternate;
}

/* 결과 숫자 */
.result-number {
    font-size: 80px;
    font-weight: 900;
    margin-top: 15px;
}

/* glow 애니메이션 */
@keyframes glow {
    from {
        box-shadow: 0px 0px 20px rgba(255,80,80,0.4);
    }
    to {
        box-shadow: 0px 0px 40px rgba(255,80,80,0.9);
    }
}

/* 입력 라벨 */
label {
    font-size: 20px !important;
    font-weight: bold !important;
    color: white !important;
}

/* metric 카드 */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.15);
    border-radius: 20px;
    padding: 15px;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.2);
}

/* 스크롤바 제거 */
::-webkit-scrollbar {
    display: none;
}

</style>
""", unsafe_allow_html=True)

# ---------------- 모델 불러오기 ----------------
rf_model = joblib.load("tomato_model.pkl")

# ---------------- 제목 ----------------
st.markdown(
    '<div class="main-title">🍅 SMART FARM AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">AI 기반 토마토 착과율 예측 시스템</div>',
    unsafe_allow_html=True
)

# ---------------- 레이아웃 ----------------
left, right = st.columns([1.2, 1])

# ---------------- 왼쪽 입력창 ----------------
with left:

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">🌱 환경 데이터 입력</div>',
        unsafe_allow_html=True
    )

    temp = st.slider("🌡 내부온도 (°C)", 0.0, 50.0, 25.0)
    humidity = st.slider("💧 내부습도 (%)", 0.0, 100.0, 60.0)
    soil_temp = st.slider("🪴 지온 (°C)", 0.0, 50.0, 20.0)

    st.markdown("###")

    predict_btn = st.button("🚀 AI 예측 시작")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- 오른쪽 대시보드 ----------------
with right:

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">📊 실시간 환경 상태</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric("온도", f"{temp:.1f}°C")

    with col2:
        st.metric("습도", f"{humidity:.1f}%")

    st.metric("지온", f"{soil_temp:.1f}°C")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- 예측 ----------------
if predict_btn:

    input_data = pd.DataFrame(
        [[temp, humidity, soil_temp]],
        columns=['내부온도', '내부습도', '지온']
    )

    predicted = rf_model.predict(input_data)

    st.markdown(
        f"""
        <div class="result-card">
            🍅 AI 예측 착과율
            <div class="result-number">
                {predicted[0]:.1f}%
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 상태 표시
    if predicted[0] >= 85:
        st.success("🌟 최적의 스마트팜 환경입니다!")
        st.balloons()

    elif predicted[0] >= 65:
        st.info("👍 양호한 생육 환경입니다.")

    else:
        st.warning("⚠️ 환경 조절이 필요합니다.")
