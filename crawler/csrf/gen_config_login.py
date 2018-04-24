import json
config = []

# target = { 'url':'https://own7.com/',
         # 'nocrawl':'logout',
        # 'headers':{
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            # 'Referer': 'https://github.com/wmyaiyj/CS5331A3/blob/master/phase1/project/spiders/test.py'
            # },
         # 'login':{
             # 'url':'https://own7.com/own7secondpage.php',
             # 'formdata':{
                 # 'user':['own7'],
                 # 'password':'own7',
                 # 'others':'test'
                 # }
             # }
        # }
# config.append(target)


app2 = {'url':'http://ec2-54-254-169-160.ap-southeast-1.compute.amazonaws.com:8081/',
         'login':{
             'url':'http://ec2-54-254-169-160.ap-southeast-1.compute.amazonaws.com:8081/',
             'formdata':{
                 'username':['morty'],
                 'password':'240610708',
                 'others':'test'
                 }
             }
        }
config.append(app2)

with open('config.json', 'w') as outfile:
    json.dump(config, outfile,indent=4)
