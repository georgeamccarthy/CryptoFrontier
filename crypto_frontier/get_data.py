import efficient_frontier

coin_codes = efficient_frontier.get_coin_codes()

df = efficient_frontier.download_data(coin_codes, start_time='2021-01-01-00-00')
df.to_csv("coin_data.csv")