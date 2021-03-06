import json
import requests
import re
from eve import Eve
from flask import Flask, redirect, url_for, request, Response
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from .settings import getSettings
"""[Retrieve entry from database table]
Retrieve entry with {key} from table {tableName} at MongoDB database (reachable by Python Eve {baseUrl})

Returns:
    [Dict] -- [table entry]
"""


def retrieveAll(key, baseUrl, tableName):
    url = baseUrl + tableName + '/' + key
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None


"""[Retrieve field of an entry from database table]
Retrieve {field} of the entry with {key} from table {tableName} at MongoDB database (reachable by Python Eve {baseUrl})

Returns:
    [Any] -- [field of table entry]
"""


def retrieve(key, field, baseUrl, tableName):
    url = baseUrl + tableName + '/' + key
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data.get(field, None)
    else:
        return None


"""[Get name of current node]

Returns:
    [Str] -- [name of node]
"""


def getSelfName(baseUrl):
    return retrieve('self', 'url', baseUrl, 'loc_to_url')


def getApp(dbname):
    app = Eve(settings=getSettings(dbname))

    """[Register TD]
    register td in target location

    Returns:
        [Response] -- [Flask HTTP Response]
    """
    @app.route('/register', methods=['POST'])
    def register():
        body = request.get_json()
        try:
            targetLoc = body['targetLoc']
            td = body['td']
        except KeyError:
            return Response("Bad request data", status=400)

        host_url = request.host_url
        headers = {
            'Content-Type': 'application/json',
            'Accept-Charset': 'UTF-8'
        }

        self_loc = getSelfName(host_url)
        child_url = retrieve(targetLoc, 'url', host_url, 'loc_to_url')
        child_loc = retrieve(targetLoc, 'childLoc', host_url,
                             'targetLoc_to_childLoc')

        # targetLoc is direct child of current node
        if child_url is not None:
            # use Eve to post
            url = child_url + 'td'
            if 'publicity' not in td:
                td['publicity'] = 0
            r = requests.post(url, data=json.dumps(td), headers=headers)
            if r.status_code != 201:
                return r

            # update aggregated data
            info_data = {'type': td['_type'], 'childLoc': targetLoc}
            r = requests.put(child_url + 'registerInfo',
                             data=json.dumps(info_data),
                             headers=headers)
            if not re.match(r'2..', str(r.status_code)):
                return r

            public_data = {'td': td}
            if td['publicity'] > 0:
                r = requests.post(host_url + 'pushUp',
                                  data=json.dumps(public_data),
                                  headers=headers)
                if not re.match(r'2..', str(r.status_code)):
                    return r
        # targetLoc is in the subtree rooted at current node
        elif child_loc is not None:
            # go to lower database use register API
            child_url = retrieve(child_loc, 'url', host_url, 'loc_to_url')
            url = child_url + 'register'
            data = request.data
            r = requests.post(url, data=data, headers=headers)
            if not re.match(r'2..', str(r.status_code)):
                return r
        # targetLoc is not in the subtree of current node
        else:
            # go to master database use register API
            master_url = retrieve('master', 'url', host_url, 'loc_to_url')
            if master_url == host_url:
                return {}
            url = master_url + 'register'
            data = request.data
            r = requests.post(url, data=data, headers=headers)
            if not re.match(r'2..', str(r.status_code)):
                return r

        return {}, 200

    """[Push up aggregated data]
    helper function to push up aggregated data in register api
    
    Returns:
        [Response] -- [Flask HTTP Response]
    """

    @app.route('/pushUp', methods=['POST'])
    def pushUp():
        body = request.get_json()
        try:
            td = body['td']
            td['publicity'] -= 1
        except KeyError:
            return Response("Bad request data", status=400)

        host_url = request.host_url
        headers = {
            'Content-Type': 'application/json',
            'Accept-Charset': 'UTF-8'
        }
        r = requests.post(host_url + 'public_td',
                          data=json.dumps(td),
                          headers=headers)
        if r.status_code != 201:
            return r

        # recursively call pushup
        if td['publicity'] > 0:
            parent_url = retrieve('parent', 'url', host_url, 'loc_to_url')
            if parent_url:
                public_data = {'td': td}
                r = requests.post(parent_url + 'pushUp',
                                  data=json.dumps(public_data),
                                  headers=headers)
                if not re.match(r'2..', str(r.status_code)):
                    return r

        return {}

    """[Search Public TDs]
    search all public tds at given location

    Returns:
        [Response] -- [Flask HTTP Response]
    """

    @app.route('/searchPublic', methods=['GET'])
    def searchPublic():
        loc = request.args.get('loc')
        if not loc:
            return Response("Bad request data", status=400)

        host_url = request.host_url
        self_loc = getSelfName(host_url)
        target_url = retrieve(loc, 'url', host_url, 'loc_to_url')
        child_loc = retrieve(loc, 'childLoc', host_url,
                             'targetLoc_to_childLoc')

        # targetLoc is current node or direct child of current node
        if self_loc == loc or target_url is not None:
            target_url = host_url if self_loc == loc else target_url
            response = retrieveAll('', target_url, 'public_td')
        else:
            if child_loc is not None:
                child_url = retrieve(child_loc, 'url', host_url, 'loc_to_url')
                target_url = child_url
            else:
                master_url = retrieve('master', 'url', host_url, 'loc_to_url')
                if host_url == master_url:
                    return Response("Target location not found", status=404)
                target_url = master_url
            response = requests.get(target_url +
                                    'searchPublic?loc={}'.format(loc))
            if not re.match(r'2..', str(response.status_code)):
                return response
            response = response.json()

        return json.dumps(response)

    @app.route('/registerInfo', methods=['PUT'])
    def registerInfo():
        body = request.get_json()
        try:
            _type = body['type']
            childLoc = body['childLoc']
        except KeyError:
            return Response("Bad request data", status=400)

        # check whether the type is already in type_to_targetLoc
        type_locs = retrieve(_type, 'childLocs', request.host_url,
                             'type_to_childLocs')
        print(type_locs)
        if type_locs is not None and childLoc in type_locs:
            return {}

        # add to type_to_targetLoc
        db_name = getSelfName(request.host_url)
        if db_name is None:
            return Response('Configuration Error, No db_name Found',
                            status=404)

        try:
            client = MongoClient('localhost', 27017)
            db = client[db_name]
            collection = db['type_to_childLocs']

            if collection.find_one({'type': _type}) is not None:
                collection.update({'type': _type},
                                  {'$push': {
                                      'childLocs': childLoc
                                  }})
            else:
                collection.insert_one({'type': _type, 'childLocs': [childLoc]})
            client.close()
        except PyMongoError:
            return Response('Database operation error', status=500)

        host_url = request.host_url
        parent_url = retrieve('parent', 'url', host_url, 'loc_to_url')

        if parent_url:
            headers = {
                'Content-Type': 'application/json',
                'Accept-Charset': 'UTF-8'
            }
            new_data = request.get_json()
            self_loc = getSelfName(request.host_url)
            new_data['childLoc'] = self_loc
            r = requests.put(parent_url + 'registerInfo',
                             data=json.dumps(new_data),
                             headers=headers)
            if not re.match(r'2..', str(r.status_code)):
                return r

        return {}

    # delete a certain thing at a specific location
    @app.route('/delete', methods=['DELETE'])
    def delete():
        targetLoc = request.args.get('targetLoc')
        toDeleteId = request.args.get('id')
        if not targetLoc or not toDeleteId:
            return Response("Bad request data", status=400)

        host_url = request.host_url
        headers = {
            'Content-Type': 'application/json',
            'Accept-Charset': 'UTF-8'
        }

        self_loc = getSelfName(host_url)
        child_url = retrieve(targetLoc, 'url', host_url, 'loc_to_url')
        child_loc = retrieve(targetLoc, 'childLoc', host_url,
                             'targetLoc_to_childLoc')

        if child_url is not None:
            # use Eve to delete
            td = retrieveAll(toDeleteId, child_url, 'td')
            if td is None:
                return Response("Thing decription not found", status=404)

            if td['publicity'] and td['publicity'] > 0:
                data = {'id': td['id'], 'publicity': td['publicity']}
                response = requests.put(host_url + 'deletePublic',
                                        data=json.dumps(data),
                                        headers=headers)
                if not re.match(r'2..', str(response.status_code)):
                    return response

            # check whether the last item of a certain type
            response = requests.get(child_url + 'searchAtLoc?type=' +
                                    td['_type'])
            if response.status_code == 200:
                tds = response.json()
            if len(tds) == 1:
                info_data = {'type': td['_type'], 'childLoc': targetLoc}
                requests.put(child_url + 'deleteInfo',
                             data=json.dumps(info_data),
                             headers=headers)
            url = child_url + 'td/' + td['_id']
            response = requests.delete(url, headers={'If-Match': td['_etag']})
            if not re.match(r'2..', str(response.status_code)):
                return response

        elif child_loc is not None:
            # go to lower database use register API
            child_url = retrieve(child_loc, 'url', host_url, 'loc_to_url')
            url = child_url + 'delete?targetLoc={}&id={}'.format(
                targetLoc, toDeleteId)
            response = requests.delete(url)
            if not re.match(r'2..', str(response.status_code)):
                return response
        else:
            # go to master database use register API
            master_url = retrieve('master', 'url', host_url, 'loc_to_url')
            if master_url == host_url:
                return Response("Target location not found", status=404)
            url = master_url + 'delete?targetLoc={}&id={}'.format(
                targetLoc, toDeleteId)
            response = requests.delete(url)
            if not re.match(r'2..', str(response.status_code)):
                return response

        return {}

    # when delete api is called, if td to be deleted is registered public, then
    # deletePublic can be used to delete all the public data
    @app.route('/deletePublic', methods=['PUT'])
    def deletePublic():
        body = request.get_json()
        try:
            id = body['id']
            publicity = body['publicity']
        except KeyError:
            return Response("Internal server error deleting public data",
                            status=500)

        host_url = request.host_url
        td = retrieveAll(id, host_url, 'public_td')
        if td is None:
            return Response("Public data to delete not found", status=404)
        url = host_url + 'public_td/' + td['_id']
        response = requests.delete(url, headers={'If-Match': td['_etag']})
        if not re.match(r'2..', str(response.status_code)):
            return response

        if publicity > 0:
            url = host_url + 'loc_to_url/parent'
            response = requests.get(url)

            if response.status_code == 200:
                parent_url = response.json().get('url', None)
                if parent_url:
                    headers = {
                        'Content-Type': 'application/json',
                        'Accept-Charset': 'UTF-8'
                    }
                    data = {'id': id, 'publicity': publicity - 1}
                    requests.put(parent_url + 'deletePublic',
                                 data=request.data,
                                 headers=headers)

        return {}

    # delete aggregated data above
    @app.route('/deleteInfo', methods=['PUT'])
    def deleteInfo():
        body = request.get_json()
        try:
            _type = body['type']
            childLoc = body['childLoc']
        except KeyError:
            return Response("Bad request data", status=400)

        try:
            # delete from type_to_targetLoc
            client = MongoClient('localhost', 27017)
            db_name = getSelfName(request.host_url)
            db = client[db_name]
            collection = db['type_to_childLocs']

            collection.update({'type': _type},
                              {'$pull': {
                                  'childLocs': childLoc
                              }})
            client.close()
        except PyMongoError:
            return Response('Database operation error', status=500)

        host_url = request.host_url
        url = host_url + 'loc_to_url/parent'
        response = requests.get(url)

        if response.status_code == 200:
            parent_url = response.json().get('url', None)
            if parent_url:
                headers = {
                    'Content-Type': 'application/json',
                    'Accept-Charset': 'UTF-8'
                }
                requests.put(parent_url + 'deleteInfo',
                             data=request.data,
                             headers=headers)

        return {}

    # relocate td from one location to another location. Publicity reserved.
    @app.route('/relocate', methods=['PUT'])
    def relocate():
        fromLoc = request.args.get('fromLoc')
        toLoc = request.args.get('toLoc')
        toReplaceId = request.args.get('id')
        if not fromLoc or not toLoc or not toReplaceId:
            return Response("Bad request data", status=400)

        master_url = retrieve('master', 'url', request.host_url, 'loc_to_url')
        response = requests.get(
            master_url +
            'searchByLocId?loc={}&id={}'.format(fromLoc, toReplaceId))
        if not re.match(r'2..', str(response.status_code)):
            return response
        td = response.json()

        for key in [
                '_id', '_updated', '_created', '_etag', '_links', 'parent'
        ]:
            td.pop(key, None)

        delete_url = master_url + 'delete?targetLoc={}&id={}'.format(
            fromLoc, toReplaceId)
        r = requests.delete(delete_url)
        if not re.match(r'2..', str(r.status_code)):
            return r

        register_url = master_url + 'register'
        data = {'targetLoc': toLoc, 'td': td}
        headers = {
            'Content-Type': 'application/json',
            'Accept-Charset': 'UTF-8'
        }
        r = requests.post(register_url, data=json.dumps(data), headers=headers)
        if not re.match(r'2..', str(r.status_code)):
            return r

        return {}

    # search by type at a certain location
    @app.route('/searchAtLoc', methods=['GET'])
    def searchAtLoc():
        _type = request.args.get('type')
        if not _type:
            return Response("Internal server error searching at location",
                            status=500)
        type_locs = retrieve(_type, 'childLocs', request.host_url,
                             'type_to_childLocs') or []

        self_name = getSelfName(request.host_url)
        result_list = list()
        if self_name in type_locs:
            # use Eve to get
            url = request.host_url + 'td?where=_type=="{}"'.format(_type)
            response = requests.get(url)
            if not re.match(r'2..', str(response.status_code)):
                return response
            result_list += response.json()['_items']
            type_locs.remove(self_name)

        child_url_set = set()
        for child_loc in type_locs:
            # collect the urls of all the children to reach out to
            child_url = retrieve(child_loc, 'url', request.host_url,
                                 'loc_to_url')
            if child_url:
                child_url_set.add(child_url)
            else:
                return Response("Internal server error searching at location",
                                status=500)

        for child_url in child_url_set:
            # continue search at related children in a DFS way
            response = requests.get(child_url + 'searchAtLoc?type=' + _type)
            if not re.match(r'2..', str(response.status_code)):
                return response
            result_list.extend(response.json())

        return json.dumps(result_list)

    # search all the tds satisfying the given location and type
    @app.route('/searchByLocType', methods=['GET'])
    def searchByLocType():
        loc = request.args.get('loc')
        _type = request.args.get('type')
        if not loc or not _type:
            return Response("Bad request data", status=400)

        host_url = request.host_url

        self_loc = getSelfName(host_url)
        target_url = retrieve(loc, 'url', host_url, 'loc_to_url')
        child_loc = retrieve(loc, 'childLoc', host_url,
                             'targetLoc_to_childLoc')

        if self_loc == loc or target_url is not None:
            # current location or one of the direct child servers is the target location
            target_url = host_url if self_loc == loc else target_url
            response = requests.get(target_url + 'searchAtLoc?type=' + _type)
        else:
            # further search is needed
            if child_loc is not None:
                # the target location is in the subtree of the current location
                child_url = retrieve(child_loc, 'url', host_url, 'loc_to_url')
                target_url = child_url
            else:
                # the target location is not in the subtree of the current location, then search from the root
                master_url = retrieve('master', 'url', host_url, 'loc_to_url')
                if host_url == master_url:
                    # if already at root, meaning that no such location or thing is in our system
                    return {}
                target_url = master_url
            response = requests.get(
                target_url +
                'searchByLocType?loc={}&type={}'.format(loc, _type))

        if not re.match(r'2..', str(response.status_code)):
            return response
        return json.dumps(response.json())

    # search a thing with a certain id at a specific location
    @app.route('/searchByLocId', methods=['GET'])
    def searchByLocId():
        loc = request.args.get('loc')
        _id = request.args.get('id')
        if not loc or not _id:
            return Response("Bad request data", status=400)

        host_url = request.host_url

        self_loc = getSelfName(host_url)
        target_url = retrieve(loc, 'url', host_url, 'loc_to_url')
        child_loc = retrieve(loc, 'childLoc', host_url,
                             'targetLoc_to_childLoc')

        if self_loc == loc or target_url is not None:
            # current location or one of the direct child servers is the target location
            target_url = host_url if self_loc == loc else target_url
            response = retrieveAll(_id, target_url, 'td')
        else:
            # further search is needed
            if child_loc is not None:
                # the target location is in the subtree of the current location
                child_url = retrieve(child_loc, 'url', host_url, 'loc_to_url')
                target_url = child_url
            else:
                # the target location is not in the subtree of the current location, then search from the root
                master_url = retrieve('master', 'url', host_url, 'loc_to_url')
                if host_url == master_url:
                    # if the search is already at root, which means that there is no such thing in our system
                    return {}
                target_url = master_url
            response = requests.get(
                target_url + 'searchByLocId?loc={}&id={}'.format(loc, _id))
            if not re.match(r'2..', str(response.status_code)):
                return response
            response = response.json()

        return json.dumps(response)

    # search by loc and type at a certain server, dns-like search structure
    @app.route('/searchByLocTypeIterative', methods=['GET'])
    def searchByLocTypeIterative():
        _loc = request.args.get('loc')
        _type = request.args.get('type')

        # start from master
        url = retrieve('master', 'url', request.host_url, 'loc_to_url')

        while True:
            response = requests.get(
                url +
                'searchAtLocIterative?loc={}&type={}'.format(_loc, _type))
            if not re.match(r'2..', str(response.status_code)):
                return response
            response = response.json()

            if "url" not in response:  # td returned
                return json.dumps(response)
            # url returned, which means a furthur search is needed
            url = response["url"]

        return {}

    # search things of a certain type at a specific location in an iterative way
    # this api could either return a url or a list of thing descriptions depending on the situation
    @app.route('/searchAtLocIterative', methods=['GET'])
    def searchAtLocIterative():
        target_loc = request.args.get('loc')
        _type = request.args.get('type')
        if not target_loc or not _type:
            return Response("Bad request data", status=400)

        host_url = request.host_url
        self_loc = getSelfName(host_url)
        if self_loc == target_loc:
            url = host_url + 'td?where=_type=="{}"'.format(_type)
            response = requests.get(url)
            if not re.match(r'2..', str(response.status_code)):
                return response
            response = response.json()['_items']
        else:
            target_url = retrieve(target_loc, 'url', host_url, 'loc_to_url')
            if target_url is None:
                child_loc = retrieve(target_loc, 'childLoc', host_url,
                                     'targetLoc_to_childLoc')
                target_url = retrieve(child_loc, 'url', host_url, 'loc_to_url')
            response = {'url': target_url}

        return json.dumps(response)

    return app
