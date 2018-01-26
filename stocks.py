
import csv
import itertools
from iexfinance import Share

URL = "https://www.google.com/search?q={ticker}&pws=0&gl=us&gws_rd=cr"
#ignore = [] #Ticker Confusions that should simply be ignored. #Automated feature
class Stocks():

	def __init__(self, stockTag):
		self.tag = stockTag
		self.name = None
		self.current = None
		self.generateName()
		if(self.name):#Only search for stock data if stock can be found
			self.scrape()



	def generateName(self):
		with open("alpha_locale.txt", "r") as alpha_locale:
			print(self.tag)
			row = alpha_locale.read().split(self.tag[0])[1].split("\n")[0].strip()
			#split the data in half at the character point
			#segment the data by newlines to separate the desired digit from the rest
			#of the text. Then, take the first item, the desired digit, and trim
			#the whitespace.
			if(row == '0'):
				row = '1' #Fixes 0-1 problem in itertools.
			with open("nasdaq.csv", "r") as stockfile:	
				for row in itertools.islice(stockfile, int(row)-1, 5359): #start at the row specified and continue until the end.
					row = row.split(",")
					if(self.tag == row[0]):# (automated version extension) --> and (self.tag not in ignore)): #if entry exists in nasdaq file, success
						self.name = row[1].replace('"', "") #trailing quotes
	
	def __eq__(self, other): #allows for the removal of duplicates
		return (self.name == other.name) and (other.tag == self.tag)

	def scrape(self):
		share = Share(self.tag) #create an iexfinance object using ticker for data extraction
		self.price = "%.2f" % float(share.get_price())
		#EXTRA INFORMATION IF DESIRED
		# self.headline = share.get_news()[0]['headline']
		# self.headline_hyper = share.get_news()[0]['url']
		# self.open = "%.2f" % float(share.get_open())
		# self.close = "%.2f" % float(share.get_close())
		# self.year_high = "%.2f" % float(share.get_years_high())
		# self.year_low = "%.2f" % float(share.get_years_low())
		self.year_change = ("%.2f" % (float(share.get_ytd_change())*100)) + " percent change."
	
	def rundown(self): #Mainly for testing purposes, to ensure data retrieval.
		print(self.price)
		#EXTRA DATA. UNCOMMENT TO USE.
		# print(self.headline)
		# print(self.open)
		# print(self.close)
		# print(self.year_high)
		# print(self.year_low)
		print(self.year_change)