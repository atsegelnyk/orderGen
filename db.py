import pymysql
from setup import *
from constants import *

def connect_to_db():
    try:
        connection = pymysql.connect(
            host=dbHost,
            port=dbPort,
            user=dbUser,
            password=dbPass,
            database=dbName,
        )
        log.info("Successfully connected to db")
    except Exception as ConnectionError:
        log.error("Connection failed")
        log.error(ConnectionError)
        exit(2)
    return connection


def insert_data(insert_query, connection):
    log.info("Inserting data to db...")
    try:
        connection.query(insert_query)
        connection.commit()
    except pymysql.Error as error:
        log.error("Failed to insert query")
        log.error(error)
        exit(2)
    finally:
        log.info("Successfully inserted to db")
        log.info("Process finished!")
        connection.close()


def generate_sql_query(orderHistory):
    log.info("Generating sql query...")
    sql_query = "INSERT INTO `order_history`(`id`, `creation_date`, `change_date`, `state`, `direction`, `instrument`, `initial_volume`, `fill_volume`, `initial_price`, `fill_price`) VALUES"
    for index in range(orderHistoryRange):
        sql_query += f"({orderHistory[index][ID]}," \
                     f"'{orderHistory[index][CREATIONDATE]}'," \
                     f"'{orderHistory[index][CHANGEDATE]}'," \
                     f"'{orderHistory[index][STATE]}'," \
                     f"'{orderHistory[index][INSTRUMENT]}'," \
                     f"'{orderHistory[index][DIRECTION]}'," \
                     f"{orderHistory[index][INITALVOLUME]}," \
                     f"{orderHistory[index][FILLVOLUME]}," \
                     f"{orderHistory[index][INITALPRICE]}," \
                     f"{orderHistory[index][FILLPRICE]}),"
    log.info("Successfully generated sql query")

    return sql_query[:-1] + ";"



