import tkinter as tk

import Window


# 問題文と答えを入れておくクラス
class DataQuestionAndAnswer:
    __question = ""
    __answer = ""

    def __init__(self, question, answer):
        self.__question = question
        self.__answer = answer

    def get_question(self):
        return self.__question

    def get_answer(self):
        return self.__answer


# アプリケーションクラス
class Application(Window.Window):
    __input_box = None  # 入力ボックス
    __question_label = None  # 問題文ラベル
    __selection_label = None  # 選択肢ラベル

    __max_question_num = 0  # 問題数
    __question_num = 0  # 現時点で答えた数
    __correct_num = 0  # 正答数
    __worse_num = 0  # 誤答数

    __selection_text = None  # 選択肢テキスト
    __question_text = None  # 質問テキスト

    __selection_check = False  # 選択肢を表示させるかどうか
    __selection_max_number = -1  # 選択肢の表示最大数

    # 終わりかどうかのフラグ
    __end_flag = False

    # テスト:答えと質問のインスタンス
    __test_data = []

    # Window override
    def set_title(self):
        self.root.title(u"単語帳")  # set title

    def __init__(self):
        Window.Window.__init__(self)

        # self.root = tk.Tk()

        # self.root.geometry(
        #     str(self.__window_width) + "x" + str(self.__window_height)
        # )  # set window size

        # create a canvas
        # self.canvas = tk.Canvas(self.root,
        #                         # width=self.__window_width,
        #                         # height=self.__window_height,
        #                         bg=self.color_white
        #                         )
        # self.canvas.pack()

        # 質問と答えを作成
        self.create_data()

        # 質問内容表示
        self.__question_text = tk.StringVar()
        self.__question_label = tk.Label(self.root, textvariable=self.__question_text)
        self.set_question()
        self.__question_label.pack()

        # 選択肢ラベル作成
        self.__selection_text = tk.StringVar()
        self.__selection_label = tk.Label(self.root, textvariable=self.__selection_text)
        self.__selection_label.pack()

        # 入力ボックス作成
        self.__input_box = tk.Entry(width=50, bg=self.color_white)
        self.__input_box.pack()

        tk.Frame.__init__(self, self.root)
        self.create_frame()

    # 質問表示メソッド
    def set_question(self):
        # 最後の問題だったとき
        if self.__end_flag is False:
            self.__question_text.set(self.__test_data[self.__question_num].get_question())

    # 選択肢作成メソッド
    def set_selection(self):
        if self.__selection_check:
            pass
        else:
            self.__selection_text.set("")  # 何も表示しない

    # 問題文と答えのインスタンスを作るメソッド
    def create_data(self):
        # テスト質問と答え
        __test_question = ["question 1", "question 2", "question 3"]
        __test_answer = ["question 1", "question 2", "question 3"]
        for q, a in zip(__test_question, __test_answer):
            print("Info: quation", q, " , answer", a)
            self.__test_data.append(DataQuestionAndAnswer(question=q, answer=a))

        self.__max_question_num = len(__test_question)  # 問題数セット
        print("Info: question number", self.__max_question_num)

    # フレーム作成メソッド
    def create_frame(self):
        # create a frame
        __frame = tk.Frame(self.root,
                           # width=self.__window_width,
                           # height=self.__window_height,
                           bg=self.color_white
                           )
        __frame.pack()
        __frame.focus_set()  # This will get the frame in focus.
        __frame.bind("<Button-1>", self.click_mouse_left)  # マウス左クリック


        # ボックスにカーソルがあっているとき
        self.__input_box.bind("<Return>", self.press_return)  # エンターキー

    # Mouse event when it presses left button.
    def click_mouse_left(self, event):
        __input_data = self.__input_box.get()
        print("press mouse", __input_data)

    # def press_returnないでのみ使用
    __check = True

    # エンターキーを押したとき
    def press_return(self, event):
        # テキストボックス内を削除
        def erase_text_box():
            self.__input_box.delete(0, tk.END)  # テキストボックス内を削除

        # 次の問題へ
        def next_question():
            # 最後の問題だったとき
            if self.__max_question_num - 1 == self.__question_num:
                self.end()
            print("Info:", self.__max_question_num, self.__question_num)
            print("Info: end?", self.__end_flag)

            self.__input_box["bg"] = self.color_white  # テキストボックスの色を変更
            erase_text_box()  # 回答ボックスの中身を消す
            self.set_selection()  # 選択肢表示
            self.__question_num += 1  # 現在の回答数を増やす
            self.set_question()  # 次の質問をセットする

        # 正答時
        def when_correct_answer():
            self.__correct_num += 1  # 正答数を増やす
            next_question()

        # 誤答時 (間違っていても, もう一度答えさせないパターン)
        def when_worse_answer(correct_answer):
            self.__check = False
            # self.__question_label["bg"] = self.__color_red
            # self.__question_label["fg"] = self.__color_white
            self.__input_box["bg"] = self.color_red  # テキストボックスの色を変更
            self.__worse_num += 1  # 誤答数を増やす

            self.__selection_text.set("正解は " + correct_answer)

        #######################################

        print("Info: ", self.__check)
        # if self.__check is None:
        #     self.__check = True

        if self.__check is True:
            __input_data = self.__input_box.get()
            print("Info: Your answer is", __input_data)
            if self.__test_data[self.__question_num].get_answer() == __input_data:
                print(__input_data, "is correct!")
                when_correct_answer()  # 正答時
            else:
                print(__input_data, "is worse...")
                print("Info: Correct answer is", self.__test_data[self.__question_num].get_answer())
                when_worse_answer(self.__test_data[self.__question_num].get_answer())
            return

        if self.__check is False:
            self.__check = True
            next_question()
            return

    #override
    def end(self):
        self.__end_flag = True
        self.quit()
        print("Info: Finish!")


if __name__ == '__main__':
    Application().start()
