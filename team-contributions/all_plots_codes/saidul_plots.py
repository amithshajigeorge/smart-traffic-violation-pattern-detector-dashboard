import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick


# Fines based on Violation Type - Stacked Bar Plot
def total_fines_generated_stackbar_plot(df_last_n_days: pd.DataFrame) -> plt.Figure:
    # ==============================================================================
    # 2. Prepare data for fines based on violation type
    df_last_n_days['Fine_Amount'] = pd.to_numeric(df_last_n_days['Fine_Amount'], errors='coerce').fillna(0)
    df_last_n_days['Fine_Paid'] = df_last_n_days['Fine_Paid'].astype(str).str.upper().str.strip()
    summary = (df_last_n_days.groupby(['Violation_Type', 'Fine_Paid'])['Fine_Amount'].sum().unstack(fill_value=0))
    summary = summary.rename(columns={'YES': 'Paid', 'NO': 'Unpaid'})
    
    # plt.style.use('dark_background') # Preserved comment from original code
    ax = summary.plot(
        kind='bar',
        stacked=True,
        figsize=(16,9),
        # two calm color
        color=['#FF6B6B', '#4ECDC4'],     # Paid, Unpaid
        edgecolor='black', 
        linewidth=1.5
    )
    plt.title('Fines Based on Violation Type', fontweight='bold')
    plt.xlabel('Violation Type', fontweight='bold')
    plt.ylabel('Total Fine Amount (₹)',fontweight='bold')
    plt.xticks(rotation=25)
    plt.yticks(rotation=25)

    # 5. Format Color Bar values, Y-axis values, and add total fine above bars
    plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))
    
    # Calculate totals for percentage calculation
    totals = summary.sum(axis=1)
    
    # Show Paid / Unpaid inside bars with Percentage
    for c in ax.containers:
        # Create custom labels with value and percentage
        labels = []
        for i, v in enumerate(c):
            height = v.get_height()
            if height > 0:
                percentage = (height / totals.iloc[i]) * 100
                labels.append(f'{percentage:.1f}%')
            else:
                labels.append('')
        ax.bar_label(c, labels=labels, label_type='center', fontsize=10, color='black', rotation=0, fontweight='bold')

    totals = summary.sum(axis=1)
    for idx, total in enumerate(totals):
        ax.text(
            idx,
            summary.iloc[idx].sum() + (max(totals) * 0.02),
            f'{total:,.0f}',
            ha='center', va='bottom', fontsize=10, fontweight='bold', color='black'
        )
    # Legend outside plot area upper left corner
    plt.tight_layout()

    plt.legend(title="Status", bbox_to_anchor=(1, 1.05), loc="upper right", ncol=2)
    return  plt.gcf()

# =====================================================================================

# Trend Analysis Line Plot
def plot_trend_analysis_line(df: pd.DataFrame) -> plt.Figure:
    """
    Generates a trend line plot.
    
    Parameters:
    - attribute_based_pivot: DataFrame containing the pivoted data for plotting.
    - x_axis_label: Label for the X-axis.
    - line_category_label: Label for the line category (legend).
    
    Returns:
    - fig: The matplotlib figure object.
    """
    # Year, Month, Year_Month, Location, Vehicle_Type, Weather_Condition, Road_Condition
    X_axis = 'Month'

    # Violation_Type, Driver_Gender
    Lines = 'Violation_Type' 

    # --- Convert date ---
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # --- Define Date Range Selector ---
    min_date = df['Date'].min()
    max_date = df['Date'].max()

    start_date = min_date       # or custom date
    end_date   = max_date       # or custom date

    # ---- SELECT RANGE ----
    # start_date = pd.to_datetime("2023-01-01")   # you can dynamically set this
    # end_date   = pd.to_datetime("2023-12-31")

    # --- Filter by date range ---
    df_filtered: pd.DataFrame = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)].copy()

    # ---- Handle Axes ----
    if X_axis == 'Year':
        df_filtered['Year'] = df_filtered['Date'].dt.year

    elif X_axis == 'Month':
        df_filtered['Month'] = df_filtered['Date'].dt.month_name()

    elif X_axis == "Year_Month":
        df_filtered['Year_Month'] = df_filtered['Date'].dt.to_period('M')

    # ---- Grouping ----
    attribute_based_counts = (
        df_filtered
        .groupby([X_axis, Lines])
        .size()
        .reset_index(name='Count')
    )

    # ---- Pivot ----
    attribute_based_pivot = (
        attribute_based_counts
        .pivot(index=X_axis, columns=Lines, values='Count')
        .fillna(0)
    )

    # ---- FIX: Convert PeriodIndex to Timestamp ----
    if isinstance(attribute_based_pivot.index, pd.PeriodIndex):
        attribute_based_pivot.index = attribute_based_pivot.index.to_timestamp()

    # ---- FIX Month Order ----
    if X_axis == 'Month':
        month_order = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        attribute_based_pivot = attribute_based_pivot.reindex(month_order)

    # ---- Plot ----
    plt.figure(figsize=(12, 6))

    markers = ['o', '*', 'x', 's', 'p', 'd', 'h', 'D', 'H']

    for i, col in enumerate(attribute_based_pivot.columns):
        plt.plot(
            attribute_based_pivot.index,
            attribute_based_pivot[col],
            marker=markers[i % len(markers)],
            linewidth=2,
            label=col
        )

    # ---- Title and Labels ----
    title_text = f"{X_axis.replace('_',' ').title()} Trend by {Lines.replace('_',' ').title()}"
    plt.title(title_text, fontsize=14)

    plt.xlabel(X_axis.replace("_", " ").title())
    plt.ylabel("Number of Violations")

    plt.xticks(rotation=45)
    plt.grid(alpha=0.3)

    plt.legend(
        title=Lines.replace("_"," ").title(),
        bbox_to_anchor=(1.05, 1),
        loc='upper left'
    )

    plt.tight_layout()
    return plt.gcf()