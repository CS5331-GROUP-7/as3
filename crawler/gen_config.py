import json
config = []

own7 = { 'url':'https://own7.com',
         'nocrawl':'logout',
        'headers':{
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'Referer': 'https://github.com/wmyaiyj/CS5331A3/blob/master/phase1/project/spiders/test.py'
            },
         'login':{
             'url':'https://own7.com/own7secondpage.php',
             'formdata':{
                 'user':['own7'],
                 'password':'own7',
                 'others':'test'
                 }
             }
        }
target = {'url':'http://target.com',
        'headers':{
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'Referer': 'https://github.com/wmyaiyj/CS5331A3/blob/master/phase1/project/spiders/test.py'
            }
         }
own7_cookie = {'url':'http://own7.com',
               'allowed_domains':'own7.com',
               'nocrawl':'logout',
               'headers':{

                   'Cookie': 'PHPSESSID=lsvu3sso4reeatetds7cajkvv0; UserDetails=own7own7; loggedin=yes'
                   },
               }
own4 = {'url':'https://own4.com'}
app2 = {'url':'http://ec2-54-254-169-160.ap-southeast-1.compute.amazonaws.com:8081/',
         'login':{
             'url':'https://own7.com/own7secondpage.php',
             'formdata':{
                 'user':['own7'],
                 'password':'own7',
                 'others':'test'
                 }
             }
        }
config.append(app2)
# config.append(own7)
#config.append(own4)
config.append(app2)

# config.append({"url": "https://own1.com"})
# config.append({"url": "https://own2.com"})
#config.append({"url": "https://own3.com"})
# config.append({"url": "https://own4.com"})
# config.append({"url": "https://own5.com"})
# config.append({"url": "https://own6.com"})
config.append(own7)
# config.append({"url": "https://own8.com"})
# config.append({"url": "https://own9.com"})
# config.append({"url": "https://own10.com"})
# config.append({"url": "https://own11.com"})
# # config.append(own7_cookie)
config.append(target)


with open('config.json', 'w') as outfile:
    json.dump(config, outfile,indent=4)
