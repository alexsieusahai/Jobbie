import os

import pyodbc

def get_cursor():
    cnxn_str = "DRIVER={MySQL ODBC 8.0 Driver};SERVER=jobbie-db.cpggzb24ffm6.ca-central-1.rds.amazonaws.com;DATABASE=jobbie_db;"
    cnxn_str += 'UID='+os.environ['JOBBIE_USER']+';'
    cnxn_str += 'PASSWORD='+os.environ['JOBBIE_PW']+';'
    cursor = pyodbc.connect(cnxn_str).cursor()
    return cursor
