import efficient_frontier
import streamlit as st
import matplotlib.pyplot as plt

st.title("CryptoFrontier")

st.text("Coins: BTC, ADA, ETH")

n_portfolios = st.slider('Choose number of generated portfolios', 20, 500)
coin_codes = ["ADA", "BTC", "ETH"]
df = efficient_frontier.download_data(coin_codes)
df, risk, returns = efficient_frontier.efficient_frontier(df, n_portfolios)

fig, ax = plt.subplots()
ax.scatter(risk, returns)
ax.set_xlabel("Risk (%)")
ax.set_ylabel("Returns (%)")

st.pyplot(fig)