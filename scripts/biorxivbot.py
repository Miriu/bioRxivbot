#!/usr/bin/env python

import time
import logging
from datetime import date, timedelta
from utils import read_from_database, get_papers, tweet_login


def search_and_tweet():
     '''
     Search papers, filter them, and tweet. 
     '''
     get_papers()
     k_now = read_from_database()
     api = tweet_login()
     n_tweets = 0
     dois = []
     for line in k_now:
          matched_kw = line[0]
          tu = list(line[1])
          doi = tu[0]
          title = tu[1]
          version = tu[2]
          if doi in dois:
               continue
          else:
               dois.append(doi)
          link = "https://www.biorxiv.org/content/" + doi +'v' + version
          n_char = len(matched_kw)
          message = 'Keywords'
          if n_char > 117:
               matched_kw_length = 117 - len(message)
               _matched_kw = matched_kw[:matched_kw_length]
               final_matched_kw = _matched_kw + '...'
          else:
               final_matched_kw = matched_kw
          # with open('temp.txt', 'w') as f:
          #      f.write(message + '\n' + final_matched_kw + '\n' + link)
          # with open('temp.txt', 'r') as f:
          #           api.update_status(f.read())
          # f.close()
          n_tweets += 1
          time.sleep(5)
     logging.info('Number of tweets today: %s', n_tweets)


if __name__ == '__main__':
     search_and_tweet()
     logging.info('End')
