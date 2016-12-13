#Import the necessary methods from tweepy library
#from tweepy.streaming import StreamListener
import tweepy
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy import Stream

#from tweepy import Stream
import json
import textwrap
import ConfigParser
import pprint

lyrics = []
counters = {}
api = ""
length = 0
screen_name = ""

class MsgListener(StreamListener):

    def on_direct_message(self, status):
        global lyrics, counters, api, screen_name, length
        
        #pprint.pprint(vars(status))
        from_screen_name = status._json['direct_message']['sender']['screen_name']
        if from_screen_name != screen_name:
            if not counters.has_key(from_screen_name):
                counters[from_screen_name]=0
            print counters[from_screen_name]
            print screen_name 
            print counters[from_screen_name]
            api.send_direct_message(screen_name=from_screen_name, text=lyrics[counters[from_screen_name]])
            if counters[from_screen_name] < length:
                counters[from_screen_name] += 1
            else:
                counters[from_screen_name] = 0
        
        #print status._json['direct_message']['sender']['screen_name']
        
    def on_error(self, status):
       print status

if __name__ == '__main__':

    Config = ConfigParser.ConfigParser()
    Config.read("config.ini")

    api_key = Config.get("twitter", "api_key")
    api_secret = Config.get("twitter", "api_secret")
    access_token = Config.get("twitter", "access_token")
    access_secret = Config.get("twitter", "access_secret")
    screen_name = Config.get("twitter", "screen_name")
    
    songfile = Config.get("song", "filename")
    lyrics = [line.rstrip('\n') for line in open(songfile)]
    length = len(lyrics) - 1
    
    auth = OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_secret)
    listener = MsgListener()
    stream = Stream(auth, listener)
    api = tweepy.API(auth)
    stream.userstream()