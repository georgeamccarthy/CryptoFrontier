from Historic_Crypto import HistoricalData
from Historic_Crypto import Cryptocurrencies
import pandas as pd

#---Get a list of the user's crypto
    
user_crypto = ['ADA-USD', 'XLM-USD', 'ETH-USD']
array = []
for i in user_crypto:
    crypto_data = HistoricalData(i,86400,'2021-01-01-00-00').retrieve_data()
    crypto_data = crypto_data[['close']]
    crypto_data = crypto_data.rename(columns={'close': '{}'.format(i)})
    array.append(crypto_data)

combined = pd.concat(array, axis=1)

df= combined.pct_change(periods=1)*100

