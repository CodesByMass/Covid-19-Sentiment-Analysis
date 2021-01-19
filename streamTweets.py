import tweepy as tw
import csv

consumer_key = "grrplDEVqTn9C2M4IaxxuOpj2" 
consumer_secret = "nNkvh2eAV9L97axJaQznvPfTJs7PZWKZ18rKfIezFFs1JtAugB"
access_token = "1118031236-WJXUjktWkt0YhgwOA8A4akQiTQxf8BIFxL3do9Y"
access_token_secret = "A0v6Le5G4qTPOuKfhAHzT7TWsR5sUx3UuN6QciWiboM2I"

#auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth = tw.AppAuthHandler(consumer_key, consumer_secret)

#auth.set_access_token(access_token, access_token_secret)

api = tw.API(auth)



csvFile = open('D:\Covid19Vaccine\sample.csv', 'a')
csvWriter = csv.writer(csvFile)
# Define the search term and the date_since date as variables
search_words = "vaccin OR covid OR vacciner OR covid 19 OR covid-19 OR me vacciner"
date_since = "2020-12-15"
tweets = tw.Cursor(api.search,
              q=search_words + " -filter:retweets",
              lang="fr",
              since=date_since,
              tweet_mode='extended')
try:              
    for tweet in tweets:
     csvWriter.writerow([tweet.id_str, tweet.user.id, tweet.user.followers_count, tweet.user.friends_count, tweet.full_text, 
     tweet.retweet_count, tweet.favorite_count])
except tw.error.TweepError:
        pass

tweets_streamed = []
tweets_streamed.extend(tweets)

#transform the tweepy tweets into a 2D array that will populate the csv	
from pandas import DataFrame
outtweets = [[tweet.id_str, 
              tweet.user.id, 
              tweet.user.followers_count, 
              tweet.user.friends_count, 
              tweet.retweet_count,
              tweet.favorite_count,
              tweet.full_text.encode("utf-8").decode("utf-8")] 
             for idx,tweet in enumerate(tweets_streamed)]
df = DataFrame(outtweets,columns=["id","user_id","followers","following", "retweets", "likes", "text"])
df.to_csv('first_tweets.csv',index=False)
df.head(3)