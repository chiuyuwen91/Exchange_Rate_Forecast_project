# Select the data we want
from bs4 import BeautifulSoup
import requests, csv, os
import pandas as pd

# Crawl data from website
url = 'https://download.bls.gov/pub/time.series/pc/'
res = requests.get(url)

# Parse the data
soup = BeautifulSoup(res.content, 'html.parser')
a_tags = soup.find_all('a')

# Create a directory
os.mkdir('info')

# Write the data into a file
with open('./info/PPI_USA.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, dialect='excel')
    writer.writerow(['info'])
    for link in a_tags:
        links = 'https://download.bls.gov' + link.get('href')
        df = pd.Series({'link': links})
        writer.writerow(df)
    csvfile.close()

