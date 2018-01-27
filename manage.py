import praw
import re
from stocks import Stocks
import os
import csv
import time
def parseForTagCommand(comment_body): #parses comments for stock tickers preceded by a ! ex: !BKS
	tags = re.findall(r'(?<=\s!)[A-Z]{1,5}(?=[\s\W])', comment_body) #regular expression for finding stock and ignoring false data
	tags_chunked = comment_body.split() #Regex can't find first string and last string because they do not have whitespace or characters on both sides.
	first = ""
	last = ""
	if(tags_chunked): #Checks the first and last "Word" in the comment, if they exist
		last = tags_chunked.pop()
		if(last[0] == '!' and last.isupper() and (len(last) < 6 and len(last) >0) and last[1:].isalpha()):
			tags.append(last[1:])
		if(tags_chunked):
			first = tags_chunked.pop(0)
			if(first[0] == '!' and first.isupper() and (len(first) < 6 and len(first) >0) and first[1:].isalpha()):
				tags.append(first[1:])
	return tags

while(True):
	reddit = praw.Reddit('bot1')#sets the bot
	r_all = reddit.subreddit("all")#sets the all subreddit, if it is used
	r_wallstreetbets = reddit.subreddit("wallstreetbets")#sets the specific subreddit

	#Creates an alpha reference sheet if none exist
	#(Alphabetizes the search query for speed)
	#This can be done manually by running rebuild.py
	char = "A"
	if not os.path.isfile("alpha_locale.txt"): #check if the file is here
		with open("alpha_locale.txt", "w+") as alpha: 
			alpha.write(char + " " + '0' + "\n") #We know the csv starts with A
			with open("nasdaq.csv", "r") as stockfile: #open csv
				reader = csv.reader(stockfile) #initialize reader
				for value, row in enumerate(reader, 1): #iterate
					if(row[0]):
						if(row[0][0] != char): #grab first char compare it
							char = row[0][0]
							alpha.write(char + " " + str(value) + "\n") #Take note of character locale

	#if this file
	# does not exist in the directory, open it.
	# this file will hold alphabetic locations for characters in the csv
	# for quick location when searching


	#Logs comments already replied to
	if not os.path.isfile("comments_replied_to.txt"):
		comments_replied_to = [] #first time running bot
	else: 
		with open("comments_replied_to.txt", "r") as c_file:
			comments_replied_to = c_file.read() #read the comments that have been already replied to
			comments_replied_to = comments_replied_to.split("\n")
			comments_replied_to = list(filter(None, comments_replied_to))
	comment_reply_skeleton = "-----------------------\n\n{name} ({tag}): \n\nCurrent Price: {cp}\n\nYear to Date: {ytd}\n\n-----------------------"
	# testComment = praw.Submission(url = "https://www.reddit.com/r/testingground4bots/comments/7styra/test_submission_for_raffle_tool/" )
	for submission in r_wallstreetbets.hot(limit = 100):#Iterates through posts of chosen subreddit0
		print(submission.title)
		submission.comments.replace_more(limit=None)
		for comment in submission.comments.list(): #Check every comment on the post
				if comment.id not in comments_replied_to: #If we haven't replied to this comment
					# if str(comment).isupper(): #Ignore comments in all caps.
					# 	pass
					#This code can be used if automated replies are activated
					#Automated replies means the program automatically replies
					#to all stock tickers, with or without a ! preceding them
					currentTags = list(set(parseForTagCommand(comment.body)))#find tags and remove duplicate tags in comment
					stockObjects = []
					for tag in currentTags:
						stock = Stocks(tag)
						if stock.name: #Stock only exists if it has a name
							stockObjects.append(stock)
					reply = ""#allows for the postage of several stocks on one comment
					for st in stockObjects:
						#REPLY TO COMMENT
						reply += comment_reply_skeleton.format(
							tag = st.tag,
							name = st.name,
							cp = st.price,
							# headline = st.headline,
							# op = st.open,
							# cl = st.close,
							# yh = st.year_high,
							# yl = st.year_low,
							# url = st.headline_hyper,
							ytd = st.year_change)+"\n\n"
					if(len(reply)>0):#if there are stock objects, and reply exists
						my_reply = comment.reply(reply + "^(I am a bot, and this action was performed automatically.)")
						comments_replied_to.append(my_reply.id)#Ensure that the program does not reply to itself
						print("Replying to... " + comment.body)#Command prompt
						comments_replied_to.append(comment.id)
	with open("comments_replied_to.txt", "w") as c_file:
		for comment_id in comments_replied_to:
			c_file.write(comment_id + "\n")#Log comments replied to
	time.sleep(600)