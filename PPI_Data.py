# assess infos from the website and store as files
from bs4 import BeautifulSoup
import pandas as pd
import requests, csv, re

file = open('C:/share_VM/work/Project_PPI/PPI_USA.csv')
readFile = str(file.readlines()).split(',')

for links in readFile:
    link = links[2:-3]
    if 'pc.data' in link:
        title = link.split('.')[-1]
        res = requests.get(link)
        content = re.compile("[^\n\r]+")
        rows = content.findall(res.text)
        # print(rows)
        fileName = 'C:/share_VM/work/Project_PPI/data/' + title + '.csv'
        print(fileName)
        with open(fileName, 'w') as csvfile:
            writer = csv.writer(csvfile, dialect='excel')
            for row in rows:
                item = re.compile(
                    "[ ]*([\\w\\d\\-\\.]+)[ ]*")
                # item = re.compile("[ ]*([^\t]+[^\s])")
                rowData = []
                for i in item.findall(row):
                    rowData.append(i)

                writer.writerow(rowData)

        csvfile.close()  # Remember to close the file

        print("done!")
    else:
        pass
