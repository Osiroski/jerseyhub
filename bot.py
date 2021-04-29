import tweepy
import os
import time
import logging
from config import twitter_api
import requests
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

#Tweet function
def tweet(sample):
  filename = 'temp.jpg'
  request = requests.get(sample.iloc[0][1], stream=True)
  season=sample.iloc[0][2]
  jersey=sample.iloc[0][0]
  players=sample.iloc[0][3]
  jersey=''.join([i for i in jersey if not i.isdigit()]).replace('.','')
  list1=sample.iloc[0][4]
  api=twitter_api()
  if request.status_code == 200:
    with open(filename, 'wb') as image:
      for chunk in request:
        image.write(chunk)
        first=api.update_with_media(status='Jersey Today👕⚽\n{}\n{}\n{}\n'.format(jersey,season,players),filename=filename)
        if len(list1)<=280:
          second=api.update_status(status=list1,in_reply_to_status_id=first.id,auto_populate_reply_metadata=True)
          third=api.update_status(status='Get your jerseys at @JerseyHub_254',in_reply_to_status_id=second.id,auto_populate_reply_metadata=True)
        elif len(list1)>280 and len(list1)<=560:
          second=api.update_status(status=list1[:280],in_reply_to_status_id=first.id,auto_populate_reply_metadata=True)
          third=api.update_status(status=list1[280:],in_reply_to_status_id=second.id,auto_populate_reply_metadata=True)
          fourth=api.update_status(status='Get your jerseys at @JerseyHub_254',in_reply_to_status_id=third.id,auto_populate_reply_metadata=True)
        elif len(list1)>560:
          second=api.update_status(status=list1[:280],in_reply_to_status_id=first.id,auto_populate_reply_metadata=True)
          third=api.update_status(status=list1[280:560],in_reply_to_status_id=second.id,auto_populate_reply_metadata=True)
          fourth=api.update_status(status='Get your jerseys at @JerseyHub_254',in_reply_to_status_id=third.id,auto_populate_reply_metadata=True)
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
