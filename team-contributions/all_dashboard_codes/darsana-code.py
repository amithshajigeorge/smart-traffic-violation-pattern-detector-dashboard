import streamlit as st
import pandas as pd
import numpy as np

def style_table(df_input):
    """
    Applies general styling and header color using Pandas Styler.
    Ensures the index column text (row_heading) is a dark color for visibility.
    """
    styles = [
        {'selector': '', 'props': [('border-collapse', 'collapse')]},
        {'selector': 'th', 'props': [
            ('background-color', '#003366'),
            ('color', 'white'),
            ('font-size', '14px'),
            ('text-align', 'center')
        ]},
        {'selector': 'td', 'props': [
            ('font-size', '14px'),
            ('text-align', 'center'),
        ]},
        {'selector': '.row_heading', 'props': [
            ('background-color', '#F0F0F0'),
            ('color', '#333333'),
            ('font-weight', 'bold'),
            ('text-align', 'left'),
        ]},
    ]

    styled_df = df_input.style.set_table_styles(styles)
    return styled_df

st.set_page_config(page_title="Indian Traffic Violation Dashboard", layout="wide")
st.markdown("<h1 style='text-align:center; color:#0D47A1; background-color:#E3F2FD; padding:10px; border-radius:5px;'>🚦 Indian Traffic Violation Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#555555;'>Comprehensive traffic violation insights and comparative analysis</p>", unsafe_allow_html=True)
st.markdown("---")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
if uploaded_file is not None:
    df_raw = pd.read_csv(uploaded_file)
    st.success("✅ Dataset Loaded Successfully!")

    df = df_raw.copy()

    # ==============================
    # 1️⃣ Sidebar Filters
    # ==============================
    st.sidebar.header("Data Filter 🔎")

    if 'Location' in df.columns:
        locations = st.sidebar.multiselect("Select Location(s)", df['Location'].unique(), default=df['Location'].unique())
        df = df[df['Location'].isin(locations)]

    if 'Violation_Type' in df.columns:
        violation_types = st.sidebar.multiselect("Select Violation Type(s)", df['Violation_Type'].unique(), default=df['Violation_Type'].unique())
        df = df[df['Violation_Type'].isin(violation_types)]

    if 'Driver_Age' in df.columns:
        min_age = int(df['Driver_Age'].min()) if not df['Driver_Age'].empty else 16
        max_age = int(df['Driver_Age'].max()) if not df['Driver_Age'].empty else 90
        age_range = st.sidebar.slider("Driver Age Range", min_age, max_age, (min_age, max_age))
        df = df[(df['Driver_Age'] >= age_range[0]) & (df['Driver_Age'] <= age_range[1])]

    st.markdown(f"**Filtered Records:** **:blue[{len(df)}]**")
    st.dataframe(df.head())

    if df.empty:
        st.warning("No data matches the selected filter criteria.")
        st.stop()

    # --- Prepare necessary helper columns ---
    if 'Date' in df.columns and 'Time' in df.columns:
        df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], errors='coerce')
        df['Day'] = df['Datetime'].dt.day_name()
        df['Month'] = df['Datetime'].dt.month_name()
        df['Hour'] = df['Datetime'].dt.hour

    if 'Fine_Paid' in df.columns:
        df['Fine_Paid_Bool'] = df['Fine_Paid'].map({'Yes': 1, 'No': 0, 'N/A': np.nan})

    st.markdown("---")

    # ==============================
    # 2️⃣ Data Quality Cards
    # ==============================
    st.markdown("<h2 style='color:#E65100;'>🧹 Data Quality Metrics</h2>", unsafe_allow_html=True)
    missing_percent = round(df.isna().mean().mean()*100,2)
    duplicate_percent = round(df.duplicated().mean()*100,2)

    outlier_count = {}
    for col in ['Recorded_Speed','Fine_Amount','Driver_Age']:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outlier_count[col] = ((df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)).sum()
        else:
            outlier_count[col] = 0

    invalid_age = ((df['Driver_Age'] < 16) | (df['Driver_Age'] > 90)).sum() if 'Driver_Age' in df.columns else 0
    invalid_speed = (df['Recorded_Speed'] < 0).sum() if 'Recorded_Speed' in df.columns else 0
    invalid_fine = (df['Fine_Amount'] < 0).sum() if 'Fine_Amount' in df.columns else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div style='background-color:#FFDDC1; padding:20px; border-radius:10px; text-align:center; margin:10px; box-shadow:2px 2px 10px rgba(0,0,0,0.1);'>
            <h3 style='color:#FF5733;'>Missing Values</h3>
            <h2 style='color:#900C3F;'>{missing_percent}%</h2>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style='background-color:#D1FFC6; padding:20px; border-radius:10px; text-align:center; margin:10px; box-shadow:2px 2px 10px rgba(0,0,0,0.1);'>
            <h3 style='color:#28A745;'>Duplicate Records</h3>
            <h2 style='color:#1B5E20;'>{duplicate_percent}%</h2>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div style='background-color:#C6E0FF; padding:20px; border-radius:10px; text-align:center; margin:10px; box-shadow:2px 2px 10px rgba(0,0,0,0.1);'>
            <h3 style='color:#0D47A1;'>Outliers (Speed/Fine/Age)</h3>
            <h2 style='color:#003366;'>{outlier_count['Recorded_Speed']}/{outlier_count['Fine_Amount']}/{outlier_count['Driver_Age']}</h2>
        </div>
        """, unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown(f"<div style='background-color:#FFE0B2; padding:20px; border-radius:10px; text-align:center; margin:10px; box-shadow:2px 2px 10px rgba(0,0,0,0.1);'><h3 style='color:#E65100;'>Invalid Ages</h3><h2 style='color:#BF360C;'>{invalid_age}</h2></div>", unsafe_allow_html=True)
    with col5:
        st.markdown(f"<div style='background-color:#E1BEE7; padding:20px; border-radius:10px; text-align:center; margin:10px; box-shadow:2px 2px 10px rgba(0,0,0,0.1);'><h3 style='color:#8E24AA;'>Invalid Speeds</h3><h2 style='color:#4A148C;'>{invalid_speed}</h2></div>", unsafe_allow_html=True)
    with col6:
        st.markdown(f"<div style='background-color:#B2DFDB; padding:20px; border-radius:10px; text-align:center; margin:10px; box-shadow:2px 2px 10px rgba(0,0,0,0.1);'><h3 style='color:#00796B;'>Invalid Fines</h3><h2 style='color:#004D40;'>{invalid_fine}</h2></div>", unsafe_allow_html=True)

    st.markdown("---")

    # ==============================
    # 3️⃣ Key Metrics Cards
    # ==============================
    st.markdown("<h2 style='color:#880E4F;'>📌 Key Metrics</h2>", unsafe_allow_html=True)
    total_violations = len(df)
    avg_fine = f"₹{df['Fine_Amount'].mean():.2f}" if 'Fine_Amount' in df.columns else "N/A"
    max_fine = f"₹{df['Fine_Amount'].max()}" if 'Fine_Amount' in df.columns else "N/A"
    min_fine = f"₹{df['Fine_Amount'].min()}" if 'Fine_Amount' in df.columns else "N/A"
    common_violation = df['Violation_Type'].mode()[0] if 'Violation_Type' in df.columns and not df['Violation_Type'].empty else "N/A"
    most_active_agency = df['Issuing_Agency'].mode()[0] if 'Issuing_Agency' in df.columns and not df['Issuing_Agency'].empty else "N/A"
    avg_passengers = round(df['Number_of_Passengers'].mean(),2) if 'Number_of_Passengers' in df.columns else "N/A"
    helmet_pct = round(df['Helmet_Worn'].value_counts(normalize=True).get('Yes',0)*100,2) if 'Helmet_Worn' in df.columns else "N/A"
    seatbelt_pct = round(df['Seatbelt_Worn'].value_counts(normalize=True).get('Yes',0)*100,2) if 'Seatbelt_Worn' in df.columns else "N/A"

    cards = [
        ("Total Violations", total_violations, "#FFF3E0", "#E65100"),
        ("Most Common Violation", common_violation, "#E8F5E9", "#1B5E20"),
        ("Most Active Agency", most_active_agency, "#E3F2FD", "#0D47A1"),
        ("Average Fine", avg_fine, "#FCE4EC", "#880E4F"),
        ("Max Fine", max_fine, "#FFF9C4", "#F57F17"),
        ("Min Fine", min_fine, "#C8E6C9", "#1B5E20"),
        ("Avg Passengers", avg_passengers, "#FFE0B2", "#BF360C"),
        ("% Helmet Worn", f"{helmet_pct}%", "#D1C4E9", "#4A148C"),
        ("% Seatbelt Worn", f"{seatbelt_pct}%", "#B2EBF2", "#006064")
    ]

    for i in range(0, len(cards), 3):
        cols = st.columns(3)
        for j, card in enumerate(cards[i:i+3]):
            with cols[j]:
                title, value, bg, color = card
                st.markdown(f"<div style='background-color:{bg}; padding:20px; border-radius:10px; text-align:center; margin:10px; box-shadow:2px 2px 10px rgba(0,0,0,0.1);'><h4 style='color:{color};'>{title}</h4><h2 style='color:{color};'>{value}</h2></div>", unsafe_allow_html=True)

    st.markdown("---")

    # ==============================
    # 4️⃣ Rule-Based Flags Cards
    # ==============================
    st.markdown("<h2 style='color:#B71C1C;'>🚩 Rule-Based Flags</h2>", unsafe_allow_html=True)
    flag_cols = []

    if 'Recorded_Speed' in df.columns and 'Speed_Limit' in df.columns:
        df['Over_Speeding_Flag'] = df['Recorded_Speed'] > df['Speed_Limit']
        flag_cols.append('Over_Speeding_Flag')

    if 'Fine_Amount' in df.columns:
        df['High_Fine_Flag'] = df['Fine_Amount'] > df['Fine_Amount'].quantile(0.90)
        flag_cols.append('High_Fine_Flag')

    if 'Driver_ID' in df.columns:
        repeat_drivers = df['Driver_ID'].value_counts()
        df['Repeat_Offender_Flag'] = df['Driver_ID'].isin(repeat_drivers[repeat_drivers>2].index)
        flag_cols.append('Repeat_Offender_Flag')

    if 'Weather_Condition' in df.columns:
        df['Bad_Weather_Risk'] = df['Weather_Condition'].isin(['Fog','Rain','Snow'])
        flag_cols.append('Bad_Weather_Risk')

    if flag_cols:
        flag_summary = {col:[df[col].sum(), round(df[col].mean()*100,2)] for col in flag_cols}
        flag_df = pd.DataFrame(flag_summary, index=["Count","Percent (%)"])

        st.table(style_table(flag_df))

    st.markdown("---")

    # ==============================
    # 5️⃣ Time-Based & Top Insights
    # ==============================
    st.markdown("<h2 style='color:#FFC107;'>⏱️ Time-Based & Top Insights (Tables Only)</h2>", unsafe_allow_html=True)

    # 5A: Time Cards
    if 'Day' in df.columns and 'Month' in df.columns and 'Hour' in df.columns:
        time_cards = [
            ("Day with Most Violations", df['Day'].value_counts().idxmax() if not df['Day'].empty else "N/A"),
            ("Month with Highest Fines", df.groupby("Month")['Fine_Amount'].sum().idxmax() if 'Fine_Amount' in df.columns and not df['Month'].empty else "N/A"),
            ("Peak Violation Hour", df['Hour'].value_counts().idxmax() if not df['Hour'].empty else "N/A")
        ]

        cols = st.columns(3)
        for i, card in enumerate(time_cards):
            title, value = card
            with cols[i]:
                st.markdown(f"<div style='background-color:#FFF9C4; padding:20px; border-radius:10px; text-align:center; margin:10px; box-shadow:2px 2px 10px rgba(0,0,0,0.1);'><h4 style='color:#F57F17;'>{title}</h4><h2 style='color:#F57F17;'>{value}</h2></div>", unsafe_allow_html=True)

    # 5B: Violation & City Tables
    cols = st.columns(2)
    with cols[0]:
        if 'Violation_Type' in df.columns:
            st.markdown("<h4 style='color:#00796B;'>Top 10 Most Frequent Violations</h4>", unsafe_allow_html=True)
            top_violation = df['Violation_Type'].value_counts().head(10).reset_index()
            top_violation.columns = ["Violation Type", "Count"]
            st.table(style_table(top_violation))

    with cols[1]:
        if 'Location' in df.columns:
            st.markdown("<h4 style='color:#00796B;'>Top 10 Locations with Most Violations</h4>", unsafe_allow_html=True)
            top_city = df['Location'].value_counts().head(10).reset_index()
            top_city.columns = ["Location", "Count"]
            st.table(style_table(top_city))

    # 5C: Time Distribution Tables
    if 'Day' in df.columns and 'Hour' in df.columns:
        st.markdown("<h4 style='color:#00796B;'>Violation Distribution by Day and Hour</h4>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<p style='font-weight:bold; color:#004D40;'>Violations by Day of Week</p>", unsafe_allow_html=True)
            st.table(style_table(df['Day'].value_counts().to_frame("Count")))
        with col2:
            st.markdown("<p style='font-weight:bold; color:#004D40;'>Violations by Hour of Day</p>", unsafe_allow_html=True)
            st.table(style_table(df['Hour'].value_counts().sort_index().to_frame("Count")))


    st.markdown("---")


    # ==============================
    # 6️⃣ Comparative Insights
    # ==============================
    st.markdown("<h2 style='color:#4A148C;'>👥 Comparative Analysis: Demographics & Vehicle Risk</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # 6A: Violation Type vs. Gender
    if 'Violation_Type' in df.columns and 'Driver_Gender' in df.columns:
        gender_pivot = pd.crosstab(df['Violation_Type'], df['Driver_Gender'], normalize='index').mul(100).round(5).sort_values(by=df['Driver_Gender'].unique()[0], ascending=False)
        gender_pivot.index.name = "Violation_Type"
        with col1:
            st.markdown("<h4 style='color:#6A1B9A;'>Gender Distribution per Violation Type (%)</h4>", unsafe_allow_html=True)
            st.table(style_table(gender_pivot.head(5)))

    # 6B: Fine vs. Vehicle Type
    if 'Vehicle_Type' in df.columns and 'Fine_Amount' in df.columns:
        vehicle_fine_pivot = df.groupby('Vehicle_Type')['Fine_Amount'].agg(['count', 'mean', 'max']).rename(columns={'count':'Total Violations', 'mean':'Avg Fine ₹', 'max':'Max Fine ₹'}).sort_values('Avg Fine ₹', ascending=False).round(2)
        vehicle_fine_pivot.index.name = "Vehicle_Type"
        with col2:
            st.markdown("<h4 style='color:#6A1B9A;'>Vehicle Type and Fine Severity</h4>", unsafe_allow_html=True)
            st.table(style_table(vehicle_fine_pivot))

    st.markdown("---")


    # ==============================
    # 7️⃣ Enforcement Effectiveness
    # ==============================
    st.markdown("<h2 style='color:#1B5E20;'>✅ Enforcement & Compliance Metrics</h2>", unsafe_allow_html=True)

    if 'Issuing_Agency' in df.columns and 'Fine_Paid_Bool' in df.columns:
        agency_payment_rate = df.groupby('Issuing_Agency')['Fine_Paid_Bool'].mean().mul(100).round(2).to_frame("% Fines Paid")
        agency_payment_rate['Total Violations'] = df['Issuing_Agency'].value_counts()
        agency_payment_rate = agency_payment_rate.sort_values('% Fines Paid', ascending=False)
        agency_payment_rate.index.name = "Issuing_Agency"

        col1, col2 = st.columns([1, 2])

        with col1:
            overall_payment_rate = df['Fine_Paid_Bool'].mean() * 100
            st.markdown(f"""
            <div style='background-color:#E8F8F5; padding:20px; border-radius:10px; text-align:center; margin:10px; box-shadow:2px 2px 10px rgba(0,0,0,0.1);'>
                <h4 style='color:#004D40;'>Overall Fine Payment Rate</h4>
                <h2 style='color:#00796B;'>{overall_payment_rate:.2f}%</h2>
            </div>
            """, unsafe_allow_html=True)

            towed_pct = df['Towed'].value_counts(normalize=True).get('Yes', 0) * 100 if 'Towed' in df.columns else 0
            st.markdown(f"""
            <div style='background-color:#F9EBEA; padding:20px; border-radius:10px; text-align:center; margin:10px; box-shadow:2px 2px 10px rgba(0,0,0,0.1);'>
                <h4 style='color:#7B241C;'>Overall Towed Rate</h4>
                <h2 style='color:#922B21;'>{towed_pct:.2f}%</h2>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("<h4 style='color:#2E7D32;'>Fine Payment Success Rate by Agency</h4>", unsafe_allow_html=True)
            st.table(style_table(agency_payment_rate))

    st.markdown("---")

else:
    st.warning("Please upload a CSV file to generate insights.")