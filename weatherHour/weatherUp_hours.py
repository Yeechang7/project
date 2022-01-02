#### 每小時更新 - 獲取每小時氣候資料####
import requests
from bs4 import BeautifulSoup
import time

'''
loc1 = 大園區
loc2 = 桃園區
loc3 = 觀音區
loc4 = 平鎮區
loc5 = 龍潭區
loc6 = 中壢區
'''
# 各站點資訊
loc_dict = {'loc1': 'e8fcf1233159a2bf6d5628d7242379b2d102ae9f7ab86c5af10e9754d2043955',
            'loc2': '2063dc93d721d794396441c2473f2d3e6e5b335903034198829e1e86eb9e83e0',
            'loc3': '31db554b69ded55ded416d34f7f8e9845f60a4a7c139f73b2e65b1592a13988b',
            'loc4': '3c45ef1549c42db5a6908f760ceab0619d21487c88a133ffe6e4332bff1588a1',
            'loc5': 'adff3d6961c3ca9833a8b72fdf2587b20a0efa40b22b5ce1134f98982cf13dcc',
            'loc6': '0005d4c25ae305606e1095778b12d1224780ea0bed47dd95e90983daf35cac1e'}

weatherDataHours = []
for locs in loc_dict.values():
    url = f'https://weather.com/zh-TW/weather/hourbyhour/l/{locs}'
    header = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
    res = requests.get(url, headers=header)
    soup = BeautifulSoup(res.text, 'html.parser')
    loc = soup.select_one('.LocationPageTitle--PresentationName--1QYny').text.split(', ')[0]
    # dateTime = soup.select_one('.DetailsSummary--daypartName--2FBp2').text
    times = time.strftime("%Y/%m/%d %H:%M", time.localtime())
    temp = soup.select('.DetailsTable--value--1q_qD')[0].text.split('°')[0]
    hum = soup.select('.DetailsTable--value--1q_qD')[2].text.split('%')[0]
    rain = soup.select('.DetailsSummary--precip--1ecIJ')[0].text.split('Rain')[1].split('%')[0]
    wType = soup.select('p[data-testid="hourlyWxPhrase"]')[0].text
    print(f'地區：{loc} , 時間：{times} , 溫度：{temp} , 濕度：{hum} , 降雨機率：{rain} , 天氣型態：{wType}')
    weather2tuple = tuple([loc, times, temp, hum, rain, wType])
    weatherDataHours.append(weather2tuple)
    print('資料轉換成功')

insert = 'insert into weather_hour_data (loc,date,temp,hum,rain,wType) values (%s,%s,%s,%s,%s,%s)'
table = 'weather_hour_data'


def Mysql_insert(sql_insert, table, data):
    import pymysql
    config = {
        "host": "airiot.tibame.cloud",
        "port": 3306,
        "user": "yi",
        "passwd": "yi",
        "db": "weather_status",
        "charset": "utf8mb4"
    }

    conn = pymysql.connect(**config)  ## **會將字典型態轉變(kwargs)
    cursor = conn.cursor()
    cursor.execute("select * from {}".format(table))
    cursor.executemany(sql_insert, data)
    conn.commit()
    print('資料筆數 :', cursor.execute("select * from {}".format(table)))

    # 關閉連線
    cursor.close()
    conn.close()


Mysql_insert(insert, table, weatherDataHours)