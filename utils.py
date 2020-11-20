import requests
from datetime import date, timedelta
import sqlite3

def get_papers():
    today = date.today()
    yesterday = today - timedelta(days = 1)
    papers = requests.get("https://api.biorxiv.org/details/biorxiv/" + str(yesterday) + "/" + str(yesterday))
    papers_dic = papers.json()
    connection = None
    connection = sqlite3.connect('tweetbot.db')
    cursor = connection.cursor()
    cursor.execute('''drop table if exists yesterday_pubs''')
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
    print(cursor.fetchall())

def load_keywords():
     with open('search.txt') as f:
          lines = [i.strip() for i in f.readlines()]
          lowline = []
          for line in lines:
               if ') AND (' in line:
                    prelowline = line.replace(') AND (', ' XXXX ')
                    prelowline = prelowline.replace('(', '(abstract LIKE \'%').replace(')', '%\')').replace(' OR ', '%\' OR abstract LIKE \'%').replace(' AND ', '%\' AND abstract LIKE \'%')
                    prelowline = prelowline.replace(' XXXX ', '%\') AND (abstract LIKE \'%')
                    lowline.append(prelowline)
               elif ') OR (' in line:
                    prelowline = line.replace(') OR (', ' XXXX ')
                    prelowline = prelowline.replace('(', '(abstract LIKE \'%').replace(')', '%\')').replace(' OR ', '%\' OR abstract LIKE \'%').replace(' AND ', '%\' AND abstract LIKE \'%')
                    prelowline = prelowline.replace(' XXXX ', '%\') OR (abstract LIKE \'%')
                    lowline.append(prelowline)
               else:
                    prelowline = line.replace(' OR ', '%\' OR abstract LIKE \'%').replace(' AND ', '%\' AND abstract LIKE \'%')
                    prelowline = 'abstract LIKE \'%' + prelowline + '%\''
                    lowline.append(prelowline)
          return lowline


def read_from_database():
     retrived = []
     connection = sqlite3.connect('tweetbot.db')
     cursor = connection.cursor()
     keywords = load_keywords()
     for k in keywords:
          sql = "SELECT doi,title,version FROM yesterday_pubs WHERE " + k + 'COLLATE NOCASE'
          cursor.execute(sql)
          retrived = cursor.fetchall()
     return retrived
