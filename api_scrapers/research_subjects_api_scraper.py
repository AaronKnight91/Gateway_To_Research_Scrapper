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
            self._cur.execute('''CREATE TABLE IF NOT EXISTS research_subjects (
                                 ns1id text,
                                 ns2id text,
                                 ns2text text,
                                 ns2percentage text)''')
        except Exception as e:
            print(e)
            
    def write_to_table(self, data):
        self._cur.execute('''INSERT INTO research_subjects VALUES (?,?,?,?)''', 
                          (data[0], data[1], data[2], data[3]))

def run():

    dataset = []
    count = 1
    
    database = WriteToDatabase("./gtr.db")
    
    while True:
        try:
            url = "https://gtr.ukri.org/gtr/api/projects?p=%s" % count
            print(url)
            page = requests.get(url)
        except:
            break
        
        soup = BeautifulSoup(page.content, "xml")

        failure = soup.findAll("ns1:failure")
        if len(failure) > 0:
            break
        
        projects = soup.findAll("ns2:project")
        
        soup.findAll("ns1:failure")
        
        for i in projects:
            
            #project = []
            ns1_id = str(i["ns1:id"])
                
            for j in i:
                ns2_id = j.findAll("ns2:id")
                ns2_text = j.findAll("ns2:text")               
                ns2_percentage = j.findAll("ns2:percentage")
        
                for k in range(len(ns2_id)):
                    tmp = [] 
                    tmp.append(ns1_id)
                    try:
                        tmp.append(ns2_id[k].text)
                    except:
                        tmp.append("")
                    try:
                        tmp.append(ns2_text[k].text)
                    except:
                        tmp.append("")
                    try:
                        tmp.append(ns2_percentage[k].text)
                    except:
                        tmp.append("")
                    database.write_to_table(tmp)
                        
                    dataset.append(tmp)
            
        count += 1
                             
if __name__ == "__main__":
    run()