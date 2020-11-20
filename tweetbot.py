import requests
from datetime import date, timedelta
import sqlite3
from utils import read_from_database, get_papers
import tweepy


def tweet_login():
     creds = []
     with open('credentials.txt') as f:
          creds = [i.strip() for i in f.readlines()]
          auth = tweepy.OAuthHandler(creds[0], creds[1])
          auth.set_access_token(creds[2], creds[3])
          api = tweepy.API(auth, , wait_on_rate_limit=True,
                              wait_on_rate_limit_notify=True)
          try:
               api.verify_credentials()
               print("Authentication OK")
          except:
               print("Error during authentication")


def search_and_tweet():
     get_papers()
     now = read_from_database()
     for line in now:
          doi = line[0]
          title = line[1]
          version = line[2]
          link = "https://www.biorxiv.org/content/" + doi +'v' + version
          n_char = len(title) + len(link)
          if n_char > 139:
               max_title_length = 136 - len(link)
               _title = title[:max_title_length]
               final_title = _title + '...'
          else:
               final_title = title
          tweet(final_title, link)


def tweet(title, link):
     tweet_login()
     api.update_status(title, link)
