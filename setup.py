import json
#import pymysql as sql
import logging as log

log.basicConfig(filename="log", format='%(levelname)s: %(message)s  at %(asctime)s', level=log.DEBUG)

log.info('opening config file...')
try:
    with open("conf/config.json", "r") as conf:
        data = json.load(conf)
except IOError:
    log.fatal('error opening config file.')
    exit(1)

log.info('file: config.json was opened successfully.')
log.info('initializing programm config...')

order_range = data["orderRange"]
orderHistoryRange = data["orderHistoryRange"]
alpha = data["alpha"]
module = data["module"]
step = data["step"]
volumeAlpha = data["volumeAlpha"]
volumeModule = data["volumeModule"]
volumeStep = data["volumeStep"]
timeAlpha = data["timeAlpha"]
timeModule = data["timeModule"]
timeStep = data["timeStep"]

startDate = data["startDate"]
endDate = data["endDate"]
block1 = data["startBlock1"]
block2 = data["startBlock2"]
block3 = data["startBlock3"]
timestampDiff = data["timestampDiff"]

log.info('program config initialize finished.')


log.info('opening dbConfig file...')
try:
    with open("conf/dbConfig.json", "r") as conf:
        data = json.load(conf)
except IOError:
    log.fatal('Error opening dbConfig file.')
    exit(1)

log.info('file: dbConfig.json was opened successfully.')


log.info('initializing database config...')
dbHost = data["host"]
dbPort = data["port"]
dbUser = data["user"]
dbPass = data["password"]
dbName = data["database"]

log.info('database config initialize finished.')

connectionString = ('DRIVER={MySQL ODBC 8.0 ANSI Driver};SERVER='+dbHost+';DATABASE='+dbName+';UID='+dbUser+';PWD='+dbPass)
