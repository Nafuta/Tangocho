import os
import tkinter as tk
import tkinter.tix
import tkinter.ttk, tkinter.messagebox
import glob

import Window
import ReadJSON
import CreateQA
import Main


class First(Window.Window):
    frame = None

    tangocho_name = None
    tangocho_path = None

    def __init__(self):
        Window.Window.__init__(self)

        self.set_title(u"単語帳(はじめる)")

        __question = tkinter.ttk.Label(self.root, text="シンプル単語帳", font=("", 40))
        __question.pack()

        # 空白
        __temp = tk.Label(self.root, text="")
        __temp.pack()

        # tanogcho directly パス
        tangocho_path = os.path.dirname(os.path.abspath(__file__)) + "\\tangocho\\*.json"
        file = glob.glob(tangocho_path)
        base_name_file = [os.path.splitext(os.path.basename(idx))[0] for idx in file]
        print("Info First: base_name_file:", base_name_file)

        # 単語帳を選択
        tangocho_set = tk.Label(self.root, text="単語帳を選択", font=("", 15))
        tangocho_set.pack()
        self.tangocho_set_com = tkinter.ttk.Combobox(self.root, font=("", 15))
        self.tangocho_set_com['values'] = base_name_file
        self.tangocho_set_com.set(base_name_file[0])

        self.tangocho_name = self.tangocho_set_com.get()

        # ボックス変更時
        # self.tangocho_set_com.bind("<<ComboboxSelected>>", self.cb_selected())
        # self.tangocho_set_com["validate"] = "focusout"
        # self.tangocho_set_com["command"] = self.cb_selected()
        self.tangocho_set_com["justify"] = "center"

        self.tangocho_set_com.pack()

        __size = 2
        # 空白
        __temp = tk.Label(self.root, text="", font=("", __size))
        __temp.pack()

        # プレイボタンを表示
        self.button_play = tkinter.ttk.Button(self.frame, text=' はじめる ', command=self.press_play, width=40)
        self.button_play.pack()

        # 空白
        __temp = tk.Label(self.root, text="", font=("", __size))
        __temp.pack()

        # 編集ボタンを表示
        self.button_edit = tkinter.ttk.Button(self.frame, text=' 編集 ', command=self.press_edit, width=40)
        self.button_edit.pack()

        # 空白
        __temp = tk.Label(self.root, text="", font=("", __size))
        __temp.pack()

        # 閉じるボタンを表示
        self.button_quit = tkinter.ttk.Button(self.frame, text=' 閉じる ', command=self.press_quit, width=40)
        # self.button_quit["bg"]="red"
        self.button_quit.pack()

    # コンボボックスを選択したとき( エラーを吐くかどうかだけのチェック )
    def cb_selected(self):
        readJSON = ReadJSON.ReadJSON()
        self.tangocho_name = self.tangocho_set_com.get()
        readJSON.set_file(str(self.tangocho_name) + ".json")
        self.tangocho_path=readJSON.get_file_path()
        print(self.tangocho_name, readJSON.get_file())
        try:
            readJSON.read_setting()
        except:
            print("Warning First.py: 単語帳読み込みエラー")
            tkinter.messagebox.showerror("Error", "単語帳が正しく読み込めませんでした.\n単語帳がない可能性, もしくは単語帳が損傷している可能性があります.")
            temp = tkinter.messagebox.askyesno("確認", "単語帳: " + self.tangocho_name + "を作りますか?")
            if temp:
                readJSON.set_tancocho_name(self.tangocho_name)
                readJSON.write_setting()
                tkinter.messagebox.showinfo("情報", "単語帳を新しく作りました.")
                return False
            else:
                return False
        print("Info First.py: cb_selected 読み込み完了")
        return True

    # 始めるボタンを押したとき
    def press_play(self):
        if self.cb_selected():
            # ウィンドウ削除
            self.destroy()

            main = Main.Main()
            print("Info First.py: path: ",self.tangocho_path)
            main.set_file(self.tangocho_name+".json")
            main.open_setting()
            print(main.get_file())


        else:
            return

    # 編集ボタンを押したとき
    def press_edit(self):
        if self.cb_selected():
            # ウィンドウ削除
            self.destroy()

            CreateQA.CreateQA(self.tangocho_name).start()
        else:
            return

    # 閉じるボタンを押したとき
    def press_quit(self):
        self.end()


if __name__ == '__main__':
    First().start()
