from function import *
from db import *


def workflow():
    currentOrder = generateCurrentOrder()
    orderHistoryList = (generateOrderHistory(currentOrder))
    sql_query = generate_sql_query(orderHistoryList)
    connection = connect_to_db()
    insert_data(sql_query, connection)
    print("Process finished!")
