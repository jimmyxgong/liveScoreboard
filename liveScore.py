#!/usr/bin/env python

"""liveScore.py: a boxscore of NBA games that updates periodically"""

__author__ = 'Jimmy Gong (jimmyxgong@gmail.com)'
__copyright__ = 'Copyright (c) 2015 Jimmy Gong'

import requests
import bs4
import time
import sys
import re
import os

def getUrl():
	"""
	Webscrape and initiate BeautifulSoup module

	Returns:
		Returns a BeautifulSoup object 
	"""
	mainUrl = 'http://www.cbssports.com/nba/scoreboard'
	res = requests.get(mainUrl)
	soup = bs4.BeautifulSoup(res.text, 'html.parser')
	return soup

def getAwayTeam(bSoup):
	"""
	Create a list of away NBA teams

	Parameters:
		bSoup: BeautifulSoup object for webscraping

	Returns:
		returns a list of NBA away teams
	"""
	elem = bSoup.select('tr.teamInfo.awayTeam > td.teamName > div > a')
	return elem	

def getHomeTeam(bSoup):
	"""
	Create a list of home NBA teams

	Parameters:
		bSoup: BeautifulSoup object for webscraping

	Returns:
		returns a list of NBA home teams
	"""
	elem = bSoup.select('tr.teamInfo.homeTeam > td.teamName > div > a')
	return elem

def getGameTime(bSoup):
	"""
	Creates a list of the current status of an NBA game

	Parameters:
		bSoup: BeautifulSoup object for webscraping

	Returns:
		returns a list of current game status 
	"""
	elem = bSoup.findAll( attrs={"class" : "nbaBoxScore"} )
	gameTimeBox = [None]*len(elem)
	i = 0
	

	for game in elem:
		currTime = game.find( atts={"class" : "gameStatus"})
		if currTime == None:
			preGame = game.find( attrs={"class" : "gameDate"} )
			if preGame == None:
				final = game.find( attrs={"class" : "finalStatus"} )
				if final == None:
					gameTimeBox[i] = 'live'
				else:
					gameTimeBox[i] =  final.text
			else:
				gameTimeBox[i] = preGame.text
		else:
			gameTimeBox[i] = currTime.text

		i=i+1

	return gameTimeBox

def getNumScorebox(bSoup):
	"""
	Creates a list of the current NBA game scores

	Parameters:
		bSoup: BeautifulSoup object for webscraping

	Returns:
		returns a list of scores corresponding to each NBA team's current score
	"""
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

def clear():
	"""
	Clears the terminal page
	"""
	os.system('clear')

#Start of main program driver

while True:
	parsedHtml = getUrl()

	#Getting names of the various nba teams
	awayTeam = getAwayTeam(parsedHtml)
	homeTeam = getHomeTeam(parsedHtml)

	gameTime = getGameTime(parsedHtml)

	#Getting score boxes
	scores = getNumScorebox(parsedHtml)
	#delay between score updates 
	sys.stdout.write('Updating')
	for i in range(0,5):
		time.sleep(1)
		sys.stdout.write('.')
		sys.stdout.flush()

	#clears the terminal page 
	clear()
	
	#main boxscore driver
	for i in range(len(awayTeam)):
		num = str(i+1)
		if i == 0:
			print '--------------'
		print 'Game ' + num + ': '
		print awayTeam[i].text + ': ' + str(scores[i*2])
		print homeTeam[i].text + ': ' + str(scores[(i*2)+1])
		print 'Game status: ' + str(gameTime[i])
		print '--------------'
		
		
	
