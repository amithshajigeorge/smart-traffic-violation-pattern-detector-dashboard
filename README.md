# 🚦 Smart Traffic Violation Pattern Detector Dashboard v0.1.0

## 📝 Overview

This project is a Streamlit web application designed to analyze traffic violation data. It provides a user-friendly interface to explore, visualize, and gain insights from traffic violation datasets. Users can upload their own data, perform analysis, and view summaries and trends.

## ✨ Features

*   **Dataset Management:**
    *   Upload your own CSV datasets.
    *   View and browse the loaded dataset.
*   **Numerical Analysis:**
    *   Get a quick overview of your dataset, including shape and sample rows.
    *   View detailed information about each column, including data types and descriptive statistics.
*   **Data Visualization:**
    *   Generate various plots to visualize data distributions and relationships.
*   **Trend Analysis:**
    *   Analyze trends in the data over time.
*   **Map Visualization:**
    *   Visualize geographical data on an interactive map.
*   **Correlation Analysis:**
    *   Explore correlations between numerical columns with a heatmap.

## 🚀 How to Run

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repository-name.git
    cd your-repository-name
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    # On Windows: .\.venv\Scripts\activate
    # On macOS/Linux: source .venv/bin/activate
    ```
3.  **Install the dependencies:**
    ```bash
    pip install .
    ```
4.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

## 📂 Project Structure

```
.
├── .gitignore
├── .python-version
├── app.py
├── core
│   ├── __init__.py
│   ├── sidebar.py
│   └── utils.py
├── dataset
│   └── Indian_Traffic_Violations.csv
├── map_data
│   ├── 01_INDIA_STATES.geojson
│   └── india_states.geojson
├── pages
│   ├── 01_Numerical_Analysis.py
│   ├── 02_Visualize_Data.py
│   ├── 03_Trend_Analysis.py
│   ├── 04_Map_Visualization.py
│   ├── 09_Upload_Dataset.py
│   └── 10_View_Dataset.py
├── pyproject.toml
├── README.md
├── uploaded_datasets
└── uv.lock
```

## 📦 Dependencies

The main dependencies for this project are listed in the `pyproject.toml` file. They include:

*   `streamlit`
*   `pandas`
*   `numpy`
*   `seaborn`
*   `matplotlib`
*   `plotly`
*   `folium`
*   `streamlit-folium`

## Recent Updates
*   **2025-11-24:**
    *   **Fake Data Generation:** Enhanced the fake data generator to produce more varied and realistic datasets. The possibilities for randomly generated data have been increased by expanding the variable lists and mappings.
*   **2025-11-22:**
    *   **Dashboard Overhaul:** Revamped the main dashboard with a dynamic summary of the last N days, including:
        *   Total violations and distribution by type.
        *   Total fines generated, with a breakdown of paid vs. unpaid amounts.
        *   Violations by location, visualized with a pie chart.
        *   Key driver insights, including average age and gender distribution.
    *   **Fake Data Generator:** Added a new feature to generate realistic fake traffic violation datasets for testing and demonstration.
    *   **Improved Dataset Management:**
        *   Enhanced the sidebar to organize datasets into categories: `Sample`, `Generated`, `Traffic Related`, and `Other`.
        *   Updated file upload logic to automatically classify and store datasets based on their columns.
*   **2025-11-21:** Added "Average Speed Exceeded vs Weather Condition" and "Average Fine Amount by Violation Type" visualizations to the Data Visualization page.
*   **2025-11-20:** Fixed a bug in the Numerical Analysis page that caused a `pyarrow.lib.ArrowInvalid` error when displaying dataset statistics for columns containing dates.