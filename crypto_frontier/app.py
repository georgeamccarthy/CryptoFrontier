import efficient_frontier
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.title("CryptoFrontier")

all_coin_codes = efficient_frontier.get_coin_codes()
#coin_codes = coin_codes[:10]

selected_coins = st.multiselect(label="Enter coin codes: (e.g. ADA, BTC, ETH...)", options=all_coin_codes)

buttons = {}

for coin_code in selected_coins:
    buttons[coin_code] = st.number_input(coin_code, 0, 100, key=coin_code)

n_portfolios = st.slider('Choose number of generated portfolios', 20, 500, value=200)

if st.button("Submit"):
    selected_coins = list(buttons.keys())
    coin_percentages = list(buttons.values())

    df = pd.read_csv("./data/coin_data.csv")[selected_coins]
    users_risk, users_return = efficient_frontier.users_point(df, coin_percentages)
    df, risk, returns = efficient_frontier.efficient_frontier(df, n_portfolios)

    fig, ax = plt.subplots()
    ax.scatter(risk, returns)
    ax.scatter(users_risk, users_return)
    ax.set_xlabel("Risk (%)")
    ax.set_ylabel("Returns (%)")

    st.pyplot(fig)