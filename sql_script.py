import sqlite3
import pandas as pd
import mysql.connector
from constants import *

class db_operations():
    def __init__(self,):
        self.mydb = mysql.connector.connect(host=LOCALHOST, user=USER_NAME,password=PASSWORD,database=DB_NAME)
        self.cursor = self.mydb.cursor()

    def insert_data(self,values):
        print("insert_data")
        print(values)
        query = "insert into data (name, location, organization) VALUES (%s, %s, %s)"
        self.cursor.execute(query,values)
        self.mydb.commit()

    def fetch_data(self):
        data=self.cursor.execute('''Select * from DATA''')
        if data:
            print(pd.DataFrame(data,columns=['name','location','organization']))
        else:
            print("no data found...")