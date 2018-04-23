import scrapy
import os
import urllib
from crawler.items import *
import logging
from lxml import html
import urlparse
import json
from urllib import urlencode

def log(msg):
    logging.log(45,msg)

def _retrieve_form_element(form, origin_url):
    fields = {}
    for x in form.inputs:
        if x.value is None:
            if type(x) == html.SelectElement:
                x.value = x.value_options[0]
            else:
                x.value = "None"
        if type(x) == html.TextareaElement:
            fields[x.name] = [""]
        elif x.name and ("type" in x.keys() and x.type != "submit") and not ("Fatal error" in x.value):
            fields[x.name] = [x.value]
    url = form.action
    if (url is None) or (url is ""):
        url = origin_url
    return {"fields": fields, "url": url,"method":form.method}


def fetch_form(url, body):
    doc = html.document_fromstring(body, base_url=url)
    form_items = []
    for form in doc.xpath('//form'):
        form_items.append(_retrieve_form_element(form, url))
    return form_items

def is_valid(url_str,allowed_domains,nocrawl):

    url = urlparse.urlparse(url_str)

    for nc in nocrawl:
        if nc in url_str:
            log('Url=%s not valid as nocrawl=%s matches'%(url_str,nc))
            return False


    if len(allowed_domains)>0 and url.hostname not in allowed_domains:
        log('Url=%s is not in allowed_domains and allowed_domain is not empty'%(url_str))
        return False

    return True

class Spider(scrapy.Spider):
    name = "p1"

    def __init__(self, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.config = {} # rules per host name

    def get_config(self,hostname):
        config = {'default_headers':{},'allowed_domains':[],'nocrawl':[]}
        if hostname in self.config:
            config = self.config[hostname]
        else:
            self.config[hostname]=config
        return config

    def start_requests(self):
        items_to_crawl = json.load(open('config.json'))
        for item in items_to_crawl:

            url_str = item['url']
            url = urlparse.urlparse(url_str)
            hostname = url.hostname
            config = self.get_config(hostname)

            if 'headers' in item:
                config['default_headers'] = item['headers']

            config['allowed_domains']=[]
            if 'allowed_domains' in item:
                allowed_domains = item['allowed_domains']
                if not type(allowed_domains) == list:allowed_domains = [allowed_domains]
                config['allowed_domains'] = allowed_domains

            if 'nocrawl' in item:
                nocrawl = item['nocrawl']
                if not type(nocrawl) == list:nocrawl= [nocrawl]
                config['nocrawl'] = nocrawl


            self.config[hostname]=config

            if 'login' in item:
                login = item['login']
                yield scrapy.FormRequest(url=login['url'],
                                         formdata= login['formdata'],
                                         callback=self.parse,
                                         meta={'dont_merge_cookies':True},
                                         dont_filter=True)
            else:
                yield scrapy.Request(url=url_str,meta={'dont_merge_cookies': True},headers=config['default_headers'],callback=self.parse)

    def handle_new_cookies(self,response):
        url = urlparse.urlparse(response.url)
        hostname = url.hostname
        config=self.get_config(hostname)
        cookie_header = ''
        for k,vs in response.headers.iteritems():
            if k.lower() == 'set-cookie':
                for v in vs:
                    if ';' in v: v=v[:v.find(';')]
                    cookie_header+=v+';'
        if len(cookie_header)>0:cookie_header=cookie_header[:-1]

        if cookie_header !='':
            if 'Cookie' not in config['default_headers']:
                config['default_headers']['Cookie']=cookie_header
            else:
                cookie_orig = config['default_headers']['Cookie']
                cookie = cookie_orig+';'+cookie_header
                config['default_headers']['Cookie']=cookie
            #return self.generate_cookie_item(response.url,config['default_headers']['Cookie'])
    def parse(self, response):
        url = urlparse.urlparse(response.url)
        hostname = url.hostname
        yield self.handle_new_cookies(response)
        log('Crawling ' + response.url)
        config = self.get_config(hostname)

        default_headers = config['default_headers']
        allowed_domains = config['allowed_domains']
        nocrawl = config['nocrawl']
        forms = fetch_form(response.url, response.body)

        for form in forms:
            item = self.generate_item_from_form(form,default_headers)

            if True:#is_valid(item['url'],allowed_domains,nocrawl):
                yield scrapy.Request(url=item['url'],
                                     meta={'dont_merge_cookies': True},
                                     headers=default_headers,
                                     callback=self.parse)
            # if no parameters don't include in potential list
            #if len(item['param'])!=0:
            yield item


        yield self.generate_item_from_url(response,default_headers)
        # Find links to the next page
        links = response.css('a::attr(href)').extract()

        for l in links:
            nexturl_str = response.urljoin(l)
            if is_valid(nexturl_str,allowed_domains,nocrawl):
                yield scrapy.Request(url=nexturl_str,
                                     headers=default_headers,
                                     meta={'dont_merge_cookies':True},
                                     callback=self.parse)

    def generate_cookie_item(self,url,cookie_header):
        item = CookieItem()
        item [ 'url' ] = url
        cookies = {}
        if cookie_header!='':
            cookies_str = cookie_header.split(';')
            for c_str in cookies_str:
                c = c_str.split('=')
                cookies[c[0]]=c[1]
        item['cookies'] = cookies
        return item
    def generate_item_from_form(self, form,default_headers):
        item = Item()
        item["url"] = form["url"]
        item["param"] = form["fields"]
        item["type"] = form['method']
        item['headers'] = default_headers
        return item

    def generate_item_from_url(self, response,default_headers):
        parsed = urlparse.urlparse(response.url)
        parameters = urlparse.parse_qs(parsed.query)

        item = Item()
        url = parsed.geturl()
        if "?" in url:
            item['url'] = url[:url.find('?')]
        else:
            item['url'] = url

        item['param'] = parameters
        item['type'] = "GET"

        referer = None
        if "Referer" in response.request.headers.keys():
            referer = response.request.headers["Referer"]
        item["headers"] = {
            "referer": referer,
            "user-agent": response.request.headers["User-Agent"]
        }
        item['headers'].update(default_headers)
        # if len(item['param'])==0:
            # return None
        return item
