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
            self._cur.execute('''CREATE TABLE IF NOT EXISTS identifier_project_lookup (
                                 ns1id text,
                                 identifier text)''')
        except Exception as e:
            print(e)
            
    def write_to_table(self, data):
        self._cur.execute('''INSERT INTO identifier_project_lookup VALUES (?,?)''', 
                          (data[0], data[1]))

def run():

    dataset = []
    count = 1
    
    database = WriteToDatabase("./gtr.db")
    
    while True:
        try:
            url =  "https://gtr.ukri.org/gtr/api/projects?p=%s" % count
            print(url)
            page = requests.get(url)
        except:
            break
        
        soup = BeautifulSoup(page.content, "xml")
        
        failure = soup.findAll("ns1:failure")
        if len(failure) > 0:
            break
        
        projects = soup.findAll("ns2:project")
        
        for i in projects:
            tmp = []            
            ns1_id = str(i["ns1:id"])
            tmp.append(ns1_id)
            ns2_identifier = i.findAll("ns2:identifier")[0].text
            tmp.append(ns2_identifier)
                    
            database.write_to_table(tmp)
                
            dataset.append(tmp)
            
        count += 1
                             
if __name__ == "__main__":
    run()