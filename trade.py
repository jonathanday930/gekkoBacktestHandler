import csv
import datetime
import sys

from exporter import exporter
import os
from datetime import date


class trade:
    rootPassword = ''

    data_exporter = ''

    asset = ''
    currency = ''
    start_date = ''
    day_delta = ''
    exchange = ''

    candle_Size_Min = 0
    warmup_Size_Min = 0

    Initial_Assets = 0
    Initial_Currency = 0
    mysql_cnx = ''

    warmup_days = 3

    def __init__(self, date, dateDelta, currencyToTrade, assetToTrade, candle_Size_Minutes, warmup_Size_Minutes,
                 tradeExchange, Initial_Assets2, Initial_Currency2, strat, cnx):
        self.start_date = date
        self.day_delta = dateDelta
        self.asset = assetToTrade
        self.currency = currencyToTrade
        self.Initial_Assets = Initial_Assets2
        self.Initial_Currency = Initial_Currency2
        self.data_exporter = exporter(self.day_delta, self.Initial_Assets, self.Initial_Currency)
        self.candle_Size_Min = candle_Size_Minutes
        self.warmup_Size_Min = warmup_Size_Minutes
        self.exchange = tradeExchange
        self.strategy = strat
        self.mysql_cnx = cnx
        self.set_table_name()
        self.rootPassword = sys.argv[1]

    def getEndDate(self):
        return self.start_date + datetime.timedelta(days=self.day_delta);

    def set_table_name(self):
        exporter.tableName = str(self.exchange) + '_' + str(self.strategy) + '_' + str(self.day_delta) + 'days'

    def importData(self):

        end_day = self.getEndDate().day
        if end_day < 10:
            end_day = '0' + str(end_day)
        end_day = str(end_day)

        end_month = self.getEndDate().month
        if (end_month < 10):
            end_month = '0' + str(end_month)
        end_month = str(end_month)

        start_date = self.start_date - datetime.timedelta(days=self.warmup_days)

        start_day = start_date.day
        if (start_day < 10):
            start_day = '0' + str(start_day)
        start_day = str(start_day)

        start_month = start_date.month
        if (start_month < 10):
            start_month = '0' + str(start_month)
        start_month = str(start_month)

        execString = "cd /home/jonathan/gekko/ && echo '"+self.rootPassword+ "' | perl backtest.pl sudo -i -f " + str(
            self.start_date.year) + "-" + start_month + "-" + start_day + " -t " + str(
            self.getEndDate().year) + "-" + end_month + "-" + end_day + " -p " + str(self.exchange) + ":" + str(
            self.currency) + ":" + self.asset
        os.system(execString)

    def clearNodeAndPerl(self):
        os.system("echo '"+self.rootPassword+ "' |sudo -S killall -s KILL node")
        os.system("echo '"+self.rootPassword+ "' |sudo -S killall -s KILL perl")


    def uploadFile(self,CSV_File):
        with open(CSV_File + '.csv') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            item = exporter(self.day_delta, self.Initial_Assets, self.Initial_Currency)
            item.absorbTOML(self.strategy)
            for line in reader:
                # while line is not done
                item.insertLine(line, self.mysql_cnx)


    def run(self, importData):

        CSV_File = datetime.datetime.now()
        CSV_File = '_' + str(CSV_File .month) + '-' + str(CSV_File .day) + '_' + str(CSV_File .hour) + ':' + str(CSV_File .minute)
        CSV_File = '/home/jonathan/gekko/backtestData/' + self.data_exporter.tableName + CSV_File

        os.system("echo '"+self.rootPassword+ "' |  sudo -S rm " + CSV_File)

        end_day = self.getEndDate().day
        if end_day < 10:
            end_day = '0' + str(end_day)
        end_day = str(end_day)

        end_month = self.getEndDate().month
        if end_month < 10:
            end_month = '0' + str(end_month)
        end_month = str(end_month)

        start_day = self.start_date.day
        if start_day < 10:
            start_day = '0' + str(start_day)
        start_day = str(start_day)

        start_month = self.start_date.month
        if start_month < 10:
            start_month = '0' + str(start_month)
        start_month = str(start_month)

        if importData:
            self.importData()

        execString = "cd /home/jonathan/gekko/ && echo '"+ self.rootPassword+ "' | perl backtest.pl -f " + str(
            self.start_date.year) + "-" + start_month + "-" + start_day + " -t " + str(
            self.getEndDate().year) + "-" + end_month + "-" + end_day + " -n " + str(
            self.candle_Size_Min) + ":" + str(self.warmup_Size_Min) + " -p " + str(self.exchange) + ":" + str(
            self.currency) + ":" + self.asset + " -s " + self.strategy + " -o "+ CSV_File + ".csv"

        print(execString)
        os.system(execString);
        self.uploadFile(CSV_File)

        #os.system('sudo rm /home/jonathan/gekko/' + self.data_exporter.tableName + ".csv")


