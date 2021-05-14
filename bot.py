import tweepy
import os
import time
import logging
from config import twitter_api
import requests
import pandas as pd
import urllib.request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

#Tweet function
def tweet(sample):
  filename = 'temp.jpg'
  urllib.request.urlretrieve(sample.iloc[0][1], filename)
  season=sample.iloc[0][2]
  jersey=sample.iloc[0][0]
  players=sample.iloc[0][3]
  jersey=''.join([i for i in jersey if not i.isdigit()]).replace('.','')
  list1=sample.iloc[0][4]
  api=twitter_api()
  chars=len(list1)
  first=api.update_with_media(status='Jersey Today👕⚽\n{}\n{}\n{}\n'.format(jersey,season,players),filename=filename)
  if chars<=280:
    second=api.update_status(status=list1[:280],in_reply_to_status_id=first.id,auto_populate_reply_metadata=True)
    mention=api.update_status(status='Get your jerseys at @JerseyHub_254',in_reply_to_status_id=second.id,auto_populate_reply_metadata=True)
  elif chars>280 and chars<=560:
    second=api.update_status(status=list1[:280],in_reply_to_status_id=first.id,auto_populate_reply_metadata=True)
    third=api.update_status(status=list1[281:561],in_reply_to_status_id=second.id,auto_populate_reply_metadata=True)
    fourth=api.update_status(status='Get your jerseys at @JerseyHub_254',in_reply_to_status_id=third.id,auto_populate_reply_metadata=True)
  elif chars>560:
    second=api.update_status(status=list1[:280],in_reply_to_status_id=first.id,auto_populate_reply_metadata=True)
    third=api.update_status(status=list1[281:561],in_reply_to_status_id=second.id,auto_populate_reply_metadata=True)
    fourth=api.update_status(status=list1[561:761],in_reply_to_status_id=second.id,auto_populate_reply_metadata=True)
    fifth=api.update_status(status='Get your jerseys at @JerseyHub_254',in_reply_to_status_id=third.id,auto_populate_reply_metadata=True)
  os.remove(filename)
      
def main():
    interval=60*60*4
    while True:
        content=pd.read_csv('tweet.csv')
        logger.info("Selecting tweet")
        # Tweet and no of hours in delay
        tweet(content.sample())
        logger.info("Tweet sent. Going to sleep now...")
        time.sleep(interval)

if __name__ == "__main__":
    main()
