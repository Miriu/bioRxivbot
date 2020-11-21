import requests
from datetime import date, timedelta
import sqlite3
from utils import read_from_database, get_papers, tweet_login
import tweepy
import time


def search_and_tweet():
     get_papers()
     now, k_now = read_from_database()
     # print(now)
     # print('\n')
     api = tweet_login()
     for line in k_now:
          matched_kw = line[0]
          tu = list(line[1])
          doi = tu[0]
          title = tu[1]
          version = tu[2]
          link = "https://www.biorxiv.org/content/" + doi +'v' + version
          n_char = len(matched_kw) + len(link)
          message = 'Keywords'
          if n_char > 139:
               matched_kw_length = 136 - len(link) - len(message)
               _matched_kw = matched_kw[:matched_kw_length]
               final_matched_kw = _matched_kw + '...'
          else:
               final_matched_kw = matched_kw
          with open('temp.txt', 'w') as f:
               f.write(message + '\n' + final_matched_kw + '\n' + link)
          with open('temp.txt', 'r') as f:
                    api.update_status(f.read())
          f.close()
          time.sleep(1)


if __name__ == '__main__':
     search_and_tweet()