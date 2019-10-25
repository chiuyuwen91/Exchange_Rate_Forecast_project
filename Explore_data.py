import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler


def makeFig(plt, title, xlabel, ylabel, fName):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(fName, dpi=100)
    # plt.show()
    return


# Observe the whole data range and then specific data ranges
for startYear, endYear in [[1964, 2019], [1999, 2006], [2006, 2011], [2011, 2019]]:
    df_new = pd.read_csv('./info/forex_signals.csv', index_col=0)
    # Keep only the data for the time range that we care about
    if startYear >= 1965:
        df_new = df_new[df_new.index >= str(startYear) + '-01']
        df_new = df_new[df_new.index < str(endYear) + '-01']
    # Use the same date format we used for the exchange rate

    df_new.index = pd.to_datetime(df_new.index)

    # df_new.plot(legend=False)df_new[list(df_new)[:]]

    # Scale the PPI data
    scaler = MinMaxScaler()
    df_new[list(df_new)] = scaler.fit_transform(df_new[list(df_new)])
    # Join the exchange rate data with the PPI data
    m = df_new[list(df_new)[:]].join(rates, how='inner').fillna(0)

    correlations = (m.corr()['USD_NTD'].sort_values(ascending=False).dropna())
    correlations0 = len(correlations.astype(float))
    plt.figure(figsize=(20, 8))
    correlations[1:26].plot.barh()
    title = "Correlation of Industrial Product Prices and USD_NTD strength (" + str(startYear) + " to " + str(
        endYear) + ")"
    xlabel = "Correlation with USD_NTD"
    ylabel = "Price of Industrial Product"
    fName = str(startYear) + 's_corr_high.png'
    makeFig(plt, title, xlabel, ylabel, fName)

    plt.figure(figsize=(20, 8))
    correlations[-25:].plot.barh()
    fName = str(startYear) + 's_corr_low.png'
    makeFig(plt, title, xlabel, ylabel, fName)

    plt.figure(figsize=(20, 8))
    correlations[1:].plot.bar()
    plt.xticks([])
    fName = str(startYear) + 's_histogram_correlations.png'
    makeFig(plt, title, ylabel, xlabel, fName)

    # Tomorrow minus today's exchange rate gives the rate delta
    # Intuition: When tomorrow's USD_CAD exchange rate is higher than today's, the result is positive
    p = m.copy(deep=True)
    p['dUSD_NTD'] = m['USD_NTD'].shift(-1) - m['USD_NTD']
    causations = p.corr()['dUSD_NTD'].sort_values(ascending=False).dropna()

    plt.figure(figsize=(20, 8))
    causations[1:].plot.bar()
    plt.xticks([])
    xlabel = "Price of Industrial Product"
    ylabel = "Correlation with change in USD_NTD next month"
    title = "Correlation with change in USD_NTD next month(" + str(startYear) + " to " + str(endYear) + ")"
    fName = str(startYear) + 's_histogram_predictions.png'
    makeFig(plt, title, xlabel, ylabel, fName)
