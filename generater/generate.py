import json
from io import open 
default_header = {
    "Referrer": "http://google.com",
    "User-Agent": "Scrapy/1.5.0 (+https://scrapy.org)"
    }
def DelLastChar(str):
    str_list = list(str)
    str_list.pop()
    return "".join(str_list)

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

class Generater:
    def __init__(self):
        """
        Starts an injector for a specific payload file
        :param payload_file: JSON file with payloads relating to a certain endpoint
        """
        # read payload_file and store
        urls = []
        self.result = []
        with open('../crawler/p1.json',mode='r',encoding='utf-8') as file:
            load_dict = json.load(file)
            load_dict = byteify(load_dict)
            self.urls = load_dict

    def generate(self,classname,payload_file):
        """
        Generate the request
        :return file named p2.json
        """
        payloads = []
        with open(payload_file,mode='r',encoding='utf-8') as file:
            load_dict = json.load(file)
            load_dict = byteify(load_dict)
            payloads = load_dict['payloads']

        with open('default.json',mode='r',encoding='utf-8') as file:
            load_dict = json.load(file)
            load_dict = byteify(load_dict)
            default_name = load_dict['payloads']


        request = []
        for item in self.urls:
            for payload in payloads:
                if 'param' in item:
                    for i,data in enumerate(item['param']):
                        paras = {}
                        for data1 in item['param']:
                            if(default_name.has_key(data1)):
                                paras[data1]=default_name[data1]
                            else:
                                paras[data1]=""

                        paras[data] = payload
                        if(item.has_key('headers')):
                            request.append({"class":classname,"url":item['url'],"header":item['headers'],"param":paras,"type":item['type']})
                        else:
                            request.append({"class":classname,"url":item['url'],"param":paras,"type":item['type']})
        self.result.append(request)
        #print request
    def savefile(self):
        #print self.result
        with open('p2.json','w') as f:
            f.write(unicode(json.dumps(self.result, indent = 4)))                

def main():
    generater = Generater();
    #generater.generate('Directory Traversal','traversal.json');
    generater.generate('Directory Traversal','traversal-passwd.json')
    generater.generate('SQL Injection','sql.json')
    generater.generate('Command Injection','commend.json')
    generater.generate('Open Redirect','redirect.json')
    
    generater.savefile();
    
main()
