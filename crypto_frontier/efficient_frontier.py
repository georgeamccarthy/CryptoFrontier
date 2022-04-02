import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from Historic_Crypto import HistoricalData


def load_fund_data(path='Funds.csv'):
    data = pd.read_csv(path)
    df = pd.DataFrame(data)
    return df


def download_data(coin_codes=['ADA', 'ETH']):
    data_list = []
    for coin_code in coin_codes:
        crypto_data = HistoricalData(coin_code+"-USD",86400,'2021-01-01-00-00').retrieve_data()
        crypto_data = crypto_data[['close']]
        crypto_data = crypto_data.rename(columns={"close": f"{coin_code}"})
        data_list.append(crypto_data)

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
    fund_weights = []
    pair = []

    fund_names = df.columns
    fund_means = df.mean().to_numpy()

    # Generate data, giving each fund a random weight.
    while len(portfolio_stds) < n_portfolios:
        # Initial values.
        check = False
        portfolio_return = 0

        # Make a portfolio with random weights for each fund.
        fund_weight = np.random.random(len(fund_names))
        # Normalise to 1.
        fund_weight /= np.sum(fund_weight)

        # Calculate the expected return value of the random portfolio.
        for i in range(len(fund_names)):
            portfolio_return += fund_weight[i] * fund_means[i]
        #---Calculate variance, use it for the deviation.
        portfolio_variance = np.dot(np.dot(fund_weight.transpose(), portfolio_covariance), fund_weight)
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
        fund_weights.append([i * 100 for i in fund_weight])
        
        
        """
        Store the data into a csv file. Big downfall is that I store a lot of 
        portfolios that are not necessarily on the frontier, further steps would be
        to fit a curve to the frontier and remove any points that are too far away
        from it. This is mainly due to the 'burn' in period where points are first 
        generated wherever to then allow optimisation.
        """

    ef_df = pd.DataFrame(fund_weights)
    ef_df.columns = fund_names
    return ef_df, portfolio_stds, portfolio_returns


def plot_frontier(portfolio_stds, portfolio_returns):
    plt.figure()
    plt.scatter(portfolio_stds, portfolio_returns)
    plt.xlabel("Risk (%)")
    plt.ylabel('Returns (%)')
    return 

    