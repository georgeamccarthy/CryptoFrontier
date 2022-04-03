from re import S
import efficient_frontier
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

current_dir = os.path.dirname(__file__)

st.title("CryptoFrontier")
st.markdown(
    """[![GitHub repo](https://img.shields.io/badge/GitHub-CryptoFrontier-brightgreen)](https://github.com/georgeamccarthy/CryptoFrontier) [![Stars badge](https://img.shields.io/github/stars/georgeamccarthy/CryptoFrontier?style=social)](https://github.com/georgeamccarthy/CryptoFrontier)"""
)
st.markdown("CryptoFrontier calculates the efficient frontier for the cryptocurrencies in a portfolio and suggests more efficient portfolios.")

image_path = os.path.join(current_dir, '../docs/frontier_plot.jpeg')
st.image(image_path, width=600)

st.markdown("An efficient portfolio has the best possible expected return for its risk. A portfolio on the efficient frontier has an optimal trade-off between risk and reward.")

st.header("Efficient Frontier Optimiser")

years = ["2019", "2021"]
year = st.selectbox(label="Select starting year for cryptocurrency market analysis.", options=years)
data_path = os.path.join(current_dir, f'./data/coin_data_{year}.csv')
all_coin_codes = pd.read_csv(data_path).columns

selected_coins = st.multiselect(label="Select cryptocurrencies by exchange code.", options=all_coin_codes)

buttons = {}

def total_percentage():
    return sum(list(buttons.values()))

for coin_code in selected_coins:
    buttons[coin_code] = st.number_input(coin_code, 0, 100-total_percentage(), key=coin_code)

n_portfolios = st.slider('Choose number of randomly generated portfolios.', 20, 500, value=200)

if st.button("Analyse"):
    if total_percentage() != 100:
        st.warning("Portfolio total is not 100%.")
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

st.markdown(
"""
###   Disclaimer

*The information provided on this website does not constitute investment advice, financial advice, trading advice, or any other sort of advice and you should not treat any of the website's content as such. We do not recommend that any cryptocurrency should be bought, sold, or held by you. Do conduct your own due diligence and consult your financial advisor before making any investment decisions.*
""")