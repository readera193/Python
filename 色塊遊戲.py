#!/usr/bin/env python
# coding: utf-8

# 色塊遊戲
import tkinter as tk
import random

level = 1                                       # 遊戲等級
keyX = 0
keyY = 0
RGB = [0] * 3

def key(event):
    global keyX, keyY, level
    keyIn = repr(event.char)[1]                 # 按 a repr() 回傳 'a'(長度為3的字串)_函式附註
    flag = 0                                    # True_有效輸入
    for row in keys:
        if (keyIn.upper() in row):
            flag = 1
    if (not flag):
        btn_start.config(state=tk.NORMAL)
        root.unbind("<Key>")
        var.set("請輸入視窗內字符或切換輸入法")
    elif (keyIn == keys[keyX][keyY] or
          keyIn == keys[keyX][keyY].lower()):   # 答對---附函式解說
        var.set("Level:"+str(level-2))
        level += 1
        game()
    else:
        btn_start.config(state=tk.NORMAL)
        root.unbind("<Key>")                    # 避免遊戲結束後玩家又按按鍵
        var.set("GameOver, Answer: "+keys[keyX][keyY]+" , Final Score:"+str(level-1))

def start():
    global level
    root.bind("<Key>", key)
    btn_start.config(state=tk.DISABLED)
    level = 1
    game()

def game():
    global keyX, keyY, level
    if (level<11):
        keyX = random.randrange(3)
        keyY = random.randrange(10)
        for i in range(3):
            RGB[i] = random.randrange(200)                                                      # 避免超出範圍---附函式解說
        for i in range(3):
            for j in range(10):
                labels[i][j].config(bg="#{:0>2x}{:0>2x}{:0>2x}".format(RGB[0], RGB[1], RGB[2]))
        RGB[random.randrange(3)] += 55-level*5                                                  # 設定不同色塊
        labels[keyX][keyY].config(bg="#{:0>2x}{:0>2x}{:0>2x}".format(RGB[0], RGB[1], RGB[2]))   # 附函式解說
        var.set("Score:"+str(level-1))
    else:
        btn_start.config(state=tk.NORMAL)
        root.unbind("<Key>")
        var.set("恭喜通關")

root = tk.Tk()
root.title("196")

# 遊戲介面
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
labels = []
for i in range(3):
    labels.append([])
    for j in range(10):
        labels[i].append(tk.Label(root, text=keys[i][j], relief="groove",
                               height=2, width=4, font=("Helvetic", 30, "bold")))
        labels[i][j].grid(row=i, column=j)

btn_start = tk.Button(root, text="Start", font=("Helvetic", 20, "bold"), command=start)              # 開始遊戲
btn_start.grid(row=3, column=0, sticky=tk.N+tk.W+tk.E+tk.S)

# 記分板
var = tk.StringVar()
score = tk.Label(root, textvariable=var, font=("Helvetic", 30, "bold"))
score.grid(row=3, column=1, columnspan=8)

root.mainloop()

