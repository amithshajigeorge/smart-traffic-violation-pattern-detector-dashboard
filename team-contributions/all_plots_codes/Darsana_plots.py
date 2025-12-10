import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
df= pd.read_csv('Indian_Traffic_Violations.csv')

#Speeding vs. Road Condition

# Calculate speeding amount
df['Speeding'] = df['Recorded_Speed'] - df['Speed_Limit']

# Filter only records where speeding happened
speed_df = df[df['Speeding'] > 0]

avg_speeding = speed_df.groupby('Road_Condition')['Speeding'].mean().reset_index()

plt.figure(figsize=(12,6))
sns.barplot(
    data=avg_speeding,
    y='Road_Condition',
    x='Speeding',
    orient='h',
    palette='magma',
    hue='Road_Condition'
)

plt.title("Average Speeding Across Different Road Conditions")
plt.xlabel("Road Condition")
plt.ylabel("Average Speeding (km/h)")
plt.show()

#=========================================================================

#Fines vs. Weather

plt.figure(figsize=(12,6))

df_severity = df.groupby('Weather_Condition')['Fine_Amount'].mean().sort_values()

sns.barplot(
    x=df_severity.values,
    y=df_severity.index,
    orient='h',
    hue=df_severity.index,
    palette='coolwarm'
)

plt.xlabel("Average Fine Amount (Severity)")
plt.ylabel("Weather Condition")
plt.title("Weather Condition vs Severity (Higher Fine = More Severe Violation)")
plt.tight_layout()
plt.show()
