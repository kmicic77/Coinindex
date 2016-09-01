""" Choose your portfolio of cryptocurrencies """
""" Program calculates how many units you should buy """
""" to have coins proportional to their market cap """
""" which is similar to Index investing """

import os, json, urllib.request


def display_menu():
	print("\n\n\n   1. Display top cryptocurrencies")
	print("   2. Choose your portfolio")
	print("   3. Exit")
def display_top():
	url="https://api.coinmarketcap.com/v1/ticker/"
	response = urllib.request.urlopen(url).read()
	data = json.loads(response.decode('utf-8'))
	for i in range(30):
		print ("{:>5}. {:>23}  {:>12} USD  Market Cap: {:>15,} USD".format(data[i]['rank'],data[i]['name'],data[i]['price_usd'],data[i]['market_cap_usd']))
	input("Press ENTER to continue")
	pass
def choose_portfolio():
	pass
	
while True:
	os.system('cls')
	display_menu()
	
	option=input("\nChoose option: ")
	if option=='3': break
	if option=='1': display_top()
	if option=='2': choose_portfolio()
print("\nThank you for using my program! To the moon! ;)\n")


