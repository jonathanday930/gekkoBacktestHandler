import os
import csv
from datetime import date, timedelta, datetime

import mysql.connector

from exporter import exporter
from trade import trade


def main():

    cnx = mysql.connector.connect(user='remote', password='remote',
                                  host='192.168.0.11',
                                  database='gekkoTests')
    print("hello BITCH")

    startingDate = datetime(2018,4,14)

   # startingDate.date.replace()

    dateDelta = 1
    currencyToTrade = 'BTC'
    assetToTrade = 'VEN'
    candle_Size_Minutes = 10
    warmup_Size_Minutes = 10
    tradeExchange = 'binance'
    Initial_Assets = 0
    Initial_Currency = 1
    strat = 'MACD'
    newTrade = trade(startingDate, dateDelta, currencyToTrade, assetToTrade, candle_Size_Minutes, warmup_Size_Minutes,
                     tradeExchange, Initial_Assets, Initial_Currency, strat, cnx)
    newTrade.run()


if __name__ == "__main__":
    main()

# PLAN
# Delete database.csv
# run a test
# take specific data from new database.csv
# put into mysql
