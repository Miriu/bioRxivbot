import requests
from datetime import date, timedelta
import sqlite3
import math
import tweepy
import logging
import os


def get_papers():
     '''
     Gets papers from bioRxiv API and creates an SQL table with them. 
     '''
     cwd =  os.getcwd()
     logging.basicConfig(filename= cwd + '/bioRxivbot/scripts/activity.log', format='%(asctime)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                          filemode='w', level=logging.DEBUG)
     logging.info('Start with get_papers')
     today = date.today()
     yesterday = today - timedelta(days = 1)
     papers = requests.get("https://api.biorxiv.org/details/biorxiv/" + str(yesterday) + "/" + str(yesterday))
     logging.info('First Request: %s', "https://api.biorxiv.org/details/biorxiv/" + str(yesterday) + "/" + str(yesterday))
     papers_dic = papers.json()
     connection = None
     connection = sqlite3.connect(cwd + '/bioRxivbot/scripts/tweetbot.db')
     cursor = connection.cursor()
     cursor.execute('''DROP TABLE if exists yesterday_pubs''')
     cursor.execute('''CREATE TABLE 'yesterday_pubs'
                         ('doi', 'title','authors', 'author_corresponding', 
                         'author_corresponding_institution', 'date', 
                         'version', 'type','license','category','abstract','published','server')''')
     for child in papers_dic['collection']:
          cursor.execute('INSERT INTO yesterday_pubs VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)', 
                         (child['doi'], child['title'], child['authors'], child['author_corresponding'], 
                         child['author_corresponding_institution'], child['date'], 
                         child['version'], child['type'], child['license'], 
                         child['category'],child['abstract'],child['published'],child['server']))
     connection.commit()
     pap = papers_dic['messages']
     pepe = pap[0]
     logging.info('Messaging from bioRxiv: %s', pepe)
     for key,value in pepe.items():
          if key == 'total':
               n_papers =  value
     if n_papers > 100:
          total_loops = math.floor(n_papers/100)
          start = 101
          for n in range(total_loops):
               papers = requests.get("https://api.biorxiv.org/details/biorxiv/" + str(yesterday) + "/" + str(yesterday) + '/' + str(start))
               logging.info('Next Request: %s', "https://api.biorxiv.org/details/biorxiv/" + str(yesterday) + "/" + str(yesterday) + '/' + str(start))
               papers_dic = papers.json()
               connection = sqlite3.connect('tweetbot.db')
               cursor = connection.cursor()
               for child in papers_dic['collection']:
                    cursor.execute('INSERT INTO yesterday_pubs VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)', 
                                   (child['doi'], child['title'], child['authors'], child['author_corresponding'], 
                                   child['author_corresponding_institution'], child['date'], 
                                   child['version'], child['type'], child['license'], 
                                   child['category'],child['abstract'],child['published'],child['server']))
               connection.commit()
               start += 100
     logging.info('Got papers OK')

def load_keywords():
     '''
     Read keywords from serach.txt file and converts them into a LIKE sqlite3 search. 
     '''
     cwd = os.getcwd()
     with open(cwd + '/bioRxivbot/scripts/search.txt') as f:
          lines = [i.strip() for i in f.readlines()]
          lowline = []
          for line in lines:
               if ') AND (' in line:
                    prelowline = line.replace(') AND (', ' XXXX ')
                    prelowline = prelowline.replace('(', '(abstract LIKE \'%').replace(')', '%\')').replace(' OR ', '%\' OR abstract LIKE \'%').replace(' AND ', '%\' AND abstract LIKE \'%').replace(' NOT ', '%\' abstract NOT LIKE \'%')
                    prelowline = prelowline.replace(' XXXX ', '%\') AND (abstract LIKE \'%')
                    lowline.append([line, prelowline])
               elif ') OR (' in line:
                    prelowline = line.replace(') OR (', ' XXXX ')
                    prelowline = prelowline.replace('(', '(abstract LIKE \'%').replace(')', '%\')').replace(' OR ', '%\' OR abstract LIKE \'%').replace(' AND ', '%\' AND abstract LIKE \'%').replace(' NOT ', '%\' abstract NOT  LIKE \'%')
                    prelowline = prelowline.replace(' XXXX ', '%\') OR (abstract LIKE \'%')
                    lowline.append([line, prelowline])
               elif ') OR (' in line:
                    prelowline = line.replace(') NOT (', ' XXXX ')
                    prelowline = prelowline.replace('(', '(abstract LIKE \'%').replace(')', '%\')').replace(' OR ', '%\' OR abstract LIKE \'%').replace(' AND ', '%\' AND abstract LIKE \'%').replace(' NOT ', '%\' abstract NOT LIKE \'%')
                    prelowline = prelowline.replace(' XXXX ', '%\') AND (abstract NOT LIKE \'%')
                    lowline.append([line, prelowline])
               else:
                    prelowline = line.replace(' OR ', '%\' OR abstract LIKE \'%').replace(' AND ', '%\' AND abstract LIKE \'%').replace(' NOT ', '%\' abstract NOT LIKE \'%')
                    prelowline = 'abstract LIKE \'%' + prelowline + '%\''
                    lowline.append([line, prelowline])
          logging.info('Keywords OK')
          return lowline

def read_from_database():
     '''
     Read keywords in abstract and retrived matched papers.
     '''
     cwd = os.getcwd()
     connection = sqlite3.connect(cwd + '/bioRxivbot/scripts/tweetbot.db')
     cursor = connection.cursor()
     keywords = load_keywords()
     key_retrived = []
     for k in keywords:
          sql = "SELECT doi,title,version FROM yesterday_pubs WHERE " + k[1] + 'COLLATE NOCASE'
          cursor.execute(sql)
          retrived = cursor.fetchall()
          for i in retrived:
               key_re = [k[0], i]
               key_retrived.append(key_re)
          if not key_retrived:
               logging.info('No papers matching keywords were found today')
     return key_retrived

def tweet_login():
     '''
     Log in to twitter account; access granted by codes provded in credential.txt file.
     '''
     creds = []
     cwd = os.getcwd()
     with open(cwd + '/bioRxivbot/scripts/credentials.txt') as f:
          creds = [i.strip() for i in f.readlines()]
          auth = tweepy.OAuthHandler(creds[0], creds[1])
          auth.set_access_token(creds[2], creds[3])
          api = tweepy.API(auth, wait_on_rate_limit=True,
                              wait_on_rate_limit_notify=True)
          try:
               api.verify_credentials()
               logging.info("Authentication OK")
          except:
               logging.critical("Error during authentication")
          return api
