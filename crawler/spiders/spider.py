import scrapy
import os
import urllib
from crawler.items import *
import logging
from lxml import html
import urlparse
import json

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
    return {"fields": fields, "url": url}


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

        self.default_headers = {}
        self.allowed_domains = {}

    def start_requests(self):
        items_to_crawl = json.load(open('config.json'))
        for item in items_to_crawl:
            config = {'default_headers':None,'allowed_domains':[],'nocrawl':[]}

            url_str = item['url']
            url = urlparse.urlparse(url_str)
            hostname = url.hostname

            if 'username' in item and 'password' in item:
                pass
                #todo login
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
            yield scrapy.Request(url=url_str,meta={'dont_merge_cookies': True},headers=config['default_headers'],callback=self.parse)


    def parse(self, response):

        url = urlparse.urlparse(response.url)
        hostname = url.hostname

        log('Crawling ' + response.url)
        #print response.body

        #print response.body
        config = {'default_headers':None,'allowed_domains':[],'nocrawl':[]}
        if hostname in self.config:
            config = self.config[hostname]

        default_headers = config['default_headers']
        allowed_domains = config['allowed_domains']
        nocrawl = config['nocrawl']

        post_forms = fetch_form(response.url, response.body)
        for post_form in post_forms:
            post_item = self.generate_post_item(post_form)

            if is_valid(post_item['url'],allowed_domains,nocrawl):
                yield scrapy.Request(url=post_item['url'],meta={'dont_merge_cookies': True},headers=default_headers,callback=self.parse)
            # if no parameters don't include in potential list
            if len(post_item['param'])!=0:
                yield post_item


        yield self.generate_get_item(response)
        # Find links to the next page
        links = response.css('a::attr(href)').extract()

        for l in links:
            nexturl_str = response.urljoin(l)

            if is_valid(nexturl_str,allowed_domains,nocrawl):
                yield scrapy.Request(url=nexturl_str,headers=default_headers,callback=self.parse)

    def generate_post_item(self, post_form):
        post_item = Item()
        post_item["url"] = post_form["url"]
        post_item["param"] = post_form["fields"]
        post_item["type"] = "POST"
        return post_item
        # if bool(post_item["param"]):
            # return post_item
        # return None

    def generate_get_item(self, response):
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
        if len(item['param'])==0:
            return None
        return item
