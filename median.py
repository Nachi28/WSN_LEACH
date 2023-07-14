import pandas as pd

df = pd.read_excel('WSN\hi.xlsx')

# Extract the column data as a Series
col_data = df["PDR"]

# Find the mx
max_value = col_data.max()

max_row = df.loc[df["PDR"] == max_value]

# Print the row
# print(max_row)
# print(max_row["No. of Nodes"].values[0])


sorted_column = col_data.sort_values(ascending=False)

# Find the last second maximum value
last_second_max = sorted_column.iloc[1]

# Print the maximum value and the last second maximum value
# print("Maximum:", max_value)
# print("Last Second Maximum value:", last_second_max)
last_sec_max_row = df.loc[df["PDR"] == last_second_max]
# print(last_sec_max_row)

print(" Ideal nodes: ",
      (last_sec_max_row["No. of Nodes"].values[0]+max_row["No. of Nodes"].values[0])/2)
