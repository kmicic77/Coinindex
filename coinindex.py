""" Choose your portfolio of cryptocurrencies """
""" Program calculates how many units you should buy """
""" to have coins proportional to their market cap """
""" which is similar to Index investing """

import os, json, urllib.request
from openpyxl import Workbook


def display_menu():
	print("\n\n\n   1. Display top cryptocurrencies")
	print("   2. Choose your portfolio")
	print("   3. Exit")
def display_top(data):
	for i in range(30):
		print ("{:>5}. {:>23}  {:>12} USD  Market Cap: {:>15,} USD".format(data[i]['rank'],data[i]['name'],
		data[i]['price_usd'],data[i]['market_cap_usd']))
	
	
def choose_portfolio(data):
	while True:
		new_list=[]
		display_top(data)
		
		choice=input("\n  Choose your coins, by typing numbers separated by commas, for example: 1,4,7,12  : ")
		choice_list=choice.split(',')
		choice_list=sorted([int(i) for i in choice_list])
		
		for item in choice_list:
			new_list.append(data[item-1])
		
		print ("\nYour portfolio:\n")
		
		for item in new_list:
			print ("{:>5}. {:>23}  {:>12} USD  Market Cap: {:>15,} USD".format(item['rank'],
			item['name'],item['price_usd'],item['market_cap_usd']))

		money=float(input("\nHow much money would you like to invest (in USD) ? "))
		total_market_cap=0

		for item in new_list:
			total_market_cap+=item['market_cap_usd']
		
		for item in new_list:
			item['proportion']=item['market_cap_usd']/total_market_cap
			item['worth_in_usd']=item['proportion']*money
			item['units']=item['worth_in_usd']/item['price_usd']
			item['in_btc']=item['worth_in_usd']/data[0]['price_usd'] #bitcoin price in USD
			
		print ("\nTo have your investment proportional to crypto market cap your portfolio should look like this: \n")
		
		for item in new_list:
			print ("{:>5}. {:>23}  {:>10.3f} units {:>12.2f} in USD {:>10.4f} in BTC".format(item['rank'],
			item['name'],item['units'],item['worth_in_usd'],item['in_btc']))

		print("\n  1. Save portfolio to text file")
		print("  2. Create .xls file")
		print("  3. Choose different coins")
		print("  4. Exit")
		
		option=input("\nChoose option: ")
		
		if option=='1' : 
			save_to_text_file(new_list)
			break
		if option=='2' : 
			create_xls(new_list)
			break
		if option=='3' : continue
		if option=='4' : break
	
def save_to_text_file(data):
	file_name=input('Save portfolio as...: ')
	with open(file_name,'w') as f:
		for item in data:
			f.write("{}. {},  {:.3f} units, {:.2f} in USD, {:.4f} in BTC\n".format(item['rank'],
			item['name'],item['units'],item['worth_in_usd'],item['in_btc']))
	print ("File {} succesfully saved\n".format(file_name))
	input("Press ENTER to continue")

	pass
def create_xls(data):
	wb=Workbook()
	ws=wb.active

	ws['D4']="Market Cap"
	ws['E4']="Percentage"
	ws['F4']="How much to invest"
	ws['G4']="Unit price (USD)"
	ws['H4']="Target"
	ws['I4']="How much I have now"
	ws['J4']="How much to buy"
	ws['K4']="Balance"

	file_name=input('Save portfolio as...(program will use Excel extension .xlsx) : ')
	file_name+=".xlsx"
	wb.save(file_name)
	print ("File {} succesfully saved\n".format(file_name))
	input("Press ENTER to continue")
	
	
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
	if option=='1':
		display_top(data)
		input("Press ENTER to continue")
	if option=='2': choose_portfolio(data)
print("\nThank you for using my program! To the moon! ;)\n")


