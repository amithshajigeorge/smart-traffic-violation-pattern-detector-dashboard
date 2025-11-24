import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from core.sidebar import render_sidebar

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(page_title="Data Visualization", page_icon="🎨", layout="wide")

st.title("🎨 Data Visualization")
st.markdown("Explore relationships and distributions in your data using various plots.")
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


# ------------------------------
# PAIR PLOT SECTION
# ------------------------------
st.markdown("## Pair Plot")
st.markdown("A pair plot shows pairwise relationships between variables. Select the columns you want to analyze.")
# --- Pair Plot Controls ---
with st.container():
    # Get numerical and a few categorical columns for selection
    numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    categorical_cols = [col for col in df.columns if df[col].dtype == 'object' and df[col].nunique() < 10]
    selectable_cols = numerical_cols + categorical_cols

    # --- Set new defaults as requested by the user ---
    # Default columns for the pair plot
    user_default_cols = ['Fine_Amount','Vehicle_Model_Year','Speed_Limit','Recorded_Speed','Alcohol_Level','Towed_num','Fine_Paid_num','Court_Appearance_num']
    valid_default_cols = [col for col in user_default_cols if col in selectable_cols]

    # Default column for the hue
    user_default_hue = 'Violation_Type'
    
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_cols = st.multiselect("Select columns for Pair Plot", options=selectable_cols, default=valid_default_cols)
    with col2:
        hue_options = [None] + categorical_cols
        # Set the default hue if it's a valid option
        hue_index = 0 # Default to None
        if user_default_hue in hue_options:
            hue_index = hue_options.index(user_default_hue)
        selected_hue = st.selectbox("Select column for color (hue)", options=hue_options, index=hue_index)

    if st.button("Generate Pair Plot"):
        if not selected_cols:
            st.error("Please select at least one column to plot.")
        elif len(selected_cols) > 5:
            st.warning("Too many columns selected. Please select 5 or fewer for a clearer plot.")
        else:
            with st.spinner("Generating Pair Plot... This may take a moment."):
                try:
                    # Use a copy of the dataframe for plotting
                    plot_df = df[selected_cols].copy()
                    if selected_hue:
                        plot_df[selected_hue] = df[selected_hue]

                    pair_plot_fig = sns.pairplot(plot_df, hue=selected_hue, corner=True, diag_kind='kde')
                    st.pyplot(pair_plot_fig, width='stretch')
                except Exception as e:
                    st.error(f"An error occurred while generating the pair plot: {e}")

# ------------------------------
# EXPANDERS FOR IMPORTENTS PLOTS
# ------------------------------
st.markdown("---")
st.markdown("## Important Visualizations")

with st.expander("Average Speed Exceeded vs Weather Condition"):
    # Date Range Selector for this plot
    start_date_speed, end_date_speed = None, None
    df_plot_speed = df.copy()
    try:
        if 'Date' in df.columns:
            df_plot_speed['Date'] = pd.to_datetime(df_plot_speed['Date'], errors='coerce')
            df_plot_speed.dropna(subset=['Date'], inplace=True)
            if not df_plot_speed['Date'].empty:
                min_date_speed = df_plot_speed['Date'].min().date()
                max_date_speed = df_plot_speed['Date'].max().date()
                
                col1, col2 = st.columns(2)
                with col1:
                    start_date_speed = st.date_input("Start date", min_date_speed, min_value=min_date_speed, max_value=max_date_speed, key="speed_start")
                with col2:
                    end_date_speed = st.date_input("End date", max_date_speed, min_value=min_date_speed, max_value=max_date_speed, key="speed_end")
            else:
                st.warning("No valid dates found in 'Date' column for Speed Exceeded plot.")
        else:
            st.info("No 'Date' column available for filtering Speed Exceeded plot.")
    except Exception as e:
        st.error(f"Error processing 'Date' column for Speed Exceeded plot: {e}")

    if start_date_speed and end_date_speed:
        if start_date_speed > end_date_speed:
            st.error("Error: End date must fall after start date for Speed Exceeded plot.")
        else:
            df_plot_speed = df_plot_speed[(df_plot_speed['Date'].dt.date >= start_date_speed) & (df_plot_speed['Date'].dt.date <= end_date_speed)]
    
    if not df_plot_speed.empty:
        try:
            # Create new feature
            df_plot_speed['Speed_Exceeded'] = df_plot_speed['Recorded_Speed'] - df_plot_speed['Speed_Limit']

            fig, ax = plt.subplots(figsize=(14,7))

            # Compute mean speed exceeded and sort
            avg_speed = df_plot_speed.groupby('Weather_Condition')['Speed_Exceeded'].mean().sort_values(ascending=False)

            # Barplot
            sns.barplot(
                x=avg_speed.index,
                y=avg_speed.values,
                palette='viridis',
                ax=ax
            )

            # Add value labels on bars
            for i, v in enumerate(avg_speed.values):
                ax.text(i, v + 0.5, f"{v:.1f}", ha='center', fontsize=10, fontweight='bold')

            # Titles and labels
            ax.set_title("Average Speed Exceeded vs Weather Condition", fontsize=16, fontweight='bold')
            ax.set_xlabel("Weather Condition", fontsize=14)
            ax.set_ylabel("Average Speed Exceeded (km/h)", fontsize=14)

            plt.xticks(rotation=45)
            ax.grid(axis='y', alpha=0.3)

            plt.tight_layout()
            st.pyplot(fig)


        except KeyError as e:
            st.error(f"Column not found: {e}. Please ensure the dataset has the required columns for this plot (Recorded_Speed, Speed_Limit, Weather_Condition).")
        except Exception as e:
            st.error(f"An error occurred while generating the plot: {e}")
    else:
        st.warning("No data available for the selected date range for Speed Exceeded plot.")

with st.expander("Average Fine Amount by Violation Type"):
    # Date Range Selector for this plot
    start_date_fine, end_date_fine = None, None
    df_plot_fine = df.copy()
    try:
        if 'Date' in df.columns:
            df_plot_fine['Date'] = pd.to_datetime(df_plot_fine['Date'], errors='coerce')
            df_plot_fine.dropna(subset=['Date'], inplace=True)
            if not df_plot_fine['Date'].empty:
                min_date_fine = df_plot_fine['Date'].min().date()
                max_date_fine = df_plot_fine['Date'].max().date()
                
                col1, col2 = st.columns(2)
                with col1:
                    start_date_fine = st.date_input("Start date", min_date_fine, min_value=min_date_fine, max_value=max_date_fine, key="fine_start")
                with col2:
                    end_date_fine = st.date_input("End date", max_date_fine, min_value=min_date_fine, max_value=max_date_fine, key="fine_end")
            else:
                st.warning("No valid dates found in 'Date' column for Fine Amount plot.")
        else:
            st.info("No 'Date' column available for filtering Fine Amount plot.")
    except Exception as e:
        st.error(f"Error processing 'Date' column for Fine Amount plot: {e}")

    if start_date_fine and end_date_fine:
        if start_date_fine > end_date_fine:
            st.error("Error: End date must fall after start date for Fine Amount plot.")
        else:
            df_plot_fine = df_plot_fine[(df_plot_fine['Date'].dt.date >= start_date_fine) & (df_plot_fine['Date'].dt.date <= end_date_fine)]

    if not df_plot_fine.empty:
        try:
            fig, ax = plt.subplots(figsize=(14,7))

            # Compute average fine amount by violation type
            avg_fines = df_plot_fine.groupby('Violation_Type')['Fine_Amount'].mean().sort_values(ascending=False)

            # Scatter plot
            ax.scatter(avg_fines.index, avg_fines.values, s=120, color='red')

            # Add value labels for each point
            for i, v in enumerate(avg_fines.values):
                ax.text(i, v + 5, f"{v:.0f}", ha='center', fontsize=10, fontweight='bold')

            # Titles and labels
            ax.set_title("Average Fine Amount by Violation Type (Scatter Plot)", fontsize=16, fontweight='bold')
            ax.set_xlabel("Violation Type", fontsize=14)
            ax.set_ylabel("Average Fine Amount (₹)", fontsize=14)

            plt.xticks(rotation=90)
            ax.grid(axis='y', alpha=0.3)
            
            plt.tight_layout()
            st.pyplot(fig)
        except KeyError as e:
            st.error(f"Column not found: {e}. Please ensure the dataset has the required columns for this plot (Violation_Type, Fine_Amount).")
        except Exception as e:
            st.error(f"An error occurred while generating the plot: {e}")
    else:
        st.warning("No data available for the selected date range for Fine Amount plot.")


# ------------------------------
# OTHER VISUALIZATIONS
# ------------------------------

st.markdown("---")
st.markdown("## Other Visualizations")

with st.expander("Bar Plot / Count Plot", expanded=True):
    st.markdown("Create a bar plot to compare a numerical value across categories, or a count plot for category frequencies.")
    
    # --- Bar Plot Controls ---
    all_categorical_cols = [col for col in df.columns if df[col].dtype == 'object' and df[col].nunique() < 100]
    all_numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    if not all_categorical_cols:
        st.warning("No suitable categorical columns found for the X-axis of a bar plot.")
    else:
        # --- Axis Selectors ---
        col1, col2 = st.columns(2)
        with col1:
            x_col_bar = st.selectbox("Select X-axis (Categorical)", options=all_categorical_cols, key="bar_x")
        with col2:
            y_options = ['Count'] + all_numerical_cols
            y_col_bar = st.selectbox("Select Y-axis (Numerical or Count)", options=y_options, key="bar_y")

        # --- Date Range Selector ---
        bar_start_date, bar_end_date = None, None
        plot_df_bar = df.copy()
        try:
            if 'Date' in df.columns:
                plot_df_bar['Date'] = pd.to_datetime(plot_df_bar['Date'], errors='coerce')
                plot_df_bar.dropna(subset=['Date'], inplace=True)
                if not plot_df_bar['Date'].empty:
                    min_date_bar = plot_df_bar['Date'].min().date()
                    max_date_bar = plot_df_bar['Date'].max().date()
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        bar_start_date = st.date_input("Start date", min_date_bar, min_value=min_date_bar, max_value=max_date_bar, key="bar_start")
                    with c2:
                        bar_end_date = st.date_input("End date", max_date_bar, min_value=min_date_bar, max_value=max_date_bar, key="bar_end")
            else:
                st.info("No 'Date' column found or date conversion failed. Cannot filter by date.")
        except Exception as e:
            st.error(f"Error processing 'Date' column for Bar Plot: {e}")

        if st.button("Generate Bar Plot"):
            # --- Plotting Logic ---
            if bar_start_date and bar_end_date and bar_start_date > bar_end_date:
                st.error("Error: End date must fall after start date.")
            else:
                # Filter by date if applicable
                if bar_start_date and bar_end_date:
                    plot_df_bar = plot_df_bar[(plot_df_bar['Date'].dt.date >= bar_start_date) & (plot_df_bar['Date'].dt.date <= bar_end_date)]
                
                if plot_df_bar.empty:
                    st.warning("No data available for the selected criteria.")
                else:
                    st.markdown(f"### Bar Plot: {y_col_bar} by {x_col_bar}")
                    
                    fig, ax = plt.subplots(figsize=(10, 6))

                    if y_col_bar == 'Count':
                        # Create a count plot using seaborn
                        sns.countplot(x=x_col_bar, data=plot_df_bar, ax=ax, order=plot_df_bar[x_col_bar].value_counts().index)
                        ax.set_title(f"Count of {x_col_bar}")
                        ax.set_ylabel("Count")
                    elif y_col_bar in all_numerical_cols:
                        # Create a bar plot of the mean using seaborn
                        sns.barplot(x=x_col_bar, y=y_col_bar, data=plot_df_bar, ax=ax, estimator=lambda x: x.mean())
                        ax.set_title(f"Mean of {y_col_bar} by {x_col_bar}")
                        ax.set_ylabel(f"Mean {y_col_bar}")
                    else:
                        st.error("Invalid selection for Y-axis.")
                        st.stop()

                    ax.set_xlabel(x_col_bar)
                    ax.tick_params(axis='x', rotation=45)
                    fig.tight_layout()
                    st.pyplot(fig, width='stretch')

                    # Display the underlying data in an expander
                    with st.expander("View Data"):
                        if y_col_bar == 'Count':
                            st.dataframe(plot_df_bar[x_col_bar].value_counts())
                        else:
                            st.dataframe(plot_df_bar.groupby(x_col_bar)[y_col_bar].mean())