# coding=utf-8
import hashlib
from http import cookiejar
import os
import random
import sys
import msvcrt
from urllib import parse,request






#登录参数之一
appid = "15000101"



cj = cookiejar.LWPCookieJar()
cookies = request.HTTPCookieProcessor(cj)
opener  = request.build_opener(cookies)

#默认协议头
DefaultHeaders = {
            "Accept":"*/*",
            "User-Agent":"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E)",
            "Accept-Language":"zh-cn",
            "Accept-Encoding":"gzip;deflate",
            "Connection":"keep-alive",
            "Referer":"http://qzone.qq.com"
}

#QQ登录
from urllib import request
from util.http import Http


class qqlogin:
    #QQ登录加密算法
    def md5(self,string):
        try:
            string = string.encode("utf-8")
        finally:
            return hashlib.md5(string).hexdigest().upper()

    def hexchar2bin(self,num):
        arry = bytearray()
        for i in range(0, len(num), 2):
            arry.append(int(num[i:i+2],16))
        return arry

    def Getp(self,password,verifycode):
        hashpasswd = self.md5(password)
        I = self.hexchar2bin(hashpasswd)
        H = self.md5(I + bytes(verifycode[2], encoding="ISO-8859-1"))
        G = self.md5(H + verifycode[1].upper())
        return G

    #验证码处理
    def GetVerifyCode(self):
        #判断是否需要验证码
        check = Http("http://check.ptlogin2.qq.com/check?regmaster=&uin=%s&appid=%s&r=%s"%(self.uin,appid,random.Random().random()))
        verify =  eval(check.split("(")[1].split(")")[0])
        verify = list(verify)
        if verify[0] == "1":
            img = "http://captcha.qq.com/getimage?uin=%s&aid=%s&%s"%(self.uin,appid,random.Random().random())
            with open("verify.jpg","wb") as f:
                rr = request.Request(url=img, headers=DefaultHeaders)
                f.write(opener.open(rr).read())
            os.popen("verify.jpg")
            verify[1] = input("需要输入验证码，请输入打开的图片\"verify.jpg\"中的验证码：\n").strip()
        return verify

    #登录
    def Login(self,uid,password,verifycode):
        p = self.Getp(password,verifycode)  #密码加密
        url = "http://ptlogin2.qq.com/login?ptlang=2052&u="+uid+"&p="+p+"&verifycode="+verifycode[1]+"&css=http://imgcache.qq.com/ptcss/b2/qzone/15000101/style.css&mibao_css=m_qzone&aid="+appid+"&u1=http%3A%2F%2Fimgcache.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone&ptredirect=1&h=1&from_ui=1&dumy=&fp=loginerroralert&action=2-14-13338&g=1&t=1&dummy="
        DefaultHeaders.update({"Referer":url}) #更新Referer
        res = Http(url,"utf-8",DefaultHeaders) #GET登录
        if res.find("登录成功") != -1:
            tempstr =  eval(res.split("(")[1].split(")")[0])
            tempstr = list(tempstr)
            print("\n昵称："+tempstr[5]+"，登录成功！")
            global checklogin
            checklogin = True
        elif res.find("验证码不正确") != -1:
            print("\n验证码错误，请重新登录")
            res = self.GetVerifyCode()
            # res = self.Login(uin,password,res)
        elif res.find("帐号或密码不正确，请重新输入") != -1:
            print("\n帐号或密码不正确，请重新输入")
            uin = input("请输入QQ号码:\n").strip()
            print("请输入QQ密码:")
            password = pwd_input().strip()
            res = self.GetVerifyCode()
            res = self.Login(uin,password,res)
        return res

    #初始化
    def __init__(self,uin,password):
        self.uin = uin  #账号、密码赋值
        self.password = password
        self.res = self.GetVerifyCode() #获取验证码
        self.Login(self.uin,self.password,self.res) #登录

#密码输入，cmd命令行下运行显示*号
def pwd_input():
    chars = []
    while True:
        try:
            newChar = msvcrt.getch().decode(encoding="utf-8")
        except:
            return input("【温馨提醒：当前未在cmd命令行下运行，密码输入无法隐藏】:\n")
        if newChar in "\r\n":
             break
        elif newChar == "\b":
             if chars:
                 del chars[-1]
                 msvcrt.putch("\b".encode(encoding="utf-8"))
                 msvcrt.putch( " ".encode(encoding="utf-8"))
                 msvcrt.putch("\b".encode(encoding="utf-8"))
        else:
            chars.append(newChar)
            msvcrt.putch("*".encode(encoding="utf-8"))
            print(chars)
    return ("".join(chars) )

#程序入口
if __name__ == "__main__":
    uin = input("请输入QQ号码:\n").strip()   #输入QQ账号
    print("请输入QQ密码:")                   #输入密码
    password = pwd_input().strip()
    qqlogin(uin,password)                   #登录到QQ网站
