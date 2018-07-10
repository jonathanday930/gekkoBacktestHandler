import os
import csv
from abc import abstractmethod
import mysql.connector


class trade:
    table_name = 'USDT:BTC_Binance_BULL_BEAR_RSI_DailyTests'
    basic_params = {
        'currency' : '',
        'asset' : '',
        'strategy' : '',
        'percent_change' : '',
        'market_change' : '',
        'winning_trades' : '',
        'best_win' : '',
        'worst_loss' : '',
        'avg_HODL_min' : '',
        'candle_size_min' : '',
        'history_size_min' : '',
        'total_trades' : '',
        'start_date' : '',
        'end_date' : '',
        'note' : ''

    }

    strategy_params = ''

    def __init__(self, line ):
        self.basic_params['currency'] = line[0]
        self.basic_params['asset']= line[1]
        self.basic_params['strategy'] = line[2]
        self.basic_params ['percent_change'] = line[3]
        self.basic_params ['market_change'] = line[4]
        self.basic_params ['winning_trades'] = line[5]
        self.basic_params ['best_win'] = line [6]
        self.basic_params ['worst_loss'] = line[7]
        self.basic_params ['avg_HODL_min'] = line[8]
        self.basic_params ['candle_size_min'] = line[9]
        self.basic_params ['history_size_min'] = line[10]
        self.basic_params ['total_trades'] = line[11]
        self.basic_params ['start_date'] = line[12]
        self.basic_params ['end_date'] = line[13]
        self.basic_params ['note'] = line[15]
        self.strategyParse(line)


    def createIfNeeded(self,cursor):

        test = "SELECT * FROM gekkoTests." + self.table_name
        cursor.execute(test)

        if cursor.fetchAll.__len__() == 0:
            create = "create table " + self.table_name + ""
            pass
        #WORK IN PROGRESS

    @abstractmethod
    def strategyParse(self, line):
        pass

class bull_bear_rsi(trade):


    # ADX
    strategy_params = {
        'SMA_long' :0 ,
        'SMA_short' : 0,
        'BULL_RSI' : 0,
        'BULL_RSI_high' : 0,
        'BULL_RSI_low' : 0,
        'BEAR_RSI' : 0,
        'BEAR_RSI_high' : 0,
        'BEAR_RSI_low' : 0,
        'BULL_MOD_high' : 0,
        'BULL_MOD_low' : 0,
        'BEAR_MOD_high' : 0,
        'BEAR_MOD_low' : 0,
        'ADX' : 0,
        'ADX_high' : 0,
        'ADX_low' : 0
        }

    def ___init__(self):
        ADX = 0

    def strategyParse(self, line):
        params = line[14].split()
        current_Var = 'nope'
        for word in params:
            if word[0] == '=' or word[0] == '[':
                pass
            else:
                if current_Var != 'nope':
                    self.strategy_params[current_Var] = int(word)
                    current_Var = 'nope'
                else:
                    if self.strategy_params.get(word,'none') != 'none':
                        current_Var = word


    def insert(self,cursor):
        base_params_names = sorted(self.basic_params)
        strat_params_names = sorted(self.strategy_params)

        sql = "insert into " + self.table_name + " ( "
        sql += base_params_names[0]
        for value in range(1,len(base_params_names)):
            sql += " , " + base_params_names[value]

        for value in range(0, len(strat_params_names)):
            sql += " , " + strat_params_names[value]

        sql += " ) VALUES ( "

        sql += self.basic_params[base_params_names[0]]

        for value in range(1, len(base_params_names)):
            item = self.basic_params[base_params_names[value]]
            if self.basic_params[base_params_names[value]] == '':
                sql += " , " + '0'
            else: sql += " , " + self.basic_params[base_params_names[value]]


        for value in range(0, len(strat_params_names)):
            sql += " , " + str(self.strategy_params[strat_params_names[value]])

        sql += " ) "

        print sql


def main():

    #start_date = '2018-04-03'
    #end_date = '2018-04-04'

    file = 'C:\Users\juliann\PycharmProjects\gekkoHandler\database.csv'
    #os.system('sudo rm ' + file)
    #os.system('sudo touch ' + file)

    #os.system('sudo perl backtest.pl - f ' + start_date + '- t ' + end_date);

    cnx = mysql.connector.connect(user='remote', password='remote',
                                  host='192.168.0.11',
                                  database='gekkoTests')

    cursor = cnx.cursor()
    cursor.execute(test)
    res = cursor.fetchall()
    len = res.__len__()
    with open(file) as csvfile:
        reader = csv.reader(csvfile)
        reader.next()
        #while line is not done
        line = reader.next()
        line[14] = 'SMA_long = 1000 SMA_short = 50 BULL_RSI = 10 BULL_RSI_high = 80 BULL_RSI_low = 60 BEAR_RSI = 15 BEAR_RSI_high = 50 BEAR_RSI_low = 20 BULL_MOD_high = 5 BULL_MOD_low = -5 BEAR_MOD_high = 15 BEAR_MOD_low = -5 ADX = 3 ADX_high = 70 ADX_low = 50';
        item = bull_bear_rsi(line);
        item.insert("aa")
        # strategy settings here




    print 'hi'


if __name__ == "__main__":
    main()

# PLAN
# Delete database.csv
# run a test
# take specific data from new database.csv
# put into mysql



