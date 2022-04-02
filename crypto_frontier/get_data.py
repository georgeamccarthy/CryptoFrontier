import efficient_frontier

coin_codes = efficient_frontier.get_coin_codes()[:2]

df = efficient_frontier.download_data(coin_codes, start_time='2010-01-01-00-00')
df.reset_index(drop=True).to_csv("crypto_frontier/data/coin_data_2015.csv", index=False)