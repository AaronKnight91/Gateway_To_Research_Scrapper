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
            self._cur.execute('''CREATE TABLE IF NOT EXISTS studentships (
                                 ns1id text,
                                 ns1href text,
                                 ns1rel text,
                                 ns1end text,
                                 ns1start text)''')
        except Exception as e:
            print(e)
            
    def write_to_table(self, data):
        self._cur.execute('''INSERT INTO studentships VALUES (?,?,?,?,?)''', 
                          (data[0], data[1], data[2], data[3], data[4]))

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

            ns1_id = i["ns1:id"]
            tmp.append(ns1_id)

            ns1href = i["ns1:href"]
            tmp.append(ns1href)

            ns1_links = i.findAll("ns1:links")[0]
            for j in ns1_links:
                href = j["ns1:href"].split("/projects/")
                if len(href) > 1:
                    try:
                        rel = j["ns1:rel"]
                        tmp.append(rel)
                    except:
                        tmp.append("")

                    try:
                        ns1_end = j["ns1:end"]
                        tmp.append(ns1_end)
                    except:
                        tmp.append("")
                    
                    try:
                        ns1_start = j["ns1:start"]
                        tmp.append(ns1_start)
                    except:
                        tmp.append("")
                        
            if len(tmp) < 5:
                while len(tmp) < 5:
                    tmp.append("")

            database.write_to_table(tmp)
                    
            dataset.append(tmp)
            
        count += 1
                             
if __name__ == "__main__":
    run()