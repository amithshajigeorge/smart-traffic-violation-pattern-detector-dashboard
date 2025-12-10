import streamlit as st
import pandas as pd
from core import (
    sidebar,
    data_variables
)

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(
    page_title="Dataset Summary - Smart Traffic Violation Pattern Detector Dashboard", 
    page_icon="assets/logo.png", 
    layout="wide"
)

# ------------------------------
# LOAD DATA
# ------------------------------
st.title("📝 Dataset Summary")
st.markdown("Visualize and analyze traffic violation data.")

df = sidebar.render_sidebar()
total_data_records = len(df)
st.metric(label="Total Data Records", value=total_data_records)

# Initialize session state for filters if not exists
if "search_violation" not in st.session_state: st.session_state.search_violation = ""
if "search_gender" not in st.session_state: st.session_state.search_gender = ""
if "search_age" not in st.session_state: st.session_state.search_age = ""
if "search_license" not in st.session_state: st.session_state.search_license = ""
# Default to all columns if not set
if "selected_columns" not in st.session_state or not st.session_state.selected_columns: 
    st.session_state.selected_columns = list(df.columns)

def clear_filters():
    st.session_state.search_violation = ""
    st.session_state.search_gender = ""
    st.session_state.search_age = ""
    st.session_state.search_license = ""
    st.session_state.selected_columns = list(df.columns)

# Filter columns present check (using existing logic)
if set(data_variables.TRAFFIC_VIOLATION_COLUMNS).issubset(set(df.columns)):
    with st.expander("Filter Data"):
        with st.form("dataset_filter_form"):
            
            # 1. Column Selection Expander
            with st.expander("📝 Select Columns", expanded=False):
                st.multiselect(
                    "Choose columns to display:", 
                    options=list(df.columns), 
                    default=st.session_state.selected_columns,
                    key="selected_columns",
                    help="Select specific columns to view in the table."
                )

            # 2. Search Query Parameters Expander
            with st.expander("🔎 Enter Search Queries", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.text_input("Violations Type Search", help="Search by Violation Type", key="search_violation")
                    st.text_input("Driver Age Search", help="Search by Driver Age", key="search_age")
                with col2:
                    st.text_input("Driver Gender Search", help="Search by Driver Gender", key="search_gender")
                    st.text_input("Driver License Search", help="Search by License Type", key="search_license")
            
            # Search Button (Form Submit)
            submitted = st.form_submit_button("Search / Apply Filters", type="primary")

        # Reset Button (outside form)
        st.button("🔄 Reset Filters", on_click=clear_filters)

# Filter the dataset logic using Session State values
df_filtered = df.copy()

if set(data_variables.TRAFFIC_VIOLATION_COLUMNS).issubset(set(df.columns)):
    # Apply Filters based on Session State (which holds the submitted form values)
    if st.session_state.search_violation:
        df_filtered = df_filtered[df_filtered['Violation_Type'].astype(str).str.contains(st.session_state.search_violation, case=False, na=False)]
    if st.session_state.search_gender:
        df_filtered = df_filtered[df_filtered['Driver_Gender'].astype(str).str.contains(st.session_state.search_gender, case=False, na=False)]
    if st.session_state.search_age:
        df_filtered = df_filtered[df_filtered['Driver_Age'].astype(str).str.contains(st.session_state.search_age, case=False, na=False)]
    if st.session_state.search_license:
        df_filtered = df_filtered[df_filtered['License_Type'].astype(str).str.contains(st.session_state.search_license, case=False, na=False)]

    # Apply Column Selection
    if st.session_state.selected_columns:
        # Filter to only selected columns (ensure they exist)
        valid_cols = [c for c in st.session_state.selected_columns if c in df_filtered.columns]
        if valid_cols:
            df_filtered = df_filtered[valid_cols]
        else:
            st.warning("No valid columns selected. Showing all.")
            df_filtered = df

    st.write(f"## Search Results: `{df_filtered.shape[0]}` Records Found")
else:
    st.error("Dataset does not contain required columns for advanced filtering.")

st.data_editor(df_filtered, width='stretch')