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
            #print self.urls
        
        with open('default.json',mode='r',encoding='utf-8') as file:
            load_dict = json.load(file)
            load_dict = byteify(load_dict)
            self.default_name = load_dict['payloads']

        with open('white_list.json',mode='r',encoding='utf-8') as file:
            load_dict = json.load(file)
            load_dict = byteify(load_dict)
            self.white_list = load_dict

      
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

        request = []
        for item in self.urls:
            #if it in the white list
            #add default cookie
            tempString = ""
            z=dict(item['headers'])
            temp = dict(item['CookieList'])
            for i,cookieItem in enumerate(temp):
                if(i!=len(temp)):
                    tempString = tempString + cookieItem+'=' + temp[cookieItem] + ';'
                else:
                    tempString = tempString + cookieItem+'=' + temp[cookieItem]

            if(len(temp)>0):
                z['Cookie']=tempString
                if(len(item['param'])<=0):
                    request.append({"class":classname,"url":item['url'],"header":z,"type":item['type']})    
                else:         
                    for data in item['param']:
                        for payload in payloads:
                            paras=dict(item['param'])
                            paras[data] = payload 
                            request.append({"class":classname,"url":item['url'],"header":z,"param":paras,"type":item['type']})
            else:
                if(len(item['param'])<=0):
                    request.append({"class":classname,"url":item['url'],"type":item['type']})    
                else:         
                    for data in item['param']:
                        for payload in payloads:
                            paras=dict(item['param'])
                            paras[data] = payload 
                            request.append({"class":classname,"url":item['url'],"param":paras,"type":item['type']})
           
            #if the url in the white list
            tempString1 = ""
            if(self.white_list.has_key(item['url'])):
                for cookieItem in item['CookieList']:
                    temp = dict(item['CookieList'])
                    if(white_list[item['url']].has_key('Cookie')):
                        z=dict(item['headers'])
                        tempString1 = ""
                        for i,cookieItem in enumerate(temp):
                            if(i!=len(temp)):
                                tempString1 = tempString1 + cookieItem+'=' + temp[cookieItem] + ';'
                            else:
                                tempString1 = tempString1 + cookieItem+'=' + temp[cookieItem]

                        z['Cookie']=tempString1
                        request.append({"class":classname,"url":item['url'],"header":z,"type":item['type']})    
                    else:   
                        for payload1 in payloads:
                            z=dict(item['headers'])
                            temp[cookieItem] = payload1
                            tempString1 = ""
                            for i,cookieItem in enumerate(temp):
                                if(i!=len(temp)):
                                    tempString1 = tempString1 + cookieItem+'=' + temp[cookieItem] + ';'
                                else:
                                    tempString1 = tempString1 + cookieItem+'=' + temp[cookieItem]

                            z['Cookie']=tempString1

                            if(len(item['param'])<=0):
                                request.append({"class":classname,"url":item['url'],"header":z,"type":item['type']})    
                            else:
                                for data in item['param']:
                                    if(white_list[item['url']].has_key(data)):
                                        request.append({"class":classname,"url":item['url'],"header":z,"param":item['param'],"type":item['type']})
                                    else:
                                        for payload in payloads:
                                            paras=dict(item['param'])
                                            paras[data] = payload 
                                            request.append({"class":classname,"url":item['url'],"header":z,"param":paras,"type":item['type']})
            #if the url is not in the white list
            else:
                for cookieItem1 in item['CookieList']:
                    for payload1 in payloads:
                        temp = dict(item['CookieList'])

                        z=dict(item['headers'])
                        temp[cookieItem1] = payload1
                        #print cookieItem1
                        tempString1 = ""
                        for i,cookieItem in enumerate(temp):
                            if(i!=len(temp)):
                                tempString1 = tempString1 + cookieItem+'=' + temp[cookieItem] + ';'
                            else:
                                tempString1 = tempString1 + cookieItem+'=' + temp[cookieItem]

                        z['Cookie']=tempString1
                        #print tempString1
                        if(len(item['param'])<=0):
                            request.append({"class":classname,"url":item['url'],"header":z,"type":item['type']})    
                        else:
                            for data in item['param']:
                                for payload in payloads:
                                    paras=dict(item['param'])
                                    paras[data] = payload 
                                    request.append({"class":classname,"url":item['url'],"header":z,"param":paras,"type":item['type']})
                            
        #print request   
        self.result.append(request)
        #print request
    def savefile(self):
        #print self.result
        with open('p2.json','w') as f:
            f.write(unicode(json.dumps(self.result, indent = 4)))                

def main():
    generater = Generater();
    # generater.generate('Directory Traversal','traversal.json');
    # generater.generate('Directory Traversal','traversal-passwd.json')
    # generater.generate('SQL Injection','sql.json')
    # generater.generate('SQL Injection','sqlall.json')
    # generater.generate('SQL Injection','sqlall2.json')
    generater.generate('Command Injection','commend.json')
    generater.generate('Open Redirect','redirect.json')
    
    generater.savefile();
    
main()
