"""
animal_db creates animal_database and its associated table
"""
import mysql.connector
from mysql.connector import errorcode
from configparser import ConfigParser
import logging
logger = logging.getLogger(__name__)

# Reads config file
config_object = ConfigParser()
config_object.read('config.ini')
serverinfo = config_object['SERVERCONFIG']

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
  " `sex` varchar(20),"
  " `age` varchar(45),"
  " `fixed` varchar(45),"
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

# Creates MySQL connection
mydb = mysql.connector.connect(
  host=serverinfo['host'],
  user=serverinfo['user'],
  password=serverinfo['password'],
  auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor(buffered=True)

# Creates animal_database, prints statement if database exists or error is encountered during database creation
try:
    mycursor.execute("CREATE DATABASE animal_database")
    logger.info("Database {} created successfully".format(DATABASE_NAME))
except mysql.connector.Error as er:
    logger.info("Error creating database: {}".format(er))

# Creates tables for animal_database, prints statement if tables exist or error is encountered during table creation
mycursor.execute("USE {}".format(DATABASE_NAME))
for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        logger.info("Creating table {}: ".format(table_name), end='')
        mycursor.execute(table_description)
    except mysql.connector.Error as er:
        if er.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            logger.info("already exists.")
        else:
            logger.error(er.msg)
    else:
        logger.info("OK")

mycursor.execute("SELECT animal_id FROM animal_database.animals;")
id_list = list(mycursor.fetchall())
database_ids = [a_id[0] for a_id in id_list]

# Closes database connection
mycursor.close()
mydb.close()




