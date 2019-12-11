from textblob import TextBlob
import tweepy
from tweepy import OAuthHandler
import re
import csv
from datetime import timedelta


"""Main script to pull data from Twitter and run the sentiment analysis"""


class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''

    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = '0k8cIuLYT2G0SQ6c79W1zxII6'
        consumer_secret = 'ujZI9Juk3Y318zE4oFt3m25EYM9oxcSlQny4325A9SU2JrHFJr'
        access_token = '900107220368539648-1lzgk0FNnZfRBj8oQu2xcThmzgUBeye'
        access_token_secret = '9BPJ5wJvO6eCBiqx8HiI1Kdrte41tTwsM2X80MV64NhGA'

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        sentiment = analysis.sentiment.polarity
        # set sentiment
        if sentiment > 0:
            return 'positive', sentiment
        elif sentiment == 0:
            return 'neutral', sentiment
        else:
            return 'negative', sentiment

    def get_tweets(self, file, start, count):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []
        start_date = None

        # keywords to look for
        keywords = ['renewable', 'oil', 'natural gas', 'nuclear', 'wind', 'solar', 'coal',
                    'warming', 'climate change']

        # tweet = self.api.get_status('tweet_id')
        with open(file) as f:
            idList = f.readlines()

        j = 0
        while j < count:

            try:
                # call twitter api to fetch tweets
                fetched_tweets = self.api.statuses_lookup(int(i) for i in idList[start:start+100])

                start_date = fetched_tweets[0].created_at

                # parsing tweets one by one
                for tweet in fetched_tweets:

                    # skip retweets
                    if tweet.retweeted or 'RT @' in tweet.text:
                        continue

                    # empty dictionary to store required params of a tweet
                    parsed_tweet = {}

                    # saving date and text of tweet
                    #parsed_tweet['id'] = tweet.id
                    parsed_tweet['date'] = tweet.created_at
                    #parsed_tweet['text'] = tweet.text.strip(',')
                    # saving sentiment of tweet
                    parsed_tweet['polarity'], parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                    # check if tweet contains a keyword
                    for keyword in keywords:
                        if keyword in tweet.text.lower():
                            parsed_tweet['keyword'] = keyword
                            tweets.append(parsed_tweet)

                    if tweet.created_at >= start_date + timedelta(days=8):
                        return tweets


            except tweepy.TweepError as e:
                # print error (if any)
                print("Error : " + str(e))

            start += 100
            j += 100

        # return parsed tweets
        return tweets


def main():
    # creating object of TwitterClient Class
    api = TwitterClient()
    file = 'id_data/climate_id.txt'
    start = 0
    count = 1000000

    # calling function to get tweets
    tweets = api.get_tweets(file, start, count)
    keys = tweets[0].keys()

    # write sentiment data to file
    with open('data_one_week.csv') as f:
        writer = csv.DictWriter(f, keys)
        writer.writeheader()
        writer.writerows(tweets)

    return


if __name__ == "__main__":
    # calling main function
    main()
