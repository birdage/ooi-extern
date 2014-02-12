#!/usr/bin/python
"""WSGI geoserver layer server """
from __future__ import print_function
from gevent.pywsgi import WSGIServer
from geoserver.catalog import Catalog
from geoserver.layer import Layer
from geoserver.store import coveragestore_from_index, datastore_from_index, \
    DataStore, CoverageStore, UnsavedDataStore, UnsavedCoverageStore
from geoserver.style import Style
from geoserver.support import prepare_upload_bundle
from geoserver.layergroup import LayerGroup, UnsavedLayerGroup
from geoserver.workspace import workspace_from_index, Workspace
from geoserver.resource import FeatureType
from geoserver.support import prepare_upload_bundle, url
import httplib2
import json
import requests

__author__ = "abird"

ADDLAYER = "addlayer"
REMOVELAYER = "removelayer"
UPDATELAYER = "updatelayer"
RESETSTORE = "resetstore"

GEO_WS = "geonode"
SERVER = "http://localhost:8080/geoserver/rest"
U_NAME = "admin"
P_WD = "admin"
GEO_STORE = "ooi"

KEY_SERVICE = 'service'
KEY_NAME = 'name'
KEY_ID = 'id'


def application(env, start_response):
    request = env['PATH_INFO']
    request = request[1:]
    cat = Catalog(SERVER, U_NAME, P_WD)

    if request == '/':
        start_response('404 Not Found', [('Content-Type', 'text/html')])
        return ["<h1>Error<b>please add request information</b>"]
    else:
        req = request.split("&")
        paramDict = {}
        if len(req) > 1:
            for param in req:
                params = param.split("=")
                paramDict[params[0]] = params[1]

            #parse request
            if (paramDict.has_key(KEY_SERVICE)):
                if (paramDict[KEY_SERVICE] == ADDLAYER):
                	if (paramDict.has_key(KEY_NAME) and paramDict.has_key(KEY_ID)):
	                    print(ADDLAYER)
	                    createLayer(paramDict[KEY_NAME], GEO_STORE, GEO_WS)

                elif (paramDict[KEY_SERVICE] == REMOVELAYER):
                	if (paramDict.has_key(KEY_NAME) and paramDict.has_key(KEY_ID)):
                		removeLayer(paramDict[KEY_NAME], GEO_STORE, GEO_WS,cat)
                    	print(REMOVELAYER)

                elif (paramDict[KEY_SERVICE] == UPDATELAYER):
                    print(UPDATELAYER)

                elif (paramDict[KEY_SERVICE] == RESETSTORE):
                   resetDataStore(cat)

    start_response('200 OK', [('Content-Type', 'text/html')])
    return ['<b>' + request + '</b>']


def startup():
    print('Serving on 8844...')
    server = WSGIServer(('', 8844), application).serve_forever()


def getGeoStoreParams():
    params = {
        'Connection timeout': '20',
        'Estimated extends': 'true',
        'Expose primary keys': 'false',
        'Loose bbox': 'true',
        'Max open prepared statements': '50',
        'database': 'postgres',
        'dbtype': 'postgis',
        'encode functions': 'false',
        'fetch size': '1000',
        'host': 'localhost',
        'max connections': '10',
        'min connections': '1',
        'namespace': 'http://www.geonode.org/',
        'port': '5432',
        'preparedStatements': 'false',
        'schema': 'public',
        'user': 'rpsdev',
        'validate connections': 'true'
    }
    return params

def resetDataStore(cat):
    print(RESETSTORE)
    geoWs = cat.get_workspace(GEO_WS)
    try:
        geoStore = cat.get_store(GEO_STORE)
        #remove all the things if it has resources
        for d in geoStore.get_resources():
            layer = cat.get_layer(d.name)
            #delete the layer
            cat.delete(layer)
            #delete the actual file
            cat.delete(d)

        cat.save(geoStore)
        cat.delete(geoStore)
    except Exception:
        print("issue getting/removing datastore")

    geoStore = cat.create_datastore(GEO_STORE, geoWs)
    geoStore.capabilitiesURL = "http://www.geonode.org/"
    geoStore.type = "PostGIS"
    geoStore.connection_parameters = getGeoStoreParams()
    #MUST SAVE IT!
    cat.save(geoStore)


def removeLayer(layer_name, store_name, workspace_name,cat):
	print (REMOVELAYER)

def createLayer(layer_name, store_name, workspace_name):

    xml = '''<?xml version='1.0' encoding='utf-8'?>
        <featureType>
		  <name>%s</name>
		  <nativeName>%s</nativeName>
		  <namespace>
		    <name>%s</name>
		    <atom:link xmlns:atom="http://www.w3.org/2005/Atom\" rel=\"alternate\" href=\"http://localhost:8080/geoserver/rest/namespaces/geonode.xml\" type=\"application/xml\"/>
		  </namespace>
		  <title>DataProductLayer</title>
		  <keywords>
		    <string>DataProductLayer</string>
		    <string>autoGeneration</string>
		  </keywords>
		  <srs>EPSG:4326</srs>
		  <nativeBoundingBox>
		    <minx>-1.0</minx>
		    <maxx>0.0</maxx>
		    <miny>-1.0</miny>
		    <maxy>0.0</maxy>
		  </nativeBoundingBox>
		  <latLonBoundingBox>
		    <minx>-1.0</minx>
		    <maxx>0.0</maxx>
		    <miny>-1.0</miny>
		    <maxy>0.0</maxy>
		  </latLonBoundingBox>
		  <projectionPolicy>FORCE_DECLARED</projectionPolicy>
		  <enabled>true</enabled>
		  <metadata>
		    <entry key=\"cachingEnabled\">false</entry>
		    <entry key=\"JDBC_VIRTUAL_TABLE\">
		      <virtualTable>
		        <name>geoserverlayer %s</name>
		        <sql>select count(*)</sql>
		        <escapeSql>false</escapeSql>
		      </virtualTable>
		    </entry>
		  </metadata>
		  <store class=\"dataStore\">
		    <name>%s</name>
		    <atom:link xmlns:atom=\"http://www.w3.org/2005/Atom\" rel=\"alternate\" href=\"http://localhost:8080/geoserver/rest/workspaces/geonode/datastores/ooi.xml\" type=\"application/xml\"/>
		  </store>
		  <maxFeatures>0</maxFeatures>
		  <numDecimals>0</numDecimals>
		  <attributes>
		    <attribute>
		      <name>count</name>
		      <minOccurs>0</minOccurs>
		      <maxOccurs>1</maxOccurs>
		      <nillable>true</nillable>
		      <binding>java.lang.Long</binding>
		    </attribute>
		  </attributes>
		</featureType>'''% (layer_name, layer_name,workspace_name, layer_name ,store_name)

    serverpath = SERVER + "/" + "workspaces" + "/" + GEO_WS + "/" + "datastores/"+GEO_STORE+"/featuretypes" 
    headers = {'Content-Type': 'application/xml'} # set what your server accepts
    auth=(U_NAME, P_WD)
    r = requests.post(serverpath,
                     data=xml, 
                     headers=headers,
                     auth=auth)

    #print r.status_code
    pass