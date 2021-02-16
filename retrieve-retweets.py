import tweepy as tw
import csv
import time

consumer_key = "" 
consumer_secret = ""
access_token = ""
access_token_secret = ""

# authorization of consumer key and consumer secret 
auth = tw.OAuthHandler(consumer_key, consumer_secret) 
  
# set access to user's access key and access secret  
auth.set_access_token(access_token, access_token_secret) 
  
# calling the api  
api = tw.API(auth,wait_on_rate_limit_notify=True) 

# Open/create a file to append data to
csvFile = open('DataFrame2_RT.csv', 'w',newline='', encoding='utf-8')

# field names  
fields = ['User_Id', 'Retweet-list'] 


#Use csv writer
csvWriter = csv.writer(csvFile)

csvWriter.writerow(fields) 

rate_limit_counter = 0
retweets_ids = []
with open('DataFrame2_Clean.csv', 'r', encoding='utf-8') as read_obj:
    csv_dict_reader = csv.DictReader(read_obj)
    for tweetLine in csv_dict_reader:
        if int(tweetLine['tweet.retweet_count']) > 0:
            while True:
                try:
                    retweets_list = api.retweets(int(tweetLine['tweet.id_str']))
                    break
                except tw.TweepError:
                    print('Waiting for the rate limit...')
                    print('%i rows written' %75*rate_limit_counter)
                    time.sleep(60*15)
                    rate_limit_counter += 1
                    continue
            for retweet in retweets_list:
                retweets_ids.append(retweet.user.id_str)
            csvWriter.writerow([tweetLine['tweet.user.id'], retweets_ids])
            retweets_ids.clear()
csvFile.close()
