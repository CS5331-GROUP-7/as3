import scrapy
import os
import urllib
from crawler.items import *
import logging
from lxml import html

import urlparse

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

class Spider(scrapy.Spider):
    name = "p1"

    def start_requests(self):
        urls = [
            'http://target.com',
        ]
        allowed_domains = [
            'target.com',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        post_forms = fetch_form(response.url, response.body)
        for post_form in post_forms:
            post_item = self.generate_post_item(post_form)
            if post_item is not None:
                yield post_item

        yield self.generate_get_item(response)

        # Find links to the next page
        links = response.css('a::attr(href)').extract()

        for l in links:
            yield scrapy.Request(response.urljoin(l),callback=self.parse)

    def generate_post_item(self, post_form):
        post_item = Item()
        post_item["url"] = post_form["url"]
        post_item["param"] = post_form["fields"]
        post_item["type"] = "POST"

        if bool(post_item["param"]):
            return post_item
        return None

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
        return item
