
import requests
from bs4 import BeautifulSoup

r = requests.get('http://www.charismamag.com/')

data = r.text
soup = BeautifulSoup(data)

for item in soup.find_all('article', class_="article"):
  
  #print item
  print '---IMAGE: ', item.find('figure', class_='featuredArticleImage')
  print '---TITLE: ', item.find('h1')
  print '---DESC: ', item.find('div', class_='contentBody')
  print '---TIME: ', item.find('time')
  #print '---SHARE COUNT ', soup.select('.socialSharing_Featured .stBubble_hcount')

  print '\n'