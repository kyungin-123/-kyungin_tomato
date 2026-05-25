import streamlit as st
import pandas as pd
import joblib

# ---------------- 페이지 설정 ----------------
st.set_page_config(
    page_title="토마토 착과율 예측",
    page_icon="🍅",
    layout="centered"
)

# ---------------- CSS ----------------
st.markdown("""
<style>

/* 전체 배경 */
.stApp {
    background: linear-gradient(to bottom, #87CEEB 0%, #dff6ff 35%, #8B5A2B 35%, #6f4518 100%);
    background-attachment: fixed;
}

/* 제목 */
.title {
    text-align: center;
    font-size: 52px;
    font-weight: bold;
    color: white;
    margin-top: 20px;
    text-shadow: 3px 3px 10px rgba(0,0,0,0.4);
}

/* 설명 */
.subtitle {
    text-align: center;
    font-size: 20px;
    color: #f5f5f5;
    margin-bottom: 35px;
}

/* 입력 카드 */
.input-box {
    background: rgba(255,255,255,0.92);
    padding: 35px;
    border-radius: 25px;
    box-shadow: 0px 10px 25px rgba(0,0,0,0.25);
}

/* 버튼 */
.stButton>button {
    width: 100%;
    height: 60px;
    border-radius: 15px;
    border: none;
    background: linear-gradient(90deg, #2e8b57, #228b22);
    color: white;
    font-size: 22px;
    font-weight: bold;
    transition: 0.3s;
}

/* 버튼 호버 */
.stButton>button:hover {
    transform: scale(1.02);
    background: linear-gradient(90deg, #228b22, #006400);
}

/* 결과 박스 */
.result-box {
    background: linear-gradient(135deg, #ff6347, #ff4500);
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    color: white;
    font-size: 34px;
    font-weight: bold;
    margin-top: 30px;
    box-shadow: 0px 8px 20px rgba(0,0,0,0.3);
}

/* 슬라이더 색 */
.stSlider > div > div > div > div {
    background-color: #228b22;
}

</style>
""", unsafe_allow_html=True)

# ---------------- 모델 불러오기 ----------------
rf_model = joblib.load("tomato_model.pkl")

# ---------------- 제목 ----------------
st.markdown(
    '<div class="title">🍅 스마트팜 착과율 예측</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">토마토 생육 환경 데이터를 분석하여 착과율을 예측합니다</div>',
    unsafe_allow_html=True
)

# ---------------- 입력 영역 ----------------
st.markdown('<div class="input-box">', unsafe_allow_html=True)

st.subheader("🌱 환경 데이터 입력")

temp = st.slider("🌡 내부온도 (°C)", 0.0, 50.0, 25.0)
humidity = st.slider("💧 내부습도 (%)", 0.0, 100.0, 60.0)
soil_temp = st.slider("🪴 지온 (°C)", 0.0, 50.0, 20.0)

st.markdown("")

predict_btn = st.button("🚜 착과율 예측하기")

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
        <div class="result-box">
            🍅 예측 착과율<br><br>
            {predicted[0]:.1f}%
        </div>
        """,
        unsafe_allow_html=True
    )

    if predicted[0] >= 80:
        st.success("🌟 매우 좋은 재배 환경입니다!")
    elif predicted[0] >= 60:
        st.info("👍 양호한 환경 상태입니다.")
    else:
        st.warning("⚠️ 환경 조절이 필요할 수 있습니다.")
