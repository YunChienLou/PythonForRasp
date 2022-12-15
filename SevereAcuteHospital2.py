from ast import Str
from xmlrpc.client import Boolean
import requests
from bs4 import BeautifulSoup
import tkinter as tk
import psutil
from datetime import datetime


class Fullscreen_Example:
    def __init__(self):
        self.window = tk.Tk()
        self.fullScreenState = False
        self.window.attributes("-fullscreen", self.fullScreenState)
        self.window.title('北市醫學中心滿床')
        self.w, self.h = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.window.geometry("%dx%d" % (self.w, self.h))
        self.window.configure(background='#242526')
        self.window.bind("<F11>", self.toggleFullScreen)
        self.window.bind("<Escape>", self.quitFullScreen)
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure([0, 1, 2, 3, 4], weight=1)
        self.window.state('zoomed')
        self.updater()
        self.window.mainloop()

    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.window.attributes("-fullscreen", self.fullScreenState)

    def quitFullScreen(self, event):
        self.fullScreenState = False
        self.window.attributes("-fullscreen", self.fullScreenState)

    def updater(self):
        self.window.after(5000, self.updater)
        fetchData()
        UI(self)


class Images:
    def __init__(self, image1, image2, image3, image4, image5, image6):
        self.low_battery_photo = image1
        self.mid_battery_photo = image2
        self.charging_battery_photo = image3
        self.no_wifi_photo = image4
        self.full_battery_photo = image5
        self.wifi_image_photo = image6


url = 'https://www.nhi.gov.tw/SysService/SevereAcuteHospital.aspx'
url2 = 'https://wapps.mmh.org.tw/WebEMR/WebEMR/Default.aspx'
url3 = 'https://reg.ntuh.gov.tw/EmgInfoBoard/NTUHEmgInfo.aspx'
response = []
requestStatus = []
targetHospital = ['新光醫院', '臺北榮總']


def UI(self):
    # batteryStatus = battery()
    # Position image
    if len(response) == 0:
        return
    else:
        for idx, res in enumerate(response):
            tk.Label(self.window, text=res['hos'], bg="#222831" if res['isFull'] == True else "#393E46", fg="#FF6363" if res['isFull'] == True else "#03C4A1", wraplength=1, font=("Arial", 85)).grid(
                column=idx, row=0, sticky="nsew")
        tk.Label(self.window, text=('正常連線' if requestStatus[0]['code'] == 200 else '連線失敗') + "\n" + requestStatus[0]['timeStamp'], bg="#222831" if not requestStatus[0]
                 ['code'] == 200 else "#393E46", fg="#FF6363" if not requestStatus[0]['code'] == 200 else "#03C4A1", font=("Arial", 25)).grid(column=4, row=0, sticky="nsew")
        # tk.Label(self.window, text='充電中' if batteryStatus.power_plugged else "電池剩餘 : \n" + secs2hours(batteryStatus.secsleft),
        #          bg="#222831" if not batteryStatus.power_plugged else "#393E46", fg="#FF6363" if not batteryStatus.power_plugged else "#03C4A1", font=("Arial", 25)).grid(column=2, row=1, sticky="nsew")


def battery():
    battery = psutil.sensors_battery()
    return battery


def secs2hours(secs):
    mm, ss = divmod(secs, 60)
    hh, mm = divmod(mm, 60)
    return "%d:%02d:%02d" % (hh, mm, ss)


def fetchData():
    response.clear()
    requestStatus.clear()
    reponse = {'hos': Str, 'isFull': Boolean}
    reponse1 = {'hos': Str, 'isFull': Boolean}
    try:
        res = requests.get(url, timeout=4)
        res2 = requests.get(url2, timeout=4)
        res3 = requests.get(url3, timeout=4)
    except (requests.exceptions.Timeout, requests.exceptions.TooManyRedirects, requests.exceptions.RequestException, requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as err:
        response.append({'hos': "連線中斷", 'isFull': True})
        print(err)

    soup = BeautifulSoup(res2.text, 'lxml')
    soup2 = BeautifulSoup(res3.text, 'lxml')
    fontList = soup.find_all('font')
    fontList2 = soup2.find_all('div')

    if fontList[6].get_text() == "否":
        isFull = False
    else:
        isFull = True
    reponse['hos'] = '台北馬偕'
    reponse['isFull'] = isFull

    if fontList2[3].get_text().strip() == "目前本院未通報119滿床":
        isFull2 = False
    else:
        isFull2 = True
    reponse1['hos'] = '臺大醫院'
    reponse1['isFull'] = isFull2
    response.append(reponse)
    response.append(reponse1)

    requestStatus.append(
        {'code': res.status_code, 'timeStamp': datetime.now().strftime("%H:%M:%S")})
    soup = BeautifulSoup(res.text, 'lxml')
    table = soup.find(id='movie-table')
    hospitalTitle = table.find_all(
        'td', {'class': ['HospTitle', 'li_lastchild']})
    for idx, x in enumerate(hospitalTitle):
        dataElement = {'hos': Str, 'isFull': Boolean}
        nameForCheck = x.get_text().strip()
        if nameForCheck in targetHospital:
            hospitalStatus = hospitalTitle[idx+1].get_text().strip()
            dataElement['hos'] = x.get_text().strip()
            dataElement['isFull'] = True if hospitalStatus == '是' else False
            response.append(dataElement)


if __name__ == '__main__':
    app = Fullscreen_Example()
