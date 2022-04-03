import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from Historic_Crypto import HistoricalData


def load_fund_data(path='Funds.csv'):
    data = pd.read_csv(path)
    df = pd.DataFrame(data)
    return df

def get_coin_codes():
    import requests

    url = "https://api.pro.coinbase.com/products"
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers).json()
    coin_codes = []
    quote_currencies = []
    for coin_data in response:
        if coin_data["quote_currency"] == "USD":
            coin_codes.append(coin_data["base_currency"])
    coin_codes.sort()
    return coin_codes

def download_data(coin_codes, start_time='2021-01-01-00-00'):
    data_list = []
    for coin_code in coin_codes:
        try:
            crypto_data = HistoricalData(coin_code+"-USD",86400,start_time).retrieve_data()
            crypto_data = crypto_data[['close']]
            crypto_data = crypto_data.rename(columns={"close": f"{coin_code}"})
            data_list.append(crypto_data)
        except:
            pass

    combined = pd.concat(data_list, axis=1)

    df = combined.pct_change(periods=1)*100
    df = df.reset_index(drop=True)
    return df


def efficient_frontier(df, n_portfolios=100):
    # Calculate the covariance matrix for the portfolio.
    portfolio_covariance = df.cov()

    # Lists to store weights, returns and risk values.
    portfolio_returns = []
    # Standard deviation of porfolio is basically the risk.
    portfolio_stds = []
    coin_weights = []
    pair = []

    coin_names = df.columns
    coin_means = df.mean().to_numpy()

    # Generate data, giving each coin a random weight.
    while len(portfolio_stds) < n_portfolios:
        # Initial values.
        check = False
        portfolio_return = 0

        # Make a portfolio with random weights for each coin.
        coin_weight = np.random.random(len(coin_names))
        # Normalise to 1.
        coin_weight /= np.sum(coin_weight)

        # Calculate the expected return value of the random portfolio.
        for i in range(len(coin_names)):
            portfolio_return += coin_weight[i] * coin_means[i]
        #---Calculate variance, use it for the deviation.
        portfolio_variance = np.dot(np.dot(coin_weight.transpose(), portfolio_covariance), coin_weight)
        portfolio_std = np.sqrt(portfolio_variance)

        """
        To optimise the efficient frontier graph, check if the data point is 
        clumped together with where most of them fall or not, as we want data 
        points on the outer edge and not below the frontier. If it does, skip it
        and keep generating until we get one on the outside. One downfall is that 
        it slows down the more points are generated as less and less points make it
        through the check, different optimisation methods could then be looked at 
        if the number of portfolios wanted is very large.
        """
        pair.append([portfolio_return, portfolio_std])
        for R,V in pair:
            if (R > portfolio_return) and (V < portfolio_std):
                check = True
                break
        if check:
            continue

        portfolio_stds.append(portfolio_std)
        portfolio_returns.append(portfolio_return)
        coin_weights.append([i * 100 for i in coin_weight])
        
        
        """
        Store the data into a csv file. Big downfall is that I store a lot of 
        portfolios that are not necessarily on the frontier, further steps would be
        to fit a curve to the frontier and remove any points that are too far away
        from it. This is mainly due to the 'burn' in period where points are first 
        generated wherever to then allow optimisation.
        """

    ef_df = pd.DataFrame(coin_weights)
    ef_df.columns = coin_names
    ef_df.insert(0, "Return", portfolio_returns, True)
    ef_df.insert(1, "Risk", portfolio_stds, True)
    return ef_df, portfolio_stds, portfolio_returns

def users_point(df, coin_weight):
    # Calculate the covariance matrix for the portfolio.
    portfolio_covariance = df.cov()
    coin_names = df.columns
    coin_means = df.mean().to_numpy()
    
    # Normalise to 1.
    coin_weight /= np.sum(coin_weight)
    
    portfolio_return = 0
    
    # Calculate the expected return value of the random portfolio.
    for i in range(0, len(coin_names)):
        portfolio_return += coin_weight[i] * coin_means[i]
    #---Calculate variance, use it for the deviation.
    portfolio_variance = np.dot(np.dot(coin_weight.transpose(), portfolio_covariance), coin_weight)
    portfolio_std = np.sqrt(portfolio_variance)

    return portfolio_std, portfolio_return

def plot_frontier(portfolio_stds, portfolio_returns):
    plt.figure()
    plt.scatter(portfolio_stds, portfolio_returns)
    plt.xlabel("Risk (%)")
    plt.ylabel('Returns (%)')
    return 
    
    
def find_optimal_return(df, risk):
    df_ef = df.iloc[(df["Risk"]-risk).abs().argsort()[:10]]
    df_ef = df_ef.iloc[(df_ef["Return"]).argmax()]
    pd.options.display.float_format = '{:,.2f}'.format
    return df_ef
    
def find_optimal_risk(df, returns):
    df_ef = df.iloc[(df["Return"]-returns).abs().argsort()[:10]]
    df_ef = df_ef.iloc[(df_ef["Risk"]).argmin()]
    pd.options.display.float_format = '{:,.2f}'.format
    return df_ef

    