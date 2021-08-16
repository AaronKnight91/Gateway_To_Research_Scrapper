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
            self._cur.execute('''CREATE TABLE IF NOT EXISTS participant_values (
                                 ns1id text,
                                 ns2participant text,
                                 ns2organisationid text,
                                 ns2organisationname text,
                                 ns2role text,
                                 ns2projectcost text,
                                 ns2grantoffer text)''')
        except Exception as e:
            print(e)
            
    def write_to_table(self, data):
        self._cur.execute('''INSERT INTO participant_values VALUES (?,?,?,?,?,?,?)''', 
                          (data[0], data[1], data[2], data[3], data[4], data[5], data[6]))

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

            participants = soup.findAll("ns2:participantValues")
            for j in participants:

                try:
                    ns2_participant = i.findAll("ns2:participant")[0].text
                    tmp.append(ns2_participant)
                except:
                    tmp.append("")

                try:                
                    ns2_organisationid = j.findAll("ns2:organisationId")[0].text
                    tmp.append(ns2_organisationid)
                except:
                    tmp.append("")
    
                try:
                    ns2_organisationname = j.findAll("ns2:organisationName")[0].text
                    tmp.append(ns2_organisationname)
                except:
                    tmp.append("")
                
                try:
                    ns2_role = j.findAll("ns2:role")[0].text
                    tmp.append(ns2_role)
                except:
                    tmp.append("")
    
                try:
                    ns2_projectcost = j.findAll("ns2:projectCost")[0].text
                    tmp.append(ns2_projectcost)
                except:
                    tmp.append("")
    
                try:
                    ns2_grantoffer = j.findAll("ns2:grantOffer")[0].text
                    tmp.append(ns2_grantoffer)
                except:
                    tmp.append("")
                        
                database.write_to_table(tmp)
                    
                dataset.append(tmp)
            
        count += 1
                             
if __name__ == "__main__":
    run()