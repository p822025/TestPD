import requests
import json

serpd='http://10.97.235.18:9080'
serts='http://10.121.11.180:8080'

serurl=serpd

# 自訂表頭
my_headers = {'accept': 'application/json'}

# 將自訂表頭加入 GET 請求中
req = requests.get(serpd +"/NPIWS/service/CAS/WARD/TEST/A102",headers = my_headers)
doc=json.loads(req.text)
retcode= doc['outMsg']['ret']
if retcode==0:
    print('has data!!')
    for vo in doc['outMsg']['rescont']:
        hisid=vo['hisid']
        print(hisid)
    
else:
    print('has error!!!')
