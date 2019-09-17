import json
import copy

def generate_by_W3C():
    # May add input parameters
    temp_dict = json.loads('''
    {
        "@context": "https://www.w3.org/2019/wot/td/v1",
        "id": "urn:dev:ops:32473-WoTLamp-1234",
        "title": "MyLampThing",
        "securityDefinitions": {
            "basic_sc": {"scheme": "basic", "in":"header"}
        },
        "security": ["basic_sc"],
        "properties": {
            "status" : {
                "type": "string",
                "forms": [{"href": "https://mylamp.example.com/status"}]
            }
        },
        "actions": {
            "toggle" : {
                "forms": [{"href": "https://mylamp.example.com/toggle"}]
            }
        },
        "events":{
            "overheating":{
                "data": {"type": "string"},
                "forms": [{
                    "href": "https://mylamp.example.com/oh",
                    "subprotocol": "longpoll"
                }]
            }
        }
    }
    ''')

    generated_jsonLds = []
    id_prefix = "urn:dev:ops:32473-WoTLamp-"

    for i in range(1000):
        copy_dict = copy.deepcopy(temp_dict)
        copy_dict["id"] = id_prefix + str(i)
        generated_jsonLds.append(copy_dict)

    with open("tds.json", "w") as f:
        json.dump(generated_jsonLds, f)

generate_by_W3C()
