import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Auto Data Analyzer", 
    page_icon="assets/logo.png", 
    layout="wide"
)

st.title("Auto Data Analyzer - Upload your data CSV file")
st.markdown("Want to know more about your data? This page helps you understand your data better.")


uploaded = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)



    # data cleaning -> remove quotes from col names and spaces from all string cells , numeric conversion wherever possible

    df.columns = df.columns.str.replace('"', '').str.strip()

    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].str.replace('"', '').str.strip()

    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='ignore')

    clean_df = df.copy()

    for col in clean_df.columns:
        # Convert num-looking values to num
        clean_df[col] = (
            clean_df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("%", "", regex=False)
            .str.replace("₹", "", regex=False)
            .str.strip()
        )
        clean_df[col] = pd.to_numeric(clean_df[col], errors="ignore")

    # Ensure numeric columns are actually numeric
    numeric_cols = clean_df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = [c for c in df.columns if c not in numeric_cols]

    # Explicitly cast Violation_ID to string to avoid PyArrow serialization errors
    if 'Violation_ID' in df.columns:
        df['Violation_ID'] = df['Violation_ID'].astype(str)

    st.subheader("Data Preview")
    st.dataframe(df, width='stretch')

    # Identify numeric & categoric cols
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div style="
                border: 2px solid #4CAF50;
                padding: 15px;
                border-radius: 10px;
                background-color: #F0FFF4;
            ">
                <h4 style="color:#2E7D32;">Numeric Columns</h4>
            </div>
        """, unsafe_allow_html=True)
        st.write(numeric_cols)

    with col2:
        st.markdown("""
            <div style="
                border: 2px solid #0288D1;
                padding: 15px;
                border-radius: 10px;
                background-color: #E3F2FD;
            ">
                <h4 style="color:#01579B;">Categorical Columns</h4>
            </div>
        """, unsafe_allow_html=True)
        st.write(categorical_cols)

    st.subheader("Choose a Column to Analyze")

    all_cols = numeric_cols + categorical_cols
    selected_col = st.selectbox("Select a column", all_cols)

    st.write(f"Visualization for field *{selected_col}*")

    # Clear all plt and sns plots
    plt.close('all')
    sns.reset_orig()
    
    # single col analysis
    if selected_col in numeric_cols:

        col_data = clean_df[selected_col].dropna()

        plot_col1, plot_col2 = st.columns(2)

        hist_title = f"Distribution Trend of {selected_col}"
        box_title = f"Variation & Outliers in {selected_col}"

        # Histogram
        with plot_col1:
            st.markdown(f"### {hist_title}")
            fig, ax = plt.subplots(figsize=(4.5, 3.2))

            ax.grid(True, color="#CCCCCC", linestyle="--", linewidth=0.6)
            ax.set_facecolor("#F9F9F9")
            fig.patch.set_facecolor('#FFFFFF')

            ax.hist(col_data, bins=20, color="#3498db", edgecolor="black", alpha=0.8)

            ax.set_xlabel(selected_col, fontweight="bold")
            ax.set_ylabel("Frequency", fontweight="bold")
            ax.tick_params(axis='both', labelsize=8)
            st.pyplot(fig)

        # Boxplot
        with plot_col2:
            st.markdown(f"### {box_title}")
            fig2, ax2 = plt.subplots(figsize=(4.5, 3.2))

            ax2.set_facecolor("#F9F9F9")
            fig2.patch.set_facecolor('#FFFFFF')
            ax2.grid(True, axis='y', linestyle="--", color="#DDDDDD", linewidth=0.6)

            ax2.boxplot(col_data, patch_artist=True,
                        boxprops=dict(facecolor="#FFCC80", color="black"),
                        whiskerprops=dict(color="black"),
                        capprops=dict(color="black"),
                        medianprops=dict(color="red", linewidth=2))

            ax2.set_ylabel(selected_col, fontweight="bold")
            ax2.tick_params(axis='y', labelsize=8)
            st.pyplot(fig2)

    else:
        # categorical
        col_data = df[selected_col].astype(str)
        value_counts = col_data.value_counts()

        cat_title = f"Category Distribution of '{selected_col}'"
        center_col = st.columns([0.15, 0.7, 0.15])[1]

        with center_col:
            st.markdown(f"### {cat_title}")

            fig3, ax3 = plt.subplots(figsize=(5.5, 3.5))

            ax3.set_facecolor("#F9F9F9")
            fig3.patch.set_facecolor("#FFFFFF")
            ax3.grid(True, axis='y', color="#DDDDDD", linestyle="--", linewidth=0.6)

            ax3.bar(
                value_counts.index,
                value_counts.values,
                color="#8e44ad",
                edgecolor="black",
                alpha=0.85,
                label="Counts"
            )

            ax3.set_ylabel("Count", fontweight="bold")
            ax3.set_xlabel(selected_col, fontweight="bold")
            ax3.tick_params(axis='x', labelrotation=35, labelsize=8)
            ax3.tick_params(axis='y', labelsize=8)
            ax3.legend()

            st.pyplot(fig3)


    # 2 columns comparing
    
    #Numeric vs Numeric → scatter plot + correlation.
    #Numeric vs Categorical → bar plot of numeric mean per category.  
    #Categorical vs Categorical → grouped bar plot (cross-tab).

    st.subheader("Compare Two Columns")

    center_block = st.columns([0.15, 0.70, 0.15])[1]

    with center_block:
        compA, compB = st.columns(2)

        col1_select = compA.selectbox("Select First Column", all_cols, key="col1")
        col2_select = compB.selectbox("Select Second Column", all_cols, key="col2")

        type1 = "numeric" if col1_select in numeric_cols else "categorical"
        type2 = "numeric" if col2_select in numeric_cols else "categorical"

        st.markdown(f"### Comparing *{col1_select}* vs *{col2_select}*")

        # numeric vs numeric
        if type1 == "numeric" and type2 == "numeric":

            x = clean_df[col1_select].dropna()
            y = clean_df[col2_select].dropna()

            st.markdown("#### Numeric Relationship Analysis")

            fig_scatter, ax_scatter = plt.subplots(figsize=(5, 3))
            ax_scatter.scatter(x, y, alpha=0.7, edgecolors="black")

            ax_scatter.set_facecolor("#F9F9F9")
            fig_scatter.patch.set_facecolor("white")

            ax_scatter.set_title(
                f"Scatter Plot: {col1_select} vs {col2_select}",
                fontsize=11,
                fontweight="bold",
            )
            ax_scatter.set_xlabel(col1_select, fontweight="bold")
            ax_scatter.set_ylabel(col2_select, fontweight="bold")

            st.pyplot(fig_scatter)

            corr = clean_df[[col1_select, col2_select]].corr().iloc[0, 1]
            st.info(f"Correlation Score: {corr:.4f}")

        # numeric vs categorical
        elif type1 != type2:

            num_col = col1_select if type1 == "numeric" else col2_select
            cat_col = col2_select if type1 == "numeric" else col1_select

            st.markdown("#### Category Impact Analysis")

            grouped = clean_df.groupby(cat_col)[num_col].mean().sort_values()

            fig_bar, ax_bar = plt.subplots(figsize=(5.2, 3))
            ax_bar.bar(
                grouped.index.astype(str),
                grouped.values,
                color="#105C66",
                edgecolor="black",
                alpha=0.9
            )
            ax_bar.set_title(
                f"Average {num_col} by {cat_col}",
                fontsize=11,
                fontweight="bold",
            )
            ax_bar.set_ylabel(f"Mean of {num_col}", fontweight="bold")
            plt.xticks(rotation=35)

            st.pyplot(fig_bar)

        # categorical vs categorical
        else:

            st.markdown("#### Category vs Category Comparison")
            cross = pd.crosstab(df[col1_select], df[col2_select])

            fig_cross, ax_cross = plt.subplots(figsize=(5.5, 3.2))
            cross.plot(kind="bar", ax=ax_cross, width=0.85)

            ax_cross.set_title(
                f"{col1_select} vs {col2_select} Count Comparison",
                fontsize=11,
                fontweight="bold"
            )
            ax_cross.set_xlabel(col1_select, fontweight="bold")
            ax_cross.set_ylabel("Count", fontweight="bold")

            plt.xticks(rotation=30)
            ax_cross.legend(
                title=col2_select,
                fontsize=8,
                title_fontsize=9,
                loc="upper right"
            )

            st.pyplot(fig_cross)