import tweepy
from tweepy import OAuthHandler
import json
import os
import datetime

with open('config.json') as config_file:
    data = json.load(config_file)

# Authenticate to Twitter
access_token = data['access_token']
access_token_secret = data['access_token_secret']
consumer_key = data['consumer_key']
consumer_secret = data['consumer_secret']

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
print("Authenticated")

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
userID_list = ['sundarpichai']
# userID_list = ["sundarpichai", 'elonmusk', 'finkd', 'JeffBezos', 'BillGates', ]
if not os.path.isdir('output'):
    os.mkdir('output')
print("Enter start date in format YYYY-MM-DD: ")
startDate = input()
print("Enter end date YYYY-MM-DD: ")
endDate = input()
start = datetime.datetime.strptime(startDate, "%Y-%m-%d")
end = datetime.datetime.strptime(endDate, "%Y-%m-%d")
# if start <= TODAY_CHECK <= end:
for user in userID_list:
    tweets_list = []
    user_info = api.get_user(user)
    name = user_info.name
    print(name)
    description = user_info.description
    location = user_info.location
    followers_count = user_info.followers_count
    friends_count = user_info.friends_count

    tweets = api.user_timeline(
        screen_name=user, count=200, include_rts=False, tweet_mode='extended')

    user_info = {
        'Total Tweets Found': len(tweets),
        "Name": name,
        "Bio": description,
        "followers_count": followers_count,
        'friends_count': friends_count,
    }
# print(user_info)
    c = 0
    tweets_list.append(user_info)
    print("Tweets Found: ", len(tweets))
    for index, info in enumerate(tweets):
        # print(info)
        check = datetime.datetime.strptime(
            str(info.created_at)[:10], "%Y-%m-%d")

        if start <= check <= end:
            c += 1
            # inRange = True
            tweet_dict = {
                'sr.no': c,
                'ID': info.id,
                'date_time_posted': str(info.created_at),
                'tweet': info.full_text
            }
        # inRange = False
            tweets_list.append(tweet_dict)
    user_info[f'Tweets found from {startDate} to {endDate}:'] = c


# print(tweets_list)
    with open(f'output/{user}.json', 'w') as outfile:
        json.dump(tweets_list, outfile, indent=4)
print('DONE :)')
