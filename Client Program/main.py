import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import pyautogui
import time
from getPortData import Port
from serial.tools import list_ports
from tkinter import filedialog, dialog
import os
import json


# 所有的手势列表：
# 大拇指 食指 中指 无名指 小指
# 左移 右移 前移 后移 上移 下移
# Roll轴顺时针 Roll轴逆时针
# Pitch轴顺时针 Pitch轴逆时针
# Yaw轴顺时针 Yaw轴逆时针
Motion = ('Thumb', 'Index Finger', 'Middle Finger', 'Ring Finger', 'Little Finger',
          'Move Right', 'Move Left', 'Forward', 'Backward', 'Upward', 'Downward',
          'Pitch Clockwise', 'Pitch Anticlockwise',
          'Roll Anticlockwise', 'Roll Clockwise',
          'Yaw Clockwise', 'Yaw Anticlockwise')

# 所有的键鼠列表（键盘可添加）
# 鼠标：左击 右击 双击 滚轮向上 滚轮向下
# 键盘：各个按键名
Mouse = ('Left Click', 'Right Click', 'Double Click', 'Scroll Up', 'Scroll Down')
Keyboard = ('ctrl', 'shift', 'alt', 'esc','tab',
'enter','fn', 'printscreen','space','win','capslock', 'delete','backspace',
'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9','f10', 'f11', 'f12',
'0', '1', '2', '3', '4', '5', '6', '7','8', '9',
'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 
'o','p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
)

# 映射表
mapping = {}  # 手势对应字符串与键鼠行为的映射表

screenWidth, screenHeight = pyautogui.size()  # 获取屏幕尺寸

# 建立软件窗口
window = tk.Tk()
window.title('Magic Glove')
window.geometry('800x800')

canvas_setting = tk.Canvas(window, bg='seashell3', height=260, width=600)
canvas_setting.place(x=20, y=10)

canvas_mapping = tk.Canvas(window, bg='seashell3', height=490, width=600)
canvas_mapping.place(x=20, y=300)

l_setting = tk.Label(window, text='SETTING', font=("Arial", 12, 'bold'), bg='seashell3')
l_setting.place(x=260, y=12)
l_mapping = tk.Label(window, text='MAPPING', font=("Arial", 12, 'bold'), bg='seashell3')
l_mapping.place(x=260, y=302)

l_motion = tk.Label(window, text='Gestures', font=("Arial", 10), bg='seashell3')
l_motion.place(x=50, y=45)
l_action = tk.Label(window, text='Keyboard & Mouse', font=("Arial", 10), bg='seashell3')
l_action.place(x=300, y=45)

mapping_show_x = 40
mapping_show_y = 330

showing_count = 0

showing_motion = []
showing_action = []
showing_arrow = []
photo_arrow = tk.PhotoImage(file="arrow.png").subsample(10, 10)


# 加号按钮的函数
def add_motion_1():
    comboxlist_motion2.place(x=50, y=110)
    add_motion2.place(x=220, y=110)
    add_motion1.place_forget()


def add_motion_2():
    comboxlist_motion3.place(x=50, y=150)
    add_motion3.place(x=220, y=150)
    add_motion2.place_forget()


def add_motion_3():
    comboxlist_motion4.place(x=50, y=190)
    add_motion4.place(x=220, y=190)
    add_motion3.place_forget()


def add_motion_4():
    comboxlist_motion5.place(x=50, y=230)
    add_motion4.place_forget()


def add_action_1():
    comboxlist_action2.place(x=300, y=110)
    add_action2.place(x=470, y=110)
    add_action1.place_forget()


def add_action_2():
    comboxlist_action3.place(x=300, y=150)
    add_action2.place_forget()


# 建立映射的函数
def set_mapping():
    # 添加映射，初始化
    mapping_key_bin = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    mapping_value = []

    # 手势设定为空，跳出提示，并退出函数
    if (comboxlist_motion1.get() == '' and
            comboxlist_motion2.get() == '' and
            comboxlist_motion3.get() == '' and
            comboxlist_motion4.get() == '' and
            comboxlist_motion5.get() == ''):
        pass

    if comboxlist_motion1.get() != '':
        mapping_key_bin[Motion.index(comboxlist_motion1.get())] = 1
    if comboxlist_motion2.get() != '':
        mapping_key_bin[Motion.index(comboxlist_motion2.get())] = 1
    if comboxlist_motion3.get() != '':
        mapping_key_bin[Motion.index(comboxlist_motion3.get())] = 1
    if comboxlist_motion4.get() != '':
        mapping_key_bin[Motion.index(comboxlist_motion4.get())] = 1
    if comboxlist_motion5.get() != '':
        mapping_key_bin[Motion.index(comboxlist_motion5.get())] = 1

    # 键鼠行为设定为空，跳出提示，并退出函数
    if (comboxlist_action1.get() == '' and
            comboxlist_action2.get() == '' and
            comboxlist_action3.get() == ''):
        pass

    if comboxlist_action1.get() != '':
        mapping_value.append(comboxlist_action1.get())
    if comboxlist_action2.get() != '':
        mapping_value.append(comboxlist_action2.get())
    if comboxlist_action3.get() != '':
        mapping_value.append(comboxlist_action3.get())

    mapping_key = ''.join(map(str, mapping_key_bin))
    # 如果该手势已经被设定，跳出提示，并退出函数
    if mapping_key in mapping:
        pass
    else:
        mapping[mapping_key] = mapping_value
    # print(mapping_key)

    # 显示映射关系
    global showing_count
    showing_str1 = ''
    showing_str2 = ''

    for i in range(len(mapping_key)):
        if mapping_key[i] == '1':
            showing_str1 += Motion[i] + ' + '
    showing_str1 = showing_str1[:-3]

    for x in mapping_value:
        showing_str2 += x + ' + '
    showing_str2 = showing_str2[:-3]

    showing_motion.append(tk.Label(window, text=showing_str1, height=2, width=34, font=('Arial', 10),
                                   wraplength=320, justify='left'))
    showing_motion[showing_count].place(x=mapping_show_x, y=mapping_show_y + showing_count * 50)
    showing_action.append(tk.Label(window, text=showing_str2, height=2, width=20, font=('Arial', 10),
                                   wraplength=180, justify='left'))
    showing_action[showing_count].place(x=mapping_show_x + 360, y=mapping_show_y + showing_count * 50)

    showing_arrow.append(tk.Label(window, image=photo_arrow, bg='seashell3'))
    showing_arrow[showing_count].place(x=mapping_show_x + 325, y=mapping_show_y + showing_count * 50 + 10)

    showing_count += 1

    # 清空选择框，回到初始状态
    reset_mapping()


# 重新设置的函数
def reset_mapping():
    # 清空选择框，回到初始状态
    comboxlist_motion1.set('')
    comboxlist_motion2.set('')
    comboxlist_motion3.set('')
    comboxlist_motion4.set('')
    comboxlist_motion5.set('')
    comboxlist_action1.set('')
    comboxlist_action2.set('')
    comboxlist_action3.set('')

    comboxlist_motion2.place_forget()
    comboxlist_motion3.place_forget()
    comboxlist_motion4.place_forget()
    comboxlist_motion5.place_forget()
    comboxlist_action2.place_forget()
    comboxlist_action3.place_forget()

    add_motion2.place_forget()
    add_motion3.place_forget()
    add_motion4.place_forget()
    add_action2.place_forget()

    add_motion1.place(x=220, y=70)
    add_action1.place(x=470, y=70)


# 清空所有映射的函数
def clear_mapping():
    # 清空映射
    mapping.clear()

    # 清空显示
    global showing_count
    for x in showing_motion:
        x.destroy()
    for x in showing_action:
        x.destroy()
    for x in showing_arrow:
        x.destroy()
    showing_motion.clear()
    showing_action.clear()
    showing_arrow.clear()
    showing_count = 0


# 加号按钮的图案
photo_plus = tk.PhotoImage(file="plus.png").subsample(10, 10)
# 8个下拉框
comvalue_motion1 = tk.StringVar().set('')
comboxlist_motion1 = ttk.Combobox(window, textvariable=comvalue_motion1, font=('Arial', 10), width=15, height=20)  # 初始化
comboxlist_motion1["values"] = Motion
comboxlist_motion1.place(x=50, y=70)
add_motion1 = tk.Button(window, image=photo_plus, command=add_motion_1)
add_motion1.place(x=220, y=70)

comvalue_motion2 = tk.StringVar().set('')
comboxlist_motion2 = ttk.Combobox(window, textvariable=comvalue_motion2, font=('Arial', 10), width=15, height=20)  # 初始化
comboxlist_motion2["values"] = Motion
add_motion2 = tk.Button(window, image=photo_plus, command=add_motion_2)

comvalue_motion3 = tk.StringVar().set('')
comboxlist_motion3 = ttk.Combobox(window, textvariable=comvalue_motion3, font=('Arial', 10), width=15, height=20)  # 初始化
comboxlist_motion3["values"] = Motion
add_motion3 = tk.Button(window, image=photo_plus, command=add_motion_3)

comvalue_motion4 = tk.StringVar().set('')
comboxlist_motion4 = ttk.Combobox(window, textvariable=comvalue_motion4, font=('Arial', 10), width=15, height=20)  # 初始化
comboxlist_motion4["values"] = Motion
add_motion4 = tk.Button(window, image=photo_plus, command=add_motion_4)

comvalue_motion5 = tk.StringVar().set('')
comboxlist_motion5 = ttk.Combobox(window, textvariable=comvalue_motion5, font=('Arial', 10), width=15, height=20)  # 初始化
comboxlist_motion5["values"] = Motion

comvalue_action1 = tk.StringVar().set('')
comboxlist_action1 = ttk.Combobox(window, textvariable=comvalue_action1, font=('Arial', 10), width=15, height=20)  # 初始化
comboxlist_action1["values"] = Mouse + Keyboard
comboxlist_action1.place(x=300, y=70)
add_action1 = tk.Button(window, image=photo_plus, command=add_action_1)
add_action1.place(x=470, y=70)

comvalue_action2 = tk.StringVar().set('')
comboxlist_action2 = ttk.Combobox(window, textvariable=comvalue_action2, font=('Arial', 10), width=15, height=20)  # 初始化
comboxlist_action2["values"] = Mouse + Keyboard
add_action2 = tk.Button(window, image=photo_plus, command=add_action_2)

comvalue_action3 = tk.StringVar().set('')
comboxlist_action3 = ttk.Combobox(window, textvariable=comvalue_action3, font=('Arial', 10), width=15, height=20)  # 初始化
comboxlist_action3["values"] = Mouse + Keyboard

# 相关按钮
b_set = tk.Button(window, text='Set', width=8, height=1, command=set_mapping)
b_set.place(x=530, y=185)
b_reset = tk.Button(window, text='Reset', width=8, height=1, command=reset_mapping)
b_reset.place(x=530, y=230)
b_clear = tk.Button(window, text='Clear', width=8, height=1, command=clear_mapping)
b_clear.place(x=530, y=750)


def KeyboardMouse(args):
    if len(args) == 1:
        if args[0] in Mouse:
            if args[0] == 'Left Click':
                pyautogui.click()
            elif args[0] == 'Right Click':
                pyautogui.rightClick()
            elif args[0] == 'Double Click':
                pyautogui.doubleClick()
            elif args[0] == 'Scroll Up':
                pyautogui.scroll(clicks=200)
            elif args[0] == 'Scroll Down':
                pyautogui.scroll(clicks=-200)

        elif args[0] in Keyboard:
            pyautogui.press(args[0])
    elif len(args) == 2:
        pyautogui.hotkey(args[0], args[1])
    elif len(args) == 3:
        pyautogui.hotkey(args[0], args[1], args[2])


# 模拟测试：设置三个映射
# 1.五个手指弯曲 '11111000000000000' --->ppt从头放映（F5） 
# 2.向上加速 '00000000010000000' --->上一页（滚轮向上）
# 3.向下加速 '00000000001000000' --->下一页（滚轮向下）
# 4.除了大拇指以外的四指弯曲 '01111000000000000' --->结束放映（esc）
# 模拟输入信号中可能存在错误信号，忽略之
input_str = ['00000000000000000', '11111000000000000',
             '00000000001000000', '00000000001000000',
             '00000000010000000', '00000000010000000',
             '01111000000000000']

# 选择串口端口
l_port = tk.Label(window, text='Serial Port', font=("Arial", 10))
l_port.place(x=650, y=50)

port_list = list(list_ports.comports())

comvalue_port = tk.StringVar().set('')
comboxlist_port = ttk.Combobox(window, textvariable=comvalue_port, font=('Arial', 10), width=10, height=5)  # 初始化
comboxlist_port["values"] = port_list
comboxlist_port.place(x=650, y=75)


# PortData = Port("COM3")

# 选择串口

# 11位串口信号 转换为 17位信号
def portstr2mystr(portstr):
    mystr = portstr[0:5]
    for x in portstr[5:]:
        if x == '0':
            mystr += '00'
        elif x == '1':
            mystr += '10'
        elif x == '2':
            mystr += '01'
    return mystr


flag = True


def start():
    PortData = Port(comboxlist_port.get()[0:4])
    #PortData = Port("COM3")
    time.sleep(1)
    pyautogui.moveTo(screenWidth / 2, screenHeight / 2, duration=0.25)
    # 这里应用串口通信传入信号
    global flag
    flag=True
    print(mapping)
    
    while flag:
        window.update()
        if not flag:
            return
        x = PortData.getData()
        if len(x) != 0:
            print(x)
            print(portstr2mystr(x))
        #time.sleep(1)
        if portstr2mystr(x) in mapping.keys():
            KeyboardMouse(mapping[portstr2mystr(x)])
            time.sleep(2)
            PortData.flush()




def stop():
    global flag
    flag = False
    print("stop")


b_stop = tk.Button(window, text='Stop', width=8, height=2, command=stop)
b_stop.place(x=700, y=250)

file_path = ''
file_text = ''

def open_job():
    global file_path
    global file_text
    file_path = filedialog.askopenfilename(title=u'选择文件', initialdir=(os.path.expanduser('F:/')))
    print('打开文件：', file_path)
    if file_path is not None:
        #with open(file=file_path, mode='r+', encoding='utf-8') as file:
            #file_text = file.read()
        #text1.insert('insert', file_text)
        with open(file_path,'r') as f:
            mapping=json.load(f)
        print(mapping)
    
    key = list(mapping.keys())
    value = list(mapping.values())
    print(key)
    print(value)

    global showing_count
    showing_count=len(key)
    
    for i in range(showing_count):
        showing_str1 = ''
        showing_str2 = ''
        mapping_key = key[i]
        mapping_value = value[i]
        for j in range(len(mapping_key)):
            if mapping_key[j] == '1':
                showing_str1 += Motion[j] + ' + '
        showing_str1 = showing_str1[:-3]

        for x in mapping_value:
            showing_str2 += x + ' + '
        showing_str2 = showing_str2[:-3]

        showing_motion.append(tk.Label(window, text=showing_str1, height=2, width=34, font=('Arial', 10),
                                   wraplength=320, justify='left'))
        showing_motion[i].place(x=mapping_show_x, y=mapping_show_y + i * 50)
        showing_action.append(tk.Label(window, text=showing_str2, height=2, width=20, font=('Arial', 10),
                                   wraplength=180, justify='left'))
        showing_action[i].place(x=mapping_show_x + 360, y=mapping_show_y + i * 50)

        showing_arrow.append(tk.Label(window, image=photo_arrow, bg='seashell3'))
        showing_arrow[i].place(x=mapping_show_x + 325, y=mapping_show_y + i * 50 + 10)

def save_job():
    global file_path
    global file_text
    file_opt = options = {}
    options['filetypes'] = [('all files', '.*'), ('text files', '.json')]
    #options['initialfile'] = 'myfile.json'
    file_path = filedialog.asksaveasfile(title=u'保存文件',defaultextension=".json", **file_opt)
    print('保存文件：', file_path)
    if file_path is not None:
        #savefile = filedialog.asksaveasfile(defaultextension=".json", **file_opt)
        json.dump(mapping, file_path)
        #np.save()
        #with open(file=file_path, mode='a+', encoding='utf-8') as file:
            #file.write(file_text)
        print('保存完成')

class about_job(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Magic Glove 1.0')
        self.root.geometry('400x200')
        #self.root.resizable(False, False)
        self.text='''Author : Computer Network Team

Date : 2020/12/13'''
        tk.Label(self.root,text=self.text,font=('Arial', 12,'bold')).place(x=40,y=50)
        self.root.mainloop()



menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='Open', command=open_job)
filemenu.add_command(label='Save', command=save_job)
filemenu.add_separator()
filemenu.add_command(label='Exit', command=window.quit)

helpmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=helpmenu)
helpmenu.add_command(label='About', command=about_job)


# 开始键
if __name__ == '__main__':
    b_start = tk.Button(window, text='Start', width=8, height=2, command=start)
    b_start.place(x=700, y=200)
    window.config(menu=menubar)
    window.mainloop()
