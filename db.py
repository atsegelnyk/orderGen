import pymysql
from setup import *

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
    except pymysql.Error as ConnectionError:
        log.error("Connection failed")
        log.error(ConnectionError)
        exit(-1)
    return connection


def insert_data(insert_query):
    connection = connect_to_db()
    try:
        connection.query(insert_query)
        connection.commit()
    except pymysql.Error as error:
        log.error("Failed to insert query")
        log.error(error)
        exit(-1)
    finally:
        connection.close()


def generate_sql_query(orderHistory):
    try:
        sql_query = "INSERT INTO `history_order`(`id`, `creation_date`, `change_date`, `state`, `instrument`, `direction`, `initial_volume`, `fill_volume`, `initial_price`, `fill_price`) VALUES"
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
                         f"{orderHistory[index][FILLPRICE]},"
        return sql_query[:-1] + ";"
    except Exception:
        log.error("Failed creating query")
        exit(-1)


