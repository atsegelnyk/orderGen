from function import *
from db import *
def Workflow():
    currentOrder = generateCurrentOrder()
    # for order in currentOrder:
    #     print(order)
    #
    orderHistoryList = (generateOrderHistory(currentOrder))
    for order in orderHistoryList:
        print(order)

    connection = connect_to_db()
