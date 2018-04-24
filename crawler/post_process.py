# this script does duplicate removals and cookies collection
import json
import os
import urlparse
import sys

def all_keys_match(p1,p2):
    for k in p1.keys():
        if k not in p2.keys():
            return False
    return True

def all_values_match(p1,p2):
    for k in p1.keys():
        if p2[k] != p1[k]:
            return False
    return True
def has_dupes(item,item_list):
    pass
crawled_items = json.load(open(sys.argv[1]))
cookies = {}
if len(crawled_items)>0:
    # collect cookies for all hosts
    for ci in crawled_items:
        url = urlparse.urlparse(ci['url'])
        hostname = url.hostname
        if hostname not in cookies:
            cookies[hostname] = {}
        if 'headers' in ci:
            if 'Cookie' in ci['headers']:
                cookies_str = ci['headers']['Cookie']
                cookies_str = cookies_str.split(';')
                for co in cookies_str:
                    ckv = co.split('=')
                    cookies[hostname][ckv[0]]=ckv[1]

    crawled_items_str = []
    no_dupes = []
    for ci in crawled_items:
        url = urlparse.urlparse(ci['url'])
        hostname = url.hostname
        ci['CookieList'] = cookies[hostname]

        crawled_items_str.append(json.dumps(ci))

    nodupes = list(set(crawled_items_str))
    print str(len(crawled_items_str)-len(nodupes)) + ' duplicates removed'
    with open(sys.argv[1], 'w') as outfile:
        outfile.write('[\n')
        for i in xrange(len(nodupes)):
            line = nodupes[i]
            if i==len(nodupes)-1:outfile.write(line+'\n')
            else:outfile.write(line+',\n')
        outfile.write(']\n')

