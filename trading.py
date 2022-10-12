import yfinance as yf
import pandas as pd
import numpy as np

from statsmodels.tsa.arima.model import ARIMA

import pyotp
import robin_stocks as robinhood

import telegram
import sys
import os

import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

# Robinhood email, password, and authentication code
RH_USER_EMAIL = ('TestEmail@gmail.com')
RH_PASSWORD = ('FakePassword')
RH_MFA_CODE = ('Double Verification Authorization Code')

# gets current data for a certain stock
def get_finance_data():
	google = yf.Ticker("GOOG")

	df = google.history(period='1d', interval="1m")[['Low']]
	df['date'] = pd.to_datetime(df.index).time
	df.set_index('date', inplace=True)

	return df

# used to estimate what the stock is going to do in the near future
# very simple model but could be updated with more information
# currently commented out so that I can demonstrate it working in the graph
def get_forecast():
	df = get_finance_data()


	y = df['Low'].values
	model = ARIMA(y_train, order=(5,0,1)).fit()
	forecast = model.forecast(steps=1)[0]

	return (y[len(y)-1], forecast)

# used to demonstrate that this script does get the correct data and uses a model to predict what the stock will do in the future
df = get_finance_data()
x = df.index.values
y = df['Low'].values

offset = int(0.10*len(df))

x_train = x[:-offset]
y_train = y[:-offset]
x_test = x[-offset:]
y_test = y[-offset:]

plt.plot(range(0,len(y_train)),y_train, label='Train')
plt.plot(range(len(y_train),len(y)),y_test,label='Test')
plt.legend()
plt.show()


# used to buy stocks from robinhood using the robin_stocks API
def trade_robinhood():
	timed_otp = pyotp.TOTP(RH_MFA_CODE).now()
	login = rh.login(RH_USER_EMAIL, RH_PASSWORD, mfa_code=timed_otp)

	last_real_data, forecast = get_forecast()
 
	#Here is where you would input logic deciding whether to buy, sell, or hold and how many shares to purchase or sell
	action = 'BUY'
	shares = 1

	if action == 'BUY':
		rh.order_buy_market('GOOG', shares)
		return f'Bought {shares} shares.'
	elif action == 'SELL':
		rh.order_sell_market('GOOG', shares)
		return f'Sold {shares} shares.'
	else:
		return f'No shares were bought nor sold.'
