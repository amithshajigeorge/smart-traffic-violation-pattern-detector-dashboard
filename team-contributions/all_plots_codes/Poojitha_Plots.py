#Average Speed Exceeded vs Weather Conditions
# Create new feature
import pandas as pd
df['Speed_Exceeded'] = df['Recorded_Speed'] - df['Speed_Limit']

plt.figure(figsize=(14,7))

# Compute mean speed exceeded and sort
avg_speed = df.groupby('Weather_Condition')['Speed_Exceeded'].mean().sort_values(ascending=False)

# Barplot
sns.barplot(
    x=avg_speed.index,
    y=avg_speed.values,
    palette='viridis'
)

# Add value labels on bars
for i, v in enumerate(avg_speed.values):
    plt.text(i, v + 0.5, f"{v:.1f}", ha='center', fontsize=10, fontweight='bold')

# Titles and labels
plt.title("Average Speed Exceeded vs Weather Condition", fontsize=16, fontweight='bold')
plt.xlabel("Weather Condition", fontsize=14)
plt.ylabel("Average Speed Exceeded (km/h)", fontsize=14)

plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()


#Average Fine Amount by Violation Type
#To show how fine amounts vary across different violation types
plt.figure(figsize=(14,7))

# Compute average fine amount by violation type
avg_fines = df.groupby('Violation_Type')['Fine_Amount'].mean().sort_values(ascending=False)

# Scatter plot
plt.scatter(avg_fines.index, avg_fines.values, s=120, color='red')

# Add value labels for each point
for i, v in enumerate(avg_fines.values):
    plt.text(i, v + 5, f"{v:.0f}", ha='center', fontsize=10, fontweight='bold')

# Titles and labels
plt.title("Average Fine Amount by Violation Type (Scatter Plot)", fontsize=16, fontweight='bold')
plt.xlabel("Violation Type", fontsize=14)
plt.ylabel("Average Fine Amount (₹)", fontsize=14)

plt.xticks(rotation=90)
plt.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()
