import requests
url = 'https://covid-19.nchc.org.tw/api/covid19?CK=covid-19@nchc.org.tw&querydata=5002&limited=全部縣市'
res = requests.get(url)
date = res.json()[0]['a01']
covid19_Taiwan = []
covid19_Foreign = []
# for i in res.json():
#     if (i["a03"] == "境外移入") & (i["a04"] == "全區") & (i["a01"] >= date):
#         data = (i["a01"], int(i["a05"]))
#         covid19_Foreign.append(data)
#         print(covid19_Foreign)
        # =============================================================================
        ### COVID19 - 變數介紹
        # "id":"ID", "a01":"個案研判日", "a02":"個案公佈日", "a03":"縣市別"
        #            "a04":"區域", "a05":"新增確診人數","a06":"累計確診人數"}
        # =============================================================================
Tyn = ['桃園區','中壢區']
for i in res.json():
    if (i["a03"] != "境外移入") & (i["a04"] != "全區") & (i["a01"] >= date):
        data = [i["a01"], i["a03"], i["a04"], int(i["a05"])]
        covid19_Taiwan.append(data)




