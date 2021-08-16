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
            self._cur.execute('''CREATE TABLE IF NOT EXISTS combined_text (
                                 ns1id text,
                                 identifier text,
                                 ns2title text,
                                 consolidated_text text)''')
        except Exception as e:
            print(e)
            
    def write_to_table(self, data):
        self._cur.execute('''INSERT INTO combined_text VALUES (?,?,?,?)''', 
                          (data[0], data[1], data[2], data[3]))

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
            
            try:
                ns2_title = i.findAll("ns2:title")[0].text
                tmp.append(ns2_title)
            except:
                tmp.append("")
            
            try:
                ns2_techAbstractText = i.findAll("ns2:techAbstractText")[0].text
            except:
                ns2_techAbstractText = ""
                
            try:
                ns2_abstract_text = i.findAll("ns2:abstractText")[0].text
            except:
                ns2_abstract_text = ""
                
            try:
                ns2_potential_impact = i.findAll("ns2:potentialImpact")[0].text
            except:
                ns2_potential_impact = ""
                
            combined_text = ns2_title + " " + ns2_techAbstractText + " " + ns2_abstract_text + " " + ns2_potential_impact
            tmp.append(combined_text)
            
            database.write_to_table(tmp)
                
            dataset.append(tmp)
            
        count += 1
                             
if __name__ == "__main__":
    run()