import requests
from bs4 import BeautifulSoup
import sqlite3

class WriteToDatabase():
    
    def __init__(self, database):
        self._database = database

        self.create_connection()
        self.create_table()
        
    def create_connection(self):
        
        self._conn = None
        try:
            self._conn = sqlite3.connect(self._database)
        except Exception as e:
            print(e)
                
    def create_table(self):
        try:
            self._cur = self._conn.cursor()
            self._cur.execute('''CREATE TABLE IF NOT EXISTS publications (
                                 ns1id text,
                                 ns1outcomeid text,
                                 ns2title text,
                                 ns2type text,
                                 ns2journaltitle text,
                                 ns2datepublished text,
                                 ns2publicationurl text,
                                 ns2author text,
                                 ns2chaptertitle text,
                                 project text)''')
        except Exception as e:
            print(e)
            
    def write_to_table(self, data):
        self._cur.execute('''INSERT INTO publications VALUES (?,?,?,?,?,?,?,?,?,?)''', 
                          (data[0], data[1], data[2], data[3], data[4], data[5], data[6],
                           data[7], data[8], data[9]))

def run():

    dataset = []
    count = 1
    
    database = WriteToDatabase("./gtr.db")
    
    while True:
        try:
            url =  "https://gtr.ukri.org/gtr/api/outcomes/publications?p=%s" % count
            print(url)
            page = requests.get(url)
        except:
            break
        
        soup = BeautifulSoup(page.content, "xml")

        failure = soup.findAll("ns1:failure")
        if len(failure) > 0:
            break
        
        projects = soup.findAll("ns2:publication")

        for i in projects:

            tmp = []
            
            try:
                ns1_id = i["ns1:id"]
                tmp.append(ns1_id)
            except:
                tmp.append("")

            try:
                ns2_id = i["ns1:outcomeid"]
                tmp.append(ns2_id)
            except:
                tmp.append("")
                
            try:
                ns2_title = i.findAll("ns2:title")[0].text
                tmp.append(ns2_title)
            except:
                tmp.append("")
            
            try:
                ns2_type = i.findAll("ns2:type")[0].text
                tmp.append(ns2_type)
            except:
                tmp.append("")
            
            try:
                ns2_journaltitle = i.findAll("ns2:journalTitle")[0].text
            except:
                ns2_journaltitle = ""
            tmp.append(ns2_journaltitle)
   
            try:
                ns2_datepublished = i.findAll("ns2:datePublished")[0].text
            except:
                ns2_datepublished = ""
            tmp.append(ns2_datepublished)

            try:
                ns2_publicationurl = i.findAll("ns2:publicationUrl")[0].text
            except:
                ns2_publicationurl = ""
            tmp.append(ns2_publicationurl)
                
            try:
                ns2_author = i.findAll("ns2:author")[0].text
            except:
                ns2_author = ""
            tmp.append(ns2_author)
                
            try:
                ns2_chaptertitle = i.findAll("ns2:chapterTitle")[0].text
            except:
                ns2_chaptertitle = ""
            tmp.append(ns2_chaptertitle)

            try:               
                ns2_project = i.findAll("ns1:link")[0]["ns1:href"]
            except:
                ns2_project = ""
            tmp.append(ns2_project)

            database.write_to_table(tmp)
                        
            dataset.append(tmp)
            
        count += 1
                             
if __name__ == "__main__":
    run()