#!/usr/bin/env python

import time
import logging
import os
from datetime import date, timedelta
from utils import read_from_database, get_papers, tweet_login


def search_and_tweet():
     '''
     Search papers, filter them, and tweet. 
     '''
     get_papers()
     k_now = read_from_database()
     if not k_now:
          logging.info('No papers found today')
     else:          
          api = tweet_login()
          dois = []
          for n_tweets, line in enumerate(k_now):
               # matched_kw = line[0] # All commented lines are for tweeting with keywords
               tu = list(line[1])
               doi = tu[0]
               matched_title = tu[1]
               version = tu[2]
               if doi in dois:
                    continue
               else:
                    dois.append(doi)
               link = "https://www.biorxiv.org/content/" + doi +'v' + version
               n_char = len(matched_title)
               #message = 'Keywords'
               if n_char > 124:   #change this number to 117 if keywords
                    #matched_kw_length = 117 - len(message)
                    matched_title_length = 124
                    _matched_title = matched_title[:matched_title_length]
                    final_matched_title = _matched_title + '...'
               else:
                    final_matched_title = matched_title
               cwd = os.getcwd()
               with open(cwd + '/bioRxivbot/scripts/temp.txt', 'w') as f:
                    #f.write(message + '\n' + final_matched_kw + '\n' + link)
                    f.write(final_matched_title + '\n' + link)
               with open(cwd + '/bioRxivbot/scripts/temp.txt', 'r') as f:
                         api.update_status(f.read())
               f.close()
               time.sleep(5)
          os.remove(os.path.join(cwd + '/bioRxivbot/scripts/temp.txt'))
          logging.info('--> tmp file deleted')
          logging.info('Number of tweets today: %s', n_tweets + 1)


if __name__ == '__main__':
     search_and_tweet()
     logging.info('End')
