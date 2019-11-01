import pandas as pd
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
    s = []
    for i, idx in enumerate(corr_limit.index):
        print(i, idx)
        # if idx in df.columns:
        new_df = df.loc[:, idx]
        s.append(new_df)
    print(s)
        # else:
        #     pass
