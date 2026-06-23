
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI Student Impact Dashboard", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("ai_student_impact_dataset.csv")

try:
    df = load_data()
except Exception as e:
    st.error(f"Failed to load CSV: {e}")
    st.stop()

st.title("🎓 AI Student Impact Dashboard")

st.sidebar.header("Filters")

if "Major_Category" in df.columns:
    selected = st.sidebar.multiselect(
        "Major Category",
        sorted(df["Major_Category"].dropna().unique())
    )
    if selected:
        df = df[df["Major_Category"].isin(selected)]

c1, c2, c3 = st.columns(3)
c1.metric("Records", len(df))
c2.metric("Average Pre GPA", round(df["Pre_Semester_GPA"].mean(), 2))
c3.metric("Average Post GPA", round(df["Post_Semester_GPA"].mean(), 2))

st.subheader("GPA Comparison")
gpa = pd.DataFrame({
    "Type":["Pre GPA","Post GPA"],
    "Value":[df["Pre_Semester_GPA"].mean(), df["Post_Semester_GPA"].mean()]
})
st.plotly_chart(px.bar(gpa, x="Type", y="Value"), use_container_width=True)

st.subheader("GenAI Usage vs GPA")
st.plotly_chart(
    px.scatter(
        df.sample(min(2000, len(df))),
        x="Weekly_GenAI_Hours",
        y="Post_Semester_GPA",
        color="Major_Category"
    ),
    use_container_width=True
)

st.subheader("Burnout Risk")
burnout = df["Burnout_Risk_Level"].value_counts().reset_index()
burnout.columns = ["Risk","Count"]
st.plotly_chart(px.pie(burnout, names="Risk", values="Count"), use_container_width=True)

st.subheader("Correlation Matrix")
corr = df.select_dtypes(include="number").corr()
st.dataframe(corr)

st.subheader("Dataset")
st.dataframe(df, use_container_width=True)
