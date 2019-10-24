
#assess infos from the website and store as files
import requests, csv,re
import pandas as pd

url = 'https://download.bls.gov/pub/time.series/pc/pc.data.01.aggregates'
res = requests.get(url)
# print(res.text)
content = re.compile("[^\n\r]+")
rows = content.findall(res.text)
#print (list.count(rows))
with open('C:/share_VM/work/Project_PPI/data/aggregates.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, dialect='excel')
    # writer.writerow(['series_id', 'year', 'period', 'value'])

    #csvData = []
    for row in rows:
        # print(row)
        # idx = 0
        item = re.compile("[ ]*([\\w\\d\\-\\.]+)[ ]*")  #If I use [^\t]+, I will access all charaters including -,whitespace
        # item = re.compile("[ ]*([^\t]+[^\s])")
        rowData = []
        for i in item.findall(row):
            rowData.append(i)
        #csvData.append(rowData)
        # print(csvData)
            # idx+=1
        # print(csvData)

            # for i in item.findall(row):
            #     csvData.append(i)
            #     # print(csvData)
        writer.writerow(rowData)

csvfile.close()    #Remember to close the file

# def getContent(self, url):
#     print(url)
#
# getContent("hello")
print("done!")
