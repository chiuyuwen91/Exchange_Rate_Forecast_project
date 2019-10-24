import pandas as pd
from io import StringIO
import datetime, time, calendar

link = 'C:/share_VM/work/Project_PPI/USA_Taiwan_Rate_Revise.csv'
# df = pd.read_csv(StringIO(link), header=None, parse_dates=['Date'], index_col='Date')
df = pd.read_csv(link)
# df['Date'] = pd.to_datetime(df['Date'])
# print(df['Date'].dtype)

# date_new = df['Date'].apply(lambda x:time.asctime(x.timetuple()))
# # data = date_new.apply(lambda x:time.strftime('%Y-%m-%d'))
# date_new = df['Date'].apply(lambda time : datetime.datetime.strptime(time, '%m-%d-%Y'))
# print(date_new)

rate = df['USD_NTD']
date = df['Date'].str.split('-')
print(date)
date_new = []
for item in date:
    item[1] = list(calendar.month_abbr).index(item[1])       #convert month name to month number
    date = '20' + item[2] + '-' + str(item[1]) + '-' + item[0]
    date = pd.to_datetime(date, format = '%Y-%m-%d')
    # date = pd.DataFrame({'Date': date}, index = pd.DatetimeIndex(date), dtype=float)
    # date = time.mktime(date.timetuple())
    date_new.append(date)
date_new = pd.DataFrame({'Date':date_new, 'USD_NTD':rate})      #write the dataframe
date_new['USD_NTD'].astype(float)
# print(date_new['Date'].dtype)
# date_new.resample('M', how = 'mean')

date_new = date_new.set_index('Date').groupby(pd.Grouper(freq='M')).mean()   #access the mean of month
print(date_new)
# df.groupby(pd.Grouper(freq='M')).mean()
date_new.to_csv('C:/share_VM/work/Project_PPI/USA_Taiwan_Rate_Clean.csv')






# df1 = df.set_index('date').groupby('product').resample('1D')['value'].ffill()
# print (df1)

