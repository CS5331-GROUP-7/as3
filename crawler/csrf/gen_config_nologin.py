import json
config = []

target = { 'url':'http://ec2-54-254-169-160.ap-southeast-1.compute.amazonaws.com:8081/',
         }
config.append(target)


with open('config.json', 'w') as outfile:
    json.dump(config, outfile,indent=4)
