from bs4 import BeautifulSoup
import requests, csv, re
import pandas as pd

url = 'https://download.bls.gov/pub/time.series/pc/'
res = requests.get(url)
soup = BeautifulSoup(res.content, 'html.parser')
# print(soup.prettify())
# title_tag = soup.title
# print(title_tag)          #access the title
# print(title_tag.string)   #access the title content
a_tags = soup.find_all('a')
# df = {}
# df = []
# for tag in a_tags:
#     content = 'https://download.bls.gov/'+ tag.string
#     df.append(content)
# for link in a_tags:
#     links = 'https://download.bls.gov'+ link.get('href')
#     df = pd.Series({'link':links})
#     print(df)
with open('C:/share_VM/work/Project_PPI/PPI_USA.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, dialect='excel')
    writer.writerow(['info'])
    for link in a_tags:
        links = 'https://download.bls.gov' + link.get('href')
        df = pd.Series({'link': links})
        writer.writerow(df)
    csvfile.close()