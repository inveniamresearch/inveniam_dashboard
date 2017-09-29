# In[]:
# Import required libraries
import pandas as pd
import pickle
import MySQLdb
from controls import query2,db_info
# In[]:
# Load required dataframes
def get_dt_set():
    dataset = dict()
    
    columns1 = ['API Well Number', 'Gas Produced, MCF',
                'Water Produced, bbl','Oil Produced, bbl' ,'Reporting Year']
    db = MySQLdb.Connect('localhost','root','loinking','inveniamfundsdb_final',charset='utf8')
    #db = MySQLdb.Connect(db_info["host"],db_info["db_user"],db_info["password"],db_info["name"],charset='utf8')
    df1 = pd.read_sql_query(query2,db)
    df = pd.concat([df1])
    df.fillna(0, inplace=True)
    columns = ['Gas Produced, MCF', 'Water Produced, bbl',
               'Oil Produced, bbl', 'Reporting Year']
    for api, df_well in df.groupby('API Well Number'):
        df_well = df_well[columns]
        df_well.index = df_well['Reporting Year']
        df_well = df_well.to_dict(orient='index')
        dataset[api] = df_well
    return dataset