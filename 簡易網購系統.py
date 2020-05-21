#!/usr/bin/env python
# coding: utf-8

# In[3]:


# 簡易網購系統
from tkinter import *
from tkinter import messagebox
import random

def itemSelected(event):
    global cateStr
    obj = event.widget                          # obj_cateLb or menuLb
    indexs = obj.curselection()
    # 點選其中一個表單時, 所有 ListBox 都會產生 <<ListboxSelect>> 事件, 
    # 沒有被點選的 ListBox 呼叫 curselection() 會回傳空 tuple
    if (len(indexs) == 0):
        return
    if (obj == cateLb):
        cateStr = cateLb.get(indexs[0])         # cateStr_家具、文具.....
        menuVar.set(tuple(cate[cateStr]))
    elif (obj == menuLb):
        index = indexs[0]                       # 目前分類下，選擇第 index 項商品
        menuStr = menuLb.get(index)
        selected = -1                           # 檢查此選項是否選過
        for i in range(scLb.size()):
            if (menuStr in scLb.get(i)):        # scLb.get(i)_"商品 * 數量", 用 in 檢查
                selected = i
                break
        if (selected == -1):                    # 沒選過
            sc.append([cateStr, menuStr, 1])
            scLb.insert(END, menuStr+" * 1")    # "商品 * 數量"
        else:
            sc[selected][2] += 1
            scLb.delete(selected)
            scLb.insert(selected, menuStr+" * "+str(sc[selected][2]))
    elif (obj == scLb):
        index = indexs[0]
        if (sc[index][2] == 1):
            del sc[index]
            scLb.delete(index)
        else:
            sc[index][2] -= 1
            scLb.delete(index)
            scLb.insert(index, sc[index][1]+" * "+str(sc[index][2]))
def check():
    total = 0
    for item in sc:
        menuStr = item[1]                       # 商品
        price = cate[item[0]][menuStr]
        qty = item[2]                           # Quantity
        charge = price * qty
        total += charge
        print(menuStr+":", price, "*", qty, "=", charge)
    print("總價:", total)
    root.destroy()

root = Tk()
root.title("1106108136")

# Category 分類
cate = {"家具":{"沙發":4000, "辦公桌":3000, "小板凳":300, "餐桌":3499, "椅子":999, "收納箱":599},     # 沙發售價 4000
        "文具":{"鋼筆":100, "奇異筆":30, "筆芯":20, "自動鉛筆":25, "麥克筆":50, "橡皮擦":20, "鉛筆盒":200},
        "衣服":{"t-shirt":299, "洋裝":699, "裙子":300, "牛仔褲":598,
              "運動褲":498, "襯衫":250, "西裝":799, "西裝褲":699, "領帶":250},
        "零食":{"牛肉乾":99, "奇多":30, "海苔":129, "可樂果":25},
        "工具":{"一字起子":199, "十字起子":199, "電鑽":2300, "電鋸":2000},
       }
# shopping cart
sc = []                                         # sc[n][0]_第n筆分類, sc[n][1]_商品, sc[n][2]_數量

frm = Frame(root)
frm.pack()

cateLb = Listbox(frm)
for item in list(cate):                         # list(cate) 只包含 keys 的陣列, 題目附註
    cateLb.insert(END, item)
cateLb.selection_set(0)                         # 要預設分類
cateStr = list(cate)[0]                         # cateStr_當前選擇的 Category, list(cate)_蒐集 keys 組成 list
cateLb.bind("<<ListboxSelect>>", itemSelected)

menuVar = StringVar()                           # StringVar() 可 set tuple, 題目附註
menuVar.set(tuple(cate[cateStr]))
menuLb = Listbox(frm, listvariable = menuVar)   # listvariable, 題目附註
menuLb.bind("<<ListboxSelect>>", itemSelected)

scLb = Listbox(frm)
scLb.bind("<<ListboxSelect>>", itemSelected)

enter = Button(root, text="Enter", font=("Helvetic", 20, "bold"), command=check)

cateLb.pack(side=LEFT)
menuLb.pack(side=LEFT)
scLb.pack(side=LEFT)
enter.pack()

root.mainloop()

