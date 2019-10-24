import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# daily exchange rate
# https://open.canada.ca/data/en/dataset/1bc25b1e-0e02-4a5e-afd7-7b96d6728aac

# Load the CSV file
rates = pd.read_csv('C:/share_VM/work/Project_PPI/USA_Taiwan_Rate.csv', low_memory=False)
# # Decide what columns we want
# rates_cols=['REF_DATE', 'VALUE']
# Only keep the closing spot price for our currency pair
# rates=rates[rates['Type of currency']=='United States dollar, closing spot rate']
# # Dump the columns we don't need, and fill null values with 0s
rates = rates.fillna(0)
rates = rates.replace('ND','0')
# Force a common index with the economic data we will be getting next
rates.index = rates['Date']
# Now that we set the index, drop the extra date column
rates.drop(['Date'], axis=1, inplace=True)
# Let's give our asset a nice human-friendly name: USD_CAD
rates.rename(columns={'Rate': 'USD_NTD'}, inplace=True)
# If rate is on a weekend or day market is closed, then use the most recent day's rate
# Weekends are 2 days long so copy Saturday stuff to Sundays
# Carry forward the rates for 3 day and 4 day market closures
# while rates[rates == 0].count(axis=0)['USD_NTD']/len(rates.index) >0:
#     print("Shifting rates. Days with rate at 0 = %",rates[rates == 0].count(axis=0)['USD_NTD']/len(rates.index))
#     rates['yesterday']= rates['USD_NTD'].shift(1)
#     rates['USD_NTD']  = np.where(rates['USD_NTD']==0, rates['yesterday'], rates['USD_NTD'])
# #Verify we don't have days with rates at 0
# print("Days with rate at 0 = %",rates[rates == 0].count(axis=0)['USD_NTD']/len(rates.index))
# # Spot check the results against a trading days calendar: http://www.swingtradesystems.com/trading-days-calendars.html
# # Graph the data
# rates.drop(['yesterday'], axis=1, inplace=True)
rates = rates.astype(float)
# print(rates)
rates.plot()
plt.show()
rates.to_csv("C:/share_VM/work/Project_PPI/USA_Taiwan_Rate_Revise.csv")


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
    df_new = pd.read_csv('C:/share_VM/work/Project_PPI/forex_signals_revise.csv', index_col=0)
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
