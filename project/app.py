from flask import Flask, render_template
from bs4 import BeautifulSoup
import twitter, json, requests, time, sys, datetime
from dateutil import parser

from pytz import timezone
import pytz


app = Flask(__name__)

api = twitter.Api(consumer_key='m5pAMifKNfva3eLKZ9UF5br4k',
                      consumer_secret='1spceNsdfZ9dQkpFDtrSd9BDobBUYAXm3LBK82JzaGxSTIMef9',
                      access_token_key='316106897-mqxOKAZP28UkNH141qP4iCnrGsmcu0w7hXkLC7hv',
                      access_token_secret='DHVs6n2nNHKulCzv1x1WPB18Z6XkmW1Z0rF3JzJ5UiHRm')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello')
def hello():
    return render_template('hello.html')

@app.route('/twit')
def twit():
  # utc=pytz.utc
  # print utc.zone

  list_of_posts = []
  screen_name = 'kvministries'
  statuses = api.GetUserTimeline(screen_name=screen_name)
  for s in statuses:
    # print s, '\n'
    link = 'https://twitter.com/'+ screen_name +'/status/'+ str(s.id)
    # postText = s.text
    # img_in_post = postText
    # if(postText.find('http') != -1):
    #   indexOfHttp = postText.index('http')
    #   img_in_post = postText[indexOfHttp:]
    # else:
    #   img_in_post = ''
    # print 'hi ', s.created_at
    date = parser.parse(s.created_at)
    # print newdate
    # print strptime(newdate)
    # date = utc.localize(newdate)
    # print date

    try:
      img_in_post = s.media[0]['media_url_https']
    except:
      img_in_post = ''

    post_object = {
      'type_of_post' : 'tweet',
      'date' : date,
      'favorite_count' : s.favorite_count,
      'name' : s.user.screen_name,
      'text' : s.text,
      'profile_image' : s.user.profile_image_url,
      'link_to_post' : link,
      'img_in_post' : img_in_post
    }
    list_of_posts.append(post_object)
    # print '------->a'


  '''
    Charismamag - scraping front page articles
  '''
  r = requests.get('http://www.charismamag.com/')

  data = r.text
  soup = BeautifulSoup(data)
  for item in soup.find_all('article', class_="article"):
    
    #article image
    figure = item.find('figure', class_='featuredArticleImage')

    # date1 = item.find('time').get_text()
    date = parser.parse(item.find('time').get_text())
    date = pytz.utc.localize(date)

    #create objects
    post_object = {
      'type_of_post' : 'article',
      'date' : date,
      'favorite_count' : 0,
      'name' : item.find('h1').get_text(),
      'text' : item.find('div', class_='contentBody').get_text(),
      'profile_image' : 'https://pbs.twimg.com/profile_images/505030509676617729/yp3FJtpO.png',
      'link_to_post' : 'http://www.charismamag.com'+figure.find('a').get('href'),
      'img_in_post' : figure.find('img')['data-src']
    }
    list_of_posts.append(post_object)
    # list_of_posts.sort(key=lambda r: r.date, reverse=True)
    # print '----> ', list_of_posts

    # print '------>b'

  # print list_of_posts
  try:
    list_of_posts.sort(key=lambda r: r['date'], reverse=True)
  except Exception as e:
    s = str(e)
    print 'error ',s
  
  # print list_of_posts
  # print 'hi'
  for x in list_of_posts:
    # print x
    x['date'] = x['date'].isoformat()
    # print x['name']
    print x['date']

    # print time.strptime(x['date'], "%Y-%m-%d")
    # print x['type_of_post']


  return json.dumps(list_of_posts)


if __name__ == '__main__':
    app.run()



