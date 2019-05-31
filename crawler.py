# -*- coding: utf-8 -*-
"""
Created on Sat May  4 15:23:59 2019

@author: USER
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def answer(rno,pwd):
    
    payload ={
            "COP": "SELF",
            "RNO": rno,
            "PWD": pwd
            #"SEND": "unable to decode value)"
            }
    headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Length": "58",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": "RNO=1"+rno+"11; _ga=GA1.3.1801870677.1542455490; _gid=GA1.3.1242989202.1555306384",
            "Host": "www.libwebpac.yuntech.edu.tw",
            "Origin": "http://www.libwebpac.yuntech.edu.tw",
            "Referer": "http://www.libwebpac.yuntech.edu.tw/Webpac2/Person.dll/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36" 
            }
    
    r=requests.session()
    
    r2 = r.get("http://www.libwebpac.yuntech.edu.tw/Webpac2/Person.dll/login",data=payload,headers=headers)
    
    #print(r2.text)
    soup=BeautifulSoup(r2.text,"html.parser")
    print(soup)
    
    u = soup.select("html frame") #a標籤
    
    try:
        a=str(u[0])
    except IndexError:
        str2="帳號或密碼錯誤"
        return str2, False
    
    
    str1=""
    
    """print(a[95:159])#擷取transkey
    print(a[163:180])#擷取transkey
    print(a[184:-3])#擷取transkey
    """
    str1+=a[95:159]
    str1+=a[163:180]
    str1+=a[184:-3]
    #print(str1)
    headers1={
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Cookie": "RNO=1"+rno+"11; _ga=GA1.3.1801870677.1542455490; _gid=GA1.3.1242989202.1555306384; _gat=1",
        "Host": "www.libwebpac.yuntech.edu.tw",
        "Referer": "http://www.libwebpac.yuntech.edu.tw/Webpac2/Person.dll/NAV?"+str1,
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"  
        }
    
    r3 = r.get("http://www.libwebpac.yuntech.edu.tw/Webpac2/Person.dll/NAV?"+str1,headers=headers1)#傳封包盜借書的網站
    
    soup1=BeautifulSoup(r3.text,"html.parser")
    y=soup1.select("html li")
    
    str2=""
    b=str(y[0])
    str2+=b[110:144]#擷取ck (hiddenfunction)
    #print(str2)
    
    str3=""
    str3+=a[95:159]
    str3+=b[110:144]
    str3+=a[184:-3]
    url = "http://www.libwebpac.yuntech.edu.tw/Webpac2/Person.dll/BORROW?"+str3
    df = pd.read_html(url)[2]  ## 回傳DataFrame類別的陣列
    
    result = []
    for i in range(1,df.shape[0]):
        result.append({'library': df[2][i], 'bookname': df[3][i], 'due': time.strptime(df[5][i], "%Y/%m/%d")})

    return result, True

if __name__ == '__main__':
    import sys    
    myid = input("id:")
    pwd = input("pwd:")
    for entry in answer(myid,pwd):
        print(entry['library'], entry['bookname'], str(entry['due']))
