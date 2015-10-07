import requests
import bs4
import time
import sys
import re

def getUrl():
	mainUrl = 'http://www.cbssports.com/nba/scoreboard'
	#mainUrl = 'http://www.cbssports.com/nba/scoreboard/20141104'
	res = requests.get(mainUrl)
	soup = bs4.BeautifulSoup(res.text, 'html.parser')
	return soup

def getAwayTeam(bSoup):
	elem = bSoup.select('tr.teamInfo.awayTeam > td.teamName > div > a')
	return elem	

def getHomeTeam(bSoup):
	elem = bSoup.select('tr.teamInfo.homeTeam > td.teamName > div > a')
	return elem

def getScores(bSoup):
	for scores in bSoup.find_all("td" , {"class" : "finalScore"}):
		print scores.next
	
	

def getGameTime(bSoup):
	elem = bSoup.select('tr.gameInfo > td > span > span')
	return elem

def getNumScorebox(bSoup):
	elem = bSoup.findAll( attrs={"class" : "nbaBoxScore"} )
	scoreBox = [None]*len(elem)*2
	i = 0
	for box in elem:
		value = box.findAll( attrs={"class" : "finalScore"})
		if len(value) == 0:		#game has not starter yet
			scoreBox[i] = 0
			scoreBox[i+1] = 0
		else:
			scoreBox[i] = value[0].text
			scoreBox[i+1] = value[1].text
		i = i+2

	return scoreBox

#Start of main program driver

parsedHtml = getUrl()

#Getting names of the various nba teams
awayTeam = getAwayTeam(parsedHtml)
homeTeam = getHomeTeam(parsedHtml)

gameTime = getGameTime(parsedHtml)
scores = getNumScorebox(parsedHtml)

#Getting scores of the current date's games
#getScores(parsedHtml)


while True:
	#delay between score updates 
	sys.stdout.write('Updating')
	for i in range(0,5):
		time.sleep(1)
		sys.stdout.write('.')
		sys.stdout.flush()
		
	sys.stderr.write("\x1b[2J\x1b[H")

	#clears the terminal page with ANSI escape characters
	
	for i in range(len(awayTeam)):
		num = str(i+1)
		if i == 0:
			print '--------------'

		if len(scores) != 0:
			print 'Game ' + num + ': '
			print awayTeam[i].text + ': ' + str(scores[i*2])
			print homeTeam[i].text + ': ' + str(scores[(i*2)+1])
			print '--------------'
		else:
			print 'Game ' + num + ': '
			print awayTeam[i].text + ': '
			print homeTeam[i].text + ': '
			print 'Game starts at: ' + gameTime[i].text
			print '--------------'			 

	
