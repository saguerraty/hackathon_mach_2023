import sqlite3, csv
import pandas as pd


class DataEngine:

    def __init__(self) -> None:
        self.con = self.__create_sqlite_db()
        self.__load_spend_data("gastos_tarjeta_train")
        self.__load_balance_data("ingresos_egresos_train")

    def __create_sqlite_db(self) -> None:
        con = sqlite3.connect("':memory:'")
        return con
    
    def __load_spend_data(self, file_name: str) -> None:
        db_con = self.con
        cur = db_con.cursor()
        cur.execute("""CREATE TABLE spend_data 
                    ('user_id','fecha','description', 'amount', 'rubro_nivel1','nombre_fantasia', 'tipo_tarjeta', 'banco');""") # use your column names here

        with open('mvp/data_files/{}.csv'.format(file_name),'r') as fin: # `with` statement available in 2.5+
            # csv.DictReader uses first line in file for column headings by default
            dr = csv.DictReader(fin) # comma is default delimiter
            to_db = [(i['user_id'], i['fecha'], i['description'], i['amount'], i['rubro_nivel1'], i['nombre_fantasia'],i['tipo_tarjeta'], i['banco']) for i in dr]

        cur.executemany("INSERT INTO spend_data ('user_id','fecha','description', 'amount', 'rubro_nivel1','nombre_fantasia', 'tipo_tarjeta','banco') VALUES (?, ? , ?, ?, ?, ?, ?, ?);", to_db)
        db_con.commit()
        

    def __load_balance_data(self, file_name: str) -> None:
        db_con = self.con
        cur = db_con.cursor()
        cur.execute("""CREATE TABLE balance_data 
                    ('user_id', 'fecha', 'tipo', 'categoria', 'amount', 'banco', 'description');""") # use your column names here

        with open('mvp/data_files/{}.csv'.format(file_name),'r') as fin: # `with` statement available in 2.5+
            # csv.DictReader uses first line in file for column headings by default
            dr = csv.DictReader(fin) # comma is default delimiter
            to_db = [(i['user_id'], i['fecha'], i['tipo'], i['categoria'], i['amount'], i['banco'],i['description']) for i in dr]

        cur.executemany("INSERT INTO balance_data ('user_id', 'fecha', 'tipo', 'categoria', 'amount', 'banco', 'description') VALUES (?, ? , ?, ?, ?, ?, ?);", to_db)
        db_con.commit()
        

    def get_user_spend(self, user_id: int) -> pd.DataFrame:
        db_con = self.con
        df = pd.read_sql_query("SELECT * FROM spend_data where user_id = {}".format(user_id), db_con)
        return df
    
    def get_user_balance(self, user_id: int) -> pd.DataFrame:
        db_con = self.con
        df = pd.read_sql_query("SELECT * FROM balance_data where user_id = {}".format(user_id), db_con)
        return df
    
    def close_db(self) -> None:
        self.con.close()