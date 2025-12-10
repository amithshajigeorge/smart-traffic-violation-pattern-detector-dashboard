#violation age vs vehicle age
df['Vehicle_Age'] = pd.to_datetime(df['Date']).dt.year - pd.to_numeric(df['Vehicle_Model_Year'])
#df = df[(df['Vehicle_Age'] >= 0) & (df['Vehicle_Age'] <= 40)]


sns.boxplot(y="Violation_Type",x="Vehicle_Age",hue="Violation_Type", data=df)
plt.title("Vehicle Age vs Violation Type")
plt.ylabel("violation type")
plt.xlabel("Vehicle age")
plt.tight_layout()
plt.show()

#violation type vs number of court appearences
court_counts = df[df['Court_Appearance_Required'] == "Yes"]['Violation_Type'].value_counts()

# Plot bar chart
plt.figure(figsize=(12,6))
sns.barplot(y=court_counts.index,x=court_counts.values)

plt.title("Violations Most Often Requiring Court Appearance")
plt.ylabel("Violation Type")
plt.xlabel("Number of Court Appearances")
plt.show()'''

# Count violations requiring court appearance
'''court_counts = (
    df[df['Court_Appearance_Required'] == "Yes"]['Violation_Type']
    .value_counts()
    .sort_values(ascending=False)   # Sort for proper ranking
)

# Use single-color gradient (e.g., Reds) – darkest for highest
colors = sns.color_palette("Reds", n_colors=len(court_counts))[::-1]

plt.figure(figsize=(12, 6))

sns.barplot(
    x=court_counts.values,
    y=court_counts.index,
    palette=colors   # Dark → light automatically (sorted)
)

plt.title("Violations Most Often Requiring Court Appearance")
plt.xlabel("Number of Court Appearances")
plt.ylabel("Violation Type")
plt.tight_layout()
plt.show()

#number of violations based on days of week
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Day'] = df['Date'].dt.day_name()
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    counts = df['Day'].value_counts().reindex(order)
    plt.figure(figsize=(8,4))
    plt.plot(counts.index, counts.values, marker='o')
    plt.title("Number of violations based on days of week")
    plt.xlabel("Day")
    plt.ylabel("Number of Violations")
    plt.show()
