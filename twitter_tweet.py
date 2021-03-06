# http://pythonprogramming.net/use-twitter-api-v1-1-python-stream-tweets/

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from pymongo import MongoClient
import os

try:
    client=MongoClient()
    client.drop_database("twitterdb")
except OSError:
    pass

ckey = "IMUFGw7o7Sm9Ygx9YhpgEelO7"
csecret = "BAli9zGOadDXzJ6boR9psKyeJZrzVb6W2ka9hy9H9SjWmStwgo"
atoken= "624867037-NxR60aaB6jUcg6Jlj7uZGdWw7od023EpAO76pP39"
asecret= "rt2lpUZpxVMEuBGO3CFvp2tu9cIQco3fI1Jnr1Jnn3vSs"

class listener (StreamListener):

    def on_data(self,data):
        try:
            client=MongoClient()
            db=client.twitterdb
            time=data.split('"created_at":"')[1].split('","id')[0]
            tweet=data.split(',"text":"')[1].split('","source')[0]
            name=data.split(',"name":"')[1].split('","screen_name')[0]
            location=data.split(',"location":"')[1].split('","url')[0]
            time_zone=data.split(',"time_zone":"')[1].split('","geo_enabled')[0]
            lang=data.split(',"lang":"')[1].split('","contributors_enabled')[0]
            Data={"Created at:: ":time,"Tweet:: ":tweet,"Name:: ":name,"Location:: ":location,"Time_Zone:: ":time_zone,"Language:: ":lang}
            print (Data)
            db.twitterdb.insert(Data)
            #output=open('twitter.txt','a')
            #output.write(Data)
            #output.write('\n')
            #output.close()
            return True
        except BaseException, e:
            print 'error', str(e)

    def on_error(self,status):
        print status

auth=OAuthHandler(ckey,csecret)
auth.set_access_token(atoken,asecret)
twitterStream=Stream(auth,listener())
twitterStream.filter(track=["twitter"])