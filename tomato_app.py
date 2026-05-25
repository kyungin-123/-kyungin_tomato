import streamlit as st
import pandas as pd
import joblib

# 페이지 설정
st.set_page_config(
    page_title="토마토 착과율 예측",
    page_icon="🍅",
    layout="centered"
)

# CSS 꾸미기
st.markdown("""
<style>

.main {
    background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
}

.stApp {
    background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
}

.title {
    text-align: center;
    font-size: 50px;
    font-weight: bold;
    color: #b22222;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    font-size: 20px;
    color: #444444;
    margin-bottom: 40px;
}

.box {
    background-color: rgba(255,255,255,0.85);
    padding: 30px;
    border-radius: 25px;
    box-shadow: 0px 8px 20px rgba(0,0,0,0.2);
}

.result-box {
    background: linear-gradient(135deg, #ff416c, #ff4b2b);
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    color: white;
    font-size: 32px;
    font-weight: bold;
    margin-top: 30px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.3);
}

.stButton>button {
    width: 100%;
    height: 60px;
    border-radius: 15px;
    border: none;
    background: linear-gradient(90deg, #ff512f, #dd2476);
    color: white;
    font-size: 22px;
    font-weight: bold;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.03);
    background: linear-gradient(90deg, #dd2476, #ff512f);
}

</style>
""", unsafe_allow_html=True)

# 모델 불러오기
rf_model = joblib.load("tomato_model.pkl")

# 제목
st.markdown('<div class="title">🍅 토마토 착과율 AI 예측</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">스마트팜 환경 데이터를 기반으로 착과율을 예측합니다</div>',
    unsafe_allow_html=True
)

# 입력창 박스
with st.container():
    st.markdown('<div class="box">', unsafe_allow_html=True)

    st.subheader("🌡 환경 데이터 입력")

    temp = st.slider("내부온도 (°C)", 0.0, 50.0, 25.0)
    humidity = st.slider("내부습도 (%)", 0.0, 100.0, 60.0)
    soil_temp = st.slider("지온 (°C)", 0.0, 50.0, 20.0)

    st.markdown("")

    predict_btn = st.button("🚀 착과율 예측하기")

    st.markdown('</div>', unsafe_allow_html=True)

# 예측
if predict_btn:

    input_data = pd.DataFrame(
        [[temp, humidity, soil_temp]],
        columns=['내부온도', '내부습도', '지온']
    )

    predicted = rf_model.predict(input_data)

    st.markdown(
        f'''
        <div class="result-box">
            🍅 예측 착과율<br><br>
            {predicted[0]:.1f}%
        </div>
        ''',
        unsafe_allow_html=True
    )

    # 추가 메시지
    if predicted[0] >= 80:
        st.success("매우 좋은 환경입니다! 🎉")
    elif predicted[0] >= 60:
        st.info("양호한 환경 상태입니다 👍")
    else:
        st.warning("환경 조절이 필요할 수 있습니다 ⚠️")
