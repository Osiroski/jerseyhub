import tweepy
import logging
from os import environ

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

#Authenticate Twitter
def twitter_api():
  auth=tweepy.OAuthHandler(environ['CONSUMER_KEY'],environ['CONSUMER_SECRET'])
  auth.set_access_token(environ['ACCESS_TOKEN'],environ['ACCESS_SECRET'])
  #create API object
  api=tweepy.API(auth)
  logger.info("API created")
  return api
  
