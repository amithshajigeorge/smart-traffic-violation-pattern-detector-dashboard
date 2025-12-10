import streamlit as st

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="About — Smart Traffic Violation Pattern Detector",
    page_icon="assets/logo.png",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .big-font {
        font-size: 20px !important;
        font-weight: 500;
        color: var(--text-color);
    }
    .feature-card {
        background-color: var(--secondary-background-color);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 1px solid #e0e0e0;
    }
    .feature-title {
        color: #2E86C1;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header Section
# -----------------------------
st.title("About Project")
st.markdown("### Smart Traffic Violation Pattern Detector")

col1, col2 = st.columns([1.5, 1])

with col1:
    st.markdown("""
    <div class="big-font">
    Welcome to the <b>Smart Traffic Violation Pattern Detector</b>, an intelligent system designed to enhance road safety through <b>data-driven insights</b>.
    <br><br>
    This project utilizes:
    <ul>
        <li><i>Advanced Analytics</i></li>
        <li><i>Smart Dashboards</i></li>
        <li><i>Data Processing</i></li>
        <li><i>Data Visualization</i></li>
    </ul>
    Our aim is to help authorities <b>identify patterns</b>, reduce accidents, and improve city-wide traffic management.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.image("assets/logo.png", width='stretch')

st.divider()

# -----------------------------
# Mission & Vision (Columns)
# -----------------------------
c1, c2 = st.columns(2)
with c1:
    with st.container(border=True):
        st.subheader("Our Mission")
        st.markdown("To revolutionize urban traffic management by empowering authorities with a **robust, scalable, and data-centric platform**. We aim to eliminate manual inefficiencies, ensure precise violation detection, and foster a culture of road safety through **actionable intelligence**.")

with c2:
    with st.container(border=True):
        st.subheader("Our Vision")
        st.markdown("To become the standard in **smart city traffic governance**, where advanced analytics and automation converge to create **zero-accident ecosystems**, ensuring seamless compliance and safer roads for every citizen.")

st.divider()

# -----------------------------
# What We Do (Expanders)
# -----------------------------
st.subheader("Our Features & Solutions")
col_feat1, col_feat2 = st.columns(2)

with col_feat1:
    with st.expander("Automated Data Processing & Scoring", expanded=True):
        st.markdown("""
        *   **Cleaning:** Cleans, structures and analyzes large-scale traffic violation data automatically.
        *   **Severity:** Applies custom severity levels to each violation type.
        *   **Risk Index:** Computes risk score per vehicle based on cumulative violations.
        """)
    
    with st.expander("Pattern & Trend Detection", expanded=True):
        st.markdown("""
        *   **Common Violations:** Finds most frequent offenses.
        *   **Peak Times:** Identifies peak time for rule-breaking.
        *   **High-Risk:** Pinpoints high-risk vehicles & regions.
        """)

with col_feat2:
    with st.expander("Interactive Visualizations", expanded=True):
        st.markdown("""
        *   **Time-Series:** Hour-wise and monthly violation trends.
        *   **Severity metrics:** Distribution of violation severity.
        *   **Demographics:** Vehicle-type and driver trends.
        *   **Financials:** Fine contribution analytics.
        """)

    with st.expander("Data Export & Reporting", expanded=True):
        st.markdown("""
        *   **Raw Data:** View and filter raw datasets.
        *   **Exports:** Support for data extraction.
        *   **Summaries:** Comprehensive statistical summaries.
        """)

st.divider()

# -----------------------------
# Technologies (Container)
# -----------------------------
st.subheader("Technologies & Libraries Used")
with st.container(border=True):
    t1, t2, t3 = st.columns(3, border=True)
    with t1:
        st.markdown("#### Frontend Used")
        st.markdown("""
        - **Streamlit** - Web Dashboard Framework  
        - **HTML/CSS** - Custom Styling  
        - **Vector Graphics** - UI Assets  
        """)
    with t2:
        st.markdown("#### Backend Logic")
        st.markdown("""
        - **Python** - Core Logic  
        - **Pandas** - Data Manipulation  
        - **NumPy** - Numerical Operations  
        """)
    with t3:
        st.markdown("#### Data Management")
        st.markdown("""
        - **CSV** - Data Storage  
        - **Matplotlib/Seaborn/Streamlit** - Visualization Engine  
        - **Folium** - Geospatial Mapping  
        """)

st.divider()

# -----------------------------
# Why It Matters (Info)
# -----------------------------
st.subheader("Why This Project Matters")
st.expander("Why it Matters", expanded=True).markdown("""
*   Urban traffic is increasing rapidly.
*   Manual monitoring is slow and inefficient.
*   Data reveals hidden patterns humans may miss.
*   Helps prevent violations and save lives.
*   Brings **transparency, accuracy & intelligence** to traffic systems.
""")

# -----------------------------
# Future Roadmap (New Section)
# -----------------------------
st.subheader("Future Roadmap")
with st.container(border=True):
    r1, r2 = st.columns(2)
    
    with r1:
        st.markdown("""
        **1. Real-time Database Integration**  
        Move from flat CSV files to SQL (PostgreSQL/MySQL) or NoSQL (MongoDB) for scalability.
        
        **2. AI/ML Forecasting**  
        Implement predictive models (ARIMA/Prophet) to forecast future violation hotspots and revenue.
        """)
        
    with r2:
        st.markdown("""
        **3. Automated Reporting**  
        Generate and email PDF/Excel reports to authorities automatically on a schedule.
        
        **4. Live Camera Feed Integration**  
        Connect to traffic camera APIs for real-time violation detection integration.
        """)
        
st.divider()

