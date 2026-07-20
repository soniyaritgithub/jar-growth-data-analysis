import pandas as pd
import matplotlib.pyplot as plt

# ==========================================================
# STEP 1: Load Excel Files
# ==========================================================

orders = pd.read_excel("data/List_of_Orders.xlsx")
details = pd.read_excel("data/Order_Details.xlsx")
targets = pd.read_excel("data/Sales_target.xlsx")

print("=" * 60)
print("DATASETS LOADED SUCCESSFULLY")
print("=" * 60)

# ==========================================================
# STEP 2: Dataset Information
# ==========================================================

print("\nOrders Shape :", orders.shape)
print("Details Shape :", details.shape)
print("Targets Shape :", targets.shape)

print("\nOrders Columns")
print(orders.columns)

print("\nDetails Columns")
print(details.columns)

print("\nTargets Columns")
print(targets.columns)

print("\nMissing Values")

print("\nOrders")
print(orders.isnull().sum())

print("\nDetails")
print(details.isnull().sum())

print("\nTargets")
print(targets.isnull().sum())

# ==========================================================
# STEP 3: Merge Datasets
# ==========================================================

merged_data = pd.merge(
    orders,
    details,
    on="Order ID"
)

print("\n" + "=" * 60)
print("MERGED DATA")
print("=" * 60)

print(merged_data.head())

print("\nMerged Shape :", merged_data.shape)

# ==========================================================
# STEP 4: Category-wise Total Sales
# ==========================================================

category_sales = merged_data.groupby("Category")["Amount"].sum()

print("\n" + "=" * 60)
print("CATEGORY-WISE TOTAL SALES")
print("=" * 60)

print(category_sales)

# ==========================================================
# STEP 5: Average Profit Per Order
# ==========================================================

average_profit = merged_data.groupby("Category")["Profit"].mean()

print("\n" + "=" * 60)
print("AVERAGE PROFIT PER ORDER")
print("=" * 60)

print(average_profit.round(2))

# ==========================================================
# STEP 6: Profit Margin
# ==========================================================

profit_margin = (
    merged_data.groupby("Category")["Profit"].sum()
    /
    merged_data.groupby("Category")["Amount"].sum()
) * 100

print("\n" + "=" * 60)
print("PROFIT MARGIN (%)")
print("=" * 60)

print(profit_margin.round(2))

# ==========================================================
# STEP 7: Summary Table
# ==========================================================

summary = pd.DataFrame({
    "Total Sales": category_sales,
    "Average Profit": average_profit,
    "Profit Margin (%)": profit_margin
})

summary = summary.round(2)

print("\n" + "=" * 60)
print("SUMMARY TABLE")
print("=" * 60)

print(summary)

# ==========================================================
# STEP 8: Top & Underperforming Categories
# ==========================================================

top_category = summary["Profit Margin (%)"].idxmax()
under_category = summary["Profit Margin (%)"].idxmin()

print("\nTop Performing Category :", top_category)
print("Underperforming Category :", under_category)

# ==========================================================
# STEP 9: Sort Summary Table
# ==========================================================

sorted_summary = summary.sort_values(
    by="Total Sales",
    ascending=False
)

print("\n" + "=" * 60)
print("SORTED SUMMARY TABLE")
print("=" * 60)

print(sorted_summary)

# ==========================================================
# STEP 10: Professional Bar Chart
# ==========================================================

plt.figure(figsize=(9,6))

bars = plt.bar(
    sorted_summary.index,
    sorted_summary["Total Sales"]
)

plt.title(
    "Category-wise Total Sales",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Category", fontsize=12)
plt.ylabel("Total Sales", fontsize=12)

for bar in bars:
    height = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width()/2,
        height + 2000,
        f"{int(height):,}",
        ha="center",
        fontsize=10,
        fontweight="bold"
    )

plt.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()

plt.savefig(
    "charts/category_sales.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# ==========================================================
# STEP 11: Business Insights
# ==========================================================

print("\n" + "=" * 60)
print("BUSINESS INSIGHTS")
print("=" * 60)

print(f"""
1. Highest Sales Category      : {sorted_summary.index[0]}
2. Lowest Sales Category       : {sorted_summary.index[-1]}
3. Top Performing Category     : {top_category}
4. Underperforming Category    : {under_category}

Recommendations:
• Increase inventory for high-performing categories.
• Review pricing and discount strategy for low-margin categories.
• Reduce operational costs in underperforming categories.
• Focus marketing campaigns on profitable product categories.
""")

# ==========================================================
# QUESTION 1 - PART 2
# Furniture Target Achievement Analysis
# ==========================================================

# Filter only Furniture category
furniture_data = targets[
    targets["Category"] == "Furniture"
]

print("\nFurniture Category Data")
print(furniture_data)
# ==========================================================
# STEP 31 - Verify Month Column
# ==========================================================

print("\nFurniture Data Columns")
print(furniture_data.columns)

print("\nFurniture Data Information")
print(furniture_data.info())
# ==========================================================
# STEP 32.1 - Sort Furniture Data by Month
# ==========================================================

furniture_data = furniture_data.sort_values(
    by="Month of Order Date"
)

print("\nFurniture Data After Sorting")
print(furniture_data)
# ==========================================================
# STEP 32.2 - Calculate Month-over-Month Change
# ==========================================================

furniture_data["MoM Change (%)"] = (
    furniture_data["Target"].pct_change() * 100
)

print("\nFurniture Data with MoM Change")
print(furniture_data)
print("\nFurniture Target Summary")

print(
    furniture_data[
        [
            "Month of Order Date",
            "Target",
            "MoM Change (%)"
        ]
    ]
)

# ==========================================================
# STEP 33.1 - Convert Month to Readable Format
# ==========================================================

furniture_data["Month"] = furniture_data["Month of Order Date"].dt.strftime("%b-%Y")

print("\nReadable Month Format")
print(furniture_data[["Month", "Target"]])

# ==========================================================
# STEP 33.2 - Professional Line Chart
# ==========================================================

plt.figure(figsize=(10, 6))

plt.plot(
    furniture_data["Month"],
    furniture_data["Target"],
    marker="o",
    linewidth=3,
    markersize=8
)

plt.title(
    "Furniture Monthly Sales Target",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Month", fontsize=12)
plt.ylabel("Sales Target", fontsize=12)

plt.xticks(rotation=45)

plt.grid(True, linestyle="--", alpha=0.5)
# Display target values on each point

for x, y in zip(furniture_data["Month"], furniture_data["Target"]):
    plt.text(
        x,
        y + 100,
        f"{y}",
        ha="center",
        fontsize=9,
        fontweight="bold"
    )
    plt.tight_layout()

plt.savefig(
    "charts/furniture_target_trend.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()
# ==========================================================
# STEP 34.1 - Highest Increase Month
# ==========================================================

highest_increase = furniture_data.loc[
    furniture_data["MoM Change (%)"].idxmax()
]

print("\nHighest Increase Month")
print(highest_increase)
# ==========================================================
# STEP 34.2 - Highest Decrease Month
# ==========================================================

highest_decrease = furniture_data.loc[
    furniture_data["MoM Change (%)"].idxmin()
]

print("\nHighest Decrease Month")
print(highest_decrease)
# ==========================================================
# STEP 34.3 - Average Monthly Target
# ==========================================================

average_target = furniture_data["Target"].mean()

print("\nAverage Monthly Target")
print(round(average_target, 2))
# ==========================================================
# STEP 34.4 - Furniture Target Summary
# ==========================================================

print("\n" + "=" * 60)
print("FURNITURE TARGET ANALYSIS SUMMARY")
print("=" * 60)

print(f"Highest Increase Month : {highest_increase['Month']}")
print(f"Highest Increase (%)   : {highest_increase['MoM Change (%)']:.2f}%")

print()

print(f"Highest Decrease Month : {highest_decrease['Month']}")
print(f"Highest Decrease (%)   : {highest_decrease['MoM Change (%)']:.2f}%")

print()

print(f"Average Monthly Target : {average_target:.2f}")
# ==========================================================
# QUESTION 1 - PART 3
# Regional Performance Insights
# ==========================================================

# Top 5 states with highest order count

top_states = (
    orders["State"]
    .value_counts()
    .head(5)
)

print("\n" + "=" * 60)
print("TOP 5 STATES BY ORDER COUNT")
print("=" * 60)

print(top_states)
# Store top state names

top_state_names = top_states.index

print("\nTop State Names")
print(top_state_names)
# Filter merged data for top 5 states

top_state_data = merged_data[
    merged_data["State"].isin(top_state_names)
]

print("\nTop State Data")
print(top_state_data.head())
# ==========================================================
# STEP 36.1 - Total Sales Per State
# ==========================================================

state_sales = (
    top_state_data
    .groupby("State")["Amount"]
    .sum()
)

print("\n" + "=" * 60)
print("TOTAL SALES PER STATE")
print("=" * 60)

print(state_sales)
# ==========================================================
# STEP 36.2 - Average Profit Per State
# ==========================================================

state_profit = (
    top_state_data
    .groupby("State")["Profit"]
    .mean()
)

print("\n" + "=" * 60)
print("AVERAGE PROFIT PER STATE")
print("=" * 60)

print(state_profit.round(2))
# ==========================================================
# STEP 36.3 - Regional Summary Table
# ==========================================================

regional_summary = pd.DataFrame({

    "Order Count": top_states,

    "Total Sales": state_sales,

    "Average Profit": state_profit

})

regional_summary = regional_summary.round(2)

print("\n" + "=" * 60)
print("REGIONAL PERFORMANCE SUMMARY")
print("=" * 60)

print(regional_summary)
# ==========================================================
# STEP 36.4 - Sort Regional Summary
# ==========================================================

regional_summary = regional_summary.sort_values(
    by="Total Sales",
    ascending=False
)

print("\nSorted Regional Summary")
print(regional_summary)
# ==========================================================
# STEP 36.5 - Best Performing State
# ==========================================================

best_state = regional_summary.index[0]

print("\nBest Performing State")
print(best_state)
# ==========================================================
# STEP 36.6 - Lowest Performing State
# ==========================================================

lowest_state = regional_summary.index[-1]

print("\nLowest Performing State")
print(lowest_state)

# ==========================================================
# STEP 37.1 - Regional Sales Bar Chart
# ==========================================================

plt.figure(figsize=(10, 6))

bars = plt.bar(
    regional_summary.index,
    regional_summary["Total Sales"]
)

plt.title(
    "Top 5 States - Total Sales",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("State", fontsize=12)
plt.ylabel("Total Sales", fontsize=12)

plt.xticks(rotation=20)

plt.grid(axis="y", linestyle="--", alpha=0.4)
# Display sales value on each bar

for bar in bars:

    height = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width()/2,
        height + 1000,
        f"{int(height):,}",
        ha="center",
        fontsize=9,
        fontweight="bold"
    )
    plt.tight_layout()

plt.savefig(
    "charts/regional_sales.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()
# ==========================================================
# STEP 37.4 - Regional Business Insights
# ==========================================================

print("\n" + "=" * 60)
print("REGIONAL BUSINESS INSIGHTS")
print("=" * 60)

print(f"""
Best Performing State : {best_state}

Lowest Performing State : {lowest_state}

Key Findings

1. {best_state} generated the highest sales among the top 5 states.

2. {lowest_state} generated the lowest sales and needs improvement.

3. Maharashtra shows strong average profitability.

4. Punjab has negative average profit, indicating possible pricing or cost issues.

Recommendations

• Increase marketing investment in high-performing states.

• Review pricing strategy in low-profit states.

• Improve logistics and inventory in underperforming regions.

• Launch regional promotional campaigns based on customer demand.

""")