from flask import Flask, render_template
import twitter, json

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
  list_of_posts = []
  statuses = api.GetUserTimeline(screen_name='kvministries')
  for s in statuses:
    post_object = {
      'type_of_post' : 'short',
      'date' : s.created_at,
      'favorite_count' :  s.favorite_count,
      'name' : s.user.screen_name,
      'text' : s.text,
      'profile_image' : s.user.profile_image_url 
    }
    list_of_posts.append(post_object)

  return json.dumps(list_of_posts)

if __name__ == '__main__':
    app.run()