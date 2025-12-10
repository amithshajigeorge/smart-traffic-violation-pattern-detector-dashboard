#Heat map
#Impact of Weather conditions on Traffic Violations - Heat Map
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r"C:\Users\saniy\OneDrive\Documents\Indian_Traffic_Violations.csv")

pivot = df.pivot_table(
    index="Violation_Type",
    columns="Weather_Condition",
    values="Violation_ID",
    aggfunc="count",
    fill_value=0
)

plt.figure(figsize=(12,8))
ax = sns.heatmap(
    pivot, 
    annot=True, 
    fmt="d", 
    cmap="YlGnBu",   
    cbar=True        
)


colorbar = ax.collections[0].colorbar
colorbar.set_label("Number of Violations")

plt.title("Impact of Weather Conditions on Traffic Violations")
plt.xlabel("Weather Condition")
plt.ylabel("Violation Type")
plt.tight_layout()
plt.show()


#Line Graph
#Average Driver Risk Level By Age group - Line Graph
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv(r"C:\Users\saniy\OneDrive\Documents\Indian_Traffic_Violations.csv")

bins = [0, 25, 35, 45, 60, 100]
labels = ["18-25", "26-35", "36-45", "46-60", "60+"]
df["Age_Group"] = pd.cut(df["Driver_Age"], bins=bins, labels=labels, include_lowest=True)

df['Alcohol_Flag'] = (df['Breathalyzer_Result'] == "Positive").astype(int)
df["Risk_Level"] = df["Previous_Violations"] + df["Alcohol_Flag"]


risk_by_age = df.groupby("Age_Group", observed=False)["Risk_Level"].mean().reset_index()

risk_by_age = risk_by_age.sort_values("Age_Group")

plt.figure(figsize=(9,5))
sns.set_style("whitegrid")

# Draw the sloped line
plt.plot(
    risk_by_age["Age_Group"],
    risk_by_age["Risk_Level"],
    marker="o",
    markersize=10,
    linewidth=2,
    color="#D43F6A"
)

# Add value labels next to each point
for i, row in risk_by_age.iterrows():
    plt.text(
        row["Age_Group"],
        row["Risk_Level"] + 0.02,
        f"{row['Risk_Level']:.2f}",
        ha="center",
        fontsize=10,
        weight="bold"
    )

plt.title("Average Driver Risk Level by Age Group ", fontsize=14, weight="bold")
plt.xlabel("Age Group")
plt.ylabel("Average Risk Level")
plt.tight_layout()
plt.show()

