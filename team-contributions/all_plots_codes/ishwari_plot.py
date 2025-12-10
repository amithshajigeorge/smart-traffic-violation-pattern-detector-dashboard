import os
import zipfile
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

#Loading and exploring the dataset
df=pd.read_csv('/content/Indian_Traffic_Violations.csv')
df.head() #showing first five rows.

#Fine Paid vs Vehicle Type
fine_data = df.groupby('Vehicle_Type')['Fine_Amount'].sum() #Groups your dataset based on each Vehicle_Type(car,bike,etc.),select only fine_Amount column,Adds up all fine amount for each vehicle type.
plt.figure(figsize=(8, 8))   #sets the overall canvas size of the graph width,height inches.
plt.pie(                     #Starts the pie chart.
    fine_data.values,        #The actual numbers(fine totals)which will form the slices.
    labels=fine_data.index,  #Labelsnfor each slice(the vehicle types)
    autopct='%1.1f%%',       #shows percentages on each slice.(1.1f one decimal place(ex:17.3%))
    startangle=90            #Rotates the pie chart starting point by 90 degree for better visual alignment.
)
plt.title("Fine Paid vs Vehicle Type", fontsize=18) #increases text size for better readability.
plt.axis('equal')            #Maintains equal scaling on x and y axis.
plt.show()                   #show the chart visually.

# Average fine per location
fine_location = df.groupby('Location')['Fine_Amount'].mean().reset_index()

plt.figure(figsize=(10,5))      #set the size of the graph width and height.
plt.plot(                       #plot the line graph,x-axis location,y-axis Fine Amount.
    fine_location['Location'],
    fine_location['Fine_Amount'],
    marker='o'#shows a dot at each point,making each locations value visible.
)
plt.title("Average Fine Amount vs Location")#add title and label for clearity.
plt.xlabel("Location")
plt.ylabel("Average Fine Amount")
plt.xticks(rotation=45)#Rotate location names to avoid overlap.
plt.grid(True) #Add gridline for easy comparison.
plt.tight_layout()#Adjust spacing automatically.adjust layout,labels and title do not overlap.
plt.show()  #Display graph.
