import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random as rand

def zero_to_nan(values):
    return [float('nan') if x==0 else x for x in values]

def read_dataframe(file_name):
	dataframe = pd.read_csv(file_name)
	return dataframe

def dataframe_statistics(dataframe):
	print(dataframe.describe())

def make_transaction(account, price, quantity, buy):
	balance = account["Balance"]
	qty = account["Quantity"]
	if buy:
			if balance >= price*10:
				print("You bought 10 shares since the stock price was favorable.")
				account["Quantity"] += 10
				account["Balance"] -= price*10
	else:
		if qty >=10:
			print("You sold 10 shares since the stock price was favorable.")
			account["Quantity"] -= 10
			account["Balance"] += price*10
		else:
			print("You sold {} shares since the stock price was favorable.".format(qty))
			account["Quantity"] -= qty
			account["Balance"] += price*qty

def get_sma(dataframe):
	count = dataframe.Open.count()
	days = 10
	dataframe_list = [0] * count

	for i in range(count):
		dataframe_list[i] = sum(dataframe['Open'].iloc[i-days:i]) / days
	return dataframe_list

def trade(dataframe, sma, account):
	bookkeeping = []
	print("Initial Account Details: {}\n".format(account))

	for i in range(len(sma)):
		curr_price = dataframe['Open'].iloc[i]
		curr_sma = sma[i]

		if curr_price < 0.95*curr_sma:
			make_transaction(account,curr_price,10, True)
			bookkeeping.append(1)
			print("Account Details: {}\n".format(account))
		elif curr_price > 1.05*curr_sma and curr_sma != 0.0:
			make_transaction(account,curr_price,10, False)
			bookkeeping.append(-1)
			print("Account Details: {}\n".format(account))
		else:
			bookkeeping.append(0)
	
	return bookkeeping

def make_plot(dataframe,sma,sell,buy):
	cp_list = []
	cs_list = []

	dataframe['Date'] = pd.to_datetime(dataframe.Date)

	plt.figure(figsize=(24,5))
	plt.title('COST Stock 1 Year Price and SMA')

	for i in range(len(sma)):
		curr_price = dataframe['Open'].iloc[i]
		curr_sma = sma[i]
		cp_list.append(curr_price)
		cs_list.append(curr_sma)

		if sell[i] == 1:
			plt.plot(dataframe['Date'][i], curr_price, 'bo', color = 'red', markersize = 8)

		if buy[i] == 1:
			plt.plot(dataframe['Date'][i], curr_price, 'bo', color = 'green', markersize = 8)
    
	plt.plot(dataframe['Date'],cp_list, color='blue', linewidth=2.0, label='Price') 
	plt.plot(dataframe['Date'],cs_list, color='magenta', linewidth=2.0, label='SMA')     
	plt.legend()                                  
	plt.show()

def main():
	#Account Details
	account = {"Balance":rand.randint(1000,100000),"Quantity":0}
	file_name = input("File name here: ")
	#Stores files info.
	dataframe = read_dataframe(file_name)

	#Prints Statistics
	dataframe_statistics(dataframe)

	#Gets sma10
	sma10 = get_sma(dataframe)
	sma10 = zero_to_nan(sma10)

	#Gets bookkeeping list
	bookkeeping = trade(dataframe,sma10,account)

	#Prints records of buys and sells
	print("Buys and Sells (0 = none, 1 = buy, -1 = sell): \n {}\n".format(bookkeeping))
	buy = []
	sell = []

	for i in range(len(bookkeeping)):
		if bookkeeping[i]==1:
			buy.append(1)
			sell.append(0)
		elif bookkeeping[i]==-1:
			buy.append(0)
			sell.append(1)
		else:
			buy.append(0)
			sell.append(0)

	#Makes plot
	make_plot(dataframe,sma10,sell,buy)


main()	