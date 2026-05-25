import streamlit as st
import pandas as pd
import joblib

# 모델 불러오기
rf_model = joblib.load("tomato_model.pkl")

st.title("🍅 착과율 예측 프로그램")

st.write("내부 환경 데이터를 입력하면 예상 착과율을 예측합니다.")

# 사용자 입력
temp = st.number_input("내부온도 입력", value=25.0)
humidity = st.number_input("내부습도 입력", value=60.0)
soil_temp = st.number_input("지온 입력", value=20.0)

# 예측 버튼
if st.button("예측하기"):

    # DataFrame 생성
    input_data = pd.DataFrame(
        [[temp, humidity, soil_temp]],
        columns=['내부온도', '내부습도', '지온']
    )

    # 예측
    predicted = rf_model.predict(input_data)

    # 결과 출력
    st.success(f"예측 착과율 : {predicted[0]:.1f}%")