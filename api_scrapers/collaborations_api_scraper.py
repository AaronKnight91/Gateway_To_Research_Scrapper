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
            self._cur.execute('''CREATE TABLE IF NOT EXISTS collaborations (
                                 ns2parentorganisation text,
                                 ns2country text,
                                 ns2childorganisation text,
                                 project text,
                                 ns1id text,
                                 org_and_dep text)''')
        except Exception as e:
            print(e)
            
    def write_to_table(self, data):
        self._cur.execute('''INSERT INTO collaborations VALUES (?,?,?,?,?,?)''', 
                          (data[0], data[1], data[2], data[3], data[4], data[5]))

def run():

    dataset = []
    count = 1
    
    database = WriteToDatabase("./gtr.db")
    
    while True:
        try:
            url =  "https://gtr.ukri.org/gtr/api/outcomes/collaborations?p=%s" % count
            print(url)
            page = requests.get(url)
        except:
            break
        
        soup = BeautifulSoup(page.content, "xml")
        
        failure = soup.findAll("ns1:failure")
        if len(failure) > 0:
            break
        
        projects = soup.findAll("ns2:collaboration")

        for i in projects:
            tmp = []            
            ns2_parentorganisation = i.findAll("ns2:parentOrganisation")[0].text
            tmp.append(ns2_parentorganisation)

            try:
                ns2_country = i.findAll("ns2:country")[0].text
            except:
                ns2_country = ""
            tmp.append(ns2_country)
                        
            try:
                ns2_childorganisation = i.findAll("ns2:childOrganisation")[0].text
            except:
                ns2_childorganisation = ""
            tmp.append(ns2_childorganisation)

            try:
                project = i.findAll("ns1:link")[0]
                project = project["ns1:href"]
            except:
                project = ""
            tmp.append(project)
            
            try:
                ns1_id = project.split("/")[-1]
            except:
                ns1_id = ""
            tmp.append(ns1_id)
            
            try:
                org_and_dep = ns2_parentorganisation + " / " + ns2_childorganisation
            except:
                org_and_dep = ""
            tmp.append(org_and_dep)
            
            database.write_to_table(tmp)
                    
            dataset.append(tmp)
            
        count += 1
                             
if __name__ == "__main__":
    run()