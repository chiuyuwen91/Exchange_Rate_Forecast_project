import pandas as pd
import csv
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

rates = pd.read_csv('./info/USD_NTD_Rate02.csv', index_col=0)

# Observe the whole data range and then specific data ranges
for startYear, endYear in [[1964, 2019]]:
    df = pd.read_csv('./info/forex_signals_test.csv', index_col=0)
    # Keep only the data for the time range that we care about
    if startYear >= 1965:
        df = df[df.index >= str(startYear) + '-01']
        df = df[df.index < str(endYear) + '-01']
    # Use the same date format we used for the exchange rate

    df.index = pd.to_datetime(df.index)

    # Scale the PPI data
    scaler = MinMaxScaler()
    # df[list(df)] = scaler.fit_transform(df[list(df)])
    df[list(df)] = scaler.fit_transform(df[list(df)])
    # Join the exchange rate data with the PPI data
    m = df[list(df)[:]].join(rates, how='inner').fillna(0)

    correlations = (m.corr()['USD_NTD'].sort_values(ascending=False).dropna())
    corr_limit = correlations[1:26]
    # print(corr_limit)
    # # print(~df.columns.duplicated())
    # with open('./info/forex_signals_corr.csv', 'w', newline='') as csvfile:
    #     writer = csv.writer(csvfile, dialect='excel')
    #     writer.writerow(corr_limit.index)
    #
    #     for i, idx in enumerate(corr_limit.index):
    #         # print(i, idx)
    #         for a, ano in enumerate(df.columns):
    #         #     # print(a, ano)
    #             if idx == ano:
    #                 new_df = df.loc[:, [idx]]
    #                 print(new_df)
    #                 writer.writerow(new_df)
    #     csvfile.close()

        # new_df.to_csv('./info/forex_signals_corr.csv', index=True, header=True)
    # s = []
    # with open('./info/forex_signals_corr.csv', 'w', newline='') as csvfile:
    #     writer = csv.DictWriter(csvfile, fieldnames=corr_limit.index, dialect='excel')
    #     writer.writeheader()
    #     # writer = csv.DictWriter(csvfile, fieldnames=[idx], dialect='excel')
    #
    #     d = {}
    #     for i, idx in enumerate(corr_limit.index):
    #         # print(i, idx)
    #         # if idx in df.columns:
    #         # writer = csv.DictWriter(csvfile, fieldnames=idx, dialect='excel')
    #         # writer.writeheader([idx])
    #
    #         new_df = df.loc[:, idx]
    #         # d.index =m.index
    #         # d[idx] = new_df
    #         writer.writerow({idx: new_df})
    #     csvfile.close()


        # s.append(new_df)
    # print(s)
    # s.to_csv('./info/forex_signals_corr.csv', index=False, header=False)
    #     # else:
    #     #     pass
