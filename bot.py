import tweepy
import os
import time
import logging
from config import twitter_api
import requests
import pandas as pd
port = int(os.environ.get(“PORT”, 5000))

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
  list1=sample.iloc[0][4].split('.')
  api=twitter_api()
  if request.status_code == 200:
    with open(filename, 'wb') as image:
      for chunk in request:
        image.write(chunk)
        try:
            first=api.update_with_media(status='Jersey Today👕⚽\n{}\n{}\n{}\n'.format(jersey,season,players),filename=filename)
            second=api.update_status(status=list1[0],in_reply_to_status_id=first.id,auto_populate_reply_metadata=True)
            third=api.update_status(status=list1[1],in_reply_to_status_id=second.id,auto_populate_reply_metadata=True)
            if len(list1)>2:
                fourth=api.update_status(status=list1[2],in_reply_to_status_id=third.id,auto_populate_reply_metadata=True)
                fifth=api.update_status(status='Get your jerseys at @JerseyHub_254',in_reply_to_status_id=fourth.id,auto_populate_reply_metadata=True)
            else:
                fourth=api.update_status(status='Get your jerseys at @JerseyHub_254',in_reply_to_status_id=third.id,auto_populate_reply_metadata=True)
        except Exception:
            pass
      os.remove(filename)
  else:
    logger.info("Unable to download image")


def main():
    interval=60*60*4
    while True:
        content=pd.read_csv('tweet.csv')
        # Tweet and no of hours in delay
        tweet(content.sample())
        time.sleep(interval)

if __name__ == "__main__":
    main()
