import efficient_frontier
import streamlit as st
import matplotlib.pyplot as plt
import requests
import numpy as np

st.title("CryptoFrontier")

url = "https://api.pro.coinbase.com/products"
headers = {"Accept": "application/json"}
response = requests.request("GET", url, headers=headers).json()
coin_codes = []
quote_currencies = []
for coin_data in response:
    if coin_data["quote_currency"] == "USD":
        coin_codes.append(coin_data["base_currency"])
coin_codes.sort()
#coin_codes = coin_codes[:10]

buttons = {}

for coin_code in coin_codes:
    buttons[coin_code] = st.number_input(coin_code, 0, 100, key=coin_code)

n_portfolios = st.slider('Choose number of generated portfolios', 20, 500, value=200)

if st.button("Submit"):
    coin_codes = list(buttons.keys())
    coin_percentages = list(buttons.values())

    mask = np.array(coin_percentages) > 0

    coin_codes = list(np.array(coin_codes)[mask])
    coin_percentages = list(np.array(coin_percentages)[mask])

    df = efficient_frontier.download_data(coin_codes)
    df, risk, returns = efficient_frontier.efficient_frontier(df, n_portfolios)

    fig, ax = plt.subplots()
    ax.scatter(risk, returns)
    ax.set_xlabel("Risk (%)")
    ax.set_ylabel("Returns (%)")

    st.pyplot(fig)