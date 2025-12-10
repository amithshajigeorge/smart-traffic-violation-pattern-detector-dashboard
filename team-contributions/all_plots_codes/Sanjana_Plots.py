#count plot
#vehicle-type based risk
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv(r"C:\Users\gowri\OneDrive\Desktop\Infosys\Indian_Traffic_Violations.csv")

vehicle_counts = df['Vehicle_Type'].value_counts().index
plt.figure(figsize=(12,6))
sns.countplot(
    y=df['Vehicle_Type'],
    order=vehicle_counts,
    palette='coolwarm'
)
plt.title('Vehicle-Type Based Risk')
plt.xlabel('Vehicle Count')
plt.ylabel('Vehicle Type')
plt.tight_layout()
plt.show()

#heatmap
#Age group vs alcohol test
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r"C:\Users\gowri\OneDrive\Desktop\Infosys\Indian_Traffic_Violations.csv")
bins = [0, 25, 35, 45, 60, 100]
labels = ["18-25", "26-35", "36-45", "46-60", "60+"]

ranges = [0, 0.03, 0.08, 0.15, 0.25, df['Alcohol_Level'].max()]
safelevels = ['Safe', 'Mild', 'Risky', 'High Risk', 'Dangerous']

df["Age_Group"] = pd.cut(df["Driver_Age"], bins=bins, labels=labels, include_lowest=True)
df["Alcohol_Range"] = pd.cut(df["Alcohol_Level"], bins=ranges, labels=safelevels, include_lowest=True)
heatmap_data = pd.crosstab(df['Age_Group'], df['Alcohol_Range'])

plt.figure(figsize=(10,6))
sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="Reds")

plt.title("Age Group vs Alcohol Test Result Heatmap")
plt.xlabel("Alcohol Test Result")
plt.ylabel("Age Group")

plt.tight_layout()
plt.show()
