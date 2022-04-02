#---Pandas dataframe is the best one I currently know for this assignment,
#---In the code it will become clear why.
import numpy as np
import pandas as pd
#---Create a data frame for the fund data.
dataf = pd.read_csv('Funds.csv')
df = pd.DataFrame(dataf)
#---Create a dataframe for the weight data obtained from efficient frontier
#---code.
dataw = pd.read_csv('Weights.csv')
dw = pd.DataFrame(dataw)
#---Remove the column with the dates, the index is our date here.
df = df.iloc[:, 1:]
dw = dw.iloc[:, 1:]
#---Remove funds with too much data missing.
df = df[df.columns[df.isnull().mean() < 0.3]]
#---Get a list of the names of funds.
F_names = list(df)
#---Make the percentages into float values in the dataframe.
for i in df:
    df[i] = df[i].str.rstrip('%').astype('float')
#---Fill nan values with means, for calculating drawdown you cannot really
#---ignore the missing data, so of course for this part simulated data
#---would be ideal.
for i in F_names:
    df[i] = df[i].fillna(df[i].mean())
#---Multiply the weights by the % returns for each month of the fund.
weight_x_return = []
for i in range(0,len(dw)):
    temp = df.multiply(dw.iloc[i], axis='columns')
    weight_x_return.append(np.array(temp)) 
#---Sum all the % returns x weights to get total % return for each month
#---for each portfolio, might have made an error in my logic, should
#---think about it a bit more. Potentially I should have turned the percentages
#---to actual returns at this point.
total_return = []
for i in range(0,len(weight_x_return)):
    temp1 = weight_x_return[i].sum(axis=1)
    total_return.append(temp1/10000)
#---Place the data back in a pandas dataframe for the rolling functions
portfolio_perc_returns = pd.DataFrame(total_return).transpose()
#---Turn the percentage returns for each month to actual returns, then 
#---for each month calculate the actual returns. For now assume initial 
#---total investment of 1.
return_array = []
for column in portfolio_perc_returns.columns:
    percentage_return = portfolio_perc_returns[column].values
    returns = []
    initial = 1
    for x in range(0, len(percentage_return)):
        initial=initial + initial*percentage_return[x]
        returns.append(initial)
    return_array.append(returns)
#---Turn once again the array to a dataframe to be able to use .rolling
#---function which helps a lot. Calculate the monthly drawdown.
return_dataframe = pd.DataFrame(return_array).transpose()
rollmax = return_dataframe.rolling(len(return_dataframe), min_periods=1).max()
monthly_drawdown = (return_dataframe-rollmax)/rollmax
max_monthly_drawdown = monthly_drawdown.rolling(len(return_dataframe), min_periods=1).min()
#---Sort the max_monthly_drawdown dataframe to find the index
#---of the portfolio which has a its max drawdown closest to 20%.
#---Could be adjusted to find several portfolios with drawdowns close to 20%.
df_sort1 = max_monthly_drawdown.iloc[-1].transpose()
df_sort2 = df_sort1.iloc[df_sort1[:].sub(-0.2).abs().idxmin()]
portfolio_index = df_sort1[:].sub(-0.2).abs().idxmin()
#---Use the index in the weights dataframe to find the respective weights for 
#---each fund.
final_df = dw.iloc[portfolio_index, :].transpose()
print(final_df)