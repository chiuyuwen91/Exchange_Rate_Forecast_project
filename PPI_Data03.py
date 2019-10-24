
#select appropriate links from the table
file = open('C:/share_VM/work/Project_PPI/PPI_USA.csv')
readFile = str(file.readlines()).split(',')

for links in readFile:
    link = links[2:-3]
    if 'pc.data' in link:
        title = link.split('.')[-1]
        print(link)
    #     data = requests.get(link)
    #     print(data)
    else:
        pass