# Plot pie chart
# Percentage of traffic violation types
violation_counts = df['Violation_Type'].value_counts()
print(violation_counts)
plt.figure(figsize=(10, 8))
plt.pie(
    violation_counts,
    labels=violation_counts.index,
    autopct='%1.1f%%',
    startangle=90
)

plt.title('Percentage of Traffic Violation Types')
plt.axis('equal')
plt.show()
-----------------------------------------------------------------------------------
# Plot line chart
# Total fines per year
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Year'] = df['Date'].dt.year

fines_per_year = df.groupby('Year')['Fine_Amount'].sum()
print(fines_per_year)

plt.figure(figsize=(10, 6))
plt.plot(fines_per_year.index, fines_per_year.values, marker='o')
plt.grid(True, which='both', linestyle='--', linewidth=0.9, alpha=0.9)
plt.title("Total Fines Per Year")
plt.xlabel("Year")
plt.ylabel("Total Fine Amount")
plt.show()
