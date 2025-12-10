import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dateutil import parser

sns.set(style="whitegrid") 
plt.rcParams.update({"figure.dpi": 110})
df = pd.read_csv("Indian_Traffic_Violations.csv")
def safe_extract_hour(t):
    try:
        return parser.parse(str(t)).hour
    except:
        return None
df['hour'] = df['Time'].apply(safe_extract_hour)
if df['hour'].isnull().all():
    raise ValueError("Time column could  not be converted. Send me sample Time values.")
hour_counts = df['hour'].value_counts().sort_index()
plt.figure(figsize=(10,5)) 
sns.lineplot(x=hour_counts.index, y=hour_counts.values, marker="o", linewidth=2)
plt.title("Peak Hour Traffic Violations", fontsize=14)
plt.xlabel("Hour of the Day (0–23)")
plt.ylabel("Number of Violations")
plt.xticks(range(0, 24))
plt.tight_layout()
plt.savefig("peak_hour_violations.png")
plt.show()
------------------------------------------------------------------------------------------------
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
df = pd.read_csv("Indian_Traffic_Violations.csv")
order = ["Slippery", "Under Construction", "Dry", "Wet", "Potholes"]
road_counts = df['Road_Condition'].value_counts()
colors = [
    "#5bbae2",    
    "#acd3e4",  
    "#135570",
    "#56a34c",        
    "#ca9998"       
]
values = [road_counts.get(x, 0) for x in order]
plt.figure(figsize=(5, 5))   
plt.pie(
    values,
    labels=order,
    autopct="%1.1f%%",
    startangle=90,
    colors=colors
)
plt.title("Violation Distribution by Road Condition")
plt.tight_layout()
plt.show()
