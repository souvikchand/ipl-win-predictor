# streamlit_app
# Proctored Score

import streamlit as st
import pickle
from functions import * 
import numpy as np


st.set_page_config(page_title="Predicted Score")
st.header("Predicted Score")

teams= ["Chennai Super Kings",
        "Delhi Capitals",
        "Gujarat Titans",
        "Kolkata Knight Riders",
        "Lucknow Super Giants",
        "Mumbai Indians",
        "Punjab Kings",
        "Rajasthan Royals",
        "Royal Challengers Bangalore",
        "Sunrisers Hyderabad"]

col1,col2 = st.columns([0.5, 0.5])

with col1:
    batting_now= st.selectbox("team that batting now", options= teams)
    innigs= st.selectbox("current innings", options= [1,2])
    over= st.text_input("current over input as {over}.{ball}", value="0.0", max_chars=4)
    wickets= st.number_input("wickets fallen", min_value=0, max_value=10)

with col2:
    bowling_now = st.selectbox("team that bowling now", options= teams)
    runs= st.number_input("runs till now", min_value=0)

with open('label_encoder (1).pkl', 'rb') as file:
    loaded_le = pickle.load(file)


bat_first_le= float(loaded_le.transform([batting_now]))
bat_second_le = float(loaded_le.transform([bowling_now]))

overs= over.split(".")
over= int(overs[0])
ball= int(overs[1])
if ball >=6:
    st.warning("ball ranges from 0 to 5")
balls_played= (over * 6) + ball 
balls_left = float(120 - balls_played)

#crr
crr= float(get_crr(runs, over, ball))

wc_left= float(wicket_left(wickets))

imput= np.array([float(innigs), bat_first_le, bat_second_le, float(runs), wc_left, crr, balls_left])
imput= imput.reshape(1,-1)

#load rf model and predict
with open('rfr_model (1).pkl', 'rb') as file:
    loaded_rfr = pickle.load(file)

output= np.round(loaded_rfr.predict(imput))
st.write(f"Predicted score: {int(output)}")

