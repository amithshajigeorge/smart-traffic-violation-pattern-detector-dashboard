import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

df=pd.read_csv("D:/Documents/Indian_Traffic_Violations.csv")
df.head()

#repeat offender analysis
plt.figure(figsize=(6,4))
colors = ['pink','skyblue','green','grey']
violations=df[df['Previous_Violations']>3].head(10)
bars=plt.barh(violations['Violation_ID'],violations['Previous_Violations'],color=colors)
plt.title('Previous Violations per Record')
plt.xlabel('Record')
plt.ylabel('Number of Previous Violations')
plt.tight_layout()
plt.legend(bars, df['Violation_ID'],loc='upper left')
plt.show()

#To identify which loations or areas register the highest number of traffic violations.
plt.figure(figsize=(8,8))
location_counts = df["Location"].value_counts()
plt.pie(location_counts, labels=location_counts.index, autopct='%1.1f%%', startangle=90)
plt.title("Percentage of Traffic Violations by Location")
plt.tight_layout()
plt.show()