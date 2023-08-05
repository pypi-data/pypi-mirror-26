# -*- coding: utf-8 -*-

##
# kt GiGA One-Box Orchestrator version 1.0
#
# Copyright 2016 kt corp. All right reserved
#
# This is a proprietary software of kt corp, and you may not use this file
# except in compliance with license agreement with kt corp.
#
# Any redistribution or use of this software, with or without modification
# shall be strictly prohibited without prior written approval of kt corp,
# and the copyright notice above does not evidence any actual or intended
# publication of such software.
##

'''
auxiliary_functions is a module that implements functions that are used by all openmano modules,
dealing with aspects such as reading/writing files, formatting inputs/outputs for quick translation
from dictionaries to appropriate database dictionaries, etc.
'''
__author__="Alfonso Tierno, Gerardo Garcia"
__date__ ="$08-sep-2014 12:21:22$"

import datetime
import random
from jsonschema import validate as js_v, exceptions as js_e
#from bs4 import BeautifulSoup

def read_file(file_to_read):
    """Reads a file specified by 'file_to_read' and returns (True,<its content as a string>) in case of success or (False, <error message>) in case of failure"""
    try:
        f = open(file_to_read, 'r')
        read_data = f.read()
        f.close()
    except Exception,e:
        return (False, str(e))
      
    return (True, read_data)

def write_file(file_to_write, text):
    """Write a file specified by 'file_to_write' and returns (True,NOne) in case of success or (False, <error message>) in case of failure"""
    try:
        f = open(file_to_write, 'w')
        f.write(text)
        f.close()
    except Exception,e:
        return (False, str(e))
      
    return (True, None)

def format_in(http_response, schema):
    try:
        client_data = http_response.json()
        js_v(client_data, schema)
        #print "Input data: ", str(client_data)
        return True, client_data
    except js_e.ValidationError, exc:
        print "validate_in error, jsonschema exception ", exc.message, "at", exc.path
        return False, ("validate_in error, jsonschema exception ", exc.message, "at", exc.path)

def remove_extra_items(data, schema):
    deleted=[]
    if type(data) is tuple or type(data) is list:
        for d in data:
            a= remove_extra_items(d, schema['items'])
            if a is not None: deleted.append(a)
    elif type(data) is dict:
        for k in data.keys():
            if 'properties' not in schema or k not in schema['properties'].keys():
                del data[k]
                deleted.append(k)
            else:
                a = remove_extra_items(data[k], schema['properties'][k])
                if a is not None:  deleted.append({k:a})
    if len(deleted) == 0: return None
    elif len(deleted) == 1: return deleted[0]
    else: return deleted

#def format_html2text(http_content):
#    soup=BeautifulSoup(http_content)
#    text = soup.p.get_text() + " " + soup.pre.get_text()
#    return text

def format_jsonerror(http_response):
    data = http_response.json()
    #print "format_jsonerror"
    #print "http_content"
    #print "http_content_error_description"
    #print data["error"]["description"]
    return data["error"]["description"]

def convert_bandwidth(data, reverse=False):
    '''Check the field bandwidth recursivelly and when found, it removes units and convert to number 
    It assumes that bandwidth is well formed
    Attributes:
        'data': dictionary bottle.FormsDict variable to be checked. None or empty is consideted valid
        'reverse': by default convert form str to int (Mbps), if True it convert from number to units
    Return:
        None
    '''
    if type(data) is dict:
        for k in data.keys():
            if type(data[k]) is dict or type(data[k]) is tuple or type(data[k]) is list:
                convert_bandwidth(data[k], reverse)
        if "bandwidth" in data:
            try:
                value=str(data["bandwidth"])
                if not reverse:
                    pos = value.find("bps")
                    if pos>0:
                        if value[pos-1]=="G": data["bandwidth"] =  int(data["bandwidth"][:pos-1]) * 1000
                        elif value[pos-1]=="k": data["bandwidth"]= int(data["bandwidth"][:pos-1]) / 1000
                        else: data["bandwidth"]= int(data["bandwidth"][:pos-1])
                else:
                    value = int(data["bandwidth"])
                    if value % 1000 == 0: data["bandwidth"]=str(value/1000) + " Gbps"
                    else: data["bandwidth"]=str(value) + " Mbps"
            except:
                print "convert_bandwidth exception for type", type(data["bandwidth"]), " data", data["bandwidth"]
                return
    if type(data) is tuple or type(data) is list:
        for k in data:
            if type(k) is dict or type(k) is tuple or type(k) is list:
                convert_bandwidth(k, reverse)
            
def convert_datetime2str(var):
    '''Converts a datetime variable to a string with the format '%Y-%m-%dT%H:%i:%s'
    It enters recursively in the dict var finding this kind of variables
    '''
    if type(var) is dict:
        for k,v in var.items():
            if type(v) is datetime.datetime:
                var[k]= v.strftime('%Y-%m-%dT%H:%M:%S')
            #hjc
            elif type(v) is datetime.date:
                print "hjc: %s is date" %v
                var[k]= v.strftime('%Y-%m-%d')    
            elif type(v) is dict or type(v) is list or type(v) is tuple: 
                convert_datetime2str(v)
        if len(var) == 0: return True
    elif type(var) is list or type(var) is tuple:
        for v in var:
            convert_datetime2str(v)

def convert_str2boolean(data, items):
    '''Check recursively the content of data, and if there is an key contained in items, convert value from string to boolean 
    Done recursively
    Attributes:
        'data': dictionary variable to be checked. None or empty is considered valid
        'items': tuple of keys to convert
    Return:
        None
    '''
    if type(data) is dict:
        for k in data.keys():
            if type(data[k]) is dict or type(data[k]) is tuple or type(data[k]) is list:
                convert_str2boolean(data[k], items)
            if k in items:
                if type(data[k]) is str:
                    if   data[k]=="false" or data[k]=="False": data[k]=False
                    elif data[k]=="true"  or data[k]=="True":  data[k]=True
    if type(data) is tuple or type(data) is list:
        for k in data:
            if type(k) is dict or type(k) is tuple or type(k) is list:
                convert_str2boolean(k, items)

def check_valid_uuid(uuid):
    id_schema = {"type" : "string", "pattern": "^[a-fA-F0-9]{8}(-[a-fA-F0-9]{4}){3}-[a-fA-F0-9]{12}$"}
    try:
        js_v(uuid, id_schema)
        return True
    except js_e.ValidationError:
        return False
    
def generate_datetime_id():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "-" + str(random.randint(1, 99)).zfill(2)

def check_valid_ipv4(ipv4_addr):
    ipv4_schema = {"type":"string","pattern":"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"}    
    try:
        js_v(ipv4_addr, ipv4_schema)
        return True
    except js_e.ValidationError:
        #logger.exception("Validation Error")
        return False
