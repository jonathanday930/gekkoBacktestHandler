import os
import csv
from abc import abstractmethod
import mysql.connector


class trade:
    daysInTrade = 0

    basic_params = {
        'currency' : '',
        'asset' : '',
        'strategy' : '',
        'exchange' : '',
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

    strategy_params = {}

    def getTableName(self):
        return str(self.basic_params['currency']) + '_' + str(self.basic_params['asset']) + '_' + \
               str(self.basic_params['exchange'])+ '_' + str(self.daysInTrade) + 'daySegments'



    def insertLine(self, line, cursor):
        self.basic_params['T_currency'] = line[0]
        self.basic_params['T_asset']= line[1]
        self.basic_params['T_strategy'] = line[2].split()[0]
        self.basic_params['T_exchange'] = line[3]
        self.basic_params ['percent_change'] = line[4]
        self.basic_params ['market_change'] = line[5]
        self.basic_params ['winning_trades'] = line[6]
        self.basic_params ['best_win'] = line [7]
        self.basic_params ['worst_loss'] = line[8]
        self.basic_params ['avg_HODL_min'] = line[9]
        self.basic_params ['candle_size_min'] = line[10]
        self.basic_params ['history_size_min'] = line[11]
        self.basic_params ['total_trades'] = line[12]
        self.basic_params ['T_start_date'] = line[13]
        self.basic_params ['T_end_date'] = line[14]
        self.basic_params ['T_note'] = line[16]
        self.strategyParse(line)

        self.createIfNeeded(cursor)



    def absorbTOML(self,tomlFileName):
        self.strategy_params = {}
        tomlFile = open("/home/jonathan/gekkoconfig/strategies/" + tomlFileName + ".toml", "r")

        for line in tomlFile:
            if line[0] == '#' or line[0] == '[':
                pass
            else:
                words = line.split()
                self.strategy_params[words[0]] = -1



    def createIfNeeded(self,cursor):

        test = "SELECT * FROM gekkoTests." + self.getTableName()
        cursor.execute(test)
        if cursor.fetchAll.__len__() == 0:
            create = "create table " + self.getTableName() + "(Test_ID int(10) unsigned NOT NULL AUTO_INCREMENT, " \
                                                         "Initial_Assets double NOT NULL, Initial_Currency double NOT" \
                                                             " NULL,"
            for param in sorted(self.basic_params):
                type = " double"
                if(param[0]+param[1] =="T_"):
                    type = " tinytext"
                create = create + ", " + str(param) + type + " NOT NULL"

            for param in sorted(self.strategy_param):
                create = create + ", " + str(param) + " double NOT NULL"

            create = create + ", PRIMARY KEY (Test_ID)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 DEFAULT " \
                              "COLLATE=utf8mb4_general_ci COMMENT='Contains backtests"
        cursor.execute(create)

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
        print(sql)


def main():

    #start_date = '2018-04-03'
    #end_date = '2018-04-04'

    #file = 'C:\Users\juliann\PycharmProjects\gekkoHandler\database.csv'
    #os.system('sudo rm ' + file)
    #os.system('sudo touch ' + file)

    #os.system('sudo perl backtest.pl - f ' + start_date + '- t ' + end_date);


    print("hello BITCH")




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




if __name__ == "__main__":
    main()

# PLAN
# Delete database.csv
# run a test
# take specific data from new database.csv
# put into mysql



