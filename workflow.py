from function import *
def Workflow():
    currentOrder = generateCurrentOrder()
    # for order in currentOrder:
    #     print(order)
    #
    orderHistoryList = (generateOrderHistory(currentOrder))
    for order in orderHistoryList:
        print(order)
