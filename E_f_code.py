#---Pandas dataframe is the best one I currently know for this assignment,
#---In the code it will become clear why.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#---Create a data frame for the fund data.
data = pd.read_csv('Funds.csv')
df = pd.DataFrame(data)
#---Remove the column with the dates, the index is our date here.
df = df.iloc[:, 1:]
#---Remove the funds with too much missing data for now, potentially 
#---data could be simulated even when only limited data is available
df = df[df.columns[df.isnull().mean() < 0.3]]
#---Get a list of the names of funds.
F_names = list(df)
#---Make the percentages into float values in the dataframe.
for i in df:
    df[i] = df[i].str.rstrip('%').astype('float')
#---Replace missing values with what you want, given more time
#---a separate code could be written to simulate data. Here I use means.
for i in F_names:
    df[i] = df[i].fillna(df[i].mean())
#---Calculate means for each fund.
fmeans = []
for i in F_names:
    fmeans.append(df[i].mean())
#---Calculate the covariance matrix for the portfolio.
pcovariance = df.cov()
#---Define some lists to store weights, return and risk values.
preturns = []
pstdevs = []
fweights = []
pair = []
#---n is the number of portfolios we want generated.
n=400
#---Loop to generate data. Giving each fund a random weight means there is
#---a very large number of combinations.
#---To speed up the process one could assign the weights in increments of
#---of 1 percent for example.
while len(pstdevs)<n:
    #---Initial values for the iteration.
    check = False
    preturn = 0
    fweight = np.zeros(shape=(len(fmeans),1))
    #---Make a portfolio with random weights for each fund.
    fweight = np.random.random(len(F_names))
    #---Make sure the percentages sum to 1.
    fweight /= np.sum(fweight)
    #---Calculate the expected return value of the random portfolio.
    for i in range(len(F_names)):
        preturn += fweight[i] * fmeans[i]
    #---Calculate variance, use it for the deviation.
    pvariance = np.dot(np.dot(fweight.transpose(), pcovariance),fweight)
    pstdev = np.sqrt(pvariance)
    #---To optimise the efficient frontier graph, check if the data point
    #---is clumped together with where most of them fall or not, as we want
    #---data points on the outer edge and not below the frontier. If it 
    #---does, skip it and keep generating until we get one on the outside.
    #---One downfall is that it slows down the more points are generated
    #---as less and less points make it through the check,
    #---different optimisation methods could then be looked at
    #---if the number of portfolios wanted is very large.
    pair.append([preturn, pstdev])
    for R,V in pair:
        if (R > preturn) and (V < pstdev):
            check = True
            break
    if check:
        continue
    #---Store the risk, returns and weights as percentages.
    pstdevs.append(pstdev)
    preturns.append(preturn)
    fweights.append([i * 100 for i in fweight])
#---Store the data into a csv file. Big downfall is that I store a lot of
#---portfolios that are not necessarily on the frontier, further steps 
#---would be to fit a curve to the frontier and remove any points that are
#---too far away from it. This is mainly due to the 'burn' in period where 
#---points are first generated wherever to then allow optimisation.
ourdata = pd.DataFrame(fweights)
ourdata.columns = F_names
ourdata.to_csv('Weights.csv')
#---Below here is code to store the returns and risks and weights into csv.
ourdata.insert(0, "Return %", preturns, True)
ourdata.insert(1, "Risk %", pstdevs, True)
ourdata.to_csv('Efficient_Frontier_Data.csv')
#---Plot data
plt.scatter(pstdevs, preturns, c='black', marker='.', linewidths='.1')
plt.xlabel('Risk (%)')
plt.ylabel('Returns (%)')
#---Admittedly a lot of optimisation could be done, there is a lot of
#---Converting between different variable types involved that potentially could 
#---be avoided with a little more work. Nevertheless, very interesting
#---assignment with a lot of different approaches!!