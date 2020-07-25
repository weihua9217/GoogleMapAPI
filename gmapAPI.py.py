import googlemaps
import pandas as pd
import openpyxl
import os

GOOGLE_API_KEY = "AIzaSyAULDBUmyyVaydPXJ_eim6WjIYupEQT_Rs"
gmaps = googlemaps.Client(key= GOOGLE_API_KEY)
df = pd.read_csv('2020Q2盤點花蓮縣20200720-即時.csv')
init_school = list()
target_school = list()
init = "臺東縣立初鹿國民中"
init_school.append("台東縣卑南鄉忠孝路2號")
# init_school.append("花蓮縣壽豐鄉中山路299號")

target = list()
for i in df["學校名稱"]:
    target.append(i)

for i in df["學校地址"]:
    target_school.append(i)

print(init_school)
print(len(target_school))
#
distance = list()
duration = list()

for i in range(len(target_school)):
    if("綠島"in target_school[i]):
        print("綠島")
        distance.append("None")
        duration.append("None")
    elif("蘭嶼"in target_school[i]):
        print("蘭嶼")
        distance.append("None")
        duration.append("None")
    else:
        all = gmaps.distance_matrix(init_school[0], target_school[i], mode='driving', region="tw")["rows"][0]["elements"][0]
        print(i,all)
        my_dist = all["distance"]["text"]
        # print(my_dist)
        my_duration = all["duration"]["text"]
        # print(my_duration)
        distance.append(my_dist)
        duration.append(my_duration)

df2 = pd.DataFrame({'起始學校':init,'目標學校':target,'距離':distance,'時間':duration})
df2.index = df2.index+1
df2.to_excel("初鹿國中_花蓮縣.xlsx",index=True)

