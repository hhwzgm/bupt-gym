import requests
import re
import time
import json
import src

if src.USERNAME == '' or src.PASSWORD == '':
    print('请先设置学号和密码！')
    exit()

now_hour = time.strftime("%H", time.localtime())
now_min  = time.strftime("%M", time.localtime())
now_sec  = time.strftime("%S", time.localtime())
print("Excute in " + now_hour + ':' + now_min + ':' + now_sec)

now_hour = int(now_hour)
now_min = int(now_min)
now_sec = int(now_sec)

HOUR = src.HOUR
MIN= src.MIN

if now_hour < HOUR or (now_hour == HOUR and now_min < MIN):
    rest = HOUR - now_hour
    sleeptime = rest*3600 + (MIN-now_min)*60 - 60 + 40 - now_sec
    print("sleep:"+ str(sleeptime) + '|' +str(sleeptime//3600)+':'+str(sleeptime%3600//60)+':'+str((sleeptime%3600)%60))
    time.sleep(sleeptime)
    print("\nWake up in " + time.strftime("%H", time.localtime()) + ':' + time.strftime("%M", time.localtime()) + ':' + time.strftime("%S", time.localtime()))

while True:
    now_hour = int(time.strftime("%H", time.localtime()))
    now_min  = int(time.strftime("%M", time.localtime()))
    if now_hour == HOUR and now_min >= MIN:
        break

time.sleep(1)
print("\nOrder in " + time.strftime("%H", time.localtime()) + ':' + time.strftime("%M", time.localtime()) + ':' + time.strftime("%S", time.localtime()))


r = requests.session()
g = r.get(url = "https://gym.byr.moe/login.php", headers = src.login_headers)

req = r.post(url = "https://gym.byr.moe/login.php", headers = src.login_headers, data = src.Data)
text = req.text

t = re.findall(r'id=\d+ class=', text)
id = t[len(t)-1][3:11]
print('https://gym.byr.moe/new.php?time=' + src.TIME + '&date='+id,end='\n\n')

req = r.get(url = 'https://gym.byr.moe/new.php?time=3' + src.TIME + '&date='+id, headers = src.req_headers)
text = req.text
t = re.findall(r'id=\d+ class=', text)

raw = json.dumps(dict(date = id, time = '3', timemill = int(round(time.time() * 1000))),separators=(',',':'))
print(raw,end='\n')
oraw = ""
for i in range(0, len(raw)):
    oraw = oraw + raw[i] + raw[len(raw) - 1 - i]

plainText = oraw
AES_KEY = src.ekey[0:16]
AES_IV = src.ekey[2:18]
enctext = src.AES_Encrypt(AES_KEY, AES_IV, plainText)

order_data = dict(blob = enctext)
order_req = r.post(url = 'https://gym.byr.moe/newOrder.php', headers = src.order_headers, data = order_data)
print(order_req.text,end="\n\n")

if(order_req.text == '1'):
    print("提交成功！")
elif(order_req.text == '3'):
    print("人数已满！")
elif(order_req.text == '2'):
    print("非法请求，请勿作死！")
elif(order_req.text == '5'):
    print("参数错误！")
elif(order_req.text == '4'):
    print("已经预约！")
elif(order_req.text == '6'):
    print("有不良记录！")
else:
    print(order_req.text)

time.sleep(30)