import os
import json
from tkinter import messagebox


class ReadJSON:
    _tangocho_path = os.path.dirname(os.path.abspath(__file__)) + "\\tangocho\\"

    _tangocho_name = ""
    _tangocho_comment = ""
    _tangocho_max_question_number = 100
    _tangocho_selection_check = False
    _tangocho_selection_check_number = 4

    _file = None

    def set_file(self, file):
        self._file = self._tangocho_path + file
        self._tangocho_name = file

    def get_file(self):
        return self._file

    def get_file_path(self):
        return self._tangocho_path

    def set_tancocho_name(self, tangocho_name):
        self._tangocho_name = tangocho_name

    # 設定ファイルを開く処理
    def read_setting(self):
        print("Info ReadJSON.py: " + self._file + "を読み込みます")
        with open(self._file, "r", encoding="utf-8") as jf:
            # jsonから読み込む
            __setting_data = json.load(jf)

        # 単語帳の名前
        self._tangocho_name = __setting_data["tangocho_name"]
        self._tangocho_comment = __setting_data["comment"]
        self._tangocho_max_question_number = int(__setting_data["max_question_number"])
        self._tangocho_selection_check = __setting_data["selection_check"]
        self._tangocho_selection_check_number = int(__setting_data["selection_check_number"])

        print("Info ReadJSON.py: " + self._tangocho_name + "を読み込み完了")
        print("Info ReadJSON.py: " + str(__setting_data))

    # 始めるボタンを押されたら
    def write_setting(self):
        print("Info ReadJSON.py: " + self._tangocho_name + "に書き込みます")

        __data = dict()
        # 単語帳の名前
        __data["tangocho_name"] = self._tangocho_name
        # 単語帳の説明
        __data["comment"] = self._tangocho_comment
        # 問題数
        __data["max_question_number"] = self._tangocho_max_question_number
        # 選択肢を用意するかどうか
        __data["selection_check"] = self._tangocho_selection_check
        # 選択肢の数
        __data["selection_check_number"] = self._tangocho_selection_check_number

        print("Info ReadJSON.py: data ", str(__data))

        with open(self._file, "w", encoding="utf-8") as jf:
            # jsonに書き込む
            json.dump(__data, jf, indent=4)

        print("Info ReadJSON.py: " + self._tangocho_name + "に書き込み完了")
