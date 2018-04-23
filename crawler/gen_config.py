import json
config = []

own7 = { 'url':'http://own7.com',
         'username':'own7',
         'password':'own7',
         'login':{
             'url':'http://own7.com/own2secondpage.php',
             'formdata':{
                 'username':'own7',
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

config.append(own7)
#config.append(own7_cookie)
# config.append(target)


with open('config.json', 'w') as outfile:
    json.dump(config, outfile,indent=4)
