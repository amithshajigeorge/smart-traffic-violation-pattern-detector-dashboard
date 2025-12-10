import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.ticker as mtick

# ---------------------------------------------------------
# UNIFORM STYLE CONFIGURATION
# ---------------------------------------------------------
# Define standard formatting constants
TITLE_SIZE = 20
LABEL_SIZE = 18
TICK_SIZE = 16
TITLE_WEIGHT = 'bold'
LABEL_WEIGHT = 'bold'
TICK_WEIGHT = 'bold' # Generalized control for X/Y tick weightage
TICK_WIDTH = 3 # Generalized control for X/Y tick width
FIG_SIZE = (16, 9)

# Define a standard color family (High intensity, distinct colors)
UNI_PALETTE = "deep" 
DISTINCT_COLORS = sns.color_palette("deep")

def apply_plot_style():
    """
    Applies the uniform style settings to matplotlib and seaborn.
    Call this at the start of plot functions or globally.
    """
    sns.set_theme(style="whitegrid", context="talk", palette=UNI_PALETTE)
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.size': TICK_SIZE,
        'axes.titlesize': TITLE_SIZE,
        'axes.titleweight': TITLE_WEIGHT,
        'axes.labelsize': LABEL_SIZE,
        'axes.labelweight': LABEL_WEIGHT,
        'xtick.labelsize': TICK_SIZE,
        'ytick.labelsize': TICK_SIZE,
        'figure.titlesize': TITLE_SIZE,
        'figure.figsize': FIG_SIZE,
        'axes.grid': True,
        'grid.alpha': 0.3,
        'xtick.major.width': TICK_WIDTH,
        'ytick.major.width': TICK_WIDTH,
        'axes.linewidth': TICK_WIDTH
    })

# Apply global style on module load
apply_plot_style()

# ---------------------------------------------------------
# PLOT FUNCTIONS
# ---------------------------------------------------------

def plot_speed_exceeded_vs_weather(df):
    """
    Plots Average Speed Exceeded vs Weather Condition.
    """
    apply_plot_style()
    df['Speed_Exceeded'] = df['Recorded_Speed'] - df['Speed_Limit']

    fig, ax = plt.subplots(figsize=FIG_SIZE)

    avg_speed = df.groupby('Weather_Condition')['Speed_Exceeded'].mean().sort_values(ascending=False)

    sns.barplot(
        x=avg_speed.index,
        y=avg_speed.values,
        hue=avg_speed.index,
        palette='magma', # Intensity based
        ax=ax,
        legend=False
    )

    # Add value labels
    for i, v in enumerate(avg_speed.values):
        ax.text(i, v + 0.5, f"{v:.1f}", ha='center', fontsize=TICK_SIZE, fontweight='bold')

    ax.set_title("Average Speed Exceeded vs Weather Condition")
    ax.set_xlabel("Weather Condition")
    ax.set_ylabel("Average Speed Exceeded (km/h)")

    plt.xticks(rotation=25, fontweight=TICK_WEIGHT)
    plt.yticks(fontweight=TICK_WEIGHT)
    plt.tight_layout()
    return fig

def plot_avg_fine_by_violation_type(df):
    """
    Plots Average Fine Amount by Violation Type (Scatter Plot).
    """
    apply_plot_style()
    fig, ax = plt.subplots(figsize=FIG_SIZE)

    avg_fines = df.groupby('Violation_Type')['Fine_Amount'].mean().sort_values(ascending=False)

    sns.scatterplot(
        x=avg_fines.index, 
        y=avg_fines.values, 
        s=200, 
        color=DISTINCT_COLORS[3], # specific bold color
        ax=ax
    )

    for i, v in enumerate(avg_fines.values):
        ax.text(i, v + 50, f"{v:.0f}", ha='center', fontsize=TICK_SIZE, fontweight='bold')

    ax.set_title("Average Fine Amount by Violation Type")
    ax.set_xlabel("Violation Type")
    ax.set_ylabel("Average Fine Amount (₹)")

    plt.xticks(rotation=25, fontweight=TICK_WEIGHT)
    plt.yticks(fontweight=TICK_WEIGHT)
    plt.tight_layout()
    return fig

def plot_bar_or_count(df, x_col, y_col):
    """
    Generates a bar plot or count plot based on the Y-axis selection.
    """
    apply_plot_style()
    fig, ax = plt.subplots(figsize=FIG_SIZE)

    if y_col == 'Count':
        sns.countplot(x=x_col, data=df, ax=ax, order=df[x_col].value_counts().index, palette=UNI_PALETTE)
        ax.set_title(f"Count of {x_col}")
        ax.set_ylabel("Count")
    else:
        sns.barplot(x=x_col, y=y_col, hue=x_col, legend=False, data=df, ax=ax, estimator=lambda x: x.mean(), palette=UNI_PALETTE)
        ax.set_title(f"Mean of {y_col} by {x_col}")
        ax.set_ylabel(f"Mean {y_col}")

    ax.set_xlabel(x_col)
    ax.set_xlabel(x_col)
    ax.tick_params(axis='x', rotation=25, labelsize=TICK_SIZE, labelcolor='black')
    # Apply weight manually since tick_params doesn't support fontweight directly easily for all backends in one go, 
    # but let's use plt.setp for reliability or just handle axis ticks.
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontweight(TICK_WEIGHT)
    fig.tight_layout()
    return fig

def plot_correlation_heatmap(df, numerical_cols):
    """
    Plots a correlation heatmap for numerical columns.
    """
    apply_plot_style()
    corr_matrix = df[numerical_cols].corr()

    fig = plt.figure(figsize=FIG_SIZE)
    sns.heatmap(
        corr_matrix, 
        annot=True, 
        cmap='coolwarm', 
        linewidths=0.5,  
        fmt=".2f",
        annot_kws={"size": TICK_SIZE, "weight": "bold"}
    )
    plt.title("Numerical Correlation Matrix")
    plt.xticks(rotation=25, fontweight=TICK_WEIGHT)
    plt.yticks(fontweight=TICK_WEIGHT)
    plt.tight_layout()
    return fig

# ---------------------------------------------------------
# TEAM PLOTS - INTEGRATED FUNCTIONS
# ---------------------------------------------------------

# --- MONIKA'S PLOTS ---

def plot_top_5_locations_violation(df):
    apply_plot_style()
    fig = plt.figure(figsize=FIG_SIZE)
    Location_Count = df['Location'].value_counts().head(5)
    sns.barplot(x=Location_Count.index, y=Location_Count.values, hue=Location_Count.index, legend=False, palette="viridis")
    plt.title("Top 5 Locations (Violations)")
    plt.xlabel("Location")
    plt.ylabel("Count")
    plt.xticks(rotation=25, fontweight=TICK_WEIGHT)
    plt.yticks(fontweight=TICK_WEIGHT)
    plt.close()
    return fig

def plot_vehicle_type_vs_violation_type(df):
    apply_plot_style()
    fig = plt.figure(figsize=FIG_SIZE)
    sns.countplot(data=df, x='Violation_Type', hue='Vehicle_Type', palette=UNI_PALETTE)
    plt.title('Vehicle Type vs Violation Type')
    plt.xlabel('Violation Type')
    plt.ylabel('Number of Violations')
    plt.legend(title='Vehicle Type', fontsize=TICK_SIZE)
    plt.xticks(rotation=25, fontweight=TICK_WEIGHT)
    plt.yticks(fontweight=TICK_WEIGHT)
    # COntrol the legend size and location out of the plot area
    plt.legend(fontsize=TICK_SIZE,loc='upper right', bbox_to_anchor=(1.2, 1))
    plt.tight_layout()
    plt.close()
    return fig

# --- AMITH'S PLOTS ---

def plot_violation_type_percentage(df):
    apply_plot_style()
    violation_counts = df['Violation_Type'].value_counts()
    fig = plt.figure(figsize=FIG_SIZE)
    
    # Use distinct colors
    plt.pie(
        violation_counts,
        labels=violation_counts.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=sns.color_palette(UNI_PALETTE),
        textprops={'fontsize': TICK_SIZE, 'weight': 'bold'}
    )
    plt.title('Percentage of Traffic Violation Types')
    plt.axis('equal')
    plt.close()
    return fig



# --- HARIKA'S PLOTS ---

def plot_repeat_offenders(df):
    apply_plot_style()
    fig = plt.figure(figsize=FIG_SIZE)
    # Use a high contrast sequential palette
    palette = sns.color_palette("rocket_r", n_colors=10) 
    
    if 'Previous_Violations' in df.columns:
        violations = df[df['Previous_Violations']>3].head(10)
        if not violations.empty:
            plt.barh(
                violations.get('Violation_ID', range(len(violations))), 
                violations['Previous_Violations'], 
                color=palette
            )
            plt.title('Repeat Offenders (Records with > 3 violations)')
            plt.xlabel('Number of Previous Violations')
            plt.ylabel('Record / Violation ID')
            plt.tight_layout()
            plt.xticks(fontweight=TICK_WEIGHT)
            plt.yticks(fontweight=TICK_WEIGHT)
        else:
            plt.text(0.5, 0.5, "No records with > 3 previous violations", ha='center', fontsize=TITLE_SIZE)
    plt.close()
    return fig

def plot_violation_by_location_pie(df):
    apply_plot_style()
    location_counts = df["Location"].value_counts()
    if len(location_counts) > 10:
        top_n = location_counts.head(10)
        others_count = location_counts.iloc[10:].sum()
        if others_count > 0:
            top_n['Others'] = others_count
        location_counts = top_n

    fig, ax = plt.subplots(figsize=FIG_SIZE)
    
    wedges, texts, autotexts = ax.pie(
        location_counts,
        autopct='%1.1f%%',
        startangle=90,
        colors=sns.color_palette("colorblind"), # Better distinction
        wedgeprops={'edgecolor': 'white', 'linewidth': 1},
        pctdistance=0.85,
        textprops={'fontsize': TICK_SIZE}
    )
    
    plt.setp(autotexts, size=12, weight="bold", color="white")
    
    ax.legend(
        wedges, 
        location_counts.index,
        title="Locations",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
        fontsize=TICK_SIZE,
        title_fontsize=LABEL_SIZE
    )
    
    ax.set_title("Violations by Location (%)")
    ax.axis('equal')
    plt.tight_layout()
    plt.close()
    return fig

# --- DARSANA'S PLOTS ---

def plot_speeding_vs_road_condition(df):
    apply_plot_style()
    df = df.copy()
    if 'Recorded_Speed' in df.columns and 'Speed_Limit' in df.columns:
        df['Speeding'] = df['Recorded_Speed'] - df['Speed_Limit']
        speed_df = df[df['Speeding'] > 0]
        
        avg_speeding = speed_df.groupby('Road_Condition')['Speeding'].mean().reset_index()
        
        fig = plt.figure(figsize=FIG_SIZE)
        sns.barplot(
            data=avg_speeding,
            y='Road_Condition',
            x='Speeding',
            orient='h',
            palette='magma', # Heat intensity
            hue='Road_Condition',
            legend=False
        )
        plt.title("Average Speeding vs Road Conditions")
        plt.xlabel("Average Speeding (km/h)")
        plt.ylabel("Road Condition")
        plt.xticks(rotation=25, fontweight=TICK_WEIGHT)
        plt.yticks(fontweight=TICK_WEIGHT)
        plt.close()
        return fig
    return None

def plot_fines_vs_weather_severity(df):
    apply_plot_style()
    fig = plt.figure(figsize=FIG_SIZE)
    df_severity = df.groupby('Weather_Condition')['Fine_Amount'].mean().sort_values()
    
    sns.barplot(
        x=df_severity.values,
        y=df_severity.index,
        orient='h',
        hue=df_severity.index,
        palette='Reds', # Intensity helps identify
        legend=False
    )
    plt.xlabel("Average Fine Amount (Severity Indicator)")
    plt.ylabel("Weather Condition")
    plt.title("Weather Condition vs Severity")
    plt.xticks(rotation=25, fontweight=TICK_WEIGHT)
    plt.yticks(fontweight=TICK_WEIGHT)
    plt.tight_layout()
    plt.close()
    return fig

# --- MRUNALINI'S PLOTS ---

def plot_severity_heatmap_by_location(df):
    apply_plot_style()
    df = df.copy()
    
    def calc_severity_score(row):
        severity = 0
        if pd.notnull(row.get('Fine_Amount')): severity += row['Fine_Amount'] / 1000
        if pd.notnull(row.get('Penalty_Points')): severity += row['Penalty_Points'] 
        if pd.notnull(row.get('Recorded_Speed')) and pd.notnull(row.get('Speed_Limit')):
            overspeed = row['Recorded_Speed'] - row['Speed_Limit']
            if overspeed > 0: severity += overspeed /10
        if pd.notnull(row.get('Alcohol_Level')): severity += row['Alcohol_Level'] * 10
        if row.get('Helmet_Worn') == 'No': severity += 10
        if row.get('Seatbelt_Worn') == 'No': severity += 10
        if row.get('Traffic_Light_Status') == 'Red': severity += 15
        if pd.notnull(row.get('Previous_Violations')): severity += row['Previous_Violations'] * 1.5
        return severity

    df['Violation_Severity_Score'] = df.apply(calc_severity_score, axis=1)
    
    location_heatmap = df.pivot_table(
        values='Violation_Severity_Score',
        index='Location',
        columns='Violation_Type',
        aggfunc='mean'
    )

    fig = plt.figure(figsize=FIG_SIZE)
    sns.heatmap(
        location_heatmap, 
        cmap='magma_r', # Updated color family
        annot=True, 
        fmt=".1f",
        annot_kws={"size": TICK_SIZE, "weight": "bold"}
    )
    plt.title("Average Severity Score Heatmap", pad=20)
    plt.xticks(rotation=25, fontweight=TICK_WEIGHT)
    plt.yticks(fontweight=TICK_WEIGHT)
    plt.tight_layout()
    plt.close()
    return fig

# --- POOJITHA'S PLOTS ---

def plot_speed_exceeded_vs_weather_2(df):
    return plot_speed_exceeded_vs_weather(df) # Reuse standardized function

def plot_avg_fine_by_violation_type_2(df):
    return plot_avg_fine_by_violation_type(df) # Reuse standardized function

# --- RAKSHITHA'S PLOTS ---



def plot_violation_by_road_condition(df):
    apply_plot_style()
    road_counts = df['Road_Condition'].value_counts()
    
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    
    wedges, texts, autotexts = ax.pie(
        road_counts,
        autopct="%1.1f%%",
        startangle=90,
        colors=sns.color_palette("Set2"),
        wedgeprops={'edgecolor': 'white'},
        pctdistance=0.85
    )
    
    plt.setp(autotexts, size=12, weight="bold")
    
    ax.legend(
        wedges, 
        road_counts.index,
        title="Road Conditions",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
        fontsize=TICK_SIZE,
        title_fontsize=LABEL_SIZE
    )

    ax.set_title("Violations by Road Condition")
    ax.axis('equal')
    plt.tight_layout()
    plt.close()
    return fig

# --- SANIYA'S PLOTS ---

def plot_weather_impact_heatmap(df):
    apply_plot_style()
    pivot = df.pivot_table(
        index="Violation_Type",
        columns="Weather_Condition",
        values="Violation_ID",
        aggfunc="count",
        fill_value=0
    )
    fig = plt.figure(figsize=FIG_SIZE)
    sns.heatmap(
        pivot, 
        annot=True, 
        fmt="d", 
        cmap="YlGnBu", # Updated color family
        cbar=True,
        annot_kws={"size": TICK_SIZE, "weight": "bold"}
    )
    plt.title("Impact of Weather Conditions")
    plt.xlabel("Weather Condition")
    plt.ylabel("Violation Type")
    plt.xticks(rotation=25, fontweight=TICK_WEIGHT)
    plt.yticks(fontweight=TICK_WEIGHT)
    plt.tight_layout()
    plt.close()
    return fig



# --- SANJANA'S PLOTS ---

def plot_vehicle_risk_countplot(df):
    apply_plot_style()
    vehicle_counts = df['Vehicle_Type'].value_counts().index
    fig = plt.figure(figsize=FIG_SIZE)
    sns.countplot(
        y=df['Vehicle_Type'],
        order=vehicle_counts,
        palette='Reds_r', # Intensity indicates risk/freq
        hue=df['Vehicle_Type'],
        legend=False
    )
    plt.title('Vehicle-Type Based Risk Analysis')
    plt.xlabel('Count')
    plt.ylabel('Vehicle Type')
    plt.xticks(rotation=25, fontweight=TICK_WEIGHT)
    plt.yticks(fontweight=TICK_WEIGHT)
    plt.tight_layout()
    plt.close()
    return fig

def plot_age_alcohol_heatmap(df):
    apply_plot_style()
    df = df.copy()
    bins = [0, 25, 35, 45, 60, 100]
    labels = ["18-25", "26-35", "36-45", "46-60", "60+"]
    
    max_alcohol = df['Alcohol_Level'].max()
    upper = max(0.251, max_alcohol)
    ranges = [0, 0.03, 0.08, 0.15, 0.25, upper]
    safelevels = ['Safe', 'Mild', 'Risky', 'High Risk', 'Dangerous']
    ranges = sorted(list(set(ranges)))
    
    if len(ranges) - 1 != len(safelevels): 
        return None

    df["Age_Group"] = pd.cut(df["Driver_Age"], bins=bins, labels=labels, include_lowest=True)
    df["Alcohol_Range"] = pd.cut(df["Alcohol_Level"], bins=ranges, labels=safelevels, include_lowest=True)
    
    heatmap_data = pd.crosstab(df['Age_Group'], df['Alcohol_Range'])
    
    fig = plt.figure(figsize=FIG_SIZE)
    sns.heatmap(
        heatmap_data, 
        annot=True, 
        fmt="d", 
        cmap="YlOrRd", # Updated Color
        annot_kws={"size": TICK_SIZE, "weight": "bold"}
    )
    plt.title("Age Group vs Alcohol Risk Heatmap")
    plt.xlabel("Alcohol Test Classification")
    plt.ylabel("Age Group")
    plt.xticks(rotation=25, fontweight=TICK_WEIGHT)
    plt.yticks(fontweight=TICK_WEIGHT)
    plt.tight_layout()
    plt.close()
    return fig

# --- ISHWARI'S PLOTS ---

def plot_fine_vs_vehicle_pie(df):
    apply_plot_style()
    fine_data = df.groupby('Vehicle_Type')['Fine_Amount'].sum()
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    
    wedges, texts, autotexts = ax.pie(
        fine_data.values,
        labels=fine_data.index,
        autopct='%1.1f%%',
        startangle=90,
        pctdistance=0.85,  # Push percentage text outward suitable for donut
        colors=sns.color_palette("Set2"),
        wedgeprops=dict(width=0.4, edgecolor='w'), # This creates the donut hole
        textprops={'fontsize': TICK_SIZE, 'weight': 'bold'}
    )
    
    # Draw a circle at the center to ensure it looks like a donut (optional with wedgeprops width but good for customization)
    # centre_circle = plt.Circle((0,0),0.70,fc='white')
    # fig.gca().add_artist(centre_circle)
    
    ax.set_title("Total Fines Paid by Vehicle Type")
    plt.axis('equal') 
    plt.close()
    return fig



# ---- Anshu's Plots ----

def plot_license_validity_by_gender(df):
    apply_plot_style()
    validity_gender = df.groupby(['License_Validity', 'Driver_Gender']).size().unstack(fill_value=0)
    
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    validity_gender.plot(
        kind='bar', 
        ax=ax, 
        color=sns.color_palette("Paired")
    )

    ax.set_title("License Validity by Gender")
    ax.set_xlabel("License Status")
    ax.set_ylabel("Count")
    plt.xticks(rotation=25, fontweight=TICK_WEIGHT)
    plt.yticks(fontweight=TICK_WEIGHT)
    ax.legend(title="Driver Gender", fontsize=TICK_SIZE)
    plt.tight_layout()
    return fig

def plot_fine_amount_distribution_vs_weather(df):
    apply_plot_style()
    plt.figure(figsize=FIG_SIZE)
    sns.violinplot(
        data=df, 
        x='Weather_Condition', 
        y='Fine_Amount', 
        inner='box', 
        palette="muted",
        hue='Weather_Condition',
        legend=False
    )
    
    plt.title("Fine Amount Distribution vs Weather")
    plt.xlabel("Weather Condition")
    plt.ylabel("Fine Amount")
    plt.xticks(rotation=25, fontweight=TICK_WEIGHT)
    plt.yticks(fontweight=TICK_WEIGHT)
    plt.tight_layout()
    return plt.gcf()

def plot_violation_types_vs_weather_heatmap(df):
    apply_plot_style()
    plt.figure(figsize=FIG_SIZE)
    heatmap_violation = pd.crosstab(df['Weather_Condition'], df['Violation_Type'])
    
    sns.heatmap(
        heatmap_violation, 
        annot=True, 
        cmap='YlOrRd',
        fmt='d',
        annot_kws={"size": TICK_SIZE, "weight": "bold"}
    )
    
    plt.title("Violation Types vs Weather")
    plt.xlabel("Violation Type")
    plt.ylabel("Weather Condition")
    plt.xticks(rotation=25, fontweight=TICK_WEIGHT)
    plt.yticks(fontweight=TICK_WEIGHT)
    plt.tight_layout()
    return plt.gcf()



def plot_driver_risk_by_age(df):
    apply_plot_style()
    df = df.copy()
    bins = [0, 25, 35, 45, 60, 100]
    labels = ["18-25", "26-35", "36-45", "46-60", "60+"]
    df["Age_Group"] = pd.cut(df["Driver_Age"], bins=bins, labels=labels, include_lowest=True)
    
    df['Alcohol_Flag'] = (df['Breathalyzer_Result'] == "Positive").astype(int)
    df["Risk_Level"] = df["Previous_Violations"] + df["Alcohol_Flag"]

    risk_by_age = df.groupby("Age_Group", observed=False)["Risk_Level"].mean().reset_index()
    risk_by_age = risk_by_age.sort_values("Age_Group")

    fig, ax = plt.subplots(figsize=FIG_SIZE)
    
    ax.plot(
        risk_by_age["Age_Group"],
        risk_by_age["Risk_Level"],
        marker="o",
        markersize=10,
        linewidth=3,
        color="#D43F6A" 
    )
    for i, row in risk_by_age.iterrows():
        ax.text(
            row["Age_Group"],
            row["Risk_Level"] + 0.02,
            f"{row['Risk_Level']:.2f}",
            ha="center",
            fontsize=TICK_SIZE,
            weight="bold",
            color="white" # Ensure explicit white for text on chart
        )
    ax.set_title("Average Driver Risk Level by Age Group", fontsize=TICK_SIZE, fontweight='bold')
    ax.set_xlabel("Age Group", fontsize=TICK_SIZE, fontweight='bold')
    ax.set_ylabel("Average Risk Level", fontsize=TICK_SIZE, fontweight='bold')
    plt.xticks(rotation=25, fontweight=TICK_WEIGHT)
    plt.yticks(fontweight=TICK_WEIGHT)
    plt.tight_layout()
    plt.close()
    return fig