import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

csv_path = './Indian_Traffic_Violations.csv'

df = pd.read_csv(csv_path)
# df = df.fillna(0)

# df['Time'] = pd.to_datetime(df['Time'], format='%H:%M')
# df['Hour'] = df['Time'].dt.hour
#
# plt.figure(figsize=(10,5))
# df['Hour'].value_counts().sort_index().plot(kind='line')
# plt.title("Violations by Hour of the Day")
# plt.xlabel("Hour")
# plt.ylabel("Count")
# plt.grid(True)
# plt.show()
#
# # histogram
# plt.figure(figsize=(8,5))
# plt.hist(df['Fine_Amount'], bins=20)
# plt.title("Fine Amount Distribution")
# plt.xlabel("Fine Amount")
# plt.ylabel("Frequency")
# plt.show()
#
# # Plot pie chart
# violation_counts = df['Violation_Type'].value_counts()
# print(violation_counts)
# plt.figure(figsize=(10, 8))
# plt.pie(
#     violation_counts,
#     labels=violation_counts.index,
#     autopct='%1.1f%%',
#     startangle=90
# )
#
# plt.title('Percentage of Traffic Violation Types')
# plt.axis('equal')
# plt.show()
#
#
# # Plot line chart
# df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
# df['Year'] = df['Date'].dt.year
#
# fines_per_year = df.groupby('Year')['Fine_Amount'].sum()
# print(fines_per_year)
#
# plt.figure(figsize=(10, 6))
# plt.plot(fines_per_year.index, fines_per_year.values, marker='o')
#
# plt.title("Total Fines Per Year")
# plt.xlabel("Year")
# plt.ylabel("Total Fine Amount")
# plt.show()
#
#
# # bar
# fine_weather = df.groupby('Weather_Condition')['Fine_Amount'].sum().reset_index()
# print(fine_weather)
#
# plt.figure(figsize=(10, 6))
# sns.barplot(data=fine_weather, x='Weather_Condition', y='Fine_Amount')
#
# plt.title("Total Fine Amount for Each Weather Condition")
# plt.xlabel("Weather Condition")
# plt.ylabel("Total Fine Amount")
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()
#
#
#  # Violion
# plt.figure(figsize=(12, 6))
# sns.violinplot(data=df, x='Weather_Condition', y='Fine_Amount', inner='box')
#
# plt.title("Fine Amount Distribution Across Different Weather Conditions")
# plt.xlabel("Weather Condition")
# plt.ylabel("Fine Amount")
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()
#
#  # Double bar
# validity_gender = df.groupby(['License_Validity', 'Driver_Gender']).size().unstack(fill_value=0)
# print(validity_gender)
# validity_gender.plot(kind='bar', figsize=(10, 6))
#
# plt.title("Number of License Validities by Gender")
# plt.xlabel("License Status")
# plt.ylabel("Count")
# plt.xticks(rotation=0)
# plt.legend(title="Driver Gender")
# plt.tight_layout()
# plt.show()
#
#
# # heat map
# plt.figure(figsize=(12, 7))
# heatmap_violation = pd.crosstab(df['Weather_Condition'], df['Violation_Type'])
#
# sns.heatmap(heatmap_violation, annot=True, cmap="YlOrRd")
#
# plt.title("Violation Types Across Different Weather Conditions")
# plt.xlabel("Violation Type")
# plt.ylabel("Weather Condition")
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

missing_percent = df.isna().mean() * 100
duplicate_percent = (df.duplicated().sum() / len(df)) * 100

impossible_age_count = 0
if 'Driver_Age' in df.columns:
    impossible_age_count = ((df['Driver_Age'] < 16) | (df['Driver_Age'] > 100)).sum()



overall_stats = {
        "Total Rows": len(df),
        "Duplicate %": round(duplicate_percent, 2),
        "Impossible Age Count": int(impossible_age_count)
    }

print("Data Quality Report\n ", overall_stats)