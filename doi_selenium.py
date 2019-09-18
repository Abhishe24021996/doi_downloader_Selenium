from selenium import webdriver
import time
import os
import sqlite3



with open('doi1.txt','r') as f:
    dois = f.read().split()



def download_pdf(lnk, download_folder, path_to_chrome_driver,j):
    options = webdriver.ChromeOptions()
    profile = {
               "plugins.plugins_list": [{"enabled": False,
                                         "name": "Chrome PDF Viewer"}],
               "download.default_directory": download_folder,
               "download.extensions_to_open": ""
                }
    options.add_experimental_option("prefs", profile)
    driver = webdriver.Chrome(path_to_chrome_driver,options = options)
    driver.get(lnk)
    driver.save_screenshot("screenshot"+str(j)+".png")

def create_table():
    cursor = connection.cursor()
    # This is the only place where int vs INTEGER matters—in auto-incrementing columns
    create_table = "CREATE TABLE IF NOT EXISTS doi_checker (sno INTEGER PRIMARY KEY AUTOINCREMENT, doi_id NVARCHAR(150) NOT NULL UNIQUE, success INT, fail INT, comment NVARCHAR(45))"
    cursor.execute(create_table)
    connection.commit()
    print("table_created")
    
def create_table_doi_folder():
    cursor = connection.cursor()
    # This is the only place where int vs INTEGER matters—in auto-incrementing columns
    create_table = "CREATE TABLE IF NOT EXISTS doi_folder (sno INTEGER PRIMARY KEY AUTOINCREMENT, doi_id NVARCHAR(150) NOT NULL UNIQUE, folder NVARCHAR(45))"
    cursor.execute(create_table)
    connection.commit()
    print("table_created")

def insert_doi_folder(doi, folder):
    cursor = connection.cursor()
    insert_table = '''INSERT INTO doi_folder (doi_id, folder) VALUES(?,?);'''
    cursor.execute(insert_table,(doi, folder))
    connection.commit()
    print("Doi entered in data.db(LOCAL)(doi_folder table)")
    
def insert_doi_status(doi,success,fail,comment):
    cursor = connection.cursor()
    insert_table = '''INSERT INTO doi_checker (doi_id, success, fail, comment) VALUES(?,?,?,?);'''
    cursor.execute(insert_table,(doi,success,fail,comment))
    connection.commit()
    print("Doi entered in data.db(LOCAL)(doi_status table)")
    
def check_db_list():
    cursor = connection.cursor()
    doi_list = "Select doi_id from doi_checker"
    cursor.execute(doi_list)
    li=[row[0] for row in cursor.fetchall()]
    return li

    
    
    
connection = sqlite3.connect('sel_doi_done.db')
create_table()
create_table_doi_folder()
checklist = check_db_list()

directory="pyf"
with open('filename.txt', 'r') as f:
    try: j=int(f.read())
    except: j=0

#download_folder =os.getcwd()+ "\\first"
path = os.getcwd()+"\\chromedriver.exe"


for item in dois:
    if item in checklist:
        print("already done")
        continue
    lnk = "http://sci-hub.tw/"+str(item)
    download_folder =os.getcwd()+ "\\" + directory + str(j)
    os.mkdir(download_folder)
    j+=1
    with open('filename.txt','w') as f:
        f.write(str(j))
    i=2
    check = os.listdir(download_folder)
    while not check:
        download_pdf(lnk,download_folder, path_to_chrome_driver=path,j=j)
        check = os.listdir(download_folder)
        i-=1
        if i == 0:
            break
    
    if check:
        print('downloaded')
        insert_doi_status(item,success=1, fail=0, comment="")
        insert_doi_folder(doi=item, folder= download_folder)
        continue
    insert_doi_status(item,success=0, fail=1, comment="failed")
    

    
    
        