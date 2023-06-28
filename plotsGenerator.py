import pandas as pd
import json
import matplotlib.pyplot as plt

# Define the file path
file_path = "measurements/changing_routers_no.csv"

# Define the column names
column_names = ["hosts", "routers", "channels", "cost"]

# Load the CSV file into a DataFrame
df = pd.read_csv(file_path, delimiter='+')

# Extract cost column into separate columns
# cost_data = df["cost"].apply(lambda x: print(pd.read_json(x,  orient='index').transpose()))# pd.Series(pd.read_json(x)))
cost_data = pd.json_normalize(df["cost"].apply(json.loads))
df = pd.concat([df, cost_data], axis=1)

# # Remove the original cost column
df.drop("cost", axis=1, inplace=True)

# Print the resulting DataFrame
print(df)

df['total_cost'] = df['cable_cost'] + df['host_cost'] + df['router_cost']

# Plot the sum of costs
plt.bar(df['routers'], df['total_cost'])
plt.xlabel('Routers')
plt.ylabel('Total Cost')
plt.title('Sum of Costs from Routers')
plt.show()