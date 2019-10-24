
# select the data we want
from IPython.display import display
import matplotlib.pyplot as plt
import pandas as pd

# Load the CSV file
df = pd.read_csv('C:/share_VM/work/Project_PPI/data_all.csv')
df = df[(True^df['period'].isin(['M13']))]
df['date'] = df['year'].astype(str) + df['period']
df['date'] = df['date'].str.replace('M', '-')
# print(df['date'] ,df['date'] , sep='\n')
# rename the date
df_sorted = df.sort_values(by=['date'], inplace=True)
# print(df)

# Decide what columns we want
categories=list(df[list(df)[0]].drop_duplicates())
df_cols=['date', 'series_id', 'value']

# Prepare an empty dataframe to fill with properly indexed economic data
new_df = pd.DataFrame(columns=df_cols)

# Toss out the columns we don't want
df = df[df_cols]

# Set the date as the index using the same format as the USD_CAD data
df.index = df['date']
new_df.index = new_df['date']

# Dump out the date column now that we applied it to the dataframe index
df.drop(['date'], axis=1, inplace=True)
new_df.drop(['date'], axis=1, inplace=True)

# Spot check the dataframe so far
display(df.head())

# Loop through the economic indicators and put each one in a dedicated column
for cat in categories:
    # Data can have problems, and not all indicators will make it through
    try:
      new_df[cat] = df[df[list(df)[0]] == cat]['value']
    except Exception as e:
      print("failed on", cat, e)
print(new_df)
# # Spot check the output dataframe
display(new_df.head())


# Graph the data
new_df.plot()
plt.show()
# Save the dataframe with the economic indicators to a file
new_df.to_csv("C:/share_VM/work/Project_PPI/forex_signals_revise.csv")
