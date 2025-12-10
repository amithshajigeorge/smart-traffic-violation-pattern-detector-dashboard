import streamlit as st
import pandas as pd
import geopandas  as gpd
import matplotlib.pyplot as plt
import seaborn as sns
from dateutil import parser
import numpy as np

# Load your dataset
df=pd.read_csv(r"C:\Users\divij\OneDrive\Desktop\Indian_Traffic_Violations.csv")

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Month'] = df['Date'].dt.month
df['DayOfWeek'] = df['Date'].dt.day_name()
df['Hour'] = pd.to_datetime(df['Time'], errors='coerce').dt.hour

# -----------------------------
# CATEGORY → GRAPH MAPPING
# -----------------------------
graphs = {
    "Number of violations Based": [
        "Number of violations based on hours of day",
        "Number of violations based on days of week",
        "Number of violations based on months of year"
    ],

    "Violation type Based": [
        "Violation type vs location feature",
        "Violation type vs vehicle type",
        "Violation type trend based on month",
        "Violation type vs vehicle age"
    ],

    "Fine Based": [
        "Average Fine amount vs location",
        "Fine paid vs vehicle type",
        "Total fines per year",
        "Fine paid vs unpaid",
        "Fine based on Violation type"
    ],

    "Weather  and Road Based": [
        "Violation distribution based on road conditions",
        "Impact of weather conditons on traffic violations",
        "Speed exceeded vs weather conditions",
        "speed exceeded vs road conditions"
    ],

    "Severity Based":[
        "Violation severity scoring feature"
    ]

}

# -----------------------------
# SIDEBAR CATEGORY DROPDOWN
# -----------------------------
st.sidebar.title("EDA Controls")

selected_category = st.sidebar.selectbox(
    "Choose Category",
    list(graphs.keys())
)

# -----------------------------
# CENTER GRAPH DROPDOWN
# -----------------------------
st.title("📊 Exploratory Data Analysis Dashboard")

selected_graph = st.selectbox(
    "Select a graph to visualize",
    graphs[selected_category]
)

st.write(f"### {selected_graph}")


# -----------------------------
# GRAPH FUNCTIONS
# -----------------------------
def plot_hoursofday():

    # Function to safely extract hour
    sns.set(style="whitegrid") 
    plt.rcParams.update({"figure.dpi": 110})

    def safe_extract_hour(t):
        try:
            return parser.parse(str(t)).hour
        except:
            return None

    # Create hour column
    df['hour'] = df['Time'].apply(safe_extract_hour)
    #df['Hour'] = pd.to_datetime(df['Time'], errors='coerce').dt.hour
    # Check if conversion failed
    if df['hour'].isnull().all():
        raise ValueError("Time column could not be converted. Send me sample Time values.")

    # Count violations per hour
    hour_counts = df['hour'].value_counts().sort_index()

    # Plot
    plt.figure(figsize=(10, 5))
    sns.lineplot(x=hour_counts.index, y=hour_counts.values, marker="o", linewidth=2)
    plt.title("Peak Hour Traffic Violations", fontsize=14)
    plt.xlabel("Hour of the Day (0–23)")
    plt.ylabel("Number of Violations")
    plt.xticks(range(0, 24))
    plt.tight_layout()
    st.pyplot(plt)

def plot_daysofweek():
    # Convert date
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    
    df['Day'] = df['Date'].dt.day_name()


    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    counts = df['Day'].value_counts().reindex(order)
    if counts.isnull().all():
        st.error("No day values found. Date parsing failed.")
        return

    plt.clf()
    plt.figure(figsize=(8,4))
    plt.plot(counts.index, counts.values, marker='o')
    plt.title("Number of violations based on days of week")
    plt.xlabel("Day")
    plt.ylabel("Number of Violations")
    plt.grid(True, alpha=0.4)

    st.pyplot(plt)


def plot_monthsofyear():
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    df['Month'] = df['Date'].dt.month
    df['Month_Name'] = df['Date'].dt.strftime('%B')

    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    monthly_counts = df['Month_Name'].value_counts().reindex(month_order)

    plt.clf()
    plt.figure(figsize=(10, 5))

    plt.plot(monthly_counts.index, monthly_counts.values, marker='o', linewidth=2)
    plt.title("Number of violations based on months of year")
    plt.xlabel("Month")
    plt.ylabel("Number of Violations")
    plt.xticks(rotation=45)
    plt.grid(True, linestyle="--", alpha=0.4)

    st.pyplot(plt)

def plot_violation_choropleth(df, shapefile_path):
    violations = df.groupby("Location").size().reset_index(name="Violation_Count")
    violations["Location"] = violations["Location"].str.strip().str.title()

    states = gpd.read_file(shapefile_path)
    states["State_Name"] = states["State_Name"].str.strip().str.title()

    merged = states.merge(
        violations,
        left_on="State_Name",
        right_on="Location",
        how="left"
    )

    fig, ax = plt.subplots(figsize=(12, 12))
    merged.plot(
        column="Violation_Count",
        cmap="Reds",
        legend=True,
        edgecolor="black",
        linewidth=0.5,
        missing_kwds={"color": "lightgrey", "label": "No Data"},
        ax=ax
    )

    plt.title("Traffic Violations Across States", fontsize=20)
    plt.axis("off")

    return fig

def plot_violation_vs_vehicle(df):
    plt.figure(figsize=(14, 8))
    sns.countplot(data=df, x='Violation_Type', hue='Vehicle_Type')

    plt.title('Vehicle Type vs Violation Type')
    plt.xlabel('Violation Type')
    plt.ylabel('Number of Violations')
    plt.xticks(rotation=45)
    plt.tight_layout()

    return plt.gcf()


def plot_violation_trend(df):
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Month'] = df['Date'].dt.month_name()

    grouped = df.groupby(['Month', 'Violation_Type']).size().reset_index(name='Count')
    pivot = grouped.pivot(index='Month', columns='Violation_Type', values='Count').fillna(0)

    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    pivot = pivot.reindex(month_order)

    plt.figure(figsize=(12, 6))
    markers = ['o','s','*','x','p','d','D','h']

    for i, col in enumerate(pivot.columns):
        plt.plot(
            pivot.index, pivot[col],
            marker=markers[i % len(markers)],
            linewidth=2,
            label=col
        )

    plt.title("Monthly Violation Trend by Violation Type")
    plt.xlabel("Month")
    plt.ylabel("Number of Violations")
    plt.xticks(rotation=45)
    plt.grid(alpha=0.3)
    plt.legend(title="Violation Type", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    return plt.gcf()


def plot_vehicle_age_vs_violation(df):
    df = df.copy()
    df['Vehicle_Age'] = pd.to_datetime(df['Date']).dt.year - pd.to_numeric(df['Vehicle_Model_Year'], errors='coerce')

    plt.figure(figsize=(14, 8))
    sns.boxplot(y="Violation_Type", x="Vehicle_Age", hue="Violation_Type", data=df)

    plt.title("Vehicle Age vs Violation Type")
    plt.xlabel("Vehicle Age")
    plt.ylabel("Violation Type")
    plt.tight_layout()

    return plt.gcf()

def plot_total_fines_per_year():
    global df
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Year'] = df['Date'].dt.year

    fines_per_year = df.groupby('Year')['Fine_Amount'].sum()

    plt.figure(figsize=(10, 6))
    plt.plot(fines_per_year.index, fines_per_year.values, marker='o')
    plt.grid(True, linestyle='--', linewidth=0.9, alpha=0.9)
    plt.title("Total fines per year")
    plt.xlabel("Year")
    plt.ylabel("Total Fine Amount")

    return plt.gcf()

def plot_avg_fine_location():
    global df

    fine_location = df.groupby('Location')['Fine_Amount'].mean().reset_index()

    plt.figure(figsize=(10,5))

    plt.plot(
        fine_location['Location'],
        fine_location['Fine_Amount'],
        marker='o'
    )

    plt.title("Average Fine Amount vs Location")
    plt.xlabel("Location")
    plt.ylabel("Average Fine Amount")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    return plt.gcf()



def plot_avg_fine_by_violation_type():
    global df

    plt.figure(figsize=(14,7))

    avg_fines = (
        df.groupby('Violation_Type')['Fine_Amount']
        .mean()
        .sort_values(ascending=False)
    )

    plt.scatter(avg_fines.index, avg_fines.values, s=120, color='red')

    for i, v in enumerate(avg_fines.values):
        plt.text(i, v + 5, f"{v:.0f}", ha='center', fontsize=10, fontweight='bold')

    plt.title("Average Fine amount vs location", fontsize=16, fontweight='bold')
    plt.xlabel("Violation Type", fontsize=14)
    plt.ylabel("Average Fine Amount (₹)", fontsize=14)
    plt.xticks(rotation=90)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()

    return plt.gcf()

def plot_fine_by_vehicle_type():
    global df

    fine_data = df.groupby('Vehicle_Type')['Fine_Amount'].sum()

    plt.figure(figsize=(8, 8))
    plt.pie(
        fine_data.values,
        labels=fine_data.index,
        autopct='%1.1f%%',
        startangle=90
    )

    plt.title("Fine Paid vs vehicle type", fontsize=18)
    plt.axis('equal')
    plt.tight_layout()

    return plt.gcf()

def total_fines_generated_stackbar_plot():
    global df

    # Make a working copy
    df_last_n_days = df.copy()

    # Convert fine amount to numeric
    df_last_n_days['Fine_Amount'] = pd.to_numeric(df_last_n_days['Fine_Amount'], errors='coerce').fillna(0)

    # Clean Fine_Paid column
    df_last_n_days['Fine_Paid'] = df_last_n_days['Fine_Paid'].astype(str).str.upper().str.strip()

    # Prepare summary table
    summary = (
        df_last_n_days
        .groupby(['Violation_Type', 'Fine_Paid'])['Fine_Amount']
        .sum()
        .unstack(fill_value=0)
    )

    summary = summary.rename(columns={'YES': 'Paid', 'NO': 'Unpaid'})

    # Plot
    plt.figure(figsize=(16, 9))
    ax = summary.plot(
        kind='bar',
        stacked=True,
        figsize=(16, 9),
        color=['#FF6B6B', '#4ECDC4'],  # Paid, Unpaid
        edgecolor='black',
        linewidth=1.5
    )

    plt.title('Fines Based on Violation Type', fontweight='bold')
    plt.xlabel('Violation Type', fontweight='bold')
    plt.ylabel('Total Fine Amount (₹)', fontweight='bold')
    plt.xticks(rotation=25)
    plt.yticks(rotation=25)

    # Format Y-axis with commas
    import matplotlib.ticker as mtick
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))

    # Compute totals for percentage labels
    totals = summary.sum(axis=1)

    # Add percentage labels inside each stacked bar
    for c in ax.containers:
        labels = []
        for i, v in enumerate(c):
            height = v.get_height()
            if height > 0:
                percentage = (height / totals.iloc[i]) * 100
                labels.append(f'{percentage:.1f}%')
            else:
                labels.append('')
        ax.bar_label(
            c,
            labels=labels,
            label_type='center',
            fontsize=10,
            color='black',
            rotation=0,
            fontweight='bold'
        )

    # Add total amount above each bar
    for idx, total in enumerate(totals):
        ax.text(
            idx,
            summary.iloc[idx].sum() + (max(totals) * 0.02),
            f'{total:,.0f}',
            ha='center',
            va='bottom',
            fontsize=10,
            fontweight='bold',
            color='black'
        )

    plt.tight_layout()

    # Legend outside
    plt.legend(
        title="Status",
        bbox_to_anchor=(1, 1.05),
        loc="upper right",
        ncol=2
    )

    return plt.gcf()

def plot_violation_by_road_condition():
    global df

    # Define custom order
    order = ["Slippery", "Under Construction", "Dry", "Wet", "Potholes"]

    # Count values
    road_counts = df['Road_Condition'].value_counts()

    # Custom colors
    colors = [
        "#5bbae2",    # Slippery
        "#acd3e4",    # Under Construction
        "#135570",    # Dry
        "#56a34c",    # Wet
        "#ca9998"     # Potholes
    ]

    # Maintain order even if some conditions don't exist
    values = [road_counts.get(x, 0) for x in order]

    # Plot
    plt.figure(figsize=(5, 5))
    plt.pie(
        values,
        labels=order,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors
    )

    plt.title("Violation distribution based on road conditions")
    plt.tight_layout()

    return plt.gcf()

def plot_weather_condition_heatmap():
    global df

    # Create pivot table
    pivot = df.pivot_table(
        index="Violation_Type",
        columns="Weather_Condition",
        values="Violation_ID",
        aggfunc="count",
        fill_value=0
    )

    # Plot heatmap
    plt.figure(figsize=(12, 8))
    ax = sns.heatmap(
        pivot,
        annot=True,
        fmt="d",
        cmap="YlGnBu",
        cbar=True
    )

    # Colorbar label
    colorbar = ax.collections[0].colorbar
    colorbar.set_label("Number of Violations")

    # Title and labels
    plt.title("Impact of Weather Conditions on Traffic Violations", fontsize=14)
    plt.xlabel("Weather Condition")
    plt.ylabel("Violation Type")
    plt.tight_layout()

    return plt.gcf()

def plot_speed_exceeded_vs_weather():
    global df

    # Compute speed exceeded
    df['Speed_Exceeded'] = df['Recorded_Speed'] - df['Speed_Limit']

    # Calculate average exceeded speed per weather type
    avg_speed = (
        df.groupby('Weather_Condition')['Speed_Exceeded']
        .mean()
        .sort_values(ascending=False)
    )

    # Plot
    plt.figure(figsize=(14, 7))
    sns.barplot(
        x=avg_speed.index,
        y=avg_speed.values,
        palette='viridis'
    )

    # Add value labels
    for i, v in enumerate(avg_speed.values):
        plt.text(i, v + 0.5, f"{v:.1f}", ha='center',
                 fontsize=10, fontweight='bold')

    # Titles and labels
    plt.title("Average Speed Exceeded vs Weather Condition", fontsize=16, fontweight='bold')
    plt.xlabel("Weather Condition", fontsize=14)
    plt.ylabel("Average Speed Exceeded (km/h)", fontsize=14)

    plt.xticks(rotation=45)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()

    return plt.gcf()

def plot_speeding_vs_road_condition():
    global df

    # Compute speeding
    df['Speeding'] = df['Recorded_Speed'] - df['Speed_Limit']

    # Filter only speeding cases
    speed_df = df[df['Speeding'] > 0]

    # Average speeding for each road condition
    avg_speeding = speed_df.groupby('Road_Condition')['Speeding'].mean().reset_index()

    # Plot
    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=avg_speeding,
        y='Road_Condition',
        x='Speeding',
        orient='h',
        palette='magma',
        hue='Road_Condition'
)

    plt.title("Average Speeding Across Different Road Conditions")
    plt.xlabel("Average Speeding (km/h)")
    plt.ylabel("Road Condition")
    plt.legend().remove()  # Removes duplicate legend
    plt.tight_layout()

    return plt.gcf()

def plot_severity_score_heatmap():
    global df

    # -----------------------
    # 1. Calculate severity score for each row
    # -----------------------
    def calc_severity_score(row):
        severity = 0

        # Fine Amount
        if pd.notnull(row['Fine_Amount']):
            severity += row['Fine_Amount'] / 1000

        # Penalty Points
        severity += row.get('Penalty_Points', 0)

        # Speed Violation
        if pd.notnull(row['Recorded_Speed']) and pd.notnull(row['Speed_Limit']):
            overspeed = row['Recorded_Speed'] - row['Speed_Limit']
            if overspeed > 0:
                severity += overspeed / 10

        # Alcohol Level
        if pd.notnull(row.get('Alcohol_Level', None)):
            severity += row['Alcohol_Level'] * 10

        # Helmet / Seatbelt
        if row.get('Helmet_Worn', '') == 'No':
            severity += 10
        if row.get('Seatbelt_Worn', '') == 'No':
            severity += 10

        # Red Light Jump
        if row.get('Traffic_Light_Status', '') == 'Red':
            severity += 15

        # Previous Violations
        severity += row.get('Previous_Violations', 0) * 1.5

        return severity

    # Apply severity score
    df['Violation_Severity_Score'] = df.apply(calc_severity_score, axis=1)

    # -----------------------
    # 2. Create pivot table
    # -----------------------
    location_heatmap = df.pivot_table(
        values='Violation_Severity_Score',
        index='Location',
        columns='Violation_Type',
        aggfunc=np.mean
    )

    # -----------------------
    # 3. Plot heatmap
    # -----------------------
    plt.figure(figsize=(14, 7))
    sns.heatmap(location_heatmap, cmap='coolwarm', annot=True)

    plt.title("Violation severity scoring feature", fontsize=14)
    plt.xlabel("Violation Type")
    plt.ylabel("Location")
    plt.tight_layout()

    return plt.gcf()

# -----------------------------
# DISPLAY SELECTED GRAPH
# -----------------------------
if selected_graph == "Number of violations based on hours of day":
    plot_hoursofday()

elif selected_graph == "Number of violations based on days of week":
    plot_daysofweek()

elif selected_graph == "Number of violations based on months of year":
    plot_monthsofyear()

elif selected_graph == "Violation type vs location feature":
    fig = plot_violation_choropleth(df, shapefile_path)
    st.pyplot(fig)

elif selected_graph == "Violation type vs vehicle type":
     fig = plot_violation_vs_vehicle(df)
     st.pyplot(fig)

elif selected_graph == "Violation type trend based on month":
      fig = plot_violation_trend(df)
      st.pyplot(fig)

elif selected_graph == "Violation type vs vehicle age":
    fig = plot_vehicle_age_vs_violation(df)
    st.pyplot(fig)

elif selected_graph == "Total fines per year":
    fig = plot_total_fines_per_year()
    st.pyplot(fig)

elif selected_graph == "Fine paid vs unpaid":
    fig = total_fines_generated_stackbar_plot()
    st.pyplot(fig)

elif selected_graph == "Average Fine amount vs location":
    fig = plot_avg_fine_location()
    st.pyplot(fig)

elif selected_graph == "Fine based on Violation type":
    fig = plot_avg_fine_by_violation_type()
    st.pyplot(fig)

elif selected_graph == "Fine paid vs vehicle type":
    fig = plot_fine_by_vehicle_type()
    st.pyplot(fig)

elif selected_graph == "Violation distribution based on road conditions":
    fig = plot_violation_by_road_condition()
    st.pyplot(fig)

elif selected_graph == "Impact of weather conditons on traffic violations":
    fig = plot_weather_condition_heatmap()
    st.pyplot(fig)  

elif selected_graph == "Speed exceeded vs weather conditions":
    fig = plot_speed_exceeded_vs_weather()   
    st.pyplot(fig)

elif selected_graph == "speed exceeded vs road conditions":
    fig = plot_speeding_vs_road_condition()
    st.pyplot(fig)  

elif selected_graph == "Violation severity scoring feature":
    fig = plot_severity_score_heatmap()
    st.pyplot(fig)