#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
from tkinter import messagebox
from crypto import EncryptData,getEntrypyKey
from tkinter import *
import pywifi
from pywifi import const,Profile
from logger import PyLog
import os

logger = PyLog()
wifiDict = {}
dir = "C:\\Users\\Administrator\\AppData\\Local\\lsTool\\"

def disconnect_wifi():
    """
    判断本机是否有无线网卡,以及连接状态
    :return: 已连接或存在无线网卡返回1,否则返回0
    """
    # 创建一个元线对象
    wifi = pywifi.PyWiFi()
    # 取当前机器,第一个元线网卡
    iface = wifi.interfaces()[0]  # 有可能有多个无线网卡,所以要指定
    # 判断是否连接成功
    if iface.status() in [const.IFACE_CONNECTED, const.IFACE_INACTIVE]:
        logger.info("wifi已连接")
        iface.disconnect()
        logger.info("wifi已经断开连接")
        return 0
    else:
        logger.error("wifi未连接")
        return 1

def connect_wifi():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    profile = Profile()
    wifiUn = wifiDict["wifiName"]
    wifiPw = wifiDict["wifiPw"]
    if not wifiUn or not wifiPw:
        messagebox.showinfo("提示","用户名和密码为空")
        return
    profile.ssid = wifiUn   #用户名
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)  #加密类型
    profile.cipher = const.CIPHER_TYPE_CCMP
    decription = EncryptData(getEntrypyKey())
    profile.key = decription.decrypt(wifiPw)
    iface.remove_all_network_profiles() #清除其他配置文件
    tmp_profile = iface.add_network_profile(profile) #加载配置文件
    iface.connect(tmp_profile)
    time.sleep(1)
    if iface.status() == const.IFACE_CONNECTED :
        logger.info('重新连接成功')
    else:
        logger.error('连接失败，重新连接')
        messagebox.showinfo("提示", "连接失败，请重新设置用户名和密码")

def reConnect_wifi():
    wifiInfo = readFile()
    if not wifiInfo:
        return
    disconnect_wifi()
    time.sleep(6)
    connect_wifi()

def wifiInfo():
    info = Tk()
    info.title("wifi信息")
    info.attributes("-toolwindow",1);#窗口只显示关闭按钮
    info.attributes("-topmost",True)#显示在最前端
    screenwidth = tk.winfo_screenwidth() / 2
    screenheight = tk.winfo_screenheight() / 2.5
    info.geometry("+%d+%d" % (screenwidth, screenheight))

    wifiNameLabel = Label(info,text="wifi名称：")
    wifiNameLabel.pack()
    wifiNameText = Entry(info)
    wifiNameText.pack()

    wifiPwLabel = Label(info,text="wifi密码")
    wifiPwLabel.pack()
    wifiPwText = Entry(info,show="*")
    wifiPwText.pack()

    def writeFile():
        wifiName = wifiNameText.get()
        wifiPw = wifiPwText.get()
        entryptionKey = getEntrypyKey()
        entryption = EncryptData(entryptionKey)
        entryptPwd = entryption.encrypt(wifiPw)

        with open(dir + "000xxx","w") as fo:
            fileText = wifiName + "\n" + entryptPwd
            fo.write(fileText)
        info.destroy()

    Button(info,text="确认",command=writeFile).pack()
    info.mainloop()

def readFile():
    global wifiDict
    if not os.path.isfile(dir + "000xxx"):
        messagebox.showinfo("提示","请先进行用户名和密码设置")
        return
    with open(dir + "000xxx","r") as fo:
        context = fo.readlines()
        if(len(context) != 2):
            messagebox.showinfo("提示","请正确填写WIFI用户名和密码")
            return
        wifiDict["wifiName"] = context[0].strip("\n")
        wifiDict["wifiPw"] = context[1]
    return wifiDict

if __name__ == '__main__':
    tk = Tk()
    tk.title("WIFI重连工具")
    # 顶级菜单
    menubar = Menu(tk)
    # 一级菜单
    fmenu = Menu(menubar)
    fmenu.add_command(label="连接", command=wifiInfo)
    # 菜单关联
    menubar.add_cascade(label="设置", menu=fmenu)

    # command 函数加() 后不用点击按钮动作就会自动执行
    B = Button(tk, text="重连", command=reConnect_wifi, width=15, height=3, fg="green", activeforeground="red",
               relief="raised")
    tk.attributes("-toolwindow", 1)  # 只显示关闭按钮,不显示最小化和最大化
    tk.attributes("-topmost", True)  # 界面显示在最前端
    # tk.overrideredirect(True) # 工具栏全部不显示
    B.pack()
    tk['menu'] = menubar
    screenwidth = tk.winfo_screenwidth() / 2.5
    screenheight = tk.winfo_screenheight() / 2.5

    tk.geometry("+%d+%d"%(screenwidth,screenheight))
    tk.mainloop()