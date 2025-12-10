import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.ticker as mtick

# This module handles plots for Trend Analysis

# ---------------------------------------------------------
# TREND ANALYSIS STYLE CONFIGURATION
# ---------------------------------------------------------
# Define standard formatting constants for Trend Analysis
# These are smaller than the main dashboard to prevent "stuck" look
TREND_TITLE_SIZE = 16
TREND_LABEL_SIZE = 14
TREND_TICK_SIZE = 12
TREND_TICK_WEIGHT = 'bold'
TREND_FIG_SIZE = (12, 6)

def apply_trend_plot_style():
    """
    Applies the specific style settings for Trend Analysis plots.
    Call this at the start of trend plot functions.
    """
    # Based on streamlit current theme the canvas color is updated
    if st.get_option("theme.base") == 'dark':
        sns.set_theme(style="dark", context="notebook")
        plt.rcParams.update({
            'font.family': 'sans-serif',
            'font.size': TREND_TICK_SIZE,
            'axes.titlesize': TREND_TITLE_SIZE,
            'axes.titleweight': 'bold',
            'axes.labelsize': TREND_LABEL_SIZE,
            'axes.labelweight': 'bold',
            'xtick.labelsize': TREND_TICK_SIZE,
            'ytick.labelsize': TREND_TICK_SIZE,
            'figure.titlesize': TREND_TITLE_SIZE,
            'figure.figsize': TREND_FIG_SIZE,
            'axes.grid': True,
            'grid.alpha': 0.3,
            # Dark Theme Settings
            'figure.facecolor': '#0E1117',   # Dark Canvas to match app background
            'axes.facecolor': '#0E1117',     # Dark Axes
            'text.color': 'white',           # White text
            'axes.labelcolor': 'white',      # White labels
            'xtick.color': 'white',          # White X ticks
            'ytick.color': 'white',          # White Y ticks
            'axes.edgecolor': 'white',       # White border
            'grid.color': '#444444'          # Subtle dark grid
        })
    else:
        sns.set_theme(style="whitegrid", context="notebook")
        plt.rcParams.update({
            'font.family': 'sans-serif',
            'font.size': TREND_TICK_SIZE,
            'axes.titlesize': TREND_TITLE_SIZE,
            'axes.titleweight': 'bold',
            'axes.labelsize': TREND_LABEL_SIZE,
            'axes.labelweight': 'bold',
            'xtick.labelsize': TREND_TICK_SIZE,
            'ytick.labelsize': TREND_TICK_SIZE,
            'figure.titlesize': TREND_TITLE_SIZE,
            'figure.figsize': TREND_FIG_SIZE,
            'axes.grid': True,
            'grid.alpha': 0.3
        })

# ==================================================================================
def plot_trend_analysis_line(attribute_based_pivot, x_axis_label, line_category_label):
    """
    Generates a trend line plot.
    
    Parameters:
    - attribute_based_pivot: DataFrame containing the pivoted data for plotting.
    - x_axis_label: Label for the X-axis.
    - line_category_label: Label for the line category (legend).
    
    Returns:
    - fig: The matplotlib figure object.
    """
    apply_trend_plot_style()
    
    fig, ax = plt.subplots(figsize=TREND_FIG_SIZE)
    markers = ['o', '*', 'x', 's', 'p', 'd', 'h', 'D', 'H']
    
    for i, col in enumerate(attribute_based_pivot.columns):
        ax.plot(
            attribute_based_pivot.index, 
            attribute_based_pivot[col], 
            marker=markers[i % len(markers)], 
            linestyle='-', 
            linewidth=2, 
            label=col
        )

    ax.set_title(f"{line_category_label.replace('_',' ').title()} Trend based on {x_axis_label.replace('_',' ').title()}", fontsize=TREND_TITLE_SIZE, fontweight='bold')
    ax.set_xlabel(x_axis_label.replace(" ", " ").title(), fontsize=TREND_LABEL_SIZE, fontweight='bold')
    ax.set_ylabel("Number of Violations", fontsize=TREND_LABEL_SIZE, fontweight='bold')
    
    plt.xticks(rotation=45, ha="right", fontsize=TREND_TICK_SIZE, fontweight=TREND_TICK_WEIGHT)
    plt.yticks(fontsize=TREND_TICK_SIZE, fontweight=TREND_TICK_WEIGHT)
    
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Place legend outside to prevent cluttering the smaller plot
    ax.legend(
        title=line_category_label.replace("_"," ").title(), 
        bbox_to_anchor=(1.02, 1), 
        loc='upper left',
        fontsize=TREND_TICK_SIZE,
        title_fontsize=TREND_LABEL_SIZE
    )
    
    fig.tight_layout()
    return fig

# Other Team Line plots




# -------------------------------------------------------------------------------
def plot_categorical_heatmap(percent_pivot, annot, x_label, y_label):
    """
    Generates a categorical heatmap.
    
    Parameters:
    - percent_pivot: DataFrame containing percentage values.
    - annot: DataFrame or array containing annotation strings.
    - x_label: Label for the X-axis.
    - y_label: Label for the Y-axis.
    
    Returns:
    - fig: The matplotlib figure object.
    """
    apply_trend_plot_style()
    
    fig, ax = plt.subplots(figsize=(14, 7)) # Heatmaps might need slightly more width
    sns.heatmap(
        percent_pivot,
        annot=annot,
        fmt="",
        cmap="coolwarm",
        linewidths=0.5,
        vmin=0,
        vmax=100,
        ax=ax,
        annot_kws={"size": TREND_TICK_SIZE, "weight": "bold"}
    )
    
    ax.set_xlabel(x_label, fontsize=TREND_LABEL_SIZE, fontweight='bold')
    ax.set_ylabel(y_label, fontsize=TREND_LABEL_SIZE, fontweight='bold')
    
    plt.xticks(rotation=45, fontweight=TREND_TICK_WEIGHT)
    plt.yticks(fontweight=TREND_TICK_WEIGHT)
    
    fig.tight_layout()
    return fig

# -------------------------------------------------------------------------------
# MOVED PLOTS FROM VISUALIZE DATA
# -------------------------------------------------------------------------------

def plot_peak_hour_traffic(df):
    apply_trend_plot_style()
    df = df.copy()
    if 'Time' in df.columns:
        try:
            df['hour'] = pd.to_datetime(df['Time'], format='%H:%M:%S', errors='coerce').dt.hour
            if df['hour'].isnull().any():
                 df['hour'] = pd.to_datetime(df['Time'], format='%H:%M', errors='coerce').dt.hour
            if df['hour'].isnull().all():
                 df['hour'] = df['Time'].astype(str).str.split(':').str[0].astype(float)
        except:
             return None

        hour_counts = df['hour'].value_counts().sort_index()
        fig, ax = plt.subplots(figsize=TREND_FIG_SIZE)
        sns.lineplot(x=hour_counts.index, y=hour_counts.values, marker="o", linewidth=3, color="teal", ax=ax)
        ax.set_title("Peak Hour Traffic Violations", fontsize=TREND_TITLE_SIZE, fontweight='bold')
        ax.set_xlabel("Hour of the Day (0–23)", fontsize=TREND_LABEL_SIZE, fontweight='bold')
        ax.set_ylabel("Number of Violations", fontsize=TREND_LABEL_SIZE, fontweight='bold')
        plt.xticks(range(0, 24), rotation=25, fontweight=TREND_TICK_WEIGHT)
        plt.yticks(fontweight=TREND_TICK_WEIGHT)
        plt.tight_layout()
        plt.close()
        return fig
    return None

def plot_fines_per_year(df):
    apply_trend_plot_style()
    df = df.copy()
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Year'] = df['Date'].dt.year
        fines_per_year = df.groupby('Year')['Fine_Amount'].sum()
        
        fig, ax = plt.subplots(figsize=TREND_FIG_SIZE)
        ax.plot(fines_per_year.index, fines_per_year.values, marker='o', linewidth=3, markersize=8, color="skyblue")
        ax.grid(True, which='both', linestyle='--', linewidth=0.9, alpha=0.5)
        ax.set_title("Total Fines Per Year", fontsize=TREND_TITLE_SIZE, fontweight='bold')
        ax.set_xlabel("Year", fontsize=TREND_LABEL_SIZE, fontweight='bold')
        ax.set_ylabel("Total Fine Amount", fontsize=TREND_LABEL_SIZE, fontweight='bold')
        plt.xticks(rotation=25, fontweight=TREND_TICK_WEIGHT)
        plt.yticks(fontweight=TREND_TICK_WEIGHT)
        plt.close()
        return fig
    else:
        return None

def plot_avg_fine_location_line(df):
    apply_trend_plot_style()
    fine_location = df.groupby('Location')['Fine_Amount'].mean().reset_index()
    fig, ax = plt.subplots(figsize=TREND_FIG_SIZE)
    ax.plot(
        fine_location['Location'],
        fine_location['Fine_Amount'],
        marker='o',
        linewidth=3,
        markersize=8,
        color="salmon"
    )
    ax.set_title("Average Fine Amount vs Location", fontsize=TREND_TITLE_SIZE, fontweight='bold')
    ax.set_xlabel("Location", fontsize=TREND_LABEL_SIZE, fontweight='bold')
    ax.set_ylabel("Average Fine Amount", fontsize=TREND_LABEL_SIZE, fontweight='bold')
    plt.xticks(rotation=25, fontweight=TREND_TICK_WEIGHT)
    plt.yticks(fontweight=TREND_TICK_WEIGHT)
    ax.grid(True)
    plt.tight_layout()
    plt.close()
    return fig

# ==================================================================================