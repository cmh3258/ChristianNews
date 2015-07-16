
import twitter

api = twitter.Api(consumer_key='m5pAMifKNfva3eLKZ9UF5br4k',
                      consumer_secret='1spceNsdfZ9dQkpFDtrSd9BDobBUYAXm3LBK82JzaGxSTIMef9',
                      access_token_key='316106897-mqxOKAZP28UkNH141qP4iCnrGsmcu0w7hXkLC7hv',
                      access_token_secret='DHVs6n2nNHKulCzv1x1WPB18Z6XkmW1Z0rF3JzJ5UiHRm')

# print api.VerifyCredentials()

#users = api.GetFriends()
#print [u for u in users]

statuses = api.GetUserTimeline(screen_name='kvministries')
for s in statuses:
  print '---Created: ', s.created_at
  print '---Favorited: ', s.favorite_count
  print '---Name: ', s.user.screen_name
  print '---Text: ', s.text
  print '---Img: ', s.user.profile_image_url, '\n'