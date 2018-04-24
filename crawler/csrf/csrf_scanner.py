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


if len(sys.argv)!=4:
    print 'Incorrect usage'
    print 'python csrf_scanner.py p1_nologin.json p1_login.json p1_login_run2.json'
    exit(0)

p1_nologin = json.load(open(sys.argv[1]))

p1_login = json.load(open(sys.argv[2]))
p1_login_run2 = json.load(open(sys.argv[3]))


print find_login_required_urls(p1_nologin,p1_login)
