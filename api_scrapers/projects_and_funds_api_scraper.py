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
            self._cur.execute('''CREATE TABLE IF NOT EXISTS projects_and_funds (
                                 ns1id text,
                                 pound text,
                                 ns1end text,
                                 ns1start text,
                                 ns1href text,
                                 ns2valuespounds_ns1amount text,
                                 project_link text,
                                 identifier text)''')
        except Exception as e:
            print(e)
            
    def write_to_table(self, data):
        # print(data)
        self._cur.execute('''INSERT INTO projects_and_funds VALUES (?,?,?,?,?,?,?,?)''', 
                          (data[0], data[1], data[2], data[3], 
                           data[4], data[5], data[6], data[7]))

class ReadFromDatabase():
    
    def __init__(self, database):
        self._database = database

        self.create_connection()
        
    def create_connection(self):
        self._conn = None
        try:
            self._conn = sqlite3.connect(self._database)
        except Exception as e:
            print(e)

    def query_database(self, ns1_id):
        try:
            self._cur = self._conn.cursor()
            identifier = self._cur.execute('''SELECT identifier FROM identifier_project_lookup
                                           WHERE ns1id="%s"''' % ns1_id)
        except Exception as e:
            print(e)

        return identifier

def run():

    dataset = []
    count = 1
    
    database = WriteToDatabase("./asd.db")
    
    while True:
        try:
            url =  "https://gtr.ukri.org/gtr/api/funds?p=%s" % count
            print(url)
            page = requests.get(url)
        except:
            break
        
        soup = BeautifulSoup(page.content, "xml")

        failure = soup.findAll("ns1:failure")
        if len(failure) > 0:
            break
        
        funds = soup.findAll("ns2:fund")
        
        for i in funds:
            
            ns1_id = i["ns1:id"]
                
            tmp = []
            tmp.append(ns1_id)

            # Not correct! Check documentation
            try:
                ns2_value_pounds = i.findAll("ns2:valuePounds")[0]
                ns2_value_pounds = ns2_value_pounds["ns1:amount"]
                if len(ns2_value_pounds) > 0:
                    tmp.append(ns2_value_pounds)
                else:
                    tmp.append("")
            except:
                tmp.append("")
                
            ns1_link = i.findAll("ns1:link")[0]
            try:
                ns1_end = ns1_link["ns1:end"]                
                if len(ns1_end) > 0:
                    tmp.append(ns1_end)
                else:
                    tmp.append("")
            except:
                tmp.append("")
            
            try:
                ns1_start = ns1_link["ns1:start"] 
                if len(ns1_start) > 0:
                    tmp.append(ns1_start)
                else:
                    tmp.append("")
            except:
                tmp.append("")

            try:
                ns1_href = i["ns1:href"]
                if len(ns1_href) > 0:
                    tmp.append(ns1_href)
                else:
                    tmp.append("")
            except:
                tmp.append("")

            try:
                ns2_pounds = i.findAll("ns2:valuePounds")
                ns1_amount = ns2_pounds["ns1_amount"]
                if len(ns1_amount) > 0:
                    tmp.append(ns1_amount)
                else:
                    tmp.append("")
            except:
                tmp.append("")

            try:
                project_link = ""
                ns1_links = i.findAll("ns1:links")[0]
                for i in ns1_links:
                    ns1_href = i["ns1:href"].split("projects/")
                    if len(ns1_href) > 1:
                        project_link = ns1_href[-1]
                    else:
                        continue
                    tmp.append(project_link)
            except:
                tmp.append("")

            try:
                identifier = ""
                query = ReadFromDatabase("./gtr.db")
                identifier = query.query_database(ns1_id)
                tmp.append(identifier)
            except:
                tmp.append("")

            database.write_to_table(tmp)
                    
            dataset.append(tmp)
            
        count += 1
                             
if __name__ == "__main__":
    run()