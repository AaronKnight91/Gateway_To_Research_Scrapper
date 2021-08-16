# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter

class GtrProjectsPipeline:
    
    def __init__(self):

        self.create_connection()
        self.create_table()        
            
    def create_connection(self):
        
        self.conn = sqlite3.connect("gtr.db")
        self.cur = self.conn.cursor()
        
    def create_table(self):
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS projects(id integer PRIMARY KEY,
                         GtR_Project_URL text,                   
                         Project_Reference text,
                         Project_Category text,
                         Title text,
                         Lead_Organisation text,
                         Department text,
                         Abstract text,
                         Technical_Summary text,        
                         Planned_Impact text,
                         Funder text,
                         Project_Status text,
                         Funded_Period_Start text,
                         Funded_Period_End text,
                         Total_Fund int,
                         Expenditure text,
                         Principle_Investigator_First_Name text,
                         Principle_Investigator_Last_Name text,
                         Principle_Investigator_Other_Name text,
                         Student_First_Name text,
                         Student_Last_Name text,
                         Student_Other_Name text,
                         Lead_Organisation_ID text,
                         Lead_Organisation_URL text,
                         Post_Code text,
                         Region text)""")
    
    def process_item(self, item, spider):
        
        self.store_db(item)        
        
        return item

    def store_db(self, item):
        
        print(item["Region"], type(item["Region"]))
        self.cur.execute("""INSERT INTO projects VALUES 
                         (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", 
                         (item["GtR Project URL"], item["Project Reference"], 
                          item["Project Category"], item["Title"], item["Lead Organisation"], 
                          item["Department"], item["Abstract"], item["Technical Summary"], 
                          item["Planned Impact"], item["Funder"], item["Project Status"], 
                          item["Funded Period Start"], item["Funded Period End"], 
                          item["Total Fund"], item["Expenditure"], 
                          item["Principle Investigator First Name"], 
                          item["Principle Investigator Last Name"], 
                          item["Principle Investigator Other Name"], item["Student First Name"], 
                          item["Student Last Name"], item["Student Other Name"], 
                          item["Lead Organisation ID"], item["Lead Organisation URL"], 
                          item["Post Code"], item["Region"]))
        
        self.conn.commit()
        
class GtrProjectOrganisationsPipeline:
    
    def __init__(self):

        self.create_connection()
        self.create_table()        
        
    def create_connection(self):
        
        self.conn = sqlite3.connect("gtr.db")
        self.cur = self.conn.cursor()
        
    def create_table(self):
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS project_organisations(id integer PRIMARY KEY,
                         Project_Reference text,
                         Title text,
                         Lead_Organisation_ID text,
                         Lead_Organisation_URL text,
                         Organisation text,
                         Organisation_Role text,
                         Organisation_URL text,
                         Organisation_ID text,
                         Project_Cost text,
                         Grant_Offer text)""")
        
    def process_item(self, item, spider):
        
        self.store_db(item)        
        
        return item

    def store_db(self, item):
        
        self.cur.execute("""INSERT INTO project_organisations VALUES 
                         (NULL,?,?,?,?,?,?,?,?,?,?)""", 
                         (item["Project Reference"], item["Title"], item["Lead Organisation ID"],
                          item["Lead Organisation URL"], item["Organisations"], 
                          item["Organisation Role"], item["Organisation URL"],
                          item["Organisation ID"], item["Project Cost"],
                          item["Grant Offer"]))
        
        self.conn.commit()

class GtrProjectPeoplePipeline:
    
    def __init__(self):

        self.create_connection()
        self.create_table()        
        
    def create_connection(self):
        
        self.conn = sqlite3.connect("gtr.db")
        self.cur = self.conn.cursor()
        
    def create_table(self):
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS project_people(id integer PRIMARY KEY,
                         Project_Reference text,
                         Title text,
                         Lead_Organisation_ID text,
                         Lead_Organisation_URL text,
                         People text,
                         Person_Role text)""")
        
    def process_item(self, item, spider):
        
        self.store_db(item)        
        
        return item

    def store_db(self, item):
        
        self.cur.execute("""INSERT INTO project_people VALUES 
                         (NULL,?,?,?,?,?,?)""", 
                         (item["Project Reference"], item["Title"], item["Lead Organisation ID"],
                          item["Lead Organisation URL"], item["People"],
                          item["Person Role"]))
        
        self.conn.commit()
        
class GtrOrganisationsPipeline:
    
    def __init__(self):

        self.create_connection()
        self.create_table()        
        
    def create_connection(self):
        
        self.conn = sqlite3.connect("gtr.db")
        self.cur = self.conn.cursor()
        
    def create_table(self):
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS organisations(id integer PRIMARY KEY,
                         Organisation_Name text,
                         Organisation_URL text,
                         Organisation_ID text,
                         Address text,
                         Region text)""")
    
    def process_item(self, item, spider):
        
        self.store_db(item)        
        
        return item

    def store_db(self, item):
        
        self.cur.execute("""INSERT INTO organisations VALUES 
                         (NULL,?,?,?,?,?)""", 
                         (item["Organisation Name"], item["Organisation URL"],
                          item["Organisation ID"], item["Address"], item["Region"]))
        
        self.conn.commit()

class GtrPeoplePipeline:
    
    def __init__(self):

        self.create_connection()
        self.create_table()                
    
    def create_connection(self):
        
        self.conn = sqlite3.connect("gtr.db")
        self.cur = self.conn.cursor()
        
    def create_table(self):
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS people(id integer PRIMARY KEY,
                         Name text,
                         First_Name text,
                         Last_Name text,
                         Organisation text)""")
    
    def process_item(self, item, spider):
        
        self.store_db(item)        
        
        return item

    def store_db(self, item):
        
        self.cur.execute("""INSERT INTO people VALUES 
                         (NULL,?,?,?,?)""", 
                         (item["Name"], item["First Name"], item["Last Name"],
                          item["Organisation"]))

        self.conn.commit()

class GtrFundsPipeline:
    
    def __init__(self):

        self.create_connection()
        self.create_table()                
    
    def create_connection(self):
        
        self.conn = sqlite3.connect("gtr.db")
        self.cur = self.conn.cursor()
        
    def create_table(self):
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS funds(id integer PRIMARY KEY,
                         Project_Reference text,
                         Funder text,
                         Project_Status text,
                         Funded_Period_Start text,
                         Funded_Period_End text,
                         Total_Fund text,
                         Expenditure text)""")
    
    def process_item(self, item, spider):
        
        self.store_db(item)        
        
        return item

    def store_db(self, item):
        
        self.cur.execute("""INSERT INTO funds VALUES 
                         (NULL,?,?,?,?,?,?,?)""", 
                         (item["Project Reference"], item["Funder"], item["Project Status"],
                          item["Funded Period Start"], item["Funded Period End"],
                          item["Total Fund"], item["Expenditure"]))

        self.conn.commit()
