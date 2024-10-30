import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV files
summary_single = pd.read_csv("single_threaded_summary.csv")
summary_single.columns = ["Single-Threaded"]

summary_multi = pd.read_csv("multi_threaded_summary.csv")
summary_multi.columns = ["Multi-Threaded"]

# Combine the data
data = pd.concat([summary_single, summary_multi], axis=1)

# Create the boxplot
plt.figure(figsize=(15, 5))
data.boxplot(column=["Single-Threaded", "Multi-Threaded"], vert=False)
plt.title("1000 Time Comparisons for Single- vs. Multi-Threaded Servers")
plt.xlabel("Average Time for 100 Requests")
plt.ylabel("Single- vs. Multi-Threaded Server")
plt.savefig("comparisonPlot.png")
plt.close()