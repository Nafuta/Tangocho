import tkinter as tk


# windowの基本的な設定
class Window(tk.Frame):
    # 色
    color_white = "white"  # 背景色
    color_red = "#FF8090"
    root = None

    # __window_width = 1152  # window size of width
    # __window_height = 648  # window size of height

    def __init__(self):
        self.root = tk.Tk()
        # create a canvas
        self.canvas = tk.Canvas(self.root,
                                # width=self.__window_width,
                                # height=self.__window_height,
                                bg=self.color_white
                                )

    def set_title(self, title):
        self.root.title(title)  # set title

    def start(self):
        self.root.mainloop()

    def end(self):
        self.root.quit()
        print("Info Window.py: quit Finish!")

    def destroy(self):
        self.root.destroy()
        print("Info Window.py: destroy Finish!")

