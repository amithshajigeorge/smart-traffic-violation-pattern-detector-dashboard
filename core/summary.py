from datetime import datetime

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

import matplotlib.ticker as mtick

"""
All Fields in the dataset:
    Violation_ID                  object
    Violation_Type                object
    Fine_Amount                    int64
    Location                      object
    Date                          object
    Time                          object
    Vehicle_Type                  object
    Vehicle_Color                 object
    Vehicle_Model_Year             int64
    Registration_State            object
    Driver_Age                     int64
    Driver_Gender                 object
    License_Type                  object
    Penalty_Points                 int64
    Weather_Condition             object
    Road_Condition                object
    Officer_ID                    object
    Issuing_Agency                object
    License_Validity              object
    Number_of_Passengers           int64
    Helmet_Worn                   object
    Seatbelt_Worn                 object
    Traffic_Light_Status          object
    Speed_Limit                    int64
    Recorded_Speed                 int64
    Alcohol_Level                float64
    Breathalyzer_Result           object
    Towed                         object
    Fine_Paid                     object
    Payment_Method                object
    Court_Appearance_Required     object
    Previous_Violations            int64
    Comments                      object
"""

# =================================================================================
def get_violations_summary_of_last_n_days(df_last_n_days: pd.DataFrame, last_n_days: int = 30) -> int:
    """
    Description:
    ---
    Returns the total number of violations in the last n days and a figure of violation types distribution.
    
    Required Fields:
    ---
    DataFrame must contain 'Date' and 'Violation_Type' columns.
    1. 'Date' column should be in datetime format.
    2. 'Violation_Type' column should contain categorical data representing different types of violations.

    Parameters:
    ---
    df (pd.DataFrame): The input DataFrame containing traffic violation data.
    last_n_days (int): The number of days to look back from the current date.
    
    Returns:
    ---
    total_no_of_violations (int): Total number of violations in the last n days
    fig (plt.Figure): A matplotlib figure object representing the violation types distribution.
    """
    # 2. calculate the no of violations in last n days
    total_no_of_violations = df_last_n_days.shape[0]

    # 3. Generate a figure of barplot for violation types
    sns.set_theme(style='darkgrid')
    plt.figure(figsize=(14,6.3))
    sns.countplot(data=df_last_n_days,
                x='Violation_Type', 
                order=df_last_n_days['Violation_Type'].value_counts().iloc[::-1].index,
                palette='viridis',
                edgecolor='black', 
                linewidth=1.5
    )
    plt.xlabel('Violation Type', fontweight='bold')
    plt.ylabel('No of Violations', fontweight='bold')
    plt.xticks(rotation=45)
    for idx, total in enumerate(df_last_n_days['Violation_Type'].value_counts().iloc[::-1]):
        plt.text(
            idx,
            total + (total_no_of_violations * 0.01),
            f'{total:,.0f}',
            ha='center', va='bottom', fontsize=10, fontweight='bold', color='black'
        )
    return total_no_of_violations, plt.gcf()

# =================================================================================
def get_total_fines_generated(df_last_n_days: pd.DataFrame, last_n_days: int = 30) -> float:

    """
    Description:
    ---
    Returns the total fines generated in the last n days.
    Required Fields:
    ---
    DataFrame must contain 'Date' and 'Fine_Amount' columns.
    1. 'Date' column should be in datetime format.
    2. 'Fine_Amount' column should contain numeric data representing fine amounts.
    Parameters:
    ---
    df (pd.DataFrame): The input DataFrame containing traffic violation data.
    last_n_days (int): The number of days to look back from the current date.
    """

    # 2. calculate total fines in last n days
    total_fines = df_last_n_days['Fine_Amount'].sum()
    avg_fine_per_violation = total_fines / df_last_n_days.shape[0] if df_last_n_days.shape[0] > 0 else 0
    # ==============================================================================
    # 3. Prepare data for fines based on violation type
    df_last_n_days['Fine_Amount'] = pd.to_numeric(df_last_n_days['Fine_Amount'], errors='coerce').fillna(0)
    df_last_n_days['Fine_Paid'] = df_last_n_days['Fine_Paid'].astype(str).str.upper().str.strip()
    summary = (df_last_n_days.groupby(['Violation_Type', 'Fine_Paid'])['Fine_Amount'].sum().unstack(fill_value=0))
    summary = summary.rename(columns={'YES': 'Paid', 'NO': 'Unpaid'})
    
    # 4. Generate a figure of fines based on violation type
    sns.set_theme(style='darkgrid')
    ax = summary.plot(
        kind='bar',
        stacked=True,
        figsize=(14,6.5),
        color=['red', 'steelblue'],     # Paid, Unpaid
        edgecolor='black', 
        linewidth=1.5
    )
    plt.xlabel('Violation Type', fontweight='bold')
    plt.ylabel('Total Fine Amount (₹)',fontweight='bold')
    plt.xticks(rotation=25)
    plt.yticks(rotation=25)

    # 5. Format Color Bar values, Y-axis values, and add total fine above bars
    plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))
    # Show Paid / Unpaid inside bars
    for c in ax.containers:
        ax.bar_label(c, label_type='center', fontsize=10, color='black', rotation=45)
    totals = summary.sum(axis=1)
    for idx, total in enumerate(totals):
        ax.text(
            idx,
            summary.iloc[idx].sum() + (max(totals) * 0.02),
            f'{total:,.0f}',
            ha='center', va='bottom', fontsize=10, fontweight='bold', color='black'
        )
    # Legend outside plot area
    plt.legend(title="Status", bbox_to_anchor=(0.5, 1.12), loc="upper center", ncol=2)
    return total_fines, avg_fine_per_violation, plt.gcf()

# =================================================================================
def get_violations_by_location(df_last_n_days: pd.DataFrame, last_n_days: int = 30):
    """
    Description:
    ---
    Returns the total number of violations for a specific location in the last n days.
    
    Required Fields:
    ---
    DataFrame must contain 'Date' and 'Location' columns.
    1. 'Date' column should be in datetime format.
    2. 'Location' column should contain location names.

    Parameters:
    ---
    df (pd.DataFrame): The input DataFrame containing traffic violation data.
    last_n_days (int): The number of days to look back from the current date.
    
    Returns:
    ---
    total_locations (int): Total number of locations with violations in the last n days.
    most_violated_location (str): The location with the highest number of violations.
    fig (plt.Figure): A matplotlib figure object representing the violations by location.
    """
    # 2. No Of Violations for the location
    location_based_violations = df_last_n_days['Location'].value_counts().reset_index()
    location_based_violations.columns = ['Location', 'No of Violations']

    # 3. Total No Of Violations
    total_locations = location_based_violations.shape[0]
    
    # 4. Top Violations Zone
    most_violated_location = location_based_violations.iloc[0]['Location']

    
    # 5. Display top 10 locations
    print(location_based_violations.head(10))

    # Plot bar chart for location based violations
    sns.set_theme(style='darkgrid')
    plt.figure(figsize=(10,6.5))
    plt.pie(
        location_based_violations['No of Violations'],
        labels=location_based_violations['Location'],
        autopct='%1.1f%%',
        startangle=140,
        colors=sns.color_palette('pastel'),
        wedgeprops={'edgecolor': 'black'}
    )
    plt.xticks(rotation=25)
    plt.yticks(rotation=25)
    return total_locations, most_violated_location, plt.gcf()


def get_driver_insights(df_last_n_days: pd.DataFrame, last_n_days: int = 30):
    """
    Description:
    ---
    Returns insights related to drivers from the dataset.
    
    Required Fields:
    ---
    DataFrame must contain 'Driver_Age
    Parameters:
    ---
    df (pd.DataFrame): The input DataFrame containing traffic violation data.
    last_n_days (int): The number of days to look back from the current date.
    Returns:
    ---
    driver_insights (dict): A dictionary containing driver insights.
    """

    # 2. Filter out records with missing Driver_Age or Driver_Gender
    df_last_n_days = df_last_n_days.dropna(subset=['Driver_Age', 'Driver_Gender'])  
    df_last_n_days['Driver_Age'] = df_last_n_days['Driver_Age'].astype(int)
    df_last_n_days['Driver_Gender'] = df_last_n_days['Driver_Gender'].astype(str)
    # =================================================================================
    # 3. Calculate insights
    avg_driver_age = df_last_n_days['Driver_Age'].mean().round(2)
    gender_distribution = df_last_n_days['Driver_Gender'].value_counts()
    most_common_gender = gender_distribution.idxmax()
    max_alcohol_level = df_last_n_days['Alcohol_Level'].max()
    # =================================================================================

    # Bar plot for gender distribution
    sns.set_theme(style='darkgrid')
    plt.figure(figsize=(14,6.5))
    sns.barplot(
        x=gender_distribution.index, 
        y=gender_distribution.values, 
        palette='viridis', 
        edgecolor='black', 
        linewidth=1.5)
    plt.xlabel('Gender', fontweight='bold')
    plt.ylabel('Count', fontweight='bold')
    plt.title('Gender Distribution', fontweight='bold')
    plt.xticks(rotation=25)
    plt.yticks(rotation=25)
    gender_fig = plt.gcf()

    return avg_driver_age, most_common_gender, max_alcohol_level, gender_fig