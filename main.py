import datetime
import glob
import os
import streamlit as st
import plotly.express as px

from nltk.sentiment import SentimentIntensityAnalyzer

diary = "diary"
if not os.path.exists(diary):
    os.mkdir(diary)

filepaths = sorted(glob.glob(f"{diary}/*.txt"))

analyser = SentimentIntensityAnalyzer()

if len(filepaths) > 0:
    negativity = []
    positivity = []
    for filepath in filepaths:
        with open(filepath) as file:
            content = file.read()
        scores = analyser.polarity_scores(content)
        positivity.append(scores["pos"])
        negativity.append(scores["neg"])

    dates = [os.path.splitext(os.path.basename(name))[0] for name in filepaths]

    st.title("Your Diary Analysis")
    st.subheader("Positivity")
    positive = px.line(x=dates, y=positivity,
                       labels={"x": "Date", "y": "Positivity"})
    st.plotly_chart(positive)

    st.subheader("Negativity")
    positive = px.line(x=dates, y=negativity,
                       labels={"x": "Date", "y": "Negativity"})
    st.plotly_chart(positive)

else:
    st.warning("No data available to analyze.")

st.header("New Diary Note")
note = st.text_area("Write your diary note here:")
if st.button("Save Note"):
    now = datetime.datetime.now()
    filename = f"{now.strftime('%Y-%m-%d')}.txt"
    filepath = os.path.join(diary, filename)
    with open(filepath, "w") as file:
        file.write(note)
    st.success(f"Note saved to {filepath}")



