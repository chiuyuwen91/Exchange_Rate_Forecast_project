import pandas as pd

"""
1.
rates = pd.read_csv('C:/share_VM/work/Project_PPI/forex_signals_revise.csv', low_memory=False)
rateSlice = rates[420:]
rateSlice.index = rateSlice['date']
# df_new = rateSlice.drop([''], axis=1, inplace=True)
rateSlice.to_csv("C:/share_VM/work/Project_PPI/forex_signals_2000_2019.csv")
"""


"""
2.
df = pd.read_csv('C:/share_VM/work/Project_PPI/forex_signals_2000_2019.csv')
df_new = df.drop(['series_id','value'], axis=1)
df_new = df_new.fillna(0)
df_new.index = df_new['date']
df_new.to_csv("C:/share_VM/work/Project_PPI/forex_signals_clean.csv")
"""


id = pd.read_csv('C:/share_VM/work/Project_PPI/ID_Industry_Product.csv')
# new_col = id.loc[:, ['industry_code', 'product_code']]
id['item'] = 'PCU' + id['industry_code'] + id['product_code']
id.to_csv('C:/share_VM/work/Project_PPI/ID_Industry_Product02.csv')
file = pd.read_csv('C:/share_VM/work/Project_PPI/forex_signals_revise.csv')

