import efficient_frontier
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

current_dir = os.path.dirname(__file__)
data_path = os.path.join(current_dir, './data/coin_data_2019.csv')

st.title("CryptoFrontier")
st.markdown(
"""
CryptoFrontier calculates the efficient frontier for the Cryptocurrencies in a portfolio and suggests more efficient portfolios.

*An efficient portfolio has the best possible expected return for its risk. A portfolio on the efficient frontier has an optimal trade-off between risk and reward.*
""")

years = ["2019", "2021"]
year = st.selectbox(label="Analyse Crypto exchange data since which year?", options=years)
data_path = os.path.join(current_dir, f'./data/coin_data_{year}.csv')
all_coin_codes = pd.read_csv(data_path).columns

selected_coins = st.multiselect(label="Select Cryptocurrencies (e.g. ETH, BTC, ADA etc.)", options=all_coin_codes)

buttons = {}

def total_percentage():
    return sum(list(buttons.values()))

for coin_code in selected_coins:
    buttons[coin_code] = st.number_input(coin_code, 0, 100-total_percentage(), key=coin_code)

n_portfolios = st.slider('Choose number of randomly generated portfolios.', 20, 500, value=200)

if st.button("Analyse"):
    if total_percentage() != 100:
        st.warning("Total portfolio is not 100%.")
    else:
        selected_coins = list(buttons.keys())
        coin_percentages = list(buttons.values())

        df = pd.read_csv(data_path)[selected_coins]
        users_risk, users_return = efficient_frontier.users_point(df, coin_percentages)
        df, risk, returns = efficient_frontier.efficient_frontier(df, n_portfolios)

        fig, ax = plt.subplots()
        ax.scatter(risk, returns, label="Randomly generated portfolios")
        ax.scatter(users_risk, users_return, label="Your portfolio")
        ax.legend()
        ax.set_xlabel("Daily risk (%)")
        ax.set_ylabel("Daily returns (%)")

        st.pyplot(fig)
