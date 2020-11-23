import mysql.connector
from mysql.connector import errorcode

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

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="\'"
)

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

mycursor.close()
mydb.close()




