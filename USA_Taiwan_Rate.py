from bs4 import BeautifulSoup
import pandas as pd
import requests, csv, calendar
import matplotlib.pyplot as plt

# daily exchange rate
# Crawl data from website
url = 'https://www.federalreserve.gov/releases/h10/hist/dat00_ta.htm'
res = requests.get(url)
soup = BeautifulSoup(res.content, 'html.parser')

table = soup.table
data = table.find_all('tr')

with open('./info/USD_NTD_Rate.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, dialect = 'excel')
    writer.writerow(['Date','Rate'])
    for tr in data:
        th = tr.find_all('th')
        td = tr.find_all('td')
        date = [d.text for d in th]
        rate = [i.text for i in td]
        Da = (str(date[0])).strip()
        Ra = (str(rate[0])).strip()
        df = pd.Series({'Date': Da, 'Rate': Ra})
        writer.writerow(df)

    csvfile.close()

# Load the CSV file
rates = pd.read_csv('./info/USD_NTD_Rate.csv', low_memory=False)

# Dump the columns we don't need, and fill null values with 0s
rates = rates.fillna(0)
rates = rates.replace('ND','0')
# Force a common index with the economic data we will be getting next
rates.index = rates['Date']
# Now that we set the index, drop the extra date column
rates.drop(['Date'], axis=1, inplace=True)
# Let's give our asset a nice human-friendly name: USD_CAD
rates.rename(columns={'Rate': 'USD_NTD'}, inplace=True)

# Spot check the results against a trading days calendar: http://www.swingtradesystems.com/trading-days-calendars.

# Graph the data
rates = rates.astype(float)
rates.plot()
plt.show()

# Notice the index
rates.to_csv('./info/USD_NTD_Rate02.csv')


df = pd.read_csv('./info/USD_NTD_Rate02.csv')
rate = df['USD_NTD']
date = df['Date'].str.split('-')

dateNew = []
for item in date:
    # convert month name to month number
    item[1] = list(calendar.month_abbr).index(item[1])
    date = '20' + item[2] + '-' + str(item[1]) + '-' + item[0]
    date = pd.to_datetime(date, format = '%Y-%m-%d')
    dateNew.append(date)
# Write the dataframe
dateNew = pd.DataFrame({'Date': dateNew, 'USD_NTD': rate})
dateNew['USD_NTD'].astype(float)

# Access the mean of month
dateNew = dateNew.set_index('Date').groupby(pd.Grouper(freq='M')).mean()
dateNew.to_csv('.info/USD_NTD_Rate03.csv')


