"""
update_animal_db retrieves information stored in the animal_data.csv file and stores that data in the animal_database
"""
from datetime import datetime
import pandas as pd
import sqlalchemy as alc
import os


def get_id(col_id, table, col_name, value):
    """
    Retrieves id of given value from table
    :param col_id: id to be retrieved
    :param table: database table where id and value are located
    :param col_name: column of table housing value
    :param value: value of whose id will be retrieved
    :return: retrieved id
    """
    result = conn.execute(f"SELECT {col_id} FROM animal_database.{table} WHERE {col_name}=\'{value}\';")
    type_id = result.fetchone()
    return type_id


def update_ids(col_id, table, col_name, value):
    """
    Verifies if given id exists in table and adds id and value if not already present.
    :param col_id: id to be examined
    :param table: database table where id and value are located
    :param col_name: column of table housing value
    :param value: value corresponding to id
    :return: matched/retrieved id
    """
    type_id = get_id(col_id, table, col_name, value)
    if type_id is None:
        conn.execute(f"INSERT INTO animal_database.{table} ({col_name}) VALUES (\'{value}\');")
        type_id = get_id(col_id, table, col_name, value)
    return type_id

host = "localhost:3306"
user = "root"
password = "\'"

add_animal = (f"INSERT INTO animal_database.animals "
              f"(animal_id, intake_id, location_id, breed_id, sex, age, fixed, intake_date, available_date) "
              f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);")

# Create SQL engine and connect to database
engine = alc.create_engine('mysql+pymysql://{}:{}@{}/animal_database'.format(user, password, host))
conn = engine.connect()
trans = conn.begin()

# Read csv and drop empty rows
df = pd.read_csv('animal_data.csv')
df.dropna(subset=['Animal ID'], inplace=True)

# Iterate through rows of csv content and add new data to database
for index, row in df.iterrows():
    breed_id = update_ids('breed_id', 'breeds', 'breed_name', df['Breed'][index])
    location_id = update_ids('location_id', 'shelters', 'location_name', df['Location'][index])
    intake_id = update_ids('intake_id', 'intakes', 'intake_status', df['Intake Status'][index])
    intake = datetime.strptime(df['Intake Date'][index], '%B %d, %Y').date()
    available = datetime.strptime(df['Available Date'][index], '%B %d, %Y').date()
    animal_data = (df['Animal ID'][index], intake_id[0], location_id[0], breed_id[0], df['Sex'][index], df['Age'][index],
                   df['Fixed'][index], intake, available)
    conn.execute(add_animal, animal_data)

master_table = conn.execute(f"SELECT * "
                f"FROM animal_database.animals as a "
                f"JOIN animal_database.breeds as b "
                f"ON a.breed_id = b.breed_id "
                f"JOIN animal_database.shelters as l "
                f"ON a.location_id = l.location_id "
                f"JOIN animal_database.intakes as i "
                f"ON a.intake_id = i.intake_id")
master_df = pd.DataFrame(master_table.fetchall())
master_df.columns = master_table.keys()
master_df.drop(['a_id', 'intake_id', 'location_id', 'breed_id'], axis=1, inplace=True)

# Commit changes to database and close connection
trans.commit()
conn.close()

breed_table = pd.read_sql_table('breeds', engine)
location_table = pd.read_sql_table('shelters', engine)


