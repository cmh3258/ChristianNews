from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import twitter, json, requests, time, sys, datetime
from dateutil import parser

from pytz import timezone
import pytz

from bson import Binary, Code
from bson.json_util import dumps

from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['test-database']

app = Flask(__name__)

api = twitter.Api(consumer_key='m5pAMifKNfva3eLKZ9UF5br4k',
                      consumer_secret='1spceNsdfZ9dQkpFDtrSd9BDobBUYAXm3LBK82JzaGxSTIMef9',
                      access_token_key='316106897-mqxOKAZP28UkNH141qP4iCnrGsmcu0w7hXkLC7hv',
                      access_token_secret='DHVs6n2nNHKulCzv1x1WPB18Z6XkmW1Z0rF3JzJ5UiHRm')


@app.route('/')
def index():
    return render_template('thesheep.html')

@app.route('/hello')
def hello():
    return render_template('hello.html')

@app.route('/savedposts')
def savedposts():
  try:
    return_posts = []
    posts = list(db.posts.find())
    print 'POSTS: ', posts
    #for post in posts.find():
      # print post
    #  return_posts.append(post)
    #print 'RETUNRING: ', jsonify(return_posts)
    return dumps(posts)
  except ValueError, e:
    print 'VE: ', e
  except TypeError, e:
    print 'TE: ', e
  except RuntimeError, e:
    print 'RE: ', e

@app.route('/savepost', methods=["POST"])
def savepost():
  print 'in savepost. bro'
  try:
    print request
  except:
    e = sys.exc_info()[0]
    print 'cant print request. ', e

  if not request.json:
    return 'No request.json', 400
  else:
    post = request.json
    post['is_saved'] = True
    post['is_published'] = False
    post['date_published'] = None
    posts = db.posts
    post_id = posts.insert_one(post).inserted_id
    print 'JSON ', request.json
    print 'post_id: ', post_id

  # # print request
  # if not request.json:
  #   return 'No request.json'
  # # print request
    return 'Success', 200

@app.route('/twit')
def twit():
  # utc=pytz.utc
  # print utc.zone

  list_of_posts = []
  screen_names = ['kvministries','BillVanderbush','TraciVanderbush','billjohnsonBJM','shawnbolz'
,'DrHeidiBaker','GeorgianBanov','che_ahn','lancewallnau','brianjohnsonM','jeramenelson','Jeff_Jansen','ChristineCaine','LauraMHackett']
  for screen_name in screen_names:
    statuses = api.GetUserTimeline(screen_name=screen_name)
    for s in statuses:
      # print s, '\n'
      link = 'https://twitter.com/'+ screen_name +'/status/'+ str(s.id)
      postText = s.text
      # img_in_post = postText
      if(postText.find('http') != -1):
        indexOfHttp = postText.index('http')
        outside_link = postText[indexOfHttp:]
      else:
        outside_link = ''
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
        'img_in_post' : img_in_post,
        'outside_link' : outside_link
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

  '''
    The gospel coalition - scraping front page articles
  '''
  r = requests.get('http://www.thegospelcoalition.org/archive')

  data = r.text
  soup = BeautifulSoup(data)
  for item in soup.find_all('article', class_="article-item"):
    
    date = parser.parse(item.find('time', class_='article-item__date').get_text())
    date = pytz.utc.localize(date)

    post_object = {
      'type_of_post' : 'article',
      'date' : date,
      'favorite_count' : 0,
      'name' : item.find('h1', class_='article-item__title').find('a').get_text(),
      'text' : item.find('p', class_='article-item__excerpt').get_text(),
      'profile_image' : 'http://s3.amazonaws.com/tgc-ee2/articles/tgclogo.jpg',
      'link_to_post' : 'http://www.thegospelcoalition.org/'+item.find('a', class_='article-item__read').get('href'),
      'img_in_post' : 'http://www.thegospelcoalition.org/'+item.find('img', class_='article-item__img')['src']
    }
    list_of_posts.append(post_object)


  # print list_of_posts
  try:
    list_of_posts.sort(key=lambda r: r['date'], reverse=True)
  except Exception as e:
    s = str(e)
    print 'error ',s
  
  # print list_of_posts
  # print 'hi'
  posts_by_date = []
  for x in list_of_posts:
    # print x
    # print x['date'].day, x['date'].month

    fountPost = False
    for date in posts_by_date:
      if date['day'] == x['date'].day and date['month'] == x['date'].month and date['year'] == x['date'].year:
        x['date'] = x['date'].isoformat()
        date['list_of_posts'].append(x)
        fountPost = True
    
    if not fountPost:
      weekday = x['date'].weekday()
      if weekday == 0:
        weekday = 'Monday'
      elif weekday == 1:
        weekday = 'Tuesday'
      elif weekday == 2:
        weekday = 'Wednesday'
      elif weekday == 3:
        weekday = 'Thursday'
      elif weekday == 4:
        weekday = 'Friday'
      elif weekday == 5:
        weekday = 'Saturday'
      else:
        weekday = 'Sunday'

      temp_post = {
        'day':x['date'].day,
        'weekday':weekday,
        'month':x['date'].month,
        'year':x['date'].year,
        'list_of_posts':[]
      }
      x['date'] = x['date'].isoformat()
      temp_post['list_of_posts'].append(x)
      posts_by_date.append(temp_post)

    # x['date'] = x['date'].isoformat()
    # print x['name']
    # print x['date']

  '''
    possible ways to have list of posts from that date

    [{day:1, month:3, list_of_posts:[]},{}]
  '''

    # print time.strptime(x['date'], "%Y-%m-%d")
    # print x['type_of_post']

  # print json.dumps(posts_by_date, indent=3)
  return json.dumps(posts_by_date)

  # return json.dumps(list_of_posts)


if __name__ == '__main__':
    app.run()



