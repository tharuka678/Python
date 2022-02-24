import requests
from flask import Flask,render_template
from wialon.api import Wialon, WialonError
from wialon import flags

wearHouseLatitude = []
wearHouselongitude = []
clientsLatitude=[]
clientsLongitude=[]
data=[{}]
try:
    token = '30bd2c9e72a5a10d26af8ab4b89ce66e263B977AA9E0F98D6E6C06C84DEF2F1EE918521B'
    wialon_api = Wialon()
    result = wialon_api.token_login(token=token)
    wialon_api.sid = result['eid']

    paramsForAll = {
    "spec": {
            "itemsType": 'avl_resource',
            "propName": 'sys_name',
            "propValueMask": '*',
            "sortType": 'sys_name',
        },
        "flags":0x1001,
        "force": 1,
        "from": 0,
        "to": 0
    }
    resultForAll = wialon_api.core_search_items(paramsForAll)
    # search for resources to find resource id
    paramsForGroups = {
        "spec": {
            "itemsType": 'avl_resource',
            "propName": 'zone_groups,sys_id',
            "propType":'propitemname',
            "propValueMask":'*',
            "sortType": 'sys_name',
        },
        "flags":0x00100000,
        "force": 1,
        "from": 0,
        "to": 0
    }
    resultForGroups = wialon_api.core_search_items(paramsForGroups)
    
    # list of all available resources
    allResource=(resultForGroups['items'])
    
    # list Group Results of client and wearhouse 
    indexOfClients=(resultForGroups['items'][0]['zg']['1']['zns'])
    indexOfWerehouse=(resultForGroups['items'][0]['zg']['2']['zns'])

    # put to list clieant lalitude and Longitude 
    for clients in indexOfClients:
        tempId=str(clients)
        lon=resultForAll['items'][0]['zl'][tempId]['b']['min_x']
        clientsLongitude.append(lon)
        lat=resultForAll['items'][0]['zl'][tempId]['b']['min_y']
        clientsLatitude.append(lat)

    # put to list wearhouse lalitude and Longitude   
    for werehouse in indexOfWerehouse:
        tempId=str(werehouse)
        lon=resultForAll['items'][0]['zl'][tempId]['b']['min_x']
        wearHouselongitude.append(lon)
        lat=resultForAll['items'][0]['zl'][tempId]['b']['min_y']
        wearHouseLatitude.append(lat)

    # All longitude latitude put in the array  
    data=[wearHouseLatitude,wearHouselongitude,clientsLatitude,clientsLongitude]
      
    wialon_api.core_logout()
except WialonError as e:
    print(e)

#API key
api_key = 'L9uhsN3tGlpKUoYOWix9tRCLN04ErQw57fCFTaGqU3g'

#---------Flask Code for creating Map--------- 
app = Flask(__name__,template_folder='template')
@app.route('/')

def map_func():
	return render_template('my/map.html',apikey=api_key,data=data)

if __name__ == '__main__':
	app.run(debug = True)

