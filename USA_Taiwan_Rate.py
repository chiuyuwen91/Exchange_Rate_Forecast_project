from bs4 import BeautifulSoup
import pandas as pd
import requests, csv

url = 'https://www.federalreserve.gov/releases/h10/hist/dat00_ta.htm'
res = requests.get(url)
soup = BeautifulSoup(res.content, 'html.parser')
# print(soup.prettify)
# info = soup.find_all('div', {'id':'content'})               #another way to access data
# data = soup.find('div', class_ = 'data-table')
table = soup.table
data = table.find_all('tr')
# print(data)
with open('C:/share_VM/work/Project_PPI/USA_Taiwan_Rate.csv', 'w') as csvfile:
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
        # print((str(date[0])).strip())
        # print((str(rate[0])).strip())