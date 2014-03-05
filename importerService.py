#!/usr/bin/python
"""WSGI geoserver layer server """
#from __future__ import print_function
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
import ast

__author__ = "abird"

ADDLAYER = "addlayer"
REMOVELAYER = "removelayer"
UPDATELAYER = "updatelayer"
RESETSTORE = "resetstore"
LISTLAYERS = "listlayers"

GEO_WS = "geonode"
SERVER = "http://localhost:8080/geoserver/rest"
U_NAME = "admin"
P_WD = "admin"
GEO_STORE = "ooi"

KEY_SERVICE = 'service'
KEY_NAME = 'name'
KEY_ID = 'id'
PARAMS = 'params'



def application(env, start_response):
    request = env['PATH_INFO']
    request = request[1:]
    cat = Catalog(SERVER, U_NAME, P_WD)
    output = ''
    
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
	                    createLayer(paramDict[KEY_NAME], GEO_STORE, GEO_WS,paramDict[PARAMS])

                elif (paramDict[KEY_SERVICE] == REMOVELAYER):
                	if (paramDict.has_key(KEY_NAME) and paramDict.has_key(KEY_ID)):
                		removeLayer(paramDict[KEY_NAME], GEO_STORE, GEO_WS,cat)

                elif (paramDict[KEY_SERVICE] == UPDATELAYER):
                    removeLayer(paramDict[KEY_NAME], GEO_STORE, GEO_WS,cat)
                    createLayer(paramDict[KEY_NAME], GEO_STORE, GEO_WS,paramDict[PARAMS])
                    print(UPDATELAYER)

                elif (paramDict[KEY_SERVICE] == LISTLAYERS):
                    layerListRet = getLayerList(cat)
                    print(UPDATELAYER)
                    print(layerListRet)
                    output = ''.join(layerListRet)
                    print output

                elif (paramDict[KEY_SERVICE] == RESETSTORE):
                   resetDataStore(cat)

    start_response('200 OK', [('Content-Type', 'text/html')])
    return ['<b>' + request + '<br>'+ output +'</b>']


def startup():
    print('Serving on 8844...')
    server = WSGIServer(('', 8844), application).serve_forever()


def getGeoStoreParams():
    params = {
        'Connection timeout': '20',
        'Estimated extends': 'true',
        'Expose primary keys': 'false',
        'Loose bbox': 'true',
        'Session startup SQL': 'select runCovTest();\nselect 1 from covtest limit 1;',
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

def getLayerList(cat):
    layerList = []
    layerList.append('List Of DataLayers')
    layerList.append('<br>')
    layerList.append('<br>')
    geoWs = cat.get_workspace(GEO_WS)
    try:
        geoStore = cat.get_store(GEO_STORE)
        for d in geoStore.get_resources():
            layerList.append(d.name)
            layerList.append('<br>')
    except Exception,e:
        print("issue getting layers",str(e))

    return layerList    


def resetDataStore(cat):
    print(RESETSTORE)
    geoWs = cat.get_workspace(GEO_WS)
    try:
        geoStore = cat.get_store(GEO_STORE)
        #remove all the things if it has resources
        for d in geoStore.get_resources():
            layer = cat.get_layer(d.name)
            if (layer):
                #delete the layer
                cat.delete(layer)
                #delete the actual file
                cat.delete(d)
            else:
                try:
                    print("layer thinks it does not exist...remove")
                    cat.delete(d)      
                    pass
                except Exception, e:
                    print("issue getting/removing layer",str(e))
                

        cat.save(geoStore)
        cat.delete(geoStore)
    except Exception,e:
        print("issue getting/removing datastore",str(e))

    try:
        if (cat.get_store(GEO_STORE)):
            #store exists for some reason was not removed!?
            print("using existing datastore")
    except Exception, e:
        print "create new"   
        #store does not exist create it, the prefered outcome 
        geoStore = cat.create_datastore(GEO_STORE, geoWs)
        geoStore.capabilitiesURL = "http://www.geonode.org/"
        geoStore.type = "PostGIS"
        geoStore.connection_parameters = getGeoStoreParams()
        #MUST SAVE IT!
        cat.save(geoStore)

def removeLayer(layer_name, store_name, workspace_name, cat):
    print (REMOVELAYER)

    geoWs = cat.get_workspace(GEO_WS)
    try:
        geoStore = cat.get_store(GEO_STORE)
        #remove all the things if it has resources
        layer = cat.get_layer(layer_name)
        if (layer):
            #delete the layer
            cat.delete(layer)
            #delete the actual file/resource
            cat.delete(cat.get_resource(layer_name))
            cat.save(geoStore)
        #else:
            #if the layer does not exist try deleting the resource
        #    cat.delete(cat.get_resource(layer_name))
        #    cat.save(geoStore)

    except Exception:
        print("issue getting/removing data layer/resource")

def createLayer(layer_name, store_name, workspace_name,params):
    print ADDLAYER

    xml = '''<?xml version='1.0' encoding='utf-8'?>
        <featureType>
		  <name>ooi_%s_ooi</name>
		  <nativeName>layer_%s</nativeName>
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
		    <minx>-180</minx>
            <maxx>180</maxx>
            <miny>-90.0</miny>
            <maxy>90.0</maxy>
		  </nativeBoundingBox>
		  <latLonBoundingBox>
		    <minx>-180</minx>
            <maxx>180</maxx>
            <miny>-90.0</miny>
            <maxy>90.0</maxy>
		  </latLonBoundingBox>
		  <projectionPolicy>FORCE_DECLARED</projectionPolicy>
		  <enabled>true</enabled>
		  <metadata>
            <entry key="time">
                <dimensionInfo>
                    <enabled>true</enabled>
                    <attribute>time</attribute>
                    <presentation>LIST</presentation>
                    <units>ISO8601</units>
                </dimensionInfo>
            </entry>
            <entry key="elevation">
                <dimensionInfo>
                <enabled>false</enabled>
                </dimensionInfo>
            </entry>
		    <entry key=\"cachingEnabled\">false</entry>
		    <entry key=\"JDBC_VIRTUAL_TABLE\">
		      <virtualTable>
		        <name>layer_%s</name>
		        <sql>select * from _%s_view</sql>
		        <escapeSql>false</escapeSql>
                <geometry>
                <name>geom</name>
                <type>Point</type>
                <srid>4326</srid>
                </geometry>
		      </virtualTable>
		    </entry>
		  </metadata>
		  <store class=\"dataStore\">
		    <name>%s</name>
		    <atom:link xmlns:atom=\"http://www.w3.org/2005/Atom\" rel=\"alternate\" href=\"http://localhost:8080/geoserver/rest/workspaces/geonode/datastores/ooi.xml\" type=\"application/xml\"/>
		  </store>
		  <maxFeatures>0</maxFeatures>
		  <numDecimals>0</numDecimals>
		  '''% (layer_name, layer_name,workspace_name, layer_name , layer_name, store_name)
          
    xml += "<attributes>"

    print "------------------\n"
    params = ast.literal_eval(params)
    #add point geom
    params['geom'] = "geom"
    print params
    print "------------------\n"

    #add attribute list
    for paramItem in params:
        xml += addAttributes(paramItem,params[paramItem])

    xml += "</attributes>"
    xml += "</featureType>"
	
    #generate layer
    serverpath = SERVER + "/" + "workspaces" + "/" + GEO_WS + "/" + "datastores/"+GEO_STORE+"/featuretypes" 
    headers = {'Content-Type': 'application/xml'} # set what your server accepts
    auth=(U_NAME, P_WD)
    r = requests.post(serverpath,
                     data=xml, 
                     headers=headers,
                     auth=auth)

    print "statusCode",r.status_code
    #print r.text
    layer_name = "ooi_"+layer_name+"_ooi"
    #append query 
    serverpath = SERVER+"/layers/"+layer_name+'.xml'
    r = requests.get(serverpath,
                 headers=headers,
                 auth=auth)

    #get the existing layer
    print "statusCode: getLayer:",r.status_code
    xml = r.text
    findString = ('</resource>')
    val= xml.find(findString)
    xmlPart1 = xml[:val+len(findString)]
    xmlAgg = xmlPart1+"\n<queryable>true</queryable>"+xml[val+len(findString):]
    #print "-----------"
    #print xmlAgg
    r = requests.put(serverpath,
                     data=xmlAgg, 
                     headers=headers,
                     auth=auth)

    print "statusCode: updateLayer:",r.status_code
    pass

def addAttributes(param,param_type):

    attribute = "<attribute>"
    attribute += "<name>"+param+"</name>"
    attribute += "<minOccurs>0</minOccurs>"
    attribute += "<maxOccurs>1</maxOccurs>"
    attribute += "<nillable>true</nillable>"
    
    if param == "geom":
        attribute += "<binding>com.vividsolutions.jts.geom.Point</binding>"
    elif param_type == "float":
        attribute += "<binding>java.lang.Float</binding>"
    elif param_type == "real":
        attribute += "<binding>java.lang.Float</binding>"  
    elif param_type == "time":
        attribute += "<binding>java.sql.Timestamp</binding>" 
    elif param_type == "int":
        attribute += "<binding>java.lang.Int</binding>"            
    else:
        attribute += "<binding>java.lang.Float</binding>"

    attribute += "</attribute>"

    return attribute

