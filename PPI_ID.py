from bs4 import BeautifulSoup
import requests, csv
import pandas as pd
from IPython.display import display
import matplotlib.pyplot as plt

url = 'https://download.bls.gov/pub/time.series/pc/pc.product'
res = requests.get(url)
soup = BeautifulSoup(res.content, 'html.parser')

with open('./info/Series_ID_transform.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, dialect='excel')
    for column in soup:
        df = column.split('\r\n')
        for row in df:
            item = row.split('\t')
            writer.writerow(item)
    csvfile.close()

# Load the CSV file
df = pd.read_csv('./info/PPI_USA_all.csv')
prodName = pd.read_csv('./info/Series_ID_transform.csv')
prodName['item'] = 'PCU' + prodName['industry_code'] + prodName['product_code']
prodName.set_index('item', inplace=True)

for i in df['series_id']:
    for newI in prodName.index:
        if i == newI:
            # acces the value which I want to switch
            item = prodName.loc[i, 'product_name']
            # replace the value, notic that it's series so need to add .str
            df['series_id'] = df['series_id'].str.replace(i, item)

        else:
            pass

# Drop the M13
df = df[(True ^ df['period'].isin(['M13']))]
df['date'] = df['year'].astype(str) + df['period']
df['date'] = df['date'].str.replace('M', '-')

# rename the date
df_sorted = df.sort_values(by=['date'], inplace=True)

# Decide what columns we want
categories = list(df[list(df)[0]].drop_duplicates())
df_cols = ['date', 'series_id', 'value']

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

# Spot check the output dataframe
display(new_df.head())

# Graph the data
new_df.plot()
plt.show()
# Save the dataframe with the economic indicators to a file
new_df.to_csv('./info/forex_signals.csv', index=True)

# Clean the data for training
rates = pd.read_csv('./info/forex_signals.csv', low_memory=False)
rateSlice = rates[336:]
df_new = rateSlice.drop(['date','series_id','value'], axis=1)
df_new = df_new.fillna(0)
df_new.to_csv('./info/forex_signals_clean.csv', index=False, header=False)
