import requests
import bs4
import time
import sys

def getUrl():
	mainUrl = 'http://www.cbssports.com/nba/scoreboard'
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
	elem = bSoup.select('td.finalScore')
	return elem


#Start of main program driver

parsedHtml = getUrl()

#Getting names of the various nba teams
awayTeam = getAwayTeam(parsedHtml)
homeTeam = getHomeTeam(parsedHtml)

#Getting scores of the current date's games
scores = getScores(parsedHtml)

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

		print 'Game ' + num + ': '
		print awayTeam[i].text + ': ' + scores[i*2].text
		print homeTeam[i].text + ': ' + scores[(i*2)+1].text
		print '--------------' 

