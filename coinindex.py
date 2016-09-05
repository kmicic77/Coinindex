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
		
		print ("{:>5}. {:>23}  {:>12} USD  Market Cap: {:>15,} USD".format(data[i]['rank'],data[i]['name'],data[i]['price_usd'],float(data[i]['market_cap_usd'])))

	
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
			item['name'],item['price_usd'],float(item['market_cap_usd'])))

		money=float(input("\nHow much money would you like to invest (in USD) ? "))
		total_market_cap=0

		for item in new_list:
			total_market_cap+=float(item['market_cap_usd'])
		
		for item in new_list:
			item['proportion']=float(item['market_cap_usd'])/total_market_cap
			item['worth_in_usd']=item['proportion']*money
			item['units']=item['worth_in_usd']/float(item['price_usd'])
			item['in_btc']=item['worth_in_usd']/float(data[0]['price_usd']) #bitcoin price in USD
			
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
	ws['H4']="Units"
	ws['I4']="How much I have now"
	ws['J4']="How much to buy"
	ws['K4']="Balance"

	ws.column_dimensions['C'].width = 15
	ws.column_dimensions['D'].width = 20
	ws.column_dimensions['E'].width = 12
	ws.column_dimensions['F'].width = 20
	ws.column_dimensions['G'].width = 20
	ws.column_dimensions['H'].width = 12
	ws.column_dimensions['I'].width = 20
	ws.column_dimensions['J'].width = 20
	ws.column_dimensions['K'].width = 12

	# filling worsheet with names and values
	#formula_1 calculates how much to buy (target minus how much I have now)
	#formula_2 calculates balance - how many percent actual holdings differ from target
	
	for i in range(len(data)):
		y=str(ws.cell(row=i+5,column=8).column)
		x=str(ws.cell(row=i+5,column=8).row)
		h5=y+x
		y1=str(ws.cell(row=i+5,column=9).column)
		x1=str(ws.cell(row=i+5,column=9).row)
		i5=y1+x1
		formula_1='='+h5+'-'+i5
		formula_2='='+h5+"/"+i5+"-1"


		ws.cell(row=(i+5),column=3,value=data[i]['name'])
		ws.cell(row=(i+5),column=4,value=float(data[i]['market_cap_usd']))
		ws.cell(row=(i+5),column=4).number_format='#,##0'
		ws.cell(row=(i+5),column=5,value=data[i]['proportion'])
		ws.cell(row=(i+5),column=5).number_format='0.00%'
		ws.cell(row=(i+5),column=6,value=data[i]['worth_in_usd'])
		ws.cell(row=(i+5),column=6).number_format='0.00'
		ws.cell(row=(i+5),column=7,value=float(data[i]['price_usd']))
		ws.cell(row=(i+5),column=7).number_format='0.00'
		ws.cell(row=(i+5),column=8,value=data[i]['units'])
		ws.cell(row=(i+5),column=8).number_format='0.000'
		ws.cell(row=(i+5),column=9,value=0)
		ws.cell(row=(i+5),column=9).number_format='0.000'
		ws.cell(row=(i+5),column=10,value=formula_1)
		ws.cell(row=(i+5),column=10).number_format='0.000'
		ws.cell(row=(i+5),column=11,value=formula_2)
		ws.cell(row=(i+5),column=11).number_format='0.00%'

	#formula_3 calculates total market cap

	formula_3='=SUM(D5:D'+str(len(data)+4)
	ws.cell(row=len(data)+7,column=3,value='Total:')
	ws.cell(row=len(data)+7,column=4,value=formula_3)
	ws.cell(row=len(data)+7,column=4).number_format='#,##0'

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


