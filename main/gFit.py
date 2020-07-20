import requests
import json

def read_activity(startTimeMillis, endTimeMillis, access_token, durationMillis=3600000):
    '''
    returns the response containing activities in range [startTimeMillis, endTimeMillis]
    '''
    headers = {
    'Content-Type': 'application/json',
    }
    params = (
        ('access_token', access_token),
    )
    # body = '{\n  "aggregateBy": [{\n    "dataTypeName": "com.google.activity.segment",\n    "dataSourceId": "raw:com.google.activity.segment:com.xiaomi.hm.health:"\n  }],\n  "bucketByTime": { "durationMillis": '+ f'{durationMillis}' + ' },\n  "startTimeMillis": ' + f'{startTimeMillis}' + ',\n  "endTimeMillis": ' + f'{endTimeMillis}' + '\n}\n'
    body = '{\n  "aggregateBy": [{\n    "dataTypeName": "com.google.activity.segment"\n  }],\n  "bucketByTime": { "durationMillis": '+ f'{durationMillis}' + ' },\n  "startTimeMillis": ' + f'{startTimeMillis}' + ',\n  "endTimeMillis": ' + f'{endTimeMillis}' + '\n}\n'

    url = "https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate"

    resp = requests.post(url=url, headers=headers, params=params, data=body)

    return resp


def sleep_code_in(resp):
    '''
    returns a bool value 'true' if user is sleeping
    '''
    
    try:
        L1 = resp["bucket"]

        for i1 in range(len(L1)):
            L2 = L1[i1]["dataset"]
            for i2 in range(len(L2)):
                L3 = L2[i2]["point"]
                for i3 in range(len(L3)):
                    L4 = L3[i3]["value"]
                    for i4 in range(len(L4)):
                        if L4[i4]["intVal"] in [72, 109, 110, 111, 112]:
                            return True
                            # return L4[i4]["intVal"]

        # return -1
        return False
    except:
        return False

def is_sleeping(startTimeMillis, endTimeMillis, access_token):

    resp = read_activity(startTimeMillis, endTimeMillis, access_token)
    # print(resp.json())
    return sleep_code_in(resp.json())


if __name__ == '__main__' :

    access_token = 'ya29.a0AfH6SMCd7e_m6kQkfjta1LvjA-DLAkw6wGAOR6Yq_ePsF0nQMkKela317QM1FkUQ3F6F4JySwiRPZwUFnQCKyNKE1OSoVxj3mTiWPObqKcgKW-sXtIFLAa6kuCzVGlBIUg4o1xubIUUtU9YrYccBmcboD_gY6xHiPpNj'

    is_sleep = is_sleeping(1584157920000,1584157920001,access_token)
    print(is_sleep)