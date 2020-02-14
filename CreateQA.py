import tkinter.ttk, tkinter.messagebox
import tkinter as tk

import First
import Window
import ReadJSON


class Manager:
    frame = None
    label = None
    t = []
    question = None
    answer = None

    def __init__(self):
        pass

    def setFrame(self, frame):
        self.frame = frame

    def setLabel(self, _text):
        self.label = tkinter.ttk.Label(self.frame, text=_text)

    def setStringVer(self):
        for i in range(2):
            self.t.append(tk.StringVar())

    def setFields(self):
        self.question = tkinter.ttk.Entry(self.frame,
                                          # textvariable=self.t[0]
                                          )
        self.answer = tkinter.ttk.Entry(self.frame,
                                        # textvariable=self.t[1]
                                        )

    def setGrid(self, _row):
        self.label.grid(row=_row, column=1)
        self.question.grid(row=_row, column=2)
        self.answer.grid(row=_row, column=3)

    def get_t(self):
        # 空欄あり判定
        if self.question.get() == '' or self.answer.get() == '':
            return ["Error"]
        return (self.question.get(), self.answer.get())


class CreateQA(Window.Window, ReadJSON.ReadJSON):
    fields = list()
    frame = None
    num = 15
    max_num = 100 # 最大問題数
    row = 0
    gap = 40

    tangocho_name = None
    result = {}

    def plus(self, num):
        num += 1
        return num

    def __init__(self, tangocho_name=""):
        Window.Window.__init__(self)
        ReadJSON.ReadJSON.__init__(self)

        self.tangocho_name = tangocho_name

        self.set_title(u"単語帳(作成): " + self.tangocho_name)
        self.root.geometry("500x550")

        self.canvas = tk.Canvas(self.root, width=500, height=5000)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        # Scrollbar を生成して配置
        bar = tk.Scrollbar(self.root, orient=tk.VERTICAL)
        bar.pack(side=tk.RIGHT, fill=tk.Y)
        bar.config(command=self.canvas.yview)
        # Canvas Widget を配置
        self.canvas.config(yscrollcommand=bar.set)
        self.canvas.config(scrollregion=(0, 0, 0, self.num * self.gap))  # スクロール範囲
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH)

        for i in range(self.num):
            temp = Manager()
            self.fields.append(temp)

        self.frame = tkinter.ttk.Frame(self.canvas)
        self.frame.grid(row=0, column=0, sticky=("N", "E", "S", "W"))

        # Frame Widgetを Canvas Widget上に配置
        self.canvas.create_window((0, 0), window=self.frame, anchor=tk.NW, width=self.canvas.cget('width'))

        __question = tkinter.ttk.Label(self.frame, text="問題")
        __answer = tkinter.ttk.Label(self.frame, text="解答")
        __question.grid(row=0, column=2, sticky="N")
        __answer.grid(row=0, column=3, sticky="N")

        for field in self.fields:
            text = u'問題: ' + str(self.plus(self.row))
            field.setFrame(self.frame)
            field.setLabel(text)
            field.setStringVer()
            field.setFields()
            field.setGrid(self.plus(self.row))

            self.row += 1

        ############## ボタン類 ###############
        #暫定処理 csvから読み込む
        # button0 = tkinter.ttk.Button(self.frame, text=' CSV読み込み ', command=self.press_csv)
        # button0.grid(row=0, column=4, sticky="NE")

        self.button1 = tkinter.ttk.Button(self.frame, text=' 登録 ', command=self.press_button)
        self.button1.grid(row=self.row + 1, column=4, sticky="NE")

        self.button2 = tkinter.ttk.Button(self.frame, text=' 欄追加 ', command=self.add_fields)
        self.button2.grid(row=self.row + 1, column=3, sticky="SE")

        self.button3 = tkinter.ttk.Button(self.frame, text=' 戻る ', command=self.press_back)
        self.button3.grid(row=0, column=1, sticky="SW")

        for child in self.frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # 単語帳名前登録
    def set_tangocho_name(self, tangocho_name):
        self.tangocho_name = tangocho_name

    # CSVよみこみを押したとき
    def press_csv(self):
        pass

    # 追加するボタンを押したとき
    def add_fields(self):
        # 問題数制限
        if self.max_num <= self.row:
            tkinter.messagebox.showinfo("追加無効", "これ以上問題を追加できません!\n問題数は" + str(self.max_num) + "までです.")
            return
            # Frame Widgetを Canvas Widget上に配置
        self.canvas.config(scrollregion=(0, 0, 100, self.row * self.gap))  # スクロール範囲

        print("Info CreateQA: row", self.row)
        print("Info CreateQA: len", len(self.fields))
        self.fields.append(Manager())
        print("Info CreateQA: len", len(self.fields))
        text = u'問題: ' + str(self.plus(self.row))
        self.fields[self.row].setFrame(self.frame)
        self.fields[self.row].setLabel(text)
        self.fields[self.row].setStringVer()
        self.fields[self.row].setFields()
        self.fields[self.row].setGrid(self.plus(self.row))
        self.button2.grid(row=self.plus(self.row) + 1, column=3, sticky="SE")
        self.button1.grid(row=self.plus(self.row) + 1, column=4, sticky="NE")
        self.row += 1

        for child in self.frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

    # 登録ボタンを押したとき
    def press_button(self):
        check = tk.messagebox.askyesno("確認", "登録してもよろしいですか?\n注意:文中や文前後に空白がある場合もそのまま登録されます.")
        if check:
            for idx in self.fields:
                if idx.get_t() == ["Error"]:  # 空欄あり
                    pass
                else:
                    temp = idx.get_t()
                    self.result[temp[0]] = temp[1]
            print("Info CreateQA: result,", self.result)
            self.end()
        else:
            return

    # 戻るボタンを押したとき
    def press_back(self):
        self.destroy()
        First.First().start()

    def get_result(self):
        return self.result

    def get_tangocho_name(self):
        return self.tangocho_name


if __name__ == '__main__':
    CreateQA("test").start()
