import os
from datetime import datetime

import streamlit as st
import pandas as pd
import numpy as np
from core.data_generator import generate_dataset_by_days

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(page_title="Datasets", page_icon="📁")

# ------------------------------
# SESSION STATE
# ------------------------------
if 'file_to_delete' not in st.session_state:
    st.session_state.file_to_delete = None

# ------------------------------
# PAGE
# ------------------------------
st.title("📁 Datasets Management")

# --- Fake Data Generator ---
with st.expander("🤖 Generate Fake Traffic Dataset"):
    st.markdown("Create a synthetic dataset for testing and demonstration purposes.")
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Select start date for generation", value=datetime(2015, 1, 1))
        end_date = st.date_input("Select end date for generation", value=datetime.now().date())

    with col2:
        min_records_per_day = st.number_input("Enter the minimum number of records per day:", min_value=1, max_value=100, value=1, step=1)
        max_records_per_day = st.number_input("Enter the maximum number of records per day:", min_value=1, max_value=100, value=10, step=1)



    if st.button("Generate and Save Dataset"):
        with st.spinner("Generating dataset ..."):
            df = pd.DataFrame(
                generate_dataset_by_days(
                    start_date=start_date.strftime('%Y-%m-%d'), 
                    end_date=end_date.strftime('%Y-%m-%d'), 
                    min_records_per_day=min_records_per_day, 
                    max_records_per_day=max_records_per_day
                )
            )
        with st.spinner("Saving dataset ..."):
            # --- Save the generated dataset ---
            save_dir = f"generated_fake_traffic_datasets/{datetime.now().strftime('%Y-%m-%d')}"
            os.makedirs(save_dir, exist_ok=True)
            
            dataset_id = 1
            while (dataset_id <= 99) and (os.path.exists(os.path.join(save_dir, f"{dataset_id:02d}_traffic_dataset.csv"))):
                dataset_id += 1
            
            if dataset_id <= 99:
                file_path = os.path.join(save_dir, f"{dataset_id:02d}_traffic_dataset.csv")
                df.to_csv(file_path, index=False)
                st.success(f"Successfully generated and saved '{os.path.basename(file_path)}' in the `{save_dir}` directory.")
                st.dataframe(df.head())
            else:
                st.warning("Dataset generation limit (99) reached for today. Please try again tomorrow.")

st.markdown("---")
st.markdown("### Upload and save new datasets")

# --- Gather existing datasets for duplicate check ---
root_upload_dir = "uploaded_datasets"
local_dataset_dir = "dataset"
all_dataset_paths = []
if os.path.exists(local_dataset_dir):
    for file_name in os.listdir(local_dataset_dir):
        if file_name.endswith('.csv'):
            all_dataset_paths.append(os.path.join(local_dataset_dir, file_name))
if os.path.exists(root_upload_dir):
    for root, _, files in os.walk(root_upload_dir):
        for file_name in files:
            if file_name.endswith('.csv'):
                all_dataset_paths.append(os.path.join(root, file_name))

# --- Traffic Violation Columns ---
TRAFFIC_VIOLATION_COLUMNS = [
    'Violation_ID', 'Violation_Type', 'Fine_Amount', 'Location', 'Date', 'Time', 
    'Vehicle_Type', 'Vehicle_Color', 'Vehicle_Model_Year', 'Registration_State', 
    'Driver_Age', 'Driver_Gender', 'License_Type', 'Penalty_Points', 
    'Weather_Condition', 'Road_Condition', 'Officer_ID', 'Issuing_Agency', 
    'License_Validity', 'Number_of_Passengers', 'Helmet_Worn', 'Seatbelt_Worn', 
    'Traffic_Light_Status', 'Speed_Limit', 'Recorded_Speed', 'Alcohol_Level', 
    'Breathalyzer_Result', 'Towed', 'Fine_Paid', 'Payment_Method', 
    'Court_Appearance_Required', 'Previous_Violations', 'Comments'
]

# --- File Uploader ---
uploaded_file = st.file_uploader("Choose a CSV file to upload", type="csv", key="datasets_page_uploader")

if uploaded_file is not None:
    st.markdown("#### Preview of Uploaded Data")
    try:
        preview_df = pd.read_csv(uploaded_file, nrows=5)
        st.dataframe(preview_df)
        uploaded_file.seek(0)

        if st.button("Upload and Save Dataset"):
            # ... (duplicate check and save logic)
            is_duplicate = False
            try:
                for existing_path in all_dataset_paths:
                    existing_basename = os.path.basename(existing_path)
                    parts = existing_basename.split('_', 1)
                    unprefixed_name = parts[1] if len(parts) == 2 and parts[0].isdigit() else existing_basename
                    if unprefixed_name == uploaded_file.name:
                        existing_df_head = pd.read_csv(existing_path, nrows=5)
                        if preview_df.equals(existing_df_head):
                            is_duplicate = True
                            st.error(f"Duplicate of '{existing_basename}' found. Upload cancelled.")
                            break
            except Exception as e:
                st.error(f"An error occurred during duplicate check: {e}")
                is_duplicate = True

            if not is_duplicate:
                try:
                    # Check columns to decide the folder
                    uploaded_df = pd.read_csv(uploaded_file)
                    uploaded_file.seek(0) # Reset file pointer
                    uploaded_columns = set(uploaded_df.columns)
                    
                    if set(TRAFFIC_VIOLATION_COLUMNS).issubset(uploaded_columns):
                        save_dir = "related_uploads"
                    else:
                        save_dir = "other_party_uploads"

                    os.makedirs(save_dir, exist_ok=True)
                    
                    file_path = os.path.join(save_dir, uploaded_file.name)

                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    st.success(f"File '{uploaded_file.name}' saved successfully in `{save_dir}`.")
                    st.rerun()
                except Exception as e:
                    st.error(f"An error occurred while saving the file: {e}")
    except Exception as e:
        st.error(f"Error processing file: {e}")

# --- Display Uploaded Datasets ---
st.markdown("---")
st.markdown("### View Previously Uploaded Datasets")

dataset_options = {}
if os.path.exists(local_dataset_dir):
    for file_name in os.listdir(local_dataset_dir):
        if file_name.endswith('.csv'):
            dataset_options[f"[Sample] / {file_name}"] = os.path.join(local_dataset_dir, file_name)

# Function to scan a directory and add to options
def scan_and_add_datasets(directory, prefix):
    if os.path.exists(directory):
        # Scan for date-based directories (for generated data)
        if "generated" in directory:
            for date_dir in sorted(os.listdir(directory), reverse=True):
                full_date_dir = os.path.join(directory, date_dir)
                if os.path.isdir(full_date_dir):
                    for file_name in sorted(os.listdir(full_date_dir)):
                        if file_name.endswith('.csv'):
                            display_name = f"[{prefix} - {date_dir}] / {file_name}"
                            dataset_options[display_name] = os.path.join(full_date_dir, file_name)
        else: # Original logic for other directories
            for file_name in sorted(os.listdir(directory)):
                if file_name.endswith('.csv'):
                    dataset_options[f"[{prefix}] / {file_name}"] = os.path.join(directory, file_name)

# Scan new directories
scan_and_add_datasets("related_uploads", "Traffic Related")
scan_and_add_datasets("generated_fake_traffic_datasets", "Generated")
scan_and_add_datasets("other_party_uploads", "Other CSVs")



if not os.path.exists(root_upload_dir) and not dataset_options and not os.path.exists("related_uploads") and not os.path.exists("other_party_uploads"):
    st.info("No datasets have been uploaded or found locally.")
else:
    if os.path.exists(root_upload_dir):
        date_dirs = [d for d in os.listdir(root_upload_dir) if os.path.isdir(os.path.join(root_upload_dir, d)) and d.startswith("Date(")]
        def get_date_from_dir_name(dir_name):
            date_str = dir_name.replace("Date(", "").replace(")", "")
            return datetime.strptime(date_str, "%d-%m-%Y")
        sorted_date_dirs = sorted(date_dirs, key=get_date_from_dir_name, reverse=True)
        for date_dir in sorted_date_dirs:
            dir_path = os.path.join(root_upload_dir, date_dir)
            files = sorted([f for f in os.listdir(dir_path) if f.endswith('.csv')])
            for file_name in files:
                dataset_options[f"[Legacy] {date_dir.replace('Date(', '').replace(')', '')} / {file_name}"] = os.path.join(dir_path, file_name)

    selected_dataset_display_name = st.selectbox("Select a dataset to view", options=["-"] + list(dataset_options.keys()))

    if selected_dataset_display_name != "-":
        file_path = dataset_options[selected_dataset_display_name]
        st.markdown(f"### Statistics for: `{selected_dataset_display_name}`")
        
        try:
            df_view = pd.read_csv(file_path)
            tab1, tab2, tab3, tab4 = st.tabs(["📋 Overview", "🔢 Numerical Summary", "🔠 Categorical Summary", "📄 Data Preview & Actions"])

            with tab1:
                st.markdown("#### Dataset Shape")
                st.write(f"Rows: `{df_view.shape[0]}`	||	Columns: `{df_view.shape[1]}`")
                st.dataframe(df_view.dtypes.reset_index().rename(columns={'index': 'Column', 0: 'Data Type'}))
            with tab2:
                st.markdown("#### Descriptive Statistics for Numerical Columns")
                st.dataframe(df_view.describe(include=np.number))
            with tab3:
                st.markdown("#### Summary for Categorical Columns")
                cat_summary = df_view.describe(include='object')
                if not cat_summary.empty: st.dataframe(cat_summary)
                else: st.info("No categorical columns found.")
            with tab4:
                st.markdown("#### First 10 Rows")
                st.dataframe(df_view.head(10))
                st.markdown("---")
                st.markdown("#### Actions")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="⬇️ Download Full Dataset",
                        data=df_view.to_csv(index=False).encode('utf-8'),
                        file_name=os.path.basename(file_path),
                        mime='text/csv',
                        width='stretch'
                    )
                with col2:
                    # Do not allow deleting sample or generated datasets
                    if not file_path.startswith(local_dataset_dir) and "generated_fake_traffic_datasets" not in file_path:
                        if st.button("🗑️ Delete Dataset", width='stretch', type="primary"):
                            st.session_state.file_to_delete = file_path
                            st.rerun()
                    else:
                        st.button("🗑️ Delete Dataset", width='stretch', disabled=True, help="Sample and generated datasets cannot be deleted.")

        except Exception as e:
            st.error(f"An error occurred while analyzing the dataset: {e}")

# --- Deletion Confirmation UI ---
if st.session_state.file_to_delete:
    file_path_to_delete = st.session_state.file_to_delete
    st.warning(f"**Are you sure you want to delete `{os.path.basename(file_path_to_delete)}`?** This action cannot be undone.")
    
    with st.container():
        col1, col2 = st.columns([3, 1])
        with col1:
            secret_code = st.text_input("Enter the special code to confirm deletion:", type="password", key="delete_code")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Confirm Deletion", width='stretch', type="primary"):
                if secret_code == "123456789":
                    try:
                        os.remove(file_path_to_delete)
                        st.success(f"Successfully deleted `{os.path.basename(file_path_to_delete)}`.")
                        st.session_state.file_to_delete = None
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error deleting file: {e}")
                else:
                    st.error("Incorrect special code. Deletion cancelled.")
        with c2:
            if st.button("❌ Cancel", width='stretch'):
                st.session_state.file_to_delete = None
                st.rerun()