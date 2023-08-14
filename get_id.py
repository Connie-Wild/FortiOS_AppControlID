import requests
import csv
import re
import time
from bs4 import BeautifulSoup

s = requests.Session()

url = 'https://www.fortiguard.com/appcontrol'

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
headers = {
    'User-Agent': user_agent
}

while True:
    try:
        get_url_info = s.get(url, headers=headers, timeout=5)
        get_url_info.raise_for_status()
        bs4Obj = BeautifulSoup(get_url_info.content, 'lxml')
        result = bs4Obj.find('div', class_='sidebar-content')
        appids = int(re.findall('[0-9]+', result.find('a').get_text().replace(',', ''))[0])
        perPage = int(len(bs4Obj.find_all('div', class_='title')))
        break
    except Exception as e:
        print(e)
        time.sleep(1)
        continue

if appids % perPage == 0:
    pages = int(appids // perPage)
else:
    pages = int(appids // perPage) + 1

i = 1
datas = []
url_base = 'https://www.fortiguard.com/appcontrol?page='

while pages + 1 > i:
    print('page:', i, '/', pages)
    url = url_base + str(i)
    try:
        time.sleep(1)
        get_url_info = s.get(url, headers=headers, timeout=5)
        get_url_info.raise_for_status()
        bs4Obj = BeautifulSoup(get_url_info.content, 'lxml')
        app_list = bs4Obj.find_all('div', class_='title')
        if len(app_list) != perPage:
            if i == pages:
                pass
            else:
                continue
    except Exception as e:
        print(e)
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

print('result:', len(datas), '/', appids)

with open('appid.csv', 'w') as file:
    writer = csv.writer(file, lineterminator='\n')
    writer.writerows(sorted(datas))
