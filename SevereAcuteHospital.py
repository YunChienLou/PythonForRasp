from xmlrpc.client import Boolean
import requests
from bs4 import BeautifulSoup

reponse = {
    'NTUH': Boolean,
    'MMH' : Boolean
}
url2 = 'https://wapps.mmh.org.tw/WebEMR/WebEMR/Default.aspx'
url3 = 'https://reg.ntuh.gov.tw/EmgInfoBoard/NTUHEmgInfo.aspx'
res = requests.get(url2).text
res2 = requests.get(url3).text
soup = BeautifulSoup(res,'lxml')
soup2 = BeautifulSoup(res2,'lxml')
fontList = soup.find_all('font')
fontList2 = soup2.find_all('div')
isFull = Boolean
isFull2 = Boolean
if fontList[6].get_text() == "否" : 
    isFull = False
else :
    isFull = True
reponse['MMH'] = isFull
reponse['NTUH'] = isFull2

if fontList2[3] == "目前本院未通報119滿床" : 
    isFull2 = False
else :
    isFull2 = True
reponse['MMH'] = isFull
reponse['NTUH'] = isFull2
print(reponse)
