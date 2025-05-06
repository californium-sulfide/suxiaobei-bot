import csv
import os
import sqlite3

def get_keyword(group_id:int|str,keyword:str)->dict[str,str]:
    return {}
    pass


database_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'database')
def save_data(databasename:str,data:list)->None:
    global database_path
    try:
        with open(database_path+"/"+databasename+".csv",'w',newline='',encoding='utf-8') as csvfile:
            spamwriter=csv.writer(csvfile,delimiter=' ',quotechar='|',quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerows(data)
    except FileNotFoundError:
        with open(database_path+"/"+databasename+".csv",'x',newline='',encoding='utf-8') as csvfile:
            spamwriter=csv.writer(csvfile,delimiter=' ',quotechar='|',quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerows(data)
def load_data(databasename:str)->list[list[str]]:
    global database_path
    try:
        with open(database_path+"/"+databasename+".csv",'r',newline='',encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile,delimiter=' ',quotechar='|')
            l=[]
            for row in spamreader:
                l.append(row)
            return l
    except FileNotFoundError:
        return []