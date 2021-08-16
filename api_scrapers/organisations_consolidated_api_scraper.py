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
            self._cur.execute('''CREATE TABLE IF NOT EXISTS organisations_consolidated (
                                 ns1id text,
                                 ns2name text)''')
        except Exception as e:
            print(e)
            
    def write_to_table(self, data):
        self._cur.execute('''INSERT INTO organisations_consolidated VALUES (?,?)''', 
                          (data[0], data[1]))

def run():

    dataset = []
    count = 1
    
    database = WriteToDatabase("./test.db")
    
    while True:
        try:
            url =  "https://gtr.ukri.org/gtr/api/organisations?p=%s" % count
            print(url)
            page = requests.get(url)
        except:
            break
        
        soup = BeautifulSoup(page.content, "xml")

        failure = soup.findAll("ns1:failure")
        if len(failure) > 0:
            break
        
        organisations = soup.findAll("ns2:organisation")
        
        for i in organisations:
            
            ns1_id = i["ns1:id"]
                
            tmp = []
            tmp.append(ns1_id)

            name = i.findAll("ns2:name")[0].text
            tmp.append(name)
            
            database.write_to_table(tmp)
                    
            dataset.append(tmp)
            
        count += 1
                             
if __name__ == "__main__":
    run()