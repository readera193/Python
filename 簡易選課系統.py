#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 簡易選課系統
from tkinter import *
from tkinter import messagebox
import random

def check():
    if (sel.size()<4 or 6<sel.size()):
        messagebox.showerror("課程數目錯誤", "請選4～6門課")
        return
    for i in range(5+1):
        for j in range(8+1):
            index = sched[i][j]
            if (index>=0):
                print(sub.get(index))
                for k in range(j+1, 8+1):           # 避免重複輸出
                    if (sched[i][k] == index):
                        sched[i][k] = -1
                    else:
                        break
    root.destroy()
    
def exit():
    res = messagebox.askokcancel("OKCANCEL", "結束或取消?")
    if (res == True):
        root.destroy()
        
def itemSelected(event):
    obj = event.widget                              # obj_sub or sel
    indexs = obj.curselection()  
    # 點選其中一個表單時, 兩個 ListBox 都會產生 <<ListboxSelect>> 事件, 
    # 沒有被點選的 ListBox 呼叫 curselection() 會回傳空 tuple
    if (len(indexs) == 0):
        return
    index = indexs[0]                               # index_課程流水號, curselection() 回傳 tuple, 單選下取得 [0] 即可
    if (obj == sub):
        course = subList[index]                     # 課程資訊
        conflict = 0                                # 衝堂 flag
        for i in range(course[2], course[3]+1):     # course[2]_開始節次, course[3]_結束節次
            if (sched[course[1]][i] >= 0):          # course[1]_星期幾
                conflict = 1
        if (conflict == 0):
            for i in range(course[2], course[3]+1):
                sched[course[1]][i] = index         # 加入課表
            sel.insert(END, sub.get(index))         # 加入清單
            mySub.append(index)                     # delete 要用
        else:
            messagebox.showerror("衝堂錯誤", "選擇的課程與目前課表衝堂，請調整課表或選擇其他課程")
    elif (obj == sel):
        course = subList[mySub.pop(index)]          # 要刪除的課程資訊, pop 題目附註
        for i in range(course[2], course[3]+1):
            sched[course[1]][i] = -1
        sel.delete(index)

root = Tk()
root.title("1106108136")
root.protocol("WM_DELETE_WINDOW", exit)

# 課表(schedule)，[星期][節]=課程流水號，row=0、column=0 捨棄不用
sched = []
for i in range(5+1):
    sched.append([-1]*(8+1))

# subject list [流水號][科目名稱(星期), 星期(數字), 開始時間, 結束時間]
subList = [["國文(一)", 1, 2, 4],
           ["英文(一)", 1, 3, 4],
           ["數學(一)", 1, 5, 7],
           ["物理(二)", 2, 2, 4],
           ["地科(二)", 2, 1, 2],
           ["化學(二)", 2, 6, 8],
           ["公民(二)", 2, 5, 6],
           ["生物(三)", 3, 1, 2],
           ["歷史(三)", 3, 2, 3],
           ["國防(三)", 3, 5, 6],
           ["體育(三)", 3, 7, 8],
           ["地理(四)", 4, 3, 4],
           ["物理實驗(四)", 4, 2, 4],
           ["化學實驗(四)", 4, 5, 7],
           ["程式設計(五)", 5, 2, 4],
          ]
mySub = []                                      # 已加入的課程，delete 要用

# 兩個 list
frm = Frame(root)
frm.pack()

scrSub = Scrollbar(frm)
sub = Listbox(frm, yscrollcommand=scrSub.set)   # subject, 可選的課程
for item in subList:
    sub.insert(END, item[0]+str(item[2])+"～"+str(item[3]))
sub.bind("<<ListboxSelect>>", itemSelected)
scrSub.config(command=sub.yview)

sel = Listbox(frm)                              # selected, 學生選擇的課程
sel.bind("<<ListboxSelect>>", itemSelected)

sub.pack(side=LEFT)
scrSub.pack(side=LEFT, fill=Y)
sel.pack(side=LEFT)

enter = Button(root, text="Enter", font=("Helvetic", 20, "bold"), command=check)
enter.pack()

root.mainloop()

