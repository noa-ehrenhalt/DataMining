import pymysql
import pandas as pd
import sqlalchemy as alc

host = "localhost:3306"
user = "root"
password = "\'"

engine = alc.create_engine('mysql+pymysql://{}:{}@{}/animal_database'.format(user, password, host))
sql_data = pd.read_sql_table('breeds', engine)


df = pd.read_csv('animal_data.csv')
df.dropna(subset=['Animal ID'], inplace=True)

def get_id(col_id, table, col_name, value):
    result = conn.execute(f"SELECT {col_id} FROM animal_database.{table} WHERE {col_name}=\'{value}\';")
    type_id = result.fetchone()
    return type_id

def update_ids(col_id, table, col_name, value):
    type_id = get_id(col_id, table, col_name, value)
    if type_id == None:
        conn.execute(f"INSERT INTO animal_database.{table} ({col_name}) VALUES (\'{value}\');")
        type_id = get_id(col_id, table, col_name, value)
    return type_id


conn = engine.connect()
trans = conn.begin()

for index, row in df.iterrows():

    breed_id = update_ids('breed_id', 'breeds', 'breed_name', df['Breed'][index])
    location_id = update_ids('location_id', 'shelters', 'location_name', df['Location'][index])
    intake_id = update_ids('intake_id', 'intakes', 'intake_status', df['Intake Status'][index])

trans.commit()
conn.close()