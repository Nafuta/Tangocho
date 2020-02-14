import sqlite3
from copy import copy

import CreateQA

"""
database

属性
単語帳名 問題 答え 正解数 出題数 状態(初めて:0,前回正解:1,前回不正解:2) 

"""


class DatabaseManager:
    data = dict()

    tangocho_name = ""
    question = ""
    answer = ""
    correct_num = 0
    pop_num = 0
    state = 0

    def __init__(self, data=None, tangocho_name="", question="", answer="", correct_num=0, pop_num=0, state=0):
        self.conn = sqlite3.connect("data.db")
        self.cursor = self.conn.cursor()

        # 初期化
        self.data = data
        print("Info DatabaseManager: data:", data)
        self.tangocho_name = tangocho_name
        self.question = question
        self.answer = answer
        self.correct_num = correct_num
        self.pop_num = pop_num
        self.state = state

    #データベース削除
    def drop(self):
        self.cursor.execute("DROP TABLE IF EXISTS main")


    #データベース作成
    def create_database(self):
        # エラー処理（例外処理）
        try:
            # CREATE
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS main (tangocho varchar(20),question varchar(40),answer varchar(40),correct_num integer,pop_num integer,state integer)"
            )

        except sqlite3.Error as e:
            print('Warning : sqlite3.Error occurred:', e.args[0])

#データベースに一行のみ追加
    def insert_one_line(self):
        try:
            self.cursor.execute("INSERT INTO main VALUES(?,?,?,?,?,?)",
                                (self.tangocho_name, self.question, self.answer, self.correct_num, self.pop_num,
                                 self.state))
            print("Info DatabaseManager: select,", self.getAllTable())
        except sqlite3.Error as e:
            print('Warning : sqlite3.Error occurred at insert_one_line:', e.args[0])

#データベースに追加
    def insert_lines(self):
        try:
            for key,value in self.data.items():
                self.cursor.execute("INSERT INTO main VALUES(?,?,?,?,?,?)",
                                    (self.tangocho_name, key, value, 0, 0, 0))
                print("Info DatabaseManager: key,value:", key,value)
        except sqlite3.Error as e:
            print('Warning : sqlite3.Error occurred at insert_one_line:', e.args[0])


    # データベースから取得
    def getAllTable(self):
        return [recode for recode in self.conn.execute("SELECT * FROM main")]

    def setData(self, data):
        self.data = copy(data)


if __name__ == '__main__':
    createQA = CreateQA.CreateQA("test")
    createQA.start()
    qa = createQA.get_result()
    print("Info DatabaseManager: qa", qa)
    name = createQA.get_tangocho_name()
    dm = DatabaseManager(tangocho_name=name, data=qa)
    dm.drop()
    dm.create_database()
    dm.insert_lines()
    print(dm.getAllTable())
