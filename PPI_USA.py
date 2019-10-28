from bs4 import BeautifulSoup
import requests, csv, os, re
import pandas as pd

# Crawl data from website
url = 'https://download.bls.gov/pub/time.series/pc/'
res = requests.get(url)

# Parse the data
soup = BeautifulSoup(res.content, 'html.parser')
a_tags = soup.find_all('a')

# Create a directory
# os.mkdir('info')

# Write the links we crawled into a file
with open('./info/PPI_USA.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, dialect='excel')
    writer.writerow(['info'])
    for link in a_tags:
        links = 'https://download.bls.gov' + link.get('href')
        df = pd.Series({'link': links})
        writer.writerow(df)
    csvfile.close()

# Open the file we just create
file = open('./info/PPI_USA.csv')
readFile = str(file.readlines()).split(',')

# Create a new directory that we gonna save all data
# os.mkdir('data')

# Access data from each link which means an item
for links in readFile:
    link = links[2:-3]
    if 'pc.data' in link:
        res = requests.get(link)
        content = re.compile("[^\n\r]+")
        rows = content.findall(res.text)

        # Access name of each item
        title = link.split('.')[-1]

        # Create path for each file(item) through their names
        fileName = os.path.join('./data/', title + '.csv')

        # Open files and write data into the file
        with open(fileName, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, dialect='excel')
            for row in rows:

                # Use regular expression to parse the info from website
                item = re.compile(
                    "[ ]*([\\w\\d\\-\\.]+)[ ]*")

                # Write data into files
                rowData = []
                for i in item.findall(row):
                    rowData.append(i)
                writer.writerow(rowData)

        # Close the files
        csvfile.close()
    else:
        pass

# Combine all files into one
path = './data'

# Go through each files
files = os.listdir(path)
s = []
for file in files:
    if not os.path.isdir(file):
        f = open(path + '/' + file)
        iter_f = iter(f)

        # Create an empty file to save all files
        with open('./info/PPI_USA_all.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, dialect='excel')
            for line in iter_f:
                df = list(line.rstrip('\n').split(','))
                writer.writerow(df)
            f.close()
