"""
from bs4 import BeautifulSoup
import requests, csv, re
import pandas as pd

url = 'https://download.bls.gov/pub/time.series/pc/pc.industry'
res = requests.get(url)
soup = BeautifulSoup(res.content, 'html.parser')
# print(soup.prettify())

with open('C:/share_VM/work/Project_PPI/ID_Industry.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, dialect = 'excel')
    for column in soup:
        # df = re.split('\t|\r\n',column)
        df = column.split('\r\n')
        for row in df:
            item = row.split('\t')
            # print(row + ' ' + str(len(item)))
        # df_new = pd.Series({'industry_code':df[0], 'industry_name':df[1]})
            writer.writerow(item)
    csvfile.close()

"""


from bs4 import BeautifulSoup
import requests, csv, re
import pandas as pd

url = 'https://download.bls.gov/pub/time.series/pc/pc.product'
res = requests.get(url)
soup = BeautifulSoup(res.content, 'html.parser')
print(soup.prettify())

with open('C:/share_VM/work/Project_PPI/ID_Industry_Product.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, dialect = 'excel')
    for column in soup:
        # df = re.split('\t|\r\n',column)
        df = column.split('\r\n')
        for row in df:
            item = row.split('\t')
            # print(row + ' ' + str(len(item)))
        # df_new = pd.Series({'industry_code':df[0], 'industry_name':df[1]})
            writer.writerow(item)
    csvfile.close()