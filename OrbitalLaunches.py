import requests
from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup
import pytz


# function to check if any of the payloads are one of status Operational, Successful or En Route
def isOneOfTheCategories(list):
	validOutcome = ['Operational','Successful','En Route']
	for l in list:
		tds = l.find_all("td")
		name = tds[-1].text.strip()
		if(name.startswith('Operational') or name.startswith('Successful') or name.startswith('En Route')):
			return True
	return False

# get webpage
result = requests.get("https://en.wikipedia.org/wiki/2019_in_spaceflight#Orbital_launches")

src = result.content

soup = BeautifulSoup(src,'lxml')
tables = soup.find_all("table")
Orbital_launches = tables[3]
trs = Orbital_launches.find_all("tr")

data = {}


i = 0
offset = 0

# recoring data locally to count number of launches getting from each table row feom webpage
while  i < len(trs):
	if( trs[i].find("td") is not None and (trs[i].find("td").has_attr("rowspan"))):
		if(trs[i].find("td").has_attr("rowspan")):
			offset = int(trs[i].find("td")['rowspan'])
			if(isOneOfTheCategories(trs[i+1:i+offset])):
				mydate = datetime.strptime(trs[i].find("td").find("span").text.strip()+" 2019", "%d %B %Y")
				
				if(str(mydate) in data):
					data[str(mydate)] = data[str(mydate)] + 1
				else:
					data[str(mydate)] = 1

			i = i + offset 
	else:
		offset = 0
		i = i + 1


start_date = datetime(year=2019, month=1, day=1)
end_date = datetime(year=2019, month=12, day=31)
delta = timedelta(days=1)

timezone = pytz.timezone('UTC')

f = open("output.csv", "w")

# looping through the all dates in 2019 and writing to csv file
while start_date <= end_date:
	if(str(start_date) in data):
		f.write(str(timezone.localize(start_date).isoformat())+", "+str(data[str(start_date)]))
		f.write("\n")
	else:
		f.write(str(timezone.localize(start_date).isoformat())+", 0")
		f.write("\n")
	start_date += delta

f.close()