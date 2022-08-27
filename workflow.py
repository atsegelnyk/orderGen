from function import *
from db import *
def Workflow():


    currentOrder = generateCurrentOrder()
    # for order in currentOrder:
    #     print(order)
    #
    orderHistoryList = (generateOrderHistory(currentOrder))
    # for order in orderHistoryList:
    #     print(order)

    sql_query = generate_sql_query(orderHistoryList)
    connection = connect_to_db()
    insert_data(sql_query, connection)

