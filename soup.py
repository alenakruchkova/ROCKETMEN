# from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup
import urllib

########################

r = urllib.urlopen('https://en.wikipedia.org/wiki/List_of_astronauts_by_first_flight').read()
soup = BeautifulSoup(r)

info = soup.find_all("tr")

my_info = info[1:552]

print my_info[0]
# astronaut_information = {}
# for element in info:
# 	astronaut_information[element.a.get_text()]={}
