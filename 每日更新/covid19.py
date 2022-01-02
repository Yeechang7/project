########### 每天抓取一次即可 ###########
########### 每天抓取一次即可 ###########
########### 每天抓取一次即可 ###########
import requests
import pymysql

# =============================================================================
# SQL連線
# =============================================================================
config = {"host": "airiot.tibame.cloud", "port": 3306, "user": "yi",
          "passwd": "yi", "db": "disease", "charset": "utf8mb4"
          }
conn = pymysql.connect(**config)  ## **會將字典型態轉變(kwargs)
cursor = conn.cursor()

# =============================================================================
### COVID19 - 變數介紹
# "id":"ID", "a01":"個案研判日", "a02":"個案公佈日", "a03":"縣市別"
#            "a04":"區域", "a05":"新增確診人數","a06":"累計確診人數"}
# =============================================================================
### 境外移入
url = 'https://covid-19.nchc.org.tw/api/covid19?CK=covid-19@nchc.org.tw&querydata=5002&limited=全部縣市'
res = requests.get(url)
covid19_Foreign = []
date = res.json()[0]['a01']
for i in res.json():
    if (i["a03"] == "境外移入") & (i["a04"] == "全區") & (i["a01"] >= date):
        data = (i["a01"], int(i["a05"]))
        covid19_Foreign.append(data)

conn = pymysql.connect(**config)  ## **會將字典型態轉變(kwargs)
cursor = conn.cursor()
cursor.execute("select * from covid19_foreign")
sql_insert = 'insert into covid19_foreign (date,number) values (%s,%s)'
cursor.executemany(sql_insert, covid19_Foreign)

# =============================================================================
### 台灣
covid19_Taiwan = []
for i in res.json():
    if (i["a03"] != "境外移入") & (i["a04"] != "全區") & (i["a01"] >= date):
        data = [i["a01"], i["a03"], i["a04"], int(i["a05"])]
        #         data2tuple = tuple([i["a01"], i["a03"],i["a04"], int(i["a05"])])
        covid19_Taiwan.append(data)

cursor.execute("select * from covid19")
sql_insert = 'insert into covid19(date,city,district,number) values (%s,%s,%s,%s)'
cursor.executemany(sql_insert, covid19_Taiwan)

# # =============================================================================
# ### 流感
# # =============================================================================
# response = requests.get("https://od.cdc.gov.tw/eic/NHI_Influenza_like_illness.json")
# data_json = response.json()
# influenza = []
# for i in data_json:
#     if (i["年"] == "2021") & (i["縣市"] == "桃園市"):
#         data = [i["就診類別"], i["年"], i["年齡別"], i["縣市"], i["週"], i["類流感健保就診人次"]]
# #         data2tuple = tuple(data = [i["健保就診總人次"], i["就診類別"], i["年"], i["年齡別"], i["縣市"], i["週"], i["類流感健保就診人次"]])
#         influenza.append(data)

# cursor.execute("select * from influenza")
# sql_insert = 'insert into influenza(type,year,age,county,week,cases) values (%s,%s,%s,%s,%s,%s)'
# cursor.executemany(sql_insert, influenza)

# # =============================================================================
# ### 腸病毒
# # =============================================================================
# response = requests.get("https://od.cdc.gov.tw/eic/NHI_EnteroviralInfection.json")
# data_json = response.json()
# enterovirus = []
# for i in data_json:
#     if i["縣市"] == "桃園市":
#         if (i["年"] <= "2021") & (i["年"] > "2018"):
#             data = (i["就診類別"], int(i["年"]), i["年齡別"], i["縣市"], int(i["週"]), int(i["腸病毒健保就診人次"]))
#             enterovirus.append(data)

# cursor.execute("select * from enterovirus")
# sql_insert = 'insert into enterovirus(type,year,age,county,week,cases) values (%s,%s,%s,%s,%s,%s)'
# cursor.executemany(sql_insert, enterovirus)

conn.commit()
cursor.close()
conn.close()
