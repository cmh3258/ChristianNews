
import requests, time
from bs4 import BeautifulSoup
from dateutil import parser


r = requests.get('http://www.charismamag.com/')

data = r.text
soup = BeautifulSoup(data)
list_of_posts = []
for item in soup.find_all('article', class_="article"):
  
  # print item
  figure = item.find('figure', class_='featuredArticleImage')
  # print '---href: ', figure.find('a').get('href')
  # print '---img: ', figure.find('img')['data-src']

  # print '---TITLE: ', item.find('h1').get_text()
  # print '---DESC: ', item.find('div', class_='contentBody').get_text()
  # print '---TIME: ', item.find('time').get_text()
  # print '---SHARE COUNT ', item.find('aside', class_='st_sharethis_hcount')
  # print 's ', item.find('time').get_text()
  date = parser.parse(item.find('time').get_text())
  # print 'd ', date


  post_object = {
    'type_of_post' : 'article',
    'date' : date,
    'favorite_count' : 0,
    'name' : item.find('h1').get_text(),
    'text' : item.find('div', class_='contentBody').get_text(),
    'profile_image' : 'https://pbs.twimg.com/profile_images/505030509676617729/yp3FJtpO.png',
    'link_to_post' : figure.find('a').get('href'),
    'img_in_post' : figure.find('img')['data-src']
  }
  list_of_posts.append(post_object)

# print list_of_posts

# list_of_posts.sort(key=lambda r: date, reverse=True)
print list_of_posts




