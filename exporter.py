class exporter:
    daysInTrade = 0
    Initial_Assets = 0
    Initial_Currency = 0

    basic_params = { }

    tableName = ''
    strategy_params = dict

    def __init__(self,daysInTrade2,Initial_Assets2,Initial_Currency2):
        self.daysInTrade = daysInTrade2
        self.Initial_Currency = Initial_Currency2
        self.Initial_Assets = Initial_Assets2


    def insertLine(self, line, cnx):
        self.basic_params['T_currency'] = str(line[0])
        self.basic_params['T_asset'] = line[1]
        self.basic_params['T_strategy'] = line[3].split()[0]
        self.basic_params['T_exchange'] = line[2]
        self.basic_params['percent_change'] = line[4]
        self.basic_params['market_change'] = line[5]
        self.basic_params['winning_trades'] = line[6]
        self.basic_params['best_win'] = line[7]
        self.basic_params['worst_loss'] = line[8]
        self.basic_params['avg_HODL_min'] = line[9]
        self.basic_params['candle_size_min'] = line[10]
        self.basic_params['history_size_min'] = line[11]
        self.basic_params['total_trades'] = line[12]
        self.basic_params['T_start_date'] = line[13]
        self.basic_params['T_end_date'] = line[14]
        self.basic_params['T_note'] = line[16]
        self.basic_params['profit_market_percent'] = line[17]
        self.basic_params['Initial_Assets'] = self.Initial_Assets
        self.basic_params['Initial_Currency'] = self.Initial_Currency
        self.basic_params['Days_In_Trade'] = self.daysInTrade;
        self.strategyParse(line)
        self.createIfNeeded(cnx)
        self.insert(cnx)

    def absorbTOML(self, tomlFileName):
        self.strategy_params = {}
        thing = "/home/jonathan/gekko/config/strategies/" + tomlFileName + ".toml"
        tomlFile = open("/home/jonathan/gekko/config/strategies/" + tomlFileName + ".toml", "r")

        for line in tomlFile:

            if line[0] == '#' or line[0] == '[' or line[0] == '\n':
                pass
            else:
                words = line.split()
                self.strategy_params[words[0]] = -1

    def createIfNeeded(self, cnx):
        cursor = cnx.cursor()
        print (self.tableName)
        test = "SELECT * FROM information_schema.tables WHERE table_name = '" + self.tableName + "'"
        cursor.execute(test)

        if cursor.fetchall().__len__() == 0:
            create = "create table " + self.tableName + "(Test_ID int(10) unsigned NOT NULL AUTO_INCREMENT " \

            for param in sorted(self.basic_params):
                type = " double"
                if param[0] + param[1] == "T_":
                    type = " tinytext"
                create = create + ", " + str(param) + type + " NOT NULL"

            for param in sorted(self.strategy_params):
                if param[0] + param[1] == "T_":
                    create = create + ", T_param_" + param[2:] + " tinytext NOT NULL"
                else:
                    create = create + ", param_" + str(param) + " double NOT NULL"

            create = create + ", PRIMARY KEY (Test_ID)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 DEFAULT " \
                              "COLLATE=utf8mb4_general_ci COMMENT='Contains backtests'"

            cursor.execute(create)

    def strategyParse(self, line):
        params = line[15].split()
        current_Var = 'nope'
        for word in params:
            if word[0] == '=' or word[0] == '[':
                pass
            else:
                if current_Var != 'nope':
                    if word[0].isnumeric() or word[0] == '-':
                        self.strategy_params[current_Var] = float(word)
                    else:
                        self.strategy_params["T_"+current_Var] = word
                    current_Var = 'nope'
                else:
                    if self.strategy_params.get(word, 'none') != 'none':
                        current_Var = word

    def insert(self, cnx):
        cursor = cnx.cursor()
        base_params_names = sorted(self.basic_params)
        strat_params_names = sorted(self.strategy_params)

        sql = "insert into " + self.tableName + " ( "


        sql += base_params_names[0]


        for value in range(1, len(base_params_names)):
            sql += " , " + base_params_names[value]

        for value in range(0, len(strat_params_names)):
            if strat_params_names[value][0] + strat_params_names[value][1] == "T_":
                sql += " , T_param_" + strat_params_names[value][2:]
            else:
                sql += " , param_" + strat_params_names[value]

        sql += " ) VALUES ( "


        if base_params_names[0][0] + base_params_names[0][1] == 'T_':
            sql += "'"+str(self.basic_params[base_params_names[0]]+"'")
        else:
            sql += str(self.basic_params[base_params_names[0]])

        for value in range(1, len(base_params_names)):
            item = self.basic_params[base_params_names[value]]
            if self.basic_params[base_params_names[value]] == '':
                sql += " , " + '0'
            else:
                if base_params_names[value][0] + base_params_names[value][1] == 'T_':
                    sql += " , '" + str(self.basic_params[base_params_names[value]]) + "' "
                else:
                    sql += " , " + str(self.basic_params[base_params_names[value]])

        for value in range(0, len(strat_params_names)):
            if strat_params_names[value][0] + strat_params_names[value][1] == 'T_':
                sql += " , '" + str(self.strategy_params[strat_params_names[value]]) + "' "
            else:
                sql += " , " + str(self.strategy_params[strat_params_names[value]])


        sql += " ); "
        print(sql)
        cursor.execute(sql)
        cnx.commit()