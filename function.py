from datetime import datetime
from setup import *
from constants import *

def percentage(percent, number):
  percentage = number/100*percent
  return percentage


def condition(todo, expression=None, eq=None, expected=None):
    if expression == 0:
        exec(todo)
    else:
        if eq == 'equals':
            if eval(expression) == eval(expected):
                exec(todo)
        elif eq == 'less':
            if eval(expression) <= eval(expected):
                exec(todo)
        elif eq == "greater":
            if eval(expression) >= eval(expected):
                exec(todo)


def psrand(alpha, module, step, number):
    previous = 0
    data_arr = []
    for i in range(number):
        current = ((alpha * previous + step) % module)
        data_arr.append(current)
        previous = current
    return data_arr

def inital_volumes_generate(alpha, module, step, number):
    previous = 0
    data_arr2 = []
    for i in range(number):
        current = ((alpha * previous + step) % module) + 0.1
        data_arr2.append(round(current, 1))
        previous = current
    return data_arr2

data_arr = psrand(alpha, module, step, order_range)
data_arr2 = inital_volumes_generate(volumeAlpha, volumeModule, volumeStep, order_range)


def id_generate(data_arr):
    id_arr = []
    for i in range(order_range):
        id_arr.append(data_arr[i])
    return id_arr


def date_generate(data_arr):
    temp = startDate
    creationDateArr = []
    for i in range(order_range):
        timestamp = temp + data_arr[i]
        temp += data_arr[i]
        creationDateArr.append(str(datetime.fromtimestamp(timestamp)))
    return creationDateArr


def direction_generate(data_arr):
    direction_arr = []
    for i in range(order_range):
        temp = (data_arr[i] % 3)
        if (temp == 0):
            direction_arr.append("sell")
        else:
            direction_arr.append("buy")
    return direction_arr


def pair_generate(data_arr):
    pair_arr = []
    for i in range(order_range):
        temp = (data_arr[i] % 10)
        if temp == 1:
            pair_arr.append("EURUSD")
        elif temp == 3:
            pair_arr.append("USDJPY")
        elif temp == 5:
            pair_arr.append("GBPUSD")
        else:
            pair_arr.append("USDCHF")
    return pair_arr


def inital_price_generate(data_arr):
    prices = []
    for i in range(order_range):
        if data_arr[i] % 100 > 0 and data_arr[i] % 100 <= 12:
            prices.append(initalPricesArr[0])
        elif data_arr[i] % 100 > 12 and data_arr[i] % 100 <= 24:
            prices.append(initalPricesArr[1])
        elif data_arr[i] % 100 > 24 and data_arr[i] % 100 <= 36:
            prices.append(initalPricesArr[2])
        elif data_arr[i] % 100 > 36 and data_arr[i] % 100 <= 48:
            prices.append(initalPricesArr[3])
        elif data_arr[i] % 100 > 48 and data_arr[i] % 100 <= 60:
            prices.append(initalPricesArr[4])
        elif data_arr[i] % 100 > 60 and data_arr[i] % 100 <= 72:
            prices.append(initalPricesArr[5])
        elif data_arr[i] % 100 > 72 and data_arr[i] % 100 <= 84:
            prices.append(initalPricesArr[6])
        else:
            prices.append(initalPricesArr[7])

    return prices

def fill_prices_generate(data_arr, initalPrice, direction):
    fillPricesArr = []
    for i in range(order_range):
        if direction == "buy":
            fillPricesArr.append(round(float(initalPrice[i]) - (float(initalPrice[i]) / float(data_arr[i])), 2))
        else:
            fillPricesArr.append(round(float(initalPrice[i]) + (float(initalPrice[i]) / float(data_arr[i])), 2))

    return fillPricesArr


def generateCurrentOrder():
    ids = id_generate(data_arr)
    dates = date_generate(data_arr)
    changeDates = date_generate(data_arr)
    states = []
    directions = direction_generate(data_arr)
    pairs = pair_generate(data_arr)
    initalVolumes = data_arr2
    fillVolumes = []
    initalPrices = inital_price_generate(data_arr)
    fillPrices = fill_prices_generate(data_arr2, initalPrices, directions)
    currentOrder = []
    for row in range(order_range):
        currentOrder.append([
                            ids[row],
                            dates[row],
                            changeDates[row],
                            "new",
                            directions[row],
                            pairs[row],
                            initalVolumes[row],
                            0,
                            initalPrices[row],
                            fillPrices[row]
                            ])

    return currentOrder


def change_date_generate(date, count):
    diff = data_arr[count]/10 + 1
    dateTimestamp = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').timestamp()
    if dateTimestamp + diff in range(block1, block1 + timestampDiff):
        changedDate = str(datetime.fromtimestamp(dateTimestamp + diff + timestampDiff).replace(microsecond=0))
    elif dateTimestamp + diff in range(block2, block2 + timestampDiff):
        changedDate = str(datetime.fromtimestamp(dateTimestamp + diff + timestampDiff).replace(microsecond=0))
    elif dateTimestamp + diff in range(block3, block3 + timestampDiff):
        changedDate = str(datetime.fromtimestamp(dateTimestamp + diff + timestampDiff).replace(microsecond=0))
    else:
        changedDate = str(datetime.fromtimestamp(dateTimestamp + diff).replace(microsecond=0))
    return changedDate


def update_state(state, psrand_arr, count):
    if state == "new":
        updState = "inProcess"

    elif state == "inProcess":
        if psrand_arr[count] % 3 == 0:
            updState = "partialFill"
        elif psrand_arr[count] % 3 == 1:
            updState = "fill"
        else:
            updState = "cancelled"

    else: #state == "fill" or state == "partialFill" or state == "cancelled":
        updState = "done"

    return updState


def update_fill_volumes(initalVolume, state, psrand_arr, count):
    if state == "new" or state == "cancelled" or state == "inProcess":
        updFillVolume = 0
    elif state == "fill" or state == "done":
        updFillVolume = initalVolume
    else:
        if psrand_arr[count] % 4 == 1:
            updFillVolume = initalVolume + 0.1
        else:
            updFillVolume = initalVolume - 0.1
    return round(updFillVolume, 2)


def update_fill_price(initalPrice, direction, psrand_arr, count):
    expression = eval('psrand_arr[count] % 10')
    if direction == "buy":

        match expression:
            case 1: updFillPrice = initalPrice - percentage(1, initalPrice)
            case 3: updFillPrice = initalPrice - percentage(2, initalPrice)
            case 5: updFillPrice = initalPrice - percentage(3, initalPrice)
            case 7: updFillPrice = initalPrice - percentage(4, initalPrice)
            case 9: updFillPrice = initalPrice - percentage(5, initalPrice)

    else:
        match expression:
            case 1: updFillPrice = initalPrice + percentage(1, initalPrice)
            case 3: updFillPrice = initalPrice + percentage(2, initalPrice)
            case 5: updFillPrice = initalPrice + percentage(3, initalPrice)
            case 7: updFillPrice = initalPrice + percentage(4, initalPrice)
            case 9: updFillPrice = initalPrice + percentage(5, initalPrice)

    return round(updFillPrice, 3)


def generateOrderHistory(currentOrderList):
    orderHistory = []
    tempCurrentOrderList = []
    for order in currentOrderList:
        orderHistory.append(order)


    for update in range(update_range):
        for order in range(order_range):
            tempCurrentOrderList.append([currentOrderList[order][ID],
                                 currentOrderList[order][CREATIONDATE],
                                 change_date_generate(currentOrderList[order][CHANGEDATE], order),
                                 update_state(currentOrderList[order][STATE], data_arr, order),
                                 currentOrderList[order][INSTRUMENT],
                                 currentOrderList[order][DIRECTION],
                                 currentOrderList[order][INITALPRICE],
                                 update_fill_volumes(currentOrderList[order][INITALVOLUME], update_state(currentOrderList[order][STATE], data_arr, order), data_arr, order),
                                 currentOrderList[order][INITALPRICE],
                                 update_fill_price(currentOrderList[order][INITALPRICE], currentOrderList[order][STATE], data_arr, order)
                                 ])
        for order in tempCurrentOrderList:
            orderHistory.append(order)
        currentOrderList = []
        for order in tempCurrentOrderList:
            currentOrderList.append(order)
        tempCurrentOrderList = []

    return orderHistory






