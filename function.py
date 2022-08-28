from datetime import datetime
from setup import *
from constants import *


def percentage(percent, number):
    percentage = number / 100 * percent
    return percentage


def psrand(alpha, module, step, number):
    previous = 0
    data_arr = []
    for i in range(number):
        current = ((alpha * previous + step) % module)
        data_arr.append(current)
        previous = current
    return data_arr


def initial_volumes_generate(alpha, module, step, number):
    previous = 0
    data_arr2 = []
    for i in range(number):
        current = ((alpha * previous + step) % module) + ivgStep
        data_arr2.append(round(current, 1))
        previous = current
    return data_arr2

data_arr = psrand(alpha, module, step, order_range)
data_arr2 = initial_volumes_generate(volumeAlpha, volumeModule, volumeStep, order_range)


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
        temp = (data_arr[i] % dgVal)
        if temp == dgEqVal:
            direction_arr.append(sellValue)
        else:
            direction_arr.append(buyValue)
    return direction_arr


def pair_generate(data_arr):
    pair_arr = []
    for i in range(order_range):
        temp = (data_arr[i] % pgValue)
        if temp == pgEqVal0:
            pair_arr.append(pair1)
        elif temp == pgEqVal1:
            pair_arr.append(pair2)
        elif temp == pgEqVal2:
            pair_arr.append(pair3)
        else:
            pair_arr.append(pair4)
    return pair_arr


def initial_price_generate(data_arr):
    prices = []
    for i in range(order_range):
        if ipgAmount0 < data_arr[i] % ipgFullAmount <= ipgAmount1:
            prices.append(initalPricesArr[0])
        elif ipgAmount1 < data_arr[i] % ipgFullAmount <= ipgAmount2:
            prices.append(initalPricesArr[1])
        elif ipgAmount2 < data_arr[i] % ipgFullAmount <= ipgAmount3:
            prices.append(initalPricesArr[2])
        elif ipgAmount3 < data_arr[i] % ipgFullAmount <= ipgAmount4:
            prices.append(initalPricesArr[3])
        elif ipgAmount4 < data_arr[i] % ipgFullAmount <= ipgAmount5:
            prices.append(initalPricesArr[4])
        elif ipgAmount5 < data_arr[i] % ipgFullAmount <= ipgAmount6:
            prices.append(initalPricesArr[5])
        elif ipgAmount6 < data_arr[i] % ipgFullAmount <= ipgAmount7:
            prices.append(initalPricesArr[6])
        else:
            prices.append(initalPricesArr[7])

    return prices


def fill_prices_generate(data_arr, initalPrice, direction):
    fillPricesArr = []
    for i in range(order_range):
        if direction == buyValue:
            fillPricesArr.append(round(float(initalPrice[i]) - (float(initalPrice[i]) / float(data_arr[i])), 2))
        else:
            fillPricesArr.append(round(float(initalPrice[i]) + (float(initalPrice[i]) / float(data_arr[i])), 2))

    return fillPricesArr


def generateCurrentOrder():
    ids = id_generate(data_arr)
    dates = date_generate(data_arr)
    changeDates = date_generate(data_arr)
    directions = direction_generate(data_arr)
    pairs = pair_generate(data_arr)
    initialVolumes = data_arr2
    initialPrices = initial_price_generate(data_arr)
    fillPrices = fill_prices_generate(data_arr2, initialPrices, directions)
    currentOrder = []
    for row in range(order_range):
        currentOrder.append([
            ids[row],
            dates[row],
            changeDates[row],
            state1,
            directions[row],
            pairs[row],
            initialVolumes[row],
            gcoFillPrice,
            initialPrices[row],
            fillPrices[row]
        ])

    return currentOrder


def change_date_generate(date, count):
    diff = data_arr[count] / cdPart + cdAdd
    dateTimestamp = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').timestamp()
    if dateTimestamp + diff in range(block1, block1 + timestampDiff):
        changedDate = str(datetime.fromtimestamp(dateTimestamp + diff + timestampDiff).replace(microsecond=microsecond))
    elif dateTimestamp + diff in range(block2, block2 + timestampDiff):
        changedDate = str(datetime.fromtimestamp(dateTimestamp + diff + timestampDiff).replace(microsecond=microsecond))
    elif dateTimestamp + diff in range(block3, block3 + timestampDiff):
        changedDate = str(datetime.fromtimestamp(dateTimestamp + diff + timestampDiff).replace(microsecond=microsecond))
    else:
        changedDate = str(datetime.fromtimestamp(dateTimestamp + diff).replace(microsecond=microsecond))
    return changedDate


def update_state(state, psrand_arr, count):
    if state == state1:
        updState = state2
    elif state == state2:
        if psrand_arr[count] % usVal == usVal0:
            updState = state4
        elif psrand_arr[count] % usVal == usVal1:
            updState = state3
        else:
            updState = state5
    else:
        updState = state6

    return updState


def update_fill_volumes(initalVolume, state, psrand_arr, count):
    if state == state1 or state == state5 or state == state2:
        updFillVolume = 0
    elif state == state3 or state == state6:
        updFillVolume = initalVolume
    else:
        if psrand_arr[count] % ufvAmount == ufvValue:
            updFillVolume = initalVolume + ivgStep
        else:
            updFillVolume = initalVolume - ivgStep
    return round(updFillVolume, 2)


def update_fill_price(initalPrice, direction, psrand_arr, count):
    global updFillPrice
    expression = eval(ufpExpression)
    if direction == buyValue:

        match expression:
            case 1:
                updFillPrice = initalPrice - percentage(randPercent1, initalPrice)
            case 3:
                updFillPrice = initalPrice - percentage(randPercent2, initalPrice)
            case 5:
                updFillPrice = initalPrice - percentage(randPercent3, initalPrice)
            case 7:
                updFillPrice = initalPrice - percentage(randPercent4, initalPrice)
            case 9:
                updFillPrice = initalPrice - percentage(randPercent5, initalPrice)

    else:
        match expression:
            case 1:
                updFillPrice = initalPrice + percentage(randPercent1, initalPrice)
            case 3:
                updFillPrice = initalPrice + percentage(randPercent2, initalPrice)
            case 5:
                updFillPrice = initalPrice + percentage(randPercent3, initalPrice)
            case 7:
                updFillPrice = initalPrice + percentage(randPercent4, initalPrice)
            case 9:
                updFillPrice = initalPrice + percentage(randPercent5, initalPrice)

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
                                         update_fill_volumes(currentOrderList[order][INITALVOLUME],
                                                             update_state(currentOrderList[order][STATE], data_arr,
                                                                          order), data_arr, order),
                                         currentOrderList[order][INITALPRICE],
                                         update_fill_price(currentOrderList[order][INITALPRICE],
                                                           currentOrderList[order][STATE], data_arr, order)
                                         ])
        for order in tempCurrentOrderList:
            orderHistory.append(order)
        currentOrderList = []
        for order in tempCurrentOrderList:
            currentOrderList.append(order)
        tempCurrentOrderList = []

    return orderHistory
