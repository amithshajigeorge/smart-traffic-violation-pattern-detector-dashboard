import streamlit as st
import pandas as pd
import numpy as np
from core.utils import filter_the_dataset, get_last_n_days_data
from core.sidebar import render_sidebar
import core.summary as dashnoard_summary

from core.data_variables import TRAFFIC_VIOLATION_COLUMNS

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(
    page_title="Smart Traffic Violation Dashboard",
    page_icon="🚦",
    layout="wide",
)



def home():
    # ------------------------------
    # HEADER / HERO SECTION
    # ------------------------------
    st.title("🚦 Smart Traffic Violation Summary Dashboard")
    st.write("---")
    # ------------------------------
    # 2x2 Grid System for Recent 30 days view
    # ------------------------------
    # Load dataset
    df = render_sidebar()
    if df is None:
        st.warning("No dataset selected. Please select one from the sidebar.")
        st.stop()
    # Filter the dataset
    if set(TRAFFIC_VIOLATION_COLUMNS).issubset(set(df.columns)) is False:
        st.error("The selected dataset does not match the required format for analysis. Please upload a valid traffic violation dataset.")
        st.error(f"Expected Columns: {TRAFFIC_VIOLATION_COLUMNS}")
        st.error(f"Actual Columns: {df.columns.tolist()}")
        expected_cols = set(TRAFFIC_VIOLATION_COLUMNS)
        actual_cols = set(df.columns)
        missing = expected_cols - actual_cols
        st.error(f"Missing Columns: {list(missing)}")
        st.error("Please Select a valid traffic violation dataset from the sidebar.")
        st.stop()
    elif df.shape[0] == 0:
        st.warning("The selected dataset is empty. Please upload a valid traffic violation dataset.")
        st.stop()
    else:
        # Filter the dataset
        df = filter_the_dataset(df)
        # Summary Calculations for Last N Days
        no_of_days_for_summary  = st.expander("Days Filter", expanded=False).slider("Select Number of Days for Summary Calculations", min_value=7, max_value=365, value=30, step=1, key="days_slider")
        df_last_n_days = get_last_n_days_data(df, no_of_days_for_summary)
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"### Total Violations (Last {no_of_days_for_summary} Days)")
            total_no_of_violations, fig = dashnoard_summary.get_violations_summary_of_last_n_days(df_last_n_days)
            
            # Display Charts
            with st.expander("View Violation Types Distribution Chart"):
                st.write("### Violation Types Distribution")
                st.pyplot(fig, use_container_width=False)
            # Metrics
            sub_col1, sub_col2, sub_col3 = st.columns(3, border=True)
            with sub_col1:
                st.metric(label="Total Violations", value=total_no_of_violations)
                
            with sub_col2:
                st.metric(label="Average Violations per Day", value=f"{int(total_no_of_violations/no_of_days_for_summary)}")
            with sub_col3:
                st.metric(label="Average Violations per Vehicle", value=f"{int(total_no_of_violations/df_last_n_days['Vehicle_Type'].nunique())}")
            st.markdown('---')
            
            # ==========================================================================================================
            st.info(f"### Violations by Location (Last {no_of_days_for_summary} Days)")
            total_locations, most_violated_location, fig_location = dashnoard_summary.get_violations_by_location(df_last_n_days)
            with st.expander("View Violations by Location Chart"):
                st.write("### Violations by Location")
                st.pyplot(fig_location, use_container_width=False,)
            # Metrics
            sub_col1, sub_col2, sub_col3 = st.columns(3, border=True)
            with sub_col1:
                st.metric(label="Total Locations with Violations", value=total_locations)
            with sub_col2:
                st.metric(label="Most Violated Location", value=most_violated_location, delta_color='inverse')
            with sub_col3:
                st.metric(label="Average Violations per Location", value=f"{int(total_no_of_violations/total_locations)}")
            st.markdown('---')
    # ==========================================================================================================
        with col2:
            st.info(f"### Total Fines (Last {no_of_days_for_summary} Days)")
            total_fines, avg_fine_per_violation, fine_based_on_violation_type = dashnoard_summary.get_total_fines_generated(df_last_n_days)
            
            # Display Charts
            with st.expander("View Fines Distribution Chart"):
                st.write("### Fines Distribution")
                st.pyplot(fine_based_on_violation_type, use_container_width=False)
            # Metrics
            sub_col1, sub_col2, sub_col3 = st.columns(3, border=True)
            with sub_col1:
                st.metric(label="Total Fines", value=f"Rs.{total_fines}")
            with sub_col2:
                st.metric(label="Average Fines per Day", value=f"Rs.{int(total_fines/no_of_days_for_summary)}")
            with sub_col3:
                st.metric(label="Average Fines per Violation", value=f"Rs.{int(avg_fine_per_violation)}")
            st.markdown('---')

            # ==========================================================================================================
            # Average Fine per Violation
            st.info(f"### Driver's Insights (Last {no_of_days_for_summary} Days)")
            avg_driver_age, most_common_gender, max_alcohol_level, gender_fig = dashnoard_summary.get_driver_insights(df_last_n_days)

            # Display Charts
            with st.expander("View Calculation Methodology"):
                st.write("### Driver Gender")
                st.pyplot(gender_fig)
            # Metrics
            sub_col1, sub_col2, sub_col3 = st.columns(3, border=True)
            with sub_col1:
                st.metric(label="Average Driver Age", value=f"{avg_driver_age} years")
            with sub_col2:
                st.metric(label="Most Common Driver Gender", value=most_common_gender)
            with sub_col3:
                st.metric(label="Maximum Alcohol Level", value=f"{max_alcohol_level}")
            st.markdown('---')

    # ------------------------------
    # INFO SECTION
    # ------------------------------

# Define the pages for navigation
pages = [
    st.Page(home, title="Home Page", icon="🏠", default=True, url_path='/'),
    st.Page("pages/01_Numerical_Analysis.py", title="Numerical Analysis", icon="📊", url_path='/numerical-analysis'),
    st.Page("pages/02_Visualize_Data.py", title="Data Visualization", icon="🎨", url_path='/data-visualization'),
    st.Page("pages/03_Trend_Analysis.py", title="Series Trends", icon="📈", url_path='/series-trends'),
    st.Page("pages/04_Map_Visualization.py", title="Map Visualization", icon="🗺️", url_path='/map-visualization'),
    st.Page("pages/09_Upload_Dataset.py", title="Data Management", icon="📂", url_path='/data-management'),
    st.Page("pages/10_View_Dataset.py", title="View Dataset", icon="📝", url_path='/view-dataset/'),
    # st.Page("pages/12_Prediction.py", title="Prediction", icon="🤖"),
]

# Create the navigation in the sidebar
pg = st.navigation(pages, position="sidebar")
pg.run()