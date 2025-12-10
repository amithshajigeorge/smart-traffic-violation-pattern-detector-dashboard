# ----------------------------------------------------------
# Combined Code: Time of Day Impact + Payment Behavior Impact
# ----------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

# Load dataset
df = pd.read_csv(r"C:\Users\Dell\Downloads\infosys spring board\Indian_Traffic_Violations.csv")


# ========================================================
# Code 1: Time-of-Day Impact on Violations (Bar Chart)
# ========================================================

df['Hour'] = pd.to_datetime(df['Time']).dt.hour
df['Time_Block'] = pd.cut(
    df['Hour'],
    bins=[0, 6, 12, 18, 24],
    labels=['Night', 'Morning', 'Afternoon', 'Evening'],
    right=False
)

plt.figure(figsize=(10,5))
sns.countplot(
    x='Time_Block',
    data=df,
    order=['Morning', 'Afternoon', 'Evening', 'Night'],
    palette='viridis'
)
plt.title('Violations Across Different Times of Day')
plt.xlabel('Time Block')
plt.ylabel('Number of Violations')
plt.tight_layout()
plt.show()


# ========================================================
# Code 2: Payment Behavior vs Fine Amount (Bar Chart)
# ========================================================

payment_vs_fine = df.groupby("Payment_Method")["Fine_Amount"].mean().reset_index()
payment_vs_fine = payment_vs_fine.sort_values(by="Fine_Amount", ascending=False)

plt.figure(figsize=(10,5))
sns.barplot(
    x="Payment_Method",
    y="Fine_Amount",
    data=payment_vs_fine,
    palette="magma"
)
plt.title("Payment Behavior vs Average Fine Amount")
plt.xlabel("Payment Method")
plt.ylabel("Average Fine Amount")
plt.tight_layout()
plt.show()
