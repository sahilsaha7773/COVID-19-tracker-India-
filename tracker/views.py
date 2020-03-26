from django.shortcuts import render
from bs4 import BeautifulSoup 
from tabulate import tabulate 
import numpy as np 
import requests

# Create your views here.
def home(request):
	extract_contents = lambda row: [x.text.replace('\n', '') for x in row] 
	URL = 'https://www.mohfw.gov.in/'

	SHORT_HEADERS = ['SNo', 'State','Indian-Confirmed', 'Foreign-Confirmed','Cured','Death'] 

	response = requests.get(URL).content 
	soup = BeautifulSoup(response, 'html.parser') 
	header = extract_contents(soup.tr.find_all('th')) 
	mydivs = soup.find_all("div", {"class": "iblock_text"})
	count = []
	label = []
	for divs in mydivs:
		count.append(extract_contents(divs.find_all('span')))
		label.append(extract_contents(divs.find_all('div')))
	passatair = count[0][0]
	totcases = int(count[1][0])+int(count[2][0])+int(count[3][0])+int(count[4][0])
	active = count[1][0]
	cured = count[2][0]
	deaths = count[3][0]
	mig = count[4][0]
	newDiv = soup.find_all("div", {"class": "content newtab"})
	stats = [] 
	all_rows=[]

	for i in newDiv:
		all_rows.append(i.find_all('tr'))
	d = []
	for j in all_rows:
		for k in j:
			d.append(extract_contents(k.find_all('td')))


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
	return render(request, 'home.html', {'passatair':passatair,'totcases':totcases, 'active':active, 'cured':cured,'deaths':deaths,'mig':mig, 'rows':d})


