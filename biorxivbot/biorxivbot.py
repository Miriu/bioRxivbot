import requests
from datetime import date, timedelta
import sqlite3
from utils import read_from_database, get_papers, tweet_login
import tweepy
import time


def search_and_tweet():
     get_papers()
     now = read_from_database()
     api = tweet_login()
     for line in now:
          doi = line[0]
          title = line[1]
          version = line[2]
          link = "https://www.biorxiv.org/content/" + doi +'v' + version
          n_char = len(title) + len(link)
          if n_char > 139:
               max_title_length = 106 - len(link)
               _title = title[:max_title_length]
               final_title = _title + '...'
          else:
               final_title = title
          with open('temp.txt', 'w') as f:
               f.write(final_title + '\n' + link)
          with open('temp.txt', 'r') as f:
                    api.update_status(f.read())
          f.close()
          time.sleep(1)


if __name__ == '__main__':
     search_and_tweet()