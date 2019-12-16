import requests
import csv
import re
import time
from bs4 import BeautifulSoup

pages = 281
i = 1
datas = []
url_base = "https://fortiguard.com/appcontrol?deepapp=&page="

s = requests.Session()

while pages + 1 > i:
    print("page:",i)
    url = url_base + str(i)
    try:
        get_url_info = s.get(url)
        bs4Obj = BeautifulSoup(get_url_info.text, 'lxml')
        app_list = bs4Obj.find_all('div', class_="title")
        if len(app_list) == 0:
            continue
    except Exception as e:
        print(e)
        time.sleep(1)
        continue
    j = 0
    while True:
        try:
            app_name = str(app_list[j].find('a').get_text())
            app_num = int(re.findall('[0-9]+', app_list[j].find('a').get('href'))[0])
            data = [app_num, app_name]
            datas.append(data)
            j += 1
        except:
            break
    i += 1

print("result:",len(datas))

with open('appid.csv', 'w') as file:
    writer = csv.writer(file, lineterminator='\n')
    writer.writerows(datas)
