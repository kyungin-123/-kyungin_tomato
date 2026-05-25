import streamlit as st
import pandas as pd
import joblib
import time

# ---------------- 설정 ----------------
st.set_page_config(
    page_title="Smart Farm AI",
    page_icon="🍅",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>

/* 상단바 제거 */
header {
    visibility: hidden;
}

[data-testid="stToolbar"] {
    display: none;
}

[data-testid="stDecoration"] {
    display: none;
}

/* 전체 배경 */
.stApp {
    background: linear-gradient(to bottom, #eefbf3, #dff5e7);
}

/* 메인 */
.block-container {
    padding-top: 1.5rem;
}

/* 제목 */
.main-title {
    text-align: center;
    font-size: 64px;
    font-weight: 800;
    color: #1b4332;

    animation: fadeIn 1s ease;
}

/* 부제목 */
.sub-title {
    text-align: center;
    font-size: 22px;
    color: #52796f;
    margin-bottom: 45px;

    animation: fadeIn 1.5s ease;
}

/* 카드 */
.card {

    background: rgba(255,255,255,0.75);

    backdrop-filter: blur(10px);

    border-radius: 28px;

    padding: 35px;

    box-shadow:
    0 8px 30px rgba(0,0,0,0.08);

    border: 1px solid rgba(255,255,255,0.4);

    animation: slideUp 0.8s ease;
}

/* 카드 hover */
.card:hover {

    transform: translateY(-3px);

    transition: 0.3s;
}

/* 섹션 제목 */
.section-title {
    font-size: 30px;
    font-weight: 700;
    color: #1b4332;
    margin-bottom: 20px;
}

/* 슬라이더 */
.stSlider > div > div > div > div {
    background: linear-gradient(90deg,#52b788,#74c69d);
}

/* 슬라이더 글씨 */
label {
    font-size: 18px !important;
    font-weight: 600 !important;
    color: #2d6a4f !important;
}

/* 버튼 */
.stButton > button {

    width: 100%;

    height: 68px;

    border-radius: 18px;

    border: none;

    background: linear-gradient(90deg,#40916c,#52b788);

    color: white;

    font-size: 24px;

    font-weight: 700;

    transition: 0.3s;

    box-shadow:
    0 8px 20px rgba(82,183,136,0.25);
}

/* 버튼 hover */
.stButton > button:hover {

    transform: scale(1.02);

    background: linear-gradient(90deg,#2d6a4f,#40916c);
}

/* metric 카드 */
[data-testid="metric-container"] {

    background: rgba(255,255,255,0.6);

    border-radius: 20px;

    padding: 20px;

    box-shadow:
    0 5px 18px rgba(0,0,0,0.06);
}

/* 결과 카드 */
.result-card {

    margin-top: 35px;

    padding: 45px;

    border-radius: 30px;

    background:
    linear-gradient(135deg,#40916c,#74c69d);

    text-align: center;

    color: white;

    animation: pop 0.6s ease;

    box-shadow:
    0 10px 30px rgba(0,0,0,0.15);
}

/* 결과 숫자 */
.result-number {

    font-size: 82px;

    font-weight: 900;

    margin-top: 10px;
}

/* 애니메이션 */
@keyframes fadeIn {

    from {
        opacity: 0;
    }

    to {
        opacity: 1;
    }
}

@keyframes slideUp {

    from {
        opacity: 0;
        transform: translateY(30px);
    }

    to {
        opacity: 1;
        transform: translateY(0px);
    }
}

@keyframes pop {

    0% {
        transform: scale(0.8);
        opacity: 0;
    }

    100% {
        transform: scale(1);
        opacity: 1;
    }
}

</style>
""", unsafe_allow_html=True)

# ---------------- 모델 ----------------
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

# ---------------- 입력 ----------------
with left:

    st.markdown('<div class="card">', unsafe_allow_html=True)

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

# ---------------- 상태창 ----------------
with right:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">📊 실시간 상태</div>',
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

    with st.spinner("AI 분석 중..."):
        time.sleep(1.5)

    input_data = pd.DataFrame(
        [[temp, humidity, soil_temp]],
        columns=['내부온도', '내부습도', '지온']
    )

    predicted = rf_model.predict(input_data)

    st.markdown(
        f'''
        <div class="result-card">
            🍅 예측 착과율
            <div class="result-number">
                {predicted[0]:.1f}%
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )

    if predicted[0] >= 85:
        st.success("🌟 최적의 생육 환경입니다!")
        st.balloons()

    elif predicted[0] >= 65:
        st.info("👍 양호한 환경 상태입니다.")

    else:
        st.warning("⚠️ 환경 조절이 필요합니다.")
