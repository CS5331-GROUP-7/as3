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

def savefile(self):
    #print self.result
    with open('sql_plus.json','w') as f:
        f.write(unicode(json.dumps(self.result, indent = 4)))                

with open('sql.json',mode='r',encoding='utf-8') as file:
    load_dict = json.load(file)
    load_dict = byteify(load_dict)
    payloads = load_dict['payloads']
    result = []
    for payload in payloads:
	    a = urllib.quote_plus(payload)
	    result.append(a)
    with open('sql_plus.json','w') as f:
        f.write(unicode(json.dumps({'payloads':result})))                
