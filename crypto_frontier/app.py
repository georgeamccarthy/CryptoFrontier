import efficient_frontier
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("CryptoFrontier")

all_coin_codes = efficient_frontier.get_coin_codes()
#coin_codes = coin_codes[:10]

selected_coins = st.multiselect(label="Enter coin codes:", options=all_coin_codes)

buttons = {}

for coin_code in selected_coins:
    buttons[coin_code] = st.number_input(coin_code, 0, 100, key=coin_code)

n_portfolios = st.slider('Choose number of generated portfolios', 20, 500, value=200)

if st.button("Submit"):
    selected_coins = list(buttons.keys())
    coin_percentages = list(buttons.values())

    mask = np.array(coin_percentages) > 0

    coin_codes = list(np.array(selected_coins)[mask])
    coin_percentages = list(np.array(coin_percentages)[mask])

    df = efficient_frontier.download_data(selected_coins)
    df, risk, returns = efficient_frontier.efficient_frontier(df, n_portfolios)

    fig, ax = plt.subplots()
    ax.scatter(risk, returns)
    ax.set_xlabel("Risk (%)")
    ax.set_ylabel("Returns (%)")

    st.pyplot(fig)