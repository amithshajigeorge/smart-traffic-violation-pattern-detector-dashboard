import streamlit as st
import pandas as pd
from core.sidebar import render_sidebar

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(
    page_title="Dataset Summary",
    page_icon="📝",
    layout="wide",
)

# ------------------------------
# LOAD DATA
# ------------------------------
df = render_sidebar()

st.title("📝 Dataset Summary")
st.markdown("### Key Statistics")

total_data_records = len(df)
st.metric(label="Total Data Records", value=total_data_records)

st.markdown("### Raw Data")
st.write("")
input_query =  st.text_input("Violations Search",help="Search for violations Type")

if input_query:
    df_filtered = df[df['Violation_Type'].astype(str).str.contains(input_query, case=False, na=False)]

    st.write(f"## Search Results:`{df_filtered.shape[0]}` Records Found")
    st.data_editor(df_filtered)
else:
    st.data_editor(df)


st.sidebar.header("About")
st.sidebar.info("This page provides a summary and raw data view of the traffic violations dataset.")