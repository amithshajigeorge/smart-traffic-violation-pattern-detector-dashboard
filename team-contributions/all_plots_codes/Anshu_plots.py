import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

csv_path = 'dataset/Indian_Traffic_Violations.csv'

df = pd.read_csv(csv_path)

 # Violion
plt.figure(figsize=(12, 6))
sns.violinplot(data=df, x='Weather_Condition', y='Fine_Amount', inner='box')

plt.title("Fine Amount Distribution Across Different Weather Conditions")
plt.xlabel("Weather Condition")
plt.ylabel("Fine Amount")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
#
# Double bar
validity_gender = df.groupby(['License_Validity', 'Driver_Gender']).size().unstack(fill_value=0)
print(validity_gender)
validity_gender.plot(kind='bar', figsize=(10, 6))

plt.title("Number of License Validities by Gender")
plt.xlabel("License Status")
plt.ylabel("Count")
plt.xticks(rotation=0)
plt.legend(title="Driver Gender")
plt.tight_layout()
plt.show()
#
#
# # heat map
plt.figure(figsize=(12, 7))
heatmap_violation = pd.crosstab(df['Weather_Condition'], df['Violation_Type'])

sns.heatmap(heatmap_violation, annot=True, cmap="YlOrRd")

plt.title("Violation Types Across Different Weather Conditions")
plt.xlabel("Violation Type")
plt.ylabel("Weather Condition")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()





