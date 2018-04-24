import sys
import json

def find_login_required_urls(nologin,login):
    nologin_urls = [i['url'] for i in nologin]
    login_urls = [i['url'] for i in login]
    # to handle cases like http://own7.com and http:/own7.com/
    # remove one last character
    #require_login_urls = [ i for i in login_urls if i not in nologin_urls and i[:-1] not in nologin_urls]
    require_login_urls = [ i for i in login_urls if i not in nologin_urls] #and i[:-1] not in nologin_urls]
    return list(set(require_login_urls))

def find_matching_items(item,item_list):
    for i in item_list:
        if item['url'] == i['url'] and item['type']==i['type']:
            pass


if __name__=='__main__':
    if len(sys.argv)!=4:
        print 'Incorrect usage'
        print 'python csrf_scanner.py p1_nologin.json p1_login.json p1_login_run2.json'
        exit(0)

    p1_nologin = json.load(open(sys.argv[1]))

    p1_login = json.load(open(sys.argv[2]))
    p1_login_run2 = json.load(open(sys.argv[3]))

    login_required_urls = find_login_required_urls(p1_nologin,p1_login)
    for item in p1_login_run2:
        if item['url'] in login_required_urls:
            if len(item['param'].keys())>0:
                pass
            matching_items = find_matching_items(item,p1_login)


