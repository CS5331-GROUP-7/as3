import urllib
import json
from io import open
def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
            for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input
def encode(s):
    return ''.join([bin(ord(c)).replace('0b','') for c in s])
def urlEncoding(filename,output):
    with open(filename,mode='r',encoding='utf-8') as file:
        load_dict = json.load(file)
        load_dict = byteify(load_dict)
        payloads = load_dict['payloads']
        result = []
        for payload in payloads:
    	    a = urllib.quote_plus(payload)
    	    result.append(a)
        with open(output,'w') as f:
            f.write(unicode(json.dumps({'payloads':result})))    
def BinaryEncoding(filename,output):
    with open(filename,mode='r',encoding='utf-8') as file:
        load_dict = json.load(file)
        load_dict = byteify(load_dict)
        payloads = load_dict['payloads']
        result = []
        for payload in payloads:
            a = encode(payload)
            result.append(a)
        with open(output,'w') as f:
            f.write(unicode(json.dumps({'payloads':result})))            

urlEncoding('sql.json','sql_url.json')
BinaryEncoding('sql.json','sql_bin.json')