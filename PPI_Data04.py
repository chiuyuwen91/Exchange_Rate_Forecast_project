
#open each files and combine to one file
import os, csv
import pandas as pd
path = 'C:/share_VM/work/Project_PPI/data'
files = os.listdir(path)
s = []
for file in files:
    if not os.path.isdir(file):
        f = open(path + '/' + file)
        iter_f = iter(f)
        str = ""


        with open('C:/share_VM/work/Project_PPI/data_all.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, dialect='excel')
            for line in iter_f:
                # str = str +line
            # s.append(str)
                df = list(line.rstrip('\n').split(','))
                print(df)
                # df = pd.Series({'info': line})
                writer.writerow(df)

            f.close()

