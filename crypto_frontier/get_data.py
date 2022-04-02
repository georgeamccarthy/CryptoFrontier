import efficient_frontier

coin_codes = efficient_frontier.get_coin_codes()

year = 2019
df = efficient_frontier.download_data(coin_codes, start_time=f'{year}-01-01-00-00')
df.reset_index(drop=True).to_csv(f"crypto_frontier/data/coin_data_{year}.csv", index=False)