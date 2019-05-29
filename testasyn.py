import requests
import asyncio
from datetime import datetime
import time


urls =['http://tw.yahoo.com','http://www.google.com','http://www.vghtpe.gov.tw','http://www.pchome.com.tw','http://www.mobile01.com']

async def get_content_asyn(url):
    retcontent = requests.get(url)
    await asyncio.sleep(1)
    print( str(datetime.now())+ ' : '+ url + ' done!!')

def get_content(url):
    retcontent = requests.get(url)
    time.sleep(1)
    print( str(datetime.now())+ ' : '+ url + ' done!!')


async def run_asyn():
    tasks = []
    for url in urls:
        tasks.append(get_content_asyn(url)) 
    await asyncio.wait(tasks)
   
def run():
    for url in urls:
        get_content(url)

t1=datetime.now()
loop = asyncio.get_event_loop()
tasks=[]
for url in urls:
    tasks.append(loop.create_task(get_content_asyn(url))) 

loop.run_until_complete(task for task in tasks)
print ('async total time : ' + str(datetime.now()-t1))
loop.close()

t2 = datetime.now()
run()
print ('total time : ' + str(datetime.now()-t2))