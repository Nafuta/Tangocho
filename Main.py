
import json
from copy import copy
from functools import partial

import Window
import ReadJSON

import tkinter as tk
import tkinter.filedialog, tkinter.messagebox, tkinter.ttk


# sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

# 基本メニュー
class Main(Window.Window, ReadJSON.ReadJSON):
    _tangocho_max_question_number = 100


    def __init__(self,db=False):
        Window.Window.__init__(self)
        ReadJSON.ReadJSON.__init__(self)

        self.set_title(u"単語帳(設定)")

        # # ボタン
        # # self.frame = tk.Frame(self.root, bg=self.color_white)
        # __open_button = tkinter.Button(
        #     self.root,
        #     text="単語帳を開く",  # 初期値
        #     width=60,  # 幅
        #     bg="lightblue",  # 色
        #     command=self.import_file  # クリックに実行する関数
        # )
        # __open_button.pack()
        if db:
            self.debug()

    def drop(self):
        self.__init__()

    def debug(self):
        # ボタン
        # self.frame = tk.Frame(self.root, bg=self.color_white)
        __open_button = tkinter.Button(
            self.root,
            text="単語帳を開く",  # 初期値
            width=60,  # 幅
            bg="lightblue",  # 色
            command=self.import_file  # クリックに実行する関数
        )
        __open_button.pack()
        print("Info Main.py: 設定ファイルを開きます")
        __fTyp = [("", "*.json")]

        self._file = tkinter.filedialog.askopenfilename(filetypes=__fTyp, initialdir=self._tangocho_path)

        # 何も開かなかったとき
        if len(self._file) == 0:
            print("Info Main.py: 何も開きませんでした")
            self.__file_open_check = False  # ファイルが開けませんでした
            return

        # 開くときの処理
        # 処理ファイル名の出力
        print("Info Main.py: " + self._file + "を開きました")

        self.drop()
        self.open_setting()

    # 単語帳を開くボタンを押したときの処理
    def import_file(self):
        self.root.withdraw()  # ウィンドウを見えないように
        self.open_setting()  # 設定ファイルを開く処理
        self.root.deiconify()  # ウィンドウを見えるように

    # 設定ファイルを開く処理
    def open_setting(self):
        # print("Info Main.py: 設定ファイルを開きます")
        # __fTyp = [("", "*.json")]
        #
        # self._file = tkinter.filedialog.askopenfilename(filetypes=__fTyp, initialdir=self._tangocho_path)
        #
        # # 何も開かなかったとき
        # if len(self._file) == 0:
        #     print("Info Main.py: 何も開きませんでした")
        #     self.__file_open_check = False  # ファイルが開けませんでした
        #     return
        #
        # # 開くときの処理
        # # 処理ファイル名の出力
        # print("Info Main.py: " + self._file + "を開きました")
        #
        # self.drop()

        try:
            self.read_setting()
        except:
            print("Warning ReadJSON.py: 設定ファイル読み込みエラー")
            tkinter.messagebox.showerror("Error", "設定ファイルが正しく読み込めませんでした.\nファイルが損傷している可能性があります.")
            temp = tkinter.messagebox.askquestion("確認", self._tangocho_name + "の設定を作り直しますか?")
            if temp:
                self.go_press()
                tkinter.messagebox.showinfo("情報", "設定ファイルを新しく作り直しました.")
                return
            else:
                return

        self.setting_scene()

    # 設定ウィンドウ
    def setting_scene(self):
        # チェックボックス
        def checked(ch):
            nonlocal __selection_check,bln
            print(bln.get())
            if ch:
                bln.set(False)
            else:
                bln.set(True)

            # 選択肢にチェックを入れるか入れないか
            if bln.get():
                __selection_check.select()
            else:
                __selection_check.deselect()

        def press(com_box, q_num_box, variable, sele_n_c):
            # nonlocal selection_num_combo, comment_box
            print("Info Main.py: comment, ", com_box.get())
            print("Info Main.py: selection, ", variable.get())
            print("Info Main.py: selection_num, ", sele_n_c.get())
            self._tangocho_comment = copy(com_box.get())
            self._tangocho_max_question_number = int(copy(q_num_box.get()))
            self._tangocho_selection_check = copy(variable.get())
            print(self._tangocho_selection_check,variable.get())
            self._tangocho_selection_check_number = int(copy(sele_n_c.get()))

            self.go_press()

        # def cb_selected(event):
        #     pass

        # ウィジェットの追加

        # 空白
        __temp = tk.Label(self.root, text="")
        __temp.pack()

        __tangocho_label = tk.Label(self.root, text="単語帳の名前")
        __tangocho_label.pack()
        __tangocho_name_label = tk.Label(self.root, text=str(self._tangocho_name))
        __tangocho_name_label.pack()

        # 空白
        __temp = tk.Label(self.root, text="")
        __temp.pack()

        __comment_label = tk.Label(self.root, text="単語帳の説明")
        __comment_label.pack()
        comment_box = tk.Entry(self.root, width=50, bg=self.color_white)
        comment_box.insert(0, self._tangocho_comment)
        comment_box.pack()
        print(self._tangocho_comment)

        # 空白
        __temp = tk.Label(self.root, text="")
        __temp.pack()

        __question_num_label = tk.Label(self.root, text="問題数(全問題数以下)")
        __question_num_label.pack()
        __question_num_box = tk.Entry(self.root, width=50, bg=self.color_white)
        __question_num_box.insert(0, self._tangocho_max_question_number)
        __question_num_box.pack()

        # 空白
        __temp = tk.Label(self.root, text="")
        __temp.pack()

        __comment_label = tk.Label(self.root, text="選択肢のヒント")
        __comment_label.pack()
        bln = tk.BooleanVar()
        print("Info Main.py: selection_check", bln.get(),self._tangocho_selection_check)
        bln.set(self._tangocho_selection_check)
        print("Info Main.py: selection_check", bln.get(),self._tangocho_selection_check)
        __selection_check = tk.Checkbutton(self.root,variable=bln, text="選択肢あり",command=partial(checked,bln.get()))


        __selection_check.pack()


        # 空白
        __temp = tk.Label(self.root, text="")
        __temp.pack()

        __selection_num_label = tk.Label(self.root, text="選択肢の数(1～8つ)\n(※選択肢ありの場合のみ有効)")
        __selection_num_label.pack()
        selection_num_combo = tkinter.ttk.Combobox(self.root, state="readonly")
        # self.__selection_num_combo.bind('<<ComboboxSelected>>', cb_selected)
        selection_num_combo['values'] = ("1", "2", "3", "4", "5", "6", "7", "8")
        selection_num_combo.set(self._tangocho_selection_check_number)
        selection_num_combo.pack()

        # go button
        # ボタン
        # self.frame = tk.Frame(self.root, bg=self.color_white)
        __go_button = tkinter.Button(
            self.root,
            text="はじめる",  # 初期値
            width=15,  # 幅
            bg="lightyellow",  # 色
            command=partial(press, comment_box, __question_num_box, bln, selection_num_combo)  # クリックに実行する関数
        )
        __go_button.pack(side="right")

    # 始めるボタンを押されたら
    def go_press(self):
        print("Info Main.py: " + self._tangocho_name + "に書き込みます")

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

        print("Info Main.py: data ", str(__data))

        with open(self._file, "w", encoding="utf-8") as jf:
            # jsonに書き込む
            json.dump(__data, jf, indent=4)

        print("Info Main.py: " + self._tangocho_name + "に書き込み完了")

        self.end()


if __name__ == '__main__':
    Main(db=True).start()
