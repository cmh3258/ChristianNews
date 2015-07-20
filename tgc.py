
import requests, time, json
from bs4 import BeautifulSoup
from dateutil import parser


r = requests.get('http://www.thegospelcoalition.org/archive')

data = r.text
soup = BeautifulSoup(data)
list_of_posts = []
for item in soup.find_all('article', class_="article-item"):
  
  # print item
  # figure = item.find('figure', class_='featuredArticleImage')
  # print '---href: ', figure.find('a').get('href')
  # print '---img: ', figure.find('img')['data-src']

  # print '---TITLE: ', item.find('h1').get_text()
  # print '---DESC: ', item.find('div', class_='contentBody').get_text()
  # print '---TIME: ', item.find('time').get_text()
  # print '---SHARE COUNT ', item.find('aside', class_='st_sharethis_hcount')
  # print 's ', item.find('time').get_text()
  date = parser.parse(item.find('time', class_='article-item__date').get_text())
  print 'd ', date


  post_object = {
    'type_of_post' : 'article',
    'date' : date,
    'favorite_count' : 0,
    'name' : item.find('h1', class_='article-item__title').find('a').get_text(),
    'text' : item.find('p', class_='article-item__excerpt').get_text(),
    'profile_image' : 'https://pbs.twimg.com/profile_images/505030509676617729/yp3FJtpO.png',
    'link_to_post' : item.find('a', class_='article-item__read').get('href'),
    'img_in_post' : item.find('img', class_='article-item__img')['src']
  }
  list_of_posts.append(post_object)

print json.dumps(list_of_posts, indent=3)

# list_of_posts.sort(key=lambda r: date, reverse=True)
print list_of_posts




