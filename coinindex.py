""" Choose your portfolio of cryptocurrencies """
""" Program calculates how many units you should buy """
""" to have coins proportional to their market cap """
""" which is similar to Index investing """

import os, json, urllib.request


def display_menu():
	print("\n\n\n   1. Display top cryptocurrencies")
	print("   2. Choose your portfolio")
	print("   3. Exit")
def display_top(data):
	for i in range(30):
		print ("{:>5}. {:>23}  {:>12} USD  Market Cap: {:>15,} USD".format(data[i]['rank'],data[i]['name'],data[i]['price_usd'],data[i]['market_cap_usd']))
	input("Press ENTER to continue")
	
def choose_portfolio(data):
	new_list=[]
	display_top(data)
	choice=input("\n  Choose your coins, by typing numbers separated by commas, for example: 1,4,7,12  :")
	choice_list=choice.split(',')
	choice_list=sorted([int(i) for i in choice_list])
	
	for item in choice_list:
		new_list.append(data[item-1])
	print ("Your portfolio:\n")
	for item in new_list:
		print ("{:>5}. {:>23}  {:>12} USD  Market Cap: {:>15,} USD".format(item['rank'],item['name'],item['price_usd'],item['market_cap_usd']))
	
	input("Press ENTER to continue")
	pass
def load_json():
	url="https://api.coinmarketcap.com/v1/ticker/"
	response = urllib.request.urlopen(url).read()
	data = json.loads(response.decode('utf-8'))
	return data

os.system('cls')	
print ("\n\n  Reading data from coinmarketcap.com...")
data=load_json()	
while True:
	os.system('cls')
	display_menu()
	
	option=input("\nChoose option: ")
	if option=='3': break
	if option=='1': display_top(data)
	if option=='2': choose_portfolio(data)
print("\nThank you for using my program! To the moon! ;)\n")


