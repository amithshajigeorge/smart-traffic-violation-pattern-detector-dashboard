import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns 

df = pd.read_csv("Indian_Traffic_Violations.csv")

violations = df.groupby("Location").size().reset_index(name="Violation_Count")

violations["Location"] = violations["Location"].str.strip().str.title()

path = r"C:\Users\mruna\Desktop\InfosysInternship\India-State-and-Country-Shapefile-Updated-Jan-2020-master\India-State-and-Country-Shapefile-Updated-Jan-2020-master\India_State_Boundary.shp"

states = gpd.read_file(path)

states["State_Name"] = states["State_Name"].str.strip().str.title()

fig, ax = plt.subplots(1, 1, figsize=(12, 12)) 

#new df merged
merged = states.merge(
    violations,
    left_on="State_Name",
    right_on="Location",
    how="left"
)

merged.plot(
    column="Violation_Count",
    cmap="Reds",
    legend=True,
    edgecolor="black",
    linewidth=0.5,
    missing_kwds={
        "color": "lightgrey",
        "label": "No Data"
    },
    ax=ax
)


plt.title("Traffic Violations in India by State", fontsize=20)
plt.axis("off")
plt.show()


#creating severity scores

def calc_severity_score(row):

    severity = 0

    # Fine Amount
    if pd.notnull(row['Fine_Amount']):
        severity += row['Fine_Amount'] / 1000

    # 2. Penalty Points
    severity += row['Penalty_Points'] 

    # 3. Speed Violation
    if pd.notnull(row['Recorded_Speed']) and pd.notnull(row['Speed_Limit']):
        overspeed = row['Recorded_Speed'] - row['Speed_Limit']
        if overspeed > 0:
            severity += overspeed /10

    # 4. Alcohol Level
    if pd.notnull(row['Alcohol_Level']):
        severity += row['Alcohol_Level'] * 10

    # 5. Helmet / Seatbelt Violation
    if row['Helmet_Worn'] == 'No':
        severity += 10
    if row['Seatbelt_Worn'] == 'No':
        severity += 10

    # 6. Traffic Light Status
    if row['Traffic_Light_Status'] == 'Red':
        severity += 15

    # 7. Previous Violations
    severity += row['Previous_Violations'] * 1.5

    return severity


df['Violation_Severity_Score'] = df.apply(calc_severity_score, axis=1)

#location wise severity scoring

location_heatmap = df.pivot_table(
    values='Violation_Severity_Score',
    index='Location',
    columns='Violation_Type',
    aggfunc=np.mean
)



plt.figure(figsize=(14,7))
sns.heatmap(location_heatmap, cmap='coolwarm', annot=True)
plt.title("Average Severity Score by Location and Violation Type")
plt.tight_layout()
plt.show()

