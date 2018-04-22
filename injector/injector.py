import json
import requests
import bs4
from difflib import Differ

default_header = {
    "Referrer": "http://google.com",
    "User-Agent": "Scrapy/1.5.0 (+https://scrapy.org)"
    }


class Injector:
    def __init__(self, payload_file):
        """
        Starts an injector for a specific payload file
        :param payload_file: JSON file with payloads relating to a certain endpoint
        """
        # read payload_file and store
        with open(payload_file) as f:
            j = json.load(f)
            self.payloads = j["results"]
        # get login info?

        pass

    def is_login_required(self, payload):
        """
        Checks if login is required
        :return:
        """
        pass

    def start_inject(self):
        """
        Start injecting payloads
        :return:
        """
        # store intermediates

        for k, v in self.payloads.iteritems():
            base_url = k
            for p in v:
                res = self.do_inject(base_url + p["endpoint"],
                               p["method"].upper(),
                               p["params"])
                if res is None:
                    continue
                print(str.format("[VUL]: {} ({})", base_url+p["endpoint"], p["params"]))
        # process intermediates, convert to output format
        # write output

    def do_inject(self, url, method, params):
        # check for login
        if method.upper() == "GET":
            return self.do_get()
        return self.do_post(url, params)

    def do_get(self):
        """
        GET without login
        :return:
        """
        pass

    def do_get_login(self):
        """
        GET with login
        :return:
        """
        pass

    def do_post(self, url, params):
        """
        POST without login
        :return:
        """
        o_req = requests.post(url, data=None, headers=default_header)
        # o_req_status = o_req.status_code
        o_req_content = o_req.content

        atk_req = requests.post(url, data=params, headers=default_header)
        # atk_req_status = atk_req.status_code
        atk_req_content = atk_req.content

        o_req_content = o_req_content.replace("None", "")

        diff_str = diff_html(o_req_content, atk_req_content)
        if diff_str.count("+") > diff_str.count("-"):
            return True
        return None

    def do_post_login(self):
        """
        POST with login
        :return:
        """
        pass


def diff_html(a, b):
    a_soup = bs4.BeautifulSoup(a, "lxml")
    b_soup = bs4.BeautifulSoup(b, "lxml")

    d = Differ()
    diff = d.compare(list(a_soup.stripped_strings), list(b_soup.stripped_strings))
    return '\n'.join(diff)


i = Injector("sample_p2.json")
i.start_inject()
