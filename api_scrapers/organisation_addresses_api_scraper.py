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
            self._cur.execute('''CREATE TABLE IF NOT EXISTS organisation_addresses (
                                 id text,
                                 Line1 text,
                                 Line2 text,
                                 Region text,
                                 Type text,
                                 Postcode text,
                                 Country text)''')
        except Exception as e:
            print(e)
            
    def write_to_table(self, data):
        self._cur.execute('''INSERT INTO organisation_addresses VALUES (?,?,?,?,?,?,?)''', 
                          (data[0], data[1], data[2], data[3], data[4], data[5], data[6]))

def run():

    dataset = []
    count = 1
    
    database = WriteToDatabase("./gtr.db")
    
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

        projects = soup.findAll("ns2:organisation")
        
        for i in projects:
            
            ns1_id = i["ns1:id"]

            tmp = []
            tmp.append(ns1_id)
            
            ns1_line1 = i.findAll("ns1:line1")
            if len(ns1_line1) > 0:
                tmp.append(ns1_line1[0].text)
            else:
                tmp.append("")

            ns1_line2 = i.findAll("ns1:line2")               
            if len(ns1_line2) > 0:
                tmp.append(ns1_line2[0].text)
            else:
                tmp.append("")

            ns1_region = i.findAll("ns1:region")
            if len(ns1_region) > 0:
                tmp.append(ns1_region[0].text)
            else:
                tmp.append("")
                
            ns1_type = i.findAll("ns1:type")
            if len(ns1_type) > 0:
                tmp.append(ns1_type[0].text)
            else:
                tmp.append("")                    

            ns1_postcode = i.findAll("ns1:postcode")
            if len(ns1_postcode) > 0:
                tmp.append(ns1_postcode[0].text)
            else:
                tmp.append("")

            try:
                ns1_country = i.findALl("ns1:country")
                if len(ns1_country) > 0:
                    tmp.append(ns1_country[0].text)
                else:
                    tmp.append("") 
            except:
                tmp.append("")

            database.write_to_table(tmp)
                
            dataset.append(tmp)
            
        count += 1
                             
if __name__ == "__main__":
    run()