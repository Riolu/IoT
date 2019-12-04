import requests
import time
import json

HEADERS = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8'}

def evaluate_register(itrs):
    url = 'http://192.168.1.189:5000/register'

    start = time.time()
    for i in range(itrs):
        payload = {
            "targetLoc": "level5",
            "td": {
                "_type": "pc", 
                "id": "urn:dev:ops:54312-pc-{}".format(i)
            }
        }

        # payloadStr = '{"targetLoc": "level5", "td": {"_type": "pc", "id": "urn:dev:ops:54312-pc-1"}}'
        
        requests.post(url, data=json.dumps(payload), headers=HEADERS)
    
    end = time.time()
    elapsed = end - start
    print("Total of {} seconds elapsed for register {} things".format(elapsed, itrs))
    print("Average time: {}".format(float(elapsed)/itrs))


if __name__ == '__main__':
    evaluate_register(100)

