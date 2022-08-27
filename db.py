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


def generate_sql_query(ID, Create_Date, Change_Date, State, Direction, Instrument, Initial_Volume, Fill_Volume, Initial_Price, Fill_Price):
    try:
        sql_query = "INSERT INTO `history_order`(`id`, `creation date`, `change date`, `state`, `instrument`, `direction`, `initial volume`, `fill volume`, `initial price`, `fill price`) VALUES"
        for i in range(orderHistoryRange):
            sql_query += f"({ID[i]}," \
                         f"'{Create_Date[i]}'," \
                         f"'{Change_Date[i]}'," \
                         f"'{State[i]}'," \
                         f"'{Direction[i]}'," \
                         f"'{Instrument[i]}'," \
                         f"{Initial_Volume[i]}," \
                         f"{Fill_Volume[i]}," \
                         f"{Initial_Price[i]}," \
                         f"{Fill_Price[i]},"
        return sql_query[:-1] + ";"
    except Exception:
        log.error("Failed creating query")
        exit(-1)


