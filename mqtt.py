from simple import MQTTClient
import json


def pubdata(c_mqtt,data):
    j_d=json.dumps(data)
    print(j_d)
    c_mqtt.publish('weather',j_d)
    return "ok"
    

def connect(client_id,server,port,username,password):
    #端口号为：6002
    c_mqtt = MQTTClient(client_id, server,port,username,password)
    c_mqtt.connect()
    print("Connected to %s" % (server))
    return c_mqtt


































