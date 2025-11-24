import streamlit as st
import pandas as pd
import json
import folium
from streamlit_folium import st_folium
from core.sidebar import render_sidebar
from core.utils import find_location_columns

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(page_title="Map Visualization", page_icon="🗺️", layout="wide")

# ------------------------------
# SESSION STATE INITIALIZATION
# ------------------------------
if 'map_data' not in st.session_state:
    st.session_state.map_data = None
if 'map_config' not in st.session_state:
    st.session_state.map_config = None

# ------------------------------
# LOAD DATA
# ------------------------------
try:
    df = render_sidebar()
    if df is None:
        st.warning("No dataset selected. Please select one from the sidebar.")
        st.stop()
except Exception as e:
    st.error(f"An error occurred while loading the data: {e}")
    st.stop()

st.title("🗺️ Map Visualization")
st.markdown("Visualize traffic violation data across India.")

# ------------------------------
# DATA PREPARATION & VALIDATION
# ------------------------------
# Load GeoJSON to get a list of known state names for matching
try:
    with open(r"map_data\01_INDIA_STATES.geojson", "r") as f:
        geojson_data_for_validation = json.load(f)
    known_states = {feature['properties']['STNAME_SH'].lower() for feature in geojson_data_for_validation['features']}
except Exception as e:
    st.error(f"Could not load or parse the GeoJSON file needed for location detection: {e}")
    st.stop()

# Find potential location columns automatically
valid_location_cols = find_location_columns(df, known_states)

if not valid_location_cols:
    st.warning("Could not automatically detect a suitable location column for map visualization.")
    st.info("This feature works best if your dataset has a column with Indian state names. Falling back to all categorical columns.")
    # As a fallback, allow user to select from any categorical column
    valid_location_cols = [col for col in df.select_dtypes(include=['object']).columns if df[col].nunique() < 50]
    if not valid_location_cols:
        st.error("No suitable categorical columns found in the dataset to use for location.")
        st.stop()

# ------------------------------
# INDIAN STATE PLOT EXPANDER
# ------------------------------
with st.expander("Indian State Plot", expanded=True):
    st.markdown("Create a choropleth map to visualize data across Indian states using Folium.")

    # --- Controls ---
    start_date_map, end_date_map = None, None
    min_date_map, max_date_map = None, None
    
    # Prepare date objects if 'Date' column is valid
    try:
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            if not df['Date'].isnull().all():
                min_date_map = df['Date'].min().date()
                max_date_map = df['Date'].max().date()
    except Exception:
        st.info("No 'Date' column found or date conversion failed.")

    col1, col2 = st.columns(2)
    with col1:
        if min_date_map and max_date_map:
            start_date_map = st.date_input("Start date", min_date_map, min_value=min_date_map, max_value=max_date_map, key="map_start")
        location_col = st.selectbox("Select State Column", options=valid_location_cols, index=valid_location_cols.index('Registration_State') if 'Registration_State' in valid_location_cols else 0, help="Select the column containing state names.")

    with col2:
        if min_date_map and max_date_map:
            end_date_map = st.date_input("End date", max_date_map, min_value=min_date_map, max_value=max_date_map, key="map_end")
        numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        value_options = ['Count of Violations'] + numerical_cols
        value_col = st.selectbox("Select Data/Value to Visualize", options=value_options)

    agg_func = st.selectbox("Select Aggregation", options=['Mean', 'Sum', 'Median'], disabled=(value_col == 'Count of Violations')) if value_col != 'Count of Violations' else 'Count'

    if st.button("Generate Folium Map"):
        if start_date_map and end_date_map and start_date_map > end_date_map:
            st.error("Error: End date must fall after start date.")
        else:
            with st.spinner("Processing data..."):
                # 1. Filter by date
                plot_df = df[(df['Date'].dt.date >= start_date_map) & (df['Date'].dt.date <= end_date_map)].copy() if start_date_map and end_date_map else df.copy()
                
                # 2. Aggregate data
                if value_col == 'Count of Violations':
                    map_data = plot_df[location_col].value_counts().reset_index()
                    map_data.columns = [location_col, 'Count of Violations']
                    color_col = 'Count of Violations'
                else:
                    agg_map = {'Mean': 'mean', 'Sum': 'sum', 'Median': 'median'}
                    map_data = plot_df.groupby(location_col)[value_col].agg(agg_map[agg_func]).reset_index()
                    color_col = value_col
                
                # 3. Store data and config in session state
                st.session_state.map_data = map_data
                st.session_state.map_config = {
                    "location_col": location_col,
                    "color_col": color_col,
                    "value_col": value_col
                }

# ------------------------------
# MAP DISPLAY
# ------------------------------
if st.session_state.map_data is not None:
    map_data = st.session_state.map_data
    config = st.session_state.map_config
    location_col = config['location_col']
    color_col = config['color_col']
    value_col = config['value_col']

    with st.spinner("Rendering map..."):
        try:
            with open("map_data/01_INDIA_STATES.geojson", "r") as f:
                geojson_data = json.load(f)
        except Exception as e:
            st.error(f"Error loading GeoJSON file: {e}")
            st.stop()

        for feature in geojson_data['features']:
            feature['properties']['st_nm_lower'] = feature['properties']['STNAME_SH'].lower()
        map_data[location_col] = map_data[location_col].str.lower()

        st.markdown(f"### {value_col} by {location_col}")
        m = folium.Map(location=[22, 82], zoom_start=4, tiles="CartoDB positron")

        choropleth = folium.Choropleth(
            geo_data=geojson_data,
            data=map_data,
            columns=[location_col, color_col],
            key_on="feature.properties.st_nm_lower",
            fill_color="YlGnBu",
            fill_opacity=0.7,
            line_opacity=0.5,
            legend_name=f"{value_col}",
        ).add_to(m)

        folium.features.GeoJsonTooltip(
            fields=['STNAME_SH'],
            aliases=['State:']
        ).add_to(choropleth.geojson)

        st_folium(m, width='stretch', height=600)

        with st.expander("View Map Data"):
            st.dataframe(map_data)
else:
    st.info("Configure the plot options above and click 'Generate Folium Map' to see the map.")
