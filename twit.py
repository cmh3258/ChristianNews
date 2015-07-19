
import twitter, time
from dateutil import parser

api = twitter.Api(consumer_key='m5pAMifKNfva3eLKZ9UF5br4k',
                      consumer_secret='1spceNsdfZ9dQkpFDtrSd9BDobBUYAXm3LBK82JzaGxSTIMef9',
                      access_token_key='316106897-mqxOKAZP28UkNH141qP4iCnrGsmcu0w7hXkLC7hv',
                      access_token_secret='DHVs6n2nNHKulCzv1x1WPB18Z6XkmW1Z0rF3JzJ5UiHRm')

# print api.VerifyCredentials()

#users = api.GetFriends()
#print [u for u in users]

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

  # print 's ', s.created_at
  date = parser.parse(s.created_at)
  # print 'd ', date
  #Sat Jul 18 13:00:41 +0000 2015
  #print 'time -> ',time.strptime(s.created_at, '%a %d %m %H:%M:%S %z %Y')


  try:
    # print 'media? ', s.media[0].media[0], '\n'
    img_in_post = s.media[0]['media_url_https']
    print 'img_in_post: ', img_in_post
  except:
    img_in_post = ''

  post_object = {
    'type_of_post' : 'tweet',
    'date' : date,
    'favorite_count' :  s.favorite_count,
    'name' : s.user.screen_name,
    'text' : s.text,
    'profile_image' : s.user.profile_image_url,
    'link_to_post' : link,
    'img_in_post' : img_in_post
  }
  list_of_posts.append(post_object)

  # print '---Created: ', s.created_at
  # print '---Favorited: ', s.favorite_count
  # print '---Name: ', s.user.screen_name
  # print '---Text: ', s.text
  # print '---Img: ', s.user.profile_image_url, '\n'
# print list_of_posts

list_of_posts.sort(key=lambda date: date, reverse=True)
print list_of_posts




