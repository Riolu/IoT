import requests
import time
import json
from tqdm import tqdm

HEADERS = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8'}


def evaluate_register(itrs):
    url = 'http://192.168.1.189:5000/register'

    start = time.time()
    for i in tqdm(range(itrs)):
        payload = {
            "targetLoc": "level5",
            "td": {
                "_type": "pc",
                "id": "urn:dev:ops:54312-pc-{}".format(i)
            }
        }
        requests.post(url, data=json.dumps(payload), headers=HEADERS)

    end = time.time()
    elapsed = end - start
    print("Total of {} seconds elapsed for register {} things".format(
        elapsed, itrs))
    print("Average time: {}".format(float(elapsed) / itrs))


def evaluate_searchByLocId(itrs):
    url = 'http://192.168.1.189:5000/searchByLocId?loc={}&id={}'

    start = time.time()
    for i in tqdm(range(itrs)):
        requests.get(url.format('level5', 'urn:dev:ops:54312-pc-{}'.format(i)))

    end = time.time()
    elapsed = end - start
    print("Total of {} seconds elapsed for searchByLocId {} things".format(
        elapsed, itrs))
    print("Average time: {}".format(float(elapsed) / itrs))


def evaluate_searchByLocTypeRecursive(itrs):
    url = 'http://192.168.1.189:5000/searchByLocType?loc={}&type={}'.format(
        'level5', 'pc')

    start = time.time()
    for _ in tqdm(range(itrs)):
        requests.get(url)

    end = time.time()
    elapsed = end - start
    print("Total of {} seconds elapsed for searchByLocTypeRecursive {} things".format(
        elapsed, itrs))
    print("Average time: {}".format(float(elapsed) / itrs))


def evaluate_searchByLocTypeIterative(itrs):
    url = 'http://192.168.1.189:5000/searchByLocTypeIterative?loc={}&type={}'.format(
        'level5', 'pc')

    start = time.time()
    for _ in tqdm(range(itrs)):
        requests.get(url)

    end = time.time()
    elapsed = end - start
    print("Total of {} seconds elapsed for searchByLocTypeIterative {} things".format(
        elapsed, itrs))
    print("Average time: {}".format(float(elapsed) / itrs))


def evaluate_delete(irts):
    url = "http://192.168.1.189:5000/delete?targetLoc={}&id={}"
    start = time.time()
    for _ in tqdm(range(itrs)):
        requests.delete(url.format('level5', 'urn:dev:ops:54312-pc-{}'.format(i)))
    end = time.time()
    elapsed = end - start
    print("Total of {} seconds elapsed for delete {} things".format(
        elapsed, itrs))
    print("Average time: {}".format(float(elapsed) / itrs))


if __name__ == '__main__':
    sep = '-'*50
    for num_itrs in [10, 100, 1000]:
        evaluate_register(num_itrs)
        print(sep)
        evaluate_searchByLocId(num_itrs)
        print(sep)
        evaluate_searchByLocTypeRecursive(num_itrs)
        print(sep)
        evaluate_searchByLocTypeIterative(num_itrs)
        print(sep)
        evaluate_delete(num_itrs)
        print(sep)
