
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI Student Impact Dashboard", layout="wide")

st.title("🎓 AI Student Impact Dashboard")

uploaded = st.file_uploader("Upload CSV", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)
else:
    try:
        df = pd.read_csv("ai_student_impact_dataset.csv")
        st.info("Using local dataset: ai_student_impact_dataset.csv")
    except Exception:
        st.warning("Upload a CSV file to begin.")
        st.stop()

st.subheader("Dataset Preview")
st.dataframe(df.head())

st.sidebar.header("Filters")

if "Major_Category" in df.columns:
    majors = st.sidebar.multiselect(
        "Major Category",
        options=sorted(df["Major_Category"].dropna().unique()),
        default=sorted(df["Major_Category"].dropna().unique())
    )
    df = df[df["Major_Category"].isin(majors)]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Rows", len(df))

with col2:
    if "Pre_Semester_GPA" in df.columns:
        st.metric("Avg Pre GPA", round(df["Pre_Semester_GPA"].mean(), 2))

with col3:
    if "Post_Semester_GPA" in df.columns:
        st.metric("Avg Post GPA", round(df["Post_Semester_GPA"].mean(), 2))

if {"Pre_Semester_GPA", "Post_Semester_GPA"}.issubset(df.columns):
    st.subheader("GPA Comparison")
    gpa_df = pd.DataFrame({
        "Type": ["Pre Semester GPA", "Post Semester GPA"],
        "Average": [df["Pre_Semester_GPA"].mean(), df["Post_Semester_GPA"].mean()]
    })
    fig = px.bar(gpa_df, x="Type", y="Average")
    st.plotly_chart(fig, use_container_width=True)

if {"Weekly_GenAI_Hours", "Post_Semester_GPA"}.issubset(df.columns):
    st.subheader("GenAI Usage vs Post GPA")
    fig = px.scatter(
        df.sample(min(3000, len(df))),
        x="Weekly_GenAI_Hours",
        y="Post_Semester_GPA",
        color="Major_Category" if "Major_Category" in df.columns else None
    )
    st.plotly_chart(fig, use_container_width=True)

if "Burnout_Risk_Level" in df.columns:
    st.subheader("Burnout Risk Distribution")
    burnout = df["Burnout_Risk_Level"].value_counts().reset_index()
    burnout.columns = ["Risk", "Count"]
    fig = px.pie(burnout, names="Risk", values="Count")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Descriptive Statistics")
st.dataframe(df.describe(include="all"))
