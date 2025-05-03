# streamlit_app
# Winner predictor

import streamlit as st
import pickle
from functions import * 
import numpy as np

st.set_page_config(page_title="win predictor")
st.header("IPL Win predictor")
st.write("based on situation in 2nd innings")

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
    bat_first= st.selectbox("team that first bat (the defenders)", options= teams)
    target= st.number_input("target score", min_value= 0, step= 1)

with col2:
    bat_second= st.selectbox("team batting now (the chasers)", options= teams)
    overs= st.text_input("current over input as {over}.{ball}", value="0.0", max_chars=4)
    runs= st.number_input("current score", min_value= 0, step= 1)
    wickets= st.number_input("wickets lost", min_value= 0, max_value= 10, step= 1)

#encode the teams
with open('label_encoder (1).pkl', 'rb') as file:
    loaded_le = pickle.load(file)

bat_first_le= float(loaded_le.transform([bat_first]))
bat_second_le = float(loaded_le.transform([bat_second]))
runs_to_get = target - runs

#balls remaining
overs= overs.split(".")
over= int(overs[0])
ball= int(overs[1])
if ball >=6:
    st.warning("ball ranges from 0 to 5")
balls_played= (over * 6) + ball 
balls_left = float(120 - balls_played)

#crr
crr= float(get_crr(runs, over, ball))

#rrr
rrr= float(get_rrr(runs_to_get, balls_left))

#wc
wc_left= float(wicket_left(wickets))


imput= np.array([bat_first_le, bat_second_le, float(target), runs_to_get, balls_left, crr, rrr, wc_left])
imput= imput.reshape(1,-1)

#load rf model and predict
with open('rfc_model.pkl', 'rb') as file:
    loaded_rfc = pickle.load(file)

output= loaded_rfc.predict_proba(imput)

if wc_left== 0 and runs_to_get> 0:
    output = np.array([1,0]).reshape(1,-1)
elif rrr > 36:
    output = np.array([1,0]).reshape(1,-1)
elif target < runs:
    output = np.array([1,0]).reshape(1,-1)



#------------------UI-----------------------
if output.shape == (1, 2):
    team1_prob = output[0, 0]
    team2_prob = output[0, 1]

    st.markdown(
        f"""
        <style>
            .progress-container {{
                display: flex;
                align-items: center;
                width: 100%;
                border: 1px solid #ccc;
                border-radius: 5px;
                overflow: hidden;
                margin-bottom: 10px;
            }}
            .progress-bar-left {{
                background-color: #4CAF50; /* Team 1 color */
                color: white;
                text-align: center;
                border-right: 1px solid #ccc;
                flex-grow: {team1_prob};
                padding: 5px 0;
            }}
            .progress-bar-right {{
                background-color: #f44336; /* Team 2 color */
                color: white;
                text-align: center;
                flex-grow: {team2_prob};
                padding: 5px 0;
            }}
            .team-label-left {{
                margin-right: 10px;
                font-weight: bold;
            }}
            .team-label-right {{
                margin-left: 10px;
                font-weight: bold;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div style="display: flex; align-items: center;">
            <div class="team-label-left">{bat_first}</div>
            <div class="progress-container">
                <div class="progress-bar-left">{team1_prob:.2%}</div>
                <div class="progress-bar-right">{team2_prob:.2%}</div>
            </div>
            <div class="team-label-right">{bat_second}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.error("Output array should have a shape of (1, 2)")

st.write(f"{runs_to_get} needed from {balls_left} balls. RRR is {rrr}")
