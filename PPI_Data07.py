
# select the data we want
from IPython.display import display
import matplotlib.pyplot as plt
import pandas as pd

# Load the CSV file
df = pd.read_csv('C:/share_VM/work/Project_PPI/data_all02.csv')
id = pd.read_csv('C:/share_VM/work/Project_PPI/ID_Industry_Product02.csv')
id.set_index('item', inplace=True)
# print(id.index)
# print(df['series_id'])
# test = id.loc['PCU1133--1133--', 'product_name']

for i in df['series_id']:
    for new_i in id.index:
        # try:
        if i == new_i:
            item = id.loc[i, 'product_name']     #acces the value which I want to switch
            # print(item)
            df['series_id'] = df['series_id'].str.replace(i, item)        #replace the value, notic that it's series so need to add .str
            print(df['series_id'])
df.to_csv('C:/share_VM/work/Project_PPI/data_all03.csv',index=False)    #without index
        # except:
        #     print('error')


# Save the dataframe with the economic indicators to a file
# df.to_csv("C:/share_VM/work/Project_PPI/forex_signals_revise02.csv")


