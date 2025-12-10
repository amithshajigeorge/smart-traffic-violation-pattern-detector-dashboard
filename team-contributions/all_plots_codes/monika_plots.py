import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
df=pd.read_csv(r"C:\Users\mouni\Downloads\Indian_Traffic_Violations.csv")
#Top 5 Locations that have highest violation
plt.figure(figsize=(10,5))
Location_Count=df['Location'].value_counts().head(5)
sns.barplot(x=Location_Count.index,y=Location_Count.values)
plt.title("Top 5 Locations that Have Violation")
plt.xlabel("Location")
plt.ylabel("Count")
plt.show()



#Vehicle type vs Violation Type
plt.figure(figsize=(14,8))
sns.countplot(data=df, x='Violation_Type',hue='Vehicle_Type')
plt.title('Vehicle Type vs Violation Type')
plt.xlabel('Violation Type')
plt.ylabel('Number of Violations')
plt.legend(title='Vehicle Type')
plt.tight_layout()
plt.show()