from django.shortcuts import render
from bs4 import BeautifulSoup 
from tabulate import tabulate 
import numpy as np 
import requests
from newsapi import NewsApiClient

# Create your views here.
def home(request):
	extract_contents = lambda row: [x.text.replace('\n', '') for x in row] 
	URL = 'https://www.mohfw.gov.in/'

	URL2 = 'https://www.worldometers.info/coronavirus/country/india/'
	SHORT_HEADERS = ['SNo', 'State','Indian-Confirmed','Foreign-Confirmed','Cured','Death'] 

	response = requests.get(URL).content 
	responsew = requests.get(URL2).content
	soup2 = BeautifulSoup(responsew, 'html.parser')
	counts = extract_contents(soup2.find_all("div", {"class":"maincounter-number"})) 

	response = requests.get(URL).content 
	soup = BeautifulSoup(response, 'html.parser') 
	header = extract_contents(soup.tr.find_all('th')) 
	mydivs = soup.find_all("div", {"class": "iblock_text"})
	count = []
	label = []
	for divs in mydivs:
		count.append(extract_contents(divs.find_all('span')))
		label.append(extract_contents(divs.find_all('div')))
	# totcases = int(int(count[1][0].replace(',',''))+int(count[2][0].replace(',',''))+int(count[3][0].replace(',',''))+int(count[4][0].replace(',','')))
	# active = int(count[1][0].replace(',',''))
	# cured = int(count[2][0].replace(',',''))
	# deaths = int(count[3][0].replace(',',''))
	totcases = int(int(counts[0].replace(',','')))
	cured = int(int(counts[2].replace(',','')))
	deaths = int(int(counts[1].replace(',','')))
	active = totcases-cured-deaths
	newDiv = soup.find_all("section", {"id": "state-data"})
	stats = [] 
	all_rows=[]

	for i in newDiv:
		all_rows.append(i.find_all('tr'))
	d = []
	for j in all_rows:
		for k in j:
			d.append(extract_contents(k.find_all('td')))

	newsapi = NewsApiClient(api_key='911a1ed9108a43dfafa3d04ab581f009')

	# /v2/top-headlines
	top_headlines_json = newsapi.get_top_headlines(q='coronavirus india',
	                                          language='en',
	                                          country='in')
	top_headlines = top_headlines_json["articles"]
	URL3 = 'https://www.worldometers.info/coronavirus/'
	responsen = requests.get(URL3).content
	soup3 = BeautifulSoup(responsen, 'html.parser')
	newc = (soup3.find_all("table",{"class":"main_table_countries"}))
	nrows = []
	for r in newc:
		nrows.append(extract_contents(r.find_all("td")))
	nrows = nrows[0]
	ind = nrows.index('India')
	newcases = nrows[ind+2]
	newdeaths = nrows[ind+4]
	seriouscases = nrows[ind+7]
	if newcases=='':
		newcases=0
	if newdeaths=='':
		newdeaths=0
	if seriouscases=='':
		seriouscases=0
	# for row in all_rows: 
	# 	stat = extract_contents(row.find_all('td')) 
	# 	if stat: 
	# 		if len(stat) == 5: 
	# 			# last row 
	# 			stat = ['', *stat] 
	# 			stats.append(stat) 
	# 		elif len(stat) == 6: 
	# 			stats.append(stat) 

	# stats[-1][1] = "Total Cases"

	# stats.remove(stats[-1]) 
	# objects = [] 
	# for row in stats : 
	# 	objects.append(row[1]) 

	# y_pos = np.arange(len(objects)) 

	# performance = [] 
	# for row in stats : 
	# 	performance.append(int(row[2]) + int(row[3])) 

	# table = tabulate(stats, headers=SHORT_HEADERS) 	
	return render(request, 'home.html', {'totcases':totcases, 'active':active, 'cured':cured,'deaths':deaths, 'rows':d, 'top_headlines':top_headlines, 'newcases':newcases,'newdeaths':newdeaths,'seriouscases':seriouscases})


