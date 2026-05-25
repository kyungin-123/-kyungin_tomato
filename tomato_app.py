import streamlit as st
import pandas as pd
import joblib
import time

# ---------------- 페이지 설정 ----------------
st.set_page_config(
    page_title="SMART FARM AI",
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
    #87CEEB 0%,
    #b8ecff 25%,
    #78c850 25%,
    #4c9a2a 45%,
    #6d4420 45%,
    #3d2412 100%);
    overflow-x: hidden;
}

/* ===== 상단 흰 바 제거 ===== */
header {
    visibility: hidden;
}

[data-testid="stToolbar"] {
    display: none;
}

[data-testid="stDecoration"] {
    display: none;
}

[data-testid="stStatusWidget"] {
    display: none;
}

/* 메인 컨테이너 */
.block-container {
    padding-top: 1rem;
}

/* 제목 */
.main-title {
    text-align: center;
    font-size: 72px;
    font-weight: 900;
    color: white;
    letter-spacing: 4px;

    animation: titleGlow 2s infinite alternate;

    text-shadow:
    0 0 10px rgba(255,255,255,0.6),
    0 0 20px rgba(0,255,100,0.7),
    0 0 40px rgba(0,255,100,0.9);
}

/* 제목 애니메이션 */
@keyframes titleGlow {
    from {
        transform: scale(1);
    }

    to {
        transform: scale(1.02);
    }
}

/* 부제목 */
.sub-title {
    text-align: center;
    font-size: 24px;
    color: white;
    margin-bottom: 40px;
    animation: fadeUp 1.2s ease;
}

/* 카드 */
.glass-card {

    background: rgba(255,255,255,0.12);

    backdrop-filter: blur(18px);

    border: 1px solid rgba(255,255,255,0.2);

    padding: 35px;

    border-radius: 30px;

    box-shadow:
    0 8px 32px rgba(0,0,0,0.35);

    animation: fadeUp 1s ease;
}

/* 등장 애니메이션 */
@keyframes fadeUp {

    from {
        opacity: 0;
        transform: translateY(30px);
    }

    to {
        opacity: 1;
        transform: translateY(0px);
    }
}

/* 섹션 제목 */
.section-title {
    font-size: 34px;
    font-weight: bold;
    color: white;
    margin-bottom: 25px;
}

/* 슬라이더 색 */
.stSlider > div > div > div > div {
    background: linear-gradient(90deg,#00ff88,#00d4ff);
}

/* 슬라이더 숫자 */
.stSlider label {
    color: white !important;
    font-size: 20px !important;
    font-weight: bold !important;
}

/* 버튼 */
.stButton > button {

    width: 100%;

    height: 75px;

    border-radius: 20px;

    border: none;

    font-size: 28px;

    font-weight: bold;

    color: white;

    background: linear-gradient(90deg,#00c853,#00e676);

    box-shadow:
    0 0 15px rgba(0,255,100,0.6),
    0 0 35px rgba(0,255,100,0.5);

    transition: all 0.3s ease;
}

/* 버튼 호버 */
.stButton > button:hover {

    transform: translateY(-5px) scale(1.02);

    box-shadow:
    0 0 25px rgba(0,255,100,0.9),
    0 0 50px rgba(0,255,100,0.8);

    background: linear-gradient(90deg,#00e676,#76ff03);
}

/* metric 카드 */
[data-testid="metric-container"] {

    background: rgba(255,255,255,0.1);

    border-radius: 20px;

    padding: 20px;

    box-shadow:
    0 5px 20px rgba(0,0,0,0.2);

    animation: pulse 2s infinite;
}

/* metric 애니메이션 */
@keyframes pulse {

    0% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.03);
    }

    100% {
        transform: scale(1);
    }
}

/* 결과 카드 */
.result-card {

    margin-top: 40px;

    background:
    linear-gradient(135deg,#ff512f,#dd2476);

    padding: 50px;

    border-radius: 35px;

    text-align: center;

    color: white;

    animation: resultGlow 1.5s infinite alternate;

    box-shadow:
    0 0 20px rgba(255,0,100,0.6),
    0 0 50px rgba(255,0,100,0.7);
}

/* 결과 glow */
@keyframes resultGlow {

    from {
        transform: scale(1);
    }

    to {
        transform: scale(1.02);
    }
}

/* 결과 숫자 */
.result-number {

    font-size: 90px;

    font-weight: 900;

    margin-top: 15px;
}

/* 스크롤바 제거 */
::-webkit-scrollbar {
    display: none;
}

</style>
""", unsafe_allow_html=True)

# ---------------- 모델 로드 ----------------
rf_model = joblib.load("tomato_model.pkl")

# ---------------- 제목 ----------------
st.markdown(
    '<div class="main-title">🍅 SMART FARM AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">차세대 AI 기반 토마토 착과율 예측 시스템</div>',
    unsafe_allow_html=True
)

# ---------------- 레이아웃 ----------------
left, right = st.columns([1.3, 1])

# ---------------- 왼쪽 ----------------
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

# ---------------- 오른쪽 ----------------
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

    # 로딩 애니메이션
    with st.spinner("🤖 AI가 환경을 분석중입니다..."):
        time.sleep(2)

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

    # 상태 메시지
    if predicted[0] >= 85:

        st.success("🌟 최적의 스마트팜 환경입니다!")

        st.balloons()

    elif predicted[0] >= 65:

        st.info("👍 양호한 생육 환경입니다.")

    else:

        st.warning("⚠️ 환경 조절이 필요합니다.")
