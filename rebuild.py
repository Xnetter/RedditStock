with open("alpha_locale.txt", "w+") as alpha: 
	alpha.write(char + " " + '0' + "\n") #We know the csv starts with A
	with open("nasdaq.csv", "r") as stockfile: #open csv
		reader = csv.reader(stockfile) #initialize reader
		for value, row in enumerate(reader, 1): #iterate
			if(row[0]):
				if(row[0][0] != char): #grab first char compare it
					char = row[0][0]
					alpha.write(char + " " + str(value) + "\n") #Take note of character locale