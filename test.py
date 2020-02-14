import tkinter as tk

root = tk.Tk()
root.title(u"Software Title")
root.geometry("400x300")

# Canvas Widget を生成
canvas = tk.Canvas(root)
def _on_mousewheel(event):
    global canvas
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)


# Scrollbar を生成して配置
bar = tk.Scrollbar(root, orient=tk.VERTICAL)
bar.pack(side=tk.RIGHT, fill=tk.Y)
bar.config(command=canvas.yview)

# Canvas Widget を配置
canvas.config(yscrollcommand=bar.set)
canvas.config(scrollregion=(0,0,400,500)) #スクロール範囲
canvas.pack(side=tk.LEFT, fill=tk.BOTH)

# Frame Widgetを 生成
frame = tk.Frame(canvas)

# Frame Widgetを Canvas Widget上に配置
canvas.create_window((0,0), window=frame, anchor=tk.NW, width=canvas.cget('width'))

# 複数の Button Widget 生成し、Frame上に配置
buttons=[]
for i in range(20):
    bt = tk.Button(frame, text=i)
    buttons.append(bt)
    bt.pack(fill=tk.X)

root.mainloop()

