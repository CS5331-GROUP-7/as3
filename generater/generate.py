import json
from io import open 
default_header = {
    "Referrer": "http://google.com",
    "User-Agent": "Scrapy/1.5.0 (+https://scrapy.org)"
    }

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
    def __init__(self, payload_file):
        """
        Starts an injector for a specific payload file
        :param payload_file: JSON file with payloads relating to a certain endpoint
        """
        # read payload_file and store
        urls = []
        with open('../crawler/p1.json',mode='r',encoding='utf-8') as file:
            load_dict = json.load(file)
            load_dict = byteify(load_dict)
            self.urls = load_dict
        with open(payload_file,mode='r',encoding='utf-8') as file1:
            load_dict =[]
            for item in file1:
                load_dict.append(byteify(item))
            self.payloads = load_dict

    def generate(self,classname):
        """
        Generate the request
        :return file named p2.json
        """
        request = []
        for item in self.urls:
            for payload in self.payloads:
                for i,data in enumerate(item['param']):
                    paras = {}
                    for data in item['param']:
                        paras[data]=""
                    paras[data] = payload 
                    if(item.has_key('headers')):
                        request.append({"class":classname,"url":item['url'],"header":item['headers'],"param":paras,"type":item['type']})
                    else:
                        request.append({"class":classname,"url":item['url'],"param":paras,"type":item['type']})
        #print request
        with open('p2.json','w') as f:
            f.write(unicode(json.dumps(request, ensure_ascii=False,indent = 4)))                


generater = Generater('sql.txt');
generater.generate("classname");
