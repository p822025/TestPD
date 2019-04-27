import asyncio
from datetime import datetime
import websockets
import json
import random

REPO = dict()
REPO[1] = {'caseno': 2, 'ward': 'A091', 'name': '王大明', 'age': 25, 'bedno': 10,
           'section': 'PEDD', 'gender': '男', 'hr': [], 'rr': [], 'bt': [],
           'sat': [], 'sbp': [], 'gcs': [], 'device': []}
REPO[2] = {'caseno': 2, 'ward': 'A091', 'name': '陳小君', 'age': 25, 'bedno': 11,
           'section': 'PEDD', 'gender': '女', 'hr': [], 'rr': [], 'bt': [],
           'sat': [], 'sbp': [], 'gcs': [], 'device': []}
REPO[3] = {'caseno': 2, 'ward': 'A091', 'name': '李雅婷', 'age': 25, 'bedno': 12,
           'section': 'PEDD', 'gender': '女', 'hr': [], 'rr': [], 'bt': [],
           'sat': [], 'sbp': [], 'gcs': [], 'device': []}
REPO[4] = {'caseno': 2, 'ward': 'A091', 'name': '張國強', 'age': 25, 'bedno': 13,
           'section': 'PEDD', 'gender': '男', 'hr': [], 'rr': [], 'bt': [],
           'sat': [], 'sbp': [], 'gcs': [], 'device': []}
REPO[5] = {'caseno': 2, 'ward': 'A091', 'name': '陶淵民', 'age': 11, 'bedno': 14,
           'section': 'PEDD', 'gender': '男', 'hr': [], 'rr': [], 'bt': [],
           'sat': [], 'sbp': [], 'gcs': [], 'device': []}
REPO[6] = {'caseno': 2, 'ward': 'A091', 'name': '麥可貝', 'age': 69, 'bedno': 15,
           'section': 'PEDD', 'gender': '男', 'hr': [], 'rr': [], 'bt': [],
           'sat': [], 'sbp': [], 'gcs': [], 'device': []}
REPO[7] = {'caseno': 2, 'ward': 'A092', 'name': '李麥克', 'age': 33, 'bedno': 21,
           'section': 'PEDD', 'gender': '男', 'hr': [], 'rr': [], 'bt': [],
           'sat': [], 'sbp': [], 'gcs': [], 'device': []}
REPO[8] = {'caseno': 2, 'ward': 'A092', 'name': '貝卡司', 'age': 22, 'bedno': 22,
           'section': 'PEDD', 'gender': '男', 'hr': [], 'rr': [], 'bt': [],
           'sat': [], 'sbp': [], 'gcs': [], 'device': []}
REPO[9] = {'caseno': 2, 'ward': 'A092', 'name': '卡卡西', 'age': 54, 'bedno': 23,
           'section': 'PEDD', 'gender': '男', 'hr': [], 'rr': [], 'bt': [],
           'sat': [], 'sbp': [], 'gcs': [], 'device': []}


USERS = dict()   # {websocket :{subscribe_type, subscribe_content, patients}}

# REPO[1]['hr'].append({'datetime': '2019-04-06 08:48', 'value': 80})
# REPO[1]['hr'].append({'datetime': '2019-04-06 10:48', 'value': 80})
# REPO[1]['rr'].append({'datetime': '2019-04-06 08:48', 'value': 20})
# REPO[1]['rr'].append({'datetime': '2019-04-06 10:48', 'value': 20})
# REPO[1]['bt'].append({'datetime': '2019-04-06 08:48', 'value': 37.5})
# REPO[1]['bt'].append({'datetime': '2019-04-06 10:48', 'value': 37.5})
# REPO[1]['sbp'].append({'datetime': '2019-04-06 08:48', 'value': 101})
# REPO[1]['sbp'].append({'datetime': '2019-04-06 10:48', 'value': 101})
# REPO[1]['sat'].append({'datetime': '2019-04-06 08:48', 'value': 96})
# REPO[1]['sat'].append({'datetime': '2019-04-06 10:48', 'value': 96})
# REPO[1]['gcs'].append({'datetime': '2019-04-06 08:48', 'value': 'E4V5M6'})
# REPO[1]['gcs'].append({'datetime': '2019-04-06 10:48', 'value': 'E4V5M6'})
# REPO[1]['device'].append(
#     {'datetime': '2019-04-06 08:48', 'value': 'Non-Invasive'})
# REPO[1]['device'].append(
#     {'datetime': '2019-04-06 10:48', 'value': 'Non-Invasive'})


def users_event():
    return json.dumps({'type': 'users', 'content': len(USERS)})


async def notify_users():
    if USERS:       # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    USERS[websocket] = {}
    await notify_users()


async def unregister(websocket):
    USERS.pop(websocket)
    await notify_users()


def getPatientCollection(ward):
    return [x for x in REPO if REPO[x]['ward'] == ward]


async def notify_patient_update(hisid):
    selected_USERS = []
    try:
        selected_USERS = [
            x for x in USERS
            if x in USERS and 'patients' in USERS[x] and hisid in USERS[x]
            ['patients']]
    finally:
        if selected_USERS:       # asyncio.wait doesn't accept an empty list
            await asyncio.wait([user.send(json.dumps({'type': 'patient', 'content': {'hisid': hisid, **REPO[hisid]}})) for user in selected_USERS])


async def subscribe(websocket, path):
    await register(websocket)
    try:
        async for message in websocket:
            print(message)
            print(websocket)
            message = json.loads(message)
            if message['action'] == 'subscribe':
                if message['type'] == 'ward':
                    patientCollection = getPatientCollection(message['content'])
                    USERS[websocket] = {
                        'subscribe_type': 'ward',
                        'subscribe_content': message['content'],
                        'patients': patientCollection}
                    await websocket.send(json.dumps({'type': 'patientcollection', 'content': [{'hisid': x, **REPO[x]} for x in patientCollection]}))
            print(USERS)
    except Exception as e:
        print('error', e)
    finally:
        await unregister(websocket)


async def timer():  # simulate patient update
    while True:
        hisid = random.randint(1, 9)
        datetime = '2019-04-0'+str(random.randint(1, 9)
                                   )+' '+str(random.randint(12, 23))+':48'
        REPO[hisid]['hr'].append(
            {'datetime': datetime, 'value': random.randint(30, 150)})

        datetime = '2019-04-0'+str(random.randint(1, 9)
                                   )+' '+str(random.randint(12, 23))+':48'
        REPO[hisid]['rr'].append(
            {'datetime': datetime, 'value': random.randint(5, 30)})

        datetime = '2019-04-0'+str(random.randint(1, 9)
                                   )+' '+str(random.randint(12, 23))+':48'
        REPO[hisid]['sat'].append(
            {'datetime': datetime, 'value': random.randint(80, 100)})

        datetime = '2019-04-0'+str(random.randint(1, 9)
                                   )+' '+str(random.randint(12, 23))+':48'
        REPO[hisid]['sbp'].append(
            {'datetime': datetime, 'value': random.randint(70, 230)})

        datetime = '2019-04-0'+str(random.randint(1, 9)
                                   )+' '+str(random.randint(12, 23))+':48'
        REPO[hisid]['bt'].append(
            {'datetime': datetime, 'value': round(random.uniform(34, 41), 1)})

        datetime = '2019-04-0'+str(random.randint(1, 9)
                                   )+' '+str(random.randint(12, 23))+':48'
        REPO[hisid]['gcs'].append(
            {'datetime': datetime, 'value': 'E4V'+str(random.randint(4, 5))+'M6'})

        datetime = '2019-04-0'+str(random.randint(1, 9)
                                   )+' '+str(random.randint(12, 23))+':48'
        REPO[hisid]['device'].append(
            {'datetime': datetime, 'value': random.choice(
                ['-', 'Non-invasive', 'Invasive'])})

        MAX_DATA = 5
        if len(REPO[hisid]['hr']) > MAX_DATA:
            REPO[hisid]['hr'].pop(0)
        if len(REPO[hisid]['rr']) > MAX_DATA:
            REPO[hisid]['rr'].pop(0)
        if len(REPO[hisid]['sat']) > MAX_DATA:
            REPO[hisid]['sat'].pop(0)
        if len(REPO[hisid]['sbp']) > MAX_DATA:
            REPO[hisid]['sbp'].pop(0)
        if len(REPO[hisid]['bt']) > MAX_DATA:
            REPO[hisid]['bt'].pop(0)
        if len(REPO[hisid]['gcs']) > MAX_DATA:
            REPO[hisid]['gcs'].pop(0)
        if len(REPO[hisid]['device']) > MAX_DATA:
            REPO[hisid]['device'].pop(0)
        
        await notify_patient_update(hisid)
        await asyncio.sleep(0.5)


start_server_subscribe = websockets.serve(subscribe, port=5000)


asyncio.get_event_loop().run_until_complete(start_server_subscribe)
asyncio.get_event_loop().run_until_complete(timer())

asyncio.get_event_loop().run_forever()
