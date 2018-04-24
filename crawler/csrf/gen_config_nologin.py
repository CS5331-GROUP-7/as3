import json
config = []

target = { 'url':'https://own7.com/',
         }
config.append(target)


with open('config.json', 'w') as outfile:
    json.dump(config, outfile,indent=4)
