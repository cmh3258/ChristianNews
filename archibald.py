
import requests
from bs4 import BeautifulSoup

r = requests.get('http://www.thearchibaldproject.com/blog/')

data = r.text
soup = BeautifulSoup(data)

for item in soup.find_all('div', class_="grid-item"):
  
  #print item
  print '---IMAGE: ', item.find('img', class_='grid-img')
  print '---TITLE: ', item.find('h3')
  print '---DESC: ', item.find('p', class_='text')
  print '---Link: ', item.find('span', class_='read-more-wrap')
  #print '---TIME: ', item.find('time')
  #print '---SHARE COUNT ', soup.select('.socialSharing_Featured .stBubble_hcount')

  print '\n'