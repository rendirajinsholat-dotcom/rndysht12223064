
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI Student Impact Analytics", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("ai_student_impact_dataset.csv")

df = load_data()

st.title("🎓 AI Student Impact Analytics Dashboard")
st.markdown("Interactive dashboard for exploring the impact of Generative AI on student outcomes.")

st.sidebar.header("Filters")

for col in ["Major_Category", "Burnout_Risk_Level"]:
    if col in df.columns:
        vals = st.sidebar.multiselect(col, sorted(df[col].dropna().unique()))
        if vals:
            df = df[df[col].isin(vals)]

num_cols = df.select_dtypes(include="number").columns.tolist()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Records", len(df))

if "Pre_Semester_GPA" in df.columns:
    c2.metric("Avg Pre GPA", f"{df['Pre_Semester_GPA'].mean():.2f}")
if "Post_Semester_GPA" in df.columns:
    c3.metric("Avg Post GPA", f"{df['Post_Semester_GPA'].mean():.2f}")
if "Weekly_GenAI_Hours" in df.columns:
    c4.metric("Avg GenAI Hours", f"{df['Weekly_GenAI_Hours'].mean():.1f}")

tab1, tab2, tab3, tab4 = st.tabs(["Overview","Correlation","Distribution","Raw Data"])

with tab1:
    if {"Pre_Semester_GPA","Post_Semester_GPA"}.issubset(df.columns):
        chart = pd.DataFrame({
            "Metric":["Pre GPA","Post GPA"],
            "Value":[df["Pre_Semester_GPA"].mean(), df["Post_Semester_GPA"].mean()]
        })
        st.plotly_chart(px.bar(chart,x="Metric",y="Value"), use_container_width=True)

with tab2:
    if len(num_cols) > 1:
        corr = df[num_cols].corr(numeric_only=True)
        st.plotly_chart(px.imshow(corr, text_auto=True), use_container_width=True)

with tab3:
    if "Weekly_GenAI_Hours" in df.columns:
        st.plotly_chart(
            px.histogram(df, x="Weekly_GenAI_Hours"),
            use_container_width=True
        )

with tab4:
    st.dataframe(df, use_container_width=True)

st.download_button(
    "Download Filtered Data",
    df.to_csv(index=False),
    "filtered_data.csv",
    "text/csv"
)
