import mysql.connector
from mysql.connector import errorcode
import sqlalchemy as alc
import pymysql
import csv
import pandas as pd

DATABASE_NAME = "animal_database"
TABLES = {}

TABLES['Breeds'] = (
  "CREATE TABLE `Breeds` ("
  " `breed_id` int NOT NULL AUTO_INCREMENT,"
  " `breed_name` varchar(45) NOT NULL,"
  " PRIMARY KEY (`breed_id`)"
  ") ENGINE=InnoDB"
)

TABLES['Shelters'] = (
  "CREATE TABLE `Shelters` ("
  " `location_id` int NOT NULL AUTO_INCREMENT,"
  " `location_name` varchar(45) NOT NULL,"
  " PRIMARY KEY (`location_id`)"
  ") ENGINE=InnoDB"
)

TABLES['Intakes'] = (
  "CREATE TABLE `Intakes` ("
  " `intake_id` int NOT NULL AUTO_INCREMENT,"
  " `intake_status` varchar(45) NOT NULL,"
  " PRIMARY KEY (`intake_id`)"
  ") ENGINE=InnoDB"
)

TABLES['Animals'] = (
  "CREATE TABLE `Animals` ("
  " `a_id` int NOT NULL AUTO_INCREMENT,"
  " `animal_id` varchar(20),"
  " `intake_id` int NOT NULL,"
  " `location_id` int NOT NULL,"
  " `breed_id` int NOT NULL,"
  " `sex` enum('Male','Female'),"
  " `age` varchar(45),"
  " `fixed` enum('Y', 'N'),"
  " `intake_date` date,"
  " `available_date` date,"
  " PRIMARY KEY (`a_id`),"
  " CONSTRAINT `Animals_ibfk_1` FOREIGN KEY (`breed_id`) "
  "     REFERENCES `Breeds` (`breed_id`) ON DELETE CASCADE,"
  " CONSTRAINT `Animals_ibfk_2` FOREIGN KEY (`location_id`) "
  "     REFERENCES `Shelters` (`location_id`) ON DELETE CASCADE,"
  " CONSTRAINT `Animals_ibfk_3` FOREIGN KEY (`intake_id`) "
  "     REFERENCES `Intakes` (`intake_id`) ON DELETE CASCADE"
  ") ENGINE=InnoDB"
)


add_breed = ("INSERT INTO Breeds "
             "(breed_name) "
             "VALUES (%s)")

add_shelters = ("INSERT INTO Shelters "
                "(location_name)"
                "VALUES (%(Location)s)")

add_intake = ("INSERT INTO Intakes "
              "(intake_status)"
              "VALUES (%(status)s)")

"""
add_animal = ("INSERT INTO Animals "
              "("
              ")")
"""



host = "localhost:3308"
user = "root"
password = "\'"

engine = alc.create_engine('mysql+pymysql://{}:{}@{}/animal_database'.format(user, password, host))
sql_data = pd.read_sql_table('Breeds', engine)


"""
mydb = mysql.connector.connect(
  host="localhost:3308",
  user="root",
  password="\'"
)
"""
mycursor = mydb.cursor()

try:
  mycursor.execute("CREATE DATABASE animal_database")
  print("Database {} created successfully".format(DATABASE_NAME))
except mysql.connector.Error as er:
  print("Error creating database: {}".format(er))


mycursor.execute("USE {}".format(DATABASE_NAME))
for table_name in TABLES:
  table_description = TABLES[table_name]
  try:
    print("Creating table {}: ".format(table_name), end='')
    mycursor.execute(table_description)
  except mysql.connector.Error as er:
    if er.errno == errorcode.ER_TABLE_EXISTS_ERROR:
      print("already exists.")
    else:
      print(er.msg)
  else:
    print("OK")



df = pd.read_csv('animal_data.csv')
df.dropna(subset=['Animal ID'], inplace=True)

for index, row in df.iterrows():
    try:
        breed_id = mycursor.execute("IF EXISTS (SELECT breed_id FROM Breeds WHERE breed_name={})"
                                    "BEGIN"
                                    "".format(df['Breed'][index]))
    except:
        breed_name = (df['Breed'][index], )
        mycursor.execute(add_breed, breed_name)
        breed_id = mycursor.lastrowid

mydb.commit()



mycursor.close()
mydb.close()




