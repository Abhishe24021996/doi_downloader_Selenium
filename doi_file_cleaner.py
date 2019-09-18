# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 16:30:13 2019

@author: Abhis
"""

import mysql.connector
import glob
import shutil
import os
#import logging
import sqlite3
import pymysql


from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')
host = config.get('main', 'host')
user = config.get('main', 'user')
password = config.get('main', 'password')
db = config.get('main', 'db')

connection = pymysql.connect(host=host,
							 user=user,
							 password=password,
							 db=db,
							 charset='utf8mb4',
							 cursorclass=pymysql.cursors.DictCursor,
							 autocommit=True)


with connection.cursor() as cur:
    cur.execute('select research_article_doi from research_article;')
    dois=[]
    for row in cur.fetchall():
        dois.append(row['research_article_doi'])
        
#####################################################################
#doi _data.db

conn = sqlite3.connect("doi_data.db")
cur = conn.cursor()
cur.execute("select doi_id from doi_status where comment = 'no keywords found'")
dois1=[]
for row in cur.fetchall():
    dois.append(row[0])



        
        
        
        
###read old file
with open('doi1.txt','r') as f:
    line=f.read().split()
    
newlines=[ l for l in line if not l in dois]

############################################################


with open('doi11.txt','w') as f:
    for li in newlines:
        f.write('%s\n' %li)
