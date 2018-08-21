import os
import csv
from datetime import date, timedelta, datetime

import mysql.connector

from exporter import exporter
from trade import trade


def main():

    cnx = mysql.connector.connect(user='remote', password='remote',
                                  host='192.168.0.16',
                                  database='gekkoTests')


    startingDate = datetime(2018,7,24)

   # startingDate.date.replace()

    dateDelta = 30
    currencyToTrade = 'ETH'
    assetToTrade = 'V'
    candle_Size_Minutes = 15
    warmup_Size_Minutes = 55
    tradeExchange = 'binance'
    Initial_Assets = 100
    Initial_Currency = 100
    strat = 'McKee_EMA_RSI_Strat_Stoploss'
    trader = trade(startingDate, dateDelta, currencyToTrade, assetToTrade, candle_Size_Minutes, warmup_Size_Minutes,
                     tradeExchange, Initial_Assets, Initial_Currency, strat, cnx)
    #trader.run(True)

    #trader.Initial_Assets = 100
    #trader.Initial_Currency = 0

    #trader.run(False)



    while True:
        trader.start_date = trader.start_date - timedelta(dateDelta)
        trader.asset = 'EOS'
        trader.run(False)
        trader.asset = 'ZRX'
        trader.run(False)
        trader.asset = 'TRX'
        trader.run(True)



if __name__ == "__main__":
    main()

# PLAN
# Delete database.csv
# run a test
# take specific data from new database.csv
# put into mysql
