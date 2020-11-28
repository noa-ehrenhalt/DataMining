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


conn = engine.connect()
trans = conn.begin()

for index, row in df.iterrows():
#    try:
    result = conn.execute(f"SELECT breed_id FROM animal_database.breeds WHERE breed_name=\'{df['Breed'][index]}\';")
    breed_id = result.fetchone()
    if breed_id == None:
        conn.execute(f"INSERT INTO animal_database.breeds (breed_name) VALUES (\'{df['Breed'][index]}\');")
#    except:
#        breed_name = (df['Breed'][index], )
#        mycursor.execute(add_breed, breed_name)
#        breed_id = mycursor.lastrowid

trans.commit()
conn.close()