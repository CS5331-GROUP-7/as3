import bs4
import errno
import itertools
import json
import os
import re
import requests
from difflib import Differ
from result_models import SQLInjectionModel, SSCInjectionModel,\
    DirectoryTraversalModel, OpenRedirectModel, CommandInjectionModel
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from tqdm import tqdm
from urlparse import urlparse
import time

# Disable the HTTPS warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

p1_file_path = "../crawler/p1.json"
p2_file_path = "../generater/p2.json"

results_dir = "../results/"
results_sql = results_dir + "sql_results.json"
results_ssc = results_dir + "ssc_results.json"
results_dtr = results_dir + "dtr_results.json"
results_ore = results_dir + "ore_results.json"
results_cmi = results_dir + "cmi_results.json"

default_header = {
    "Referrer": "http://google.com",
    "User-Agent": "Scrapy/1.5.0 (+https://scrapy.org)"
}

regex_numsym = re.compile(r"[\d|_^+]|(.{1,4}/)")


class Injector:
    def __init__(self, payload_file):
        """
        Starts an injector for a specific payload file
        :param payload_file: JSON file with payloads relating to a certain endpoint
        """
        # read payload_file and store
        with open(payload_file) as pf:
            j = json.load(pf)
            self.payloads = list(itertools.chain.from_iterable(j))
        pf.close()

        # read for header info
        with open(p1_file_path) as hf:
            d = json.load(hf)
            self.crawler_info = {}
            for v in d:
                header = None
                if "headers" in v:
                    header = v["headers"]

                param = {}
                if "param" in v:
                    param = v["param"]

                if "type" in v and "param" in v and "headers" in v:
                    self.crawler_info[v["type"]+v["url"]] = {
                        "headers": header,
                        "param": param
                    }
                elif "type" in v and "param" not in v and "headers" in v:
                    self.crawler_info[v["type"] + v["url"]] = {
                        "headers": header
                    }
                elif "type" in v and "param" in v and "headers" not in v:
                    self.crawler_info[v["type"] + v["url"]] = {
                        "param": param
                    }

        hf.close()

        # for output
        self.sqli_results = SQLInjectionModel()
        self.ssci_results = SSCInjectionModel()
        self.dtra_results = DirectoryTraversalModel()
        self.opre_results = OpenRedirectModel()
        self.cmdi_results = CommandInjectionModel()

        # start attacking
        # self.start_inject()

        # if not self.sqli_results.results\
        #         and not self.ssci_results.results\
        #         and not self.dtra_results.results\
        #         and not self.opre_results.results\
        #         and not self.cmdi_results.results:
        #     print("==== NO RESULTS ====")

        # end and output
        # self.end_inject()

    def start_inject(self):
        """
        Start injecting payloads
        :return:
        """

        for p in tqdm(self.payloads):
            url = p["url"]
            key = p["type"]+url

            o_params = {}
            o_headers = default_header
            if key in self.crawler_info:
                vals = self.crawler_info.get(key)
                if "param" in vals:
                    o_params = vals["param"]
                if "headers" in vals and vals["headers"] is not None:
                    o_headers = vals["headers"]

            atk_params = {}
            atk_headers = o_headers
            if "header" in p:
                atk_headers = p["header"]
                for i in atk_headers:
                    if type(atk_headers[i]) is dict:
                        atk_headers[i] = ''.join('{}={}'.format(key, val.encode('ascii', 'ignore')) for key, val in atk_headers[i].items())
                    if atk_headers[i] is None:
                        continue
                    atk_headers[i] = atk_headers[i].encode('ascii', 'ignore')
            if "param" in p:
                atk_params = p["param"]

            res = self.do_inject(url,
                                 p["type"].upper(),
                                 atk_params,
                                 o_params,
                                 o_headers,
                                 atk_headers,
                                 p["class"])

            if res is False or res is None:
                continue

            # add to corresponding result
            if p["class"] == "SQL Injection":
                self.sqli_results.add_payload(url, p)
            elif p["class"] == "Server Side Code Injection":
                self.ssci_results.add_payload(url, p)
            elif p["class"] == "Directory Traversal":
                self.dtra_results.add_payload(url, p)
            elif p["class"] == "Open Redirect":
                self.opre_results.add_payload(url, p)
            elif p["class"] == "Command Injection":
                self.cmdi_results.add_payload(url, p)
            else:
                tqdm.write(str.format("[ERR]: Unable to identify payload for {} ({})"), p["url"], p["class"])
                continue
            tqdm.write(str.format("[VUL]: {} ({})", p["url"], p["type"]))

    def do_inject(self, url, method, atk_params, o_params, o_headers, atk_headers, atk_type):
        if method.upper() == "GET":
            o_req = requests.get(url, params=o_params, headers=o_headers, verify=False)
            atk_req = requests.get(url, params=atk_params, headers=atk_headers, verify=False)
        else:
            o_req = requests.post(url, data=o_params, headers=o_headers, verify=False)
            atk_req = requests.post(url, data=atk_params, headers=atk_headers, verify=False)

        if o_req.status_code == 500 or atk_req.status_code == 500:
            tqdm.write(str.format("[WARN]: Status 500 encountered while processing request for  ({})", url, method))
            return False

        # use original params
        o_req_content = unicode(o_req.content, errors="replace")
        # replace away original param
        for k, v in o_params.iteritems():
            o_req_content = o_req_content.replace(k, "")
            if type(v) is list or type(v) is tuple:
                for p in v:
                    o_req_content = o_req_content.replace(p, "")
            elif v is not None:
                o_req_content = o_req_content.replace(v, "")
        for k, v in o_headers.iteritems():
            o_req_content = o_req_content.replace(k, "")
            if k.lower() == "cookie":
                a = v.split("=")
                for s in a:
                    o_req_content.replace(s, "")
            elif v is not None:
                o_req_content = o_req_content.replace(v, "")

        atk_req_content = unicode(atk_req.content, errors="replace")
        for k, v in atk_params.iteritems():
            atk_req_content = atk_req_content.replace(k, "")
            if type(v) is list or type(v) is tuple:
                for p in v:
                    atk_req_content = atk_req_content.replace(p, "")
            elif v is not None:
                atk_req_content = atk_req_content.replace(v, "")
        for k, v in atk_headers.iteritems():
            atk_req_content = atk_req_content.replace(k, "")
            if k.lower() == "cookie":
                a = v.split("=")
                for s in a:
                    atk_req_content.replace(s, "")
            elif v is not None:
                atk_req_content = atk_req_content.replace(v, "")

        # workaround, may need additional check for wanted domain
        if atk_type == "Open Redirect" \
                and urlparse(atk_req.url).netloc != urlparse(o_req.url).netloc:
            return True

        return is_html_diff(o_req_content, atk_req_content)

    def end_inject(self):
        # check for existence of output dir
        if not os.path.exists(os.path.dirname(results_dir)):
            try:
                os.makedirs(os.path.dirname(results_dir))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        # write outputs
        with open(results_sql, "w") as sqlf:
            sqlf.write(self.sqli_results.get_json())
        sqlf.close()

        with open(results_ssc, "w") as sscf:
            sscf.write(self.ssci_results.get_json())
        sscf.close()

        with open(results_dtr, "w") as dtrf:
            dtrf.write(self.dtra_results.get_json())
        dtrf.close()

        with open(results_ore, "w") as oref:
            oref.write(self.opre_results.get_json())
        oref.close()

        with open(results_cmi, "w") as cmif:
            cmif.write(self.cmdi_results.get_json())
        cmif.close()


def is_html_diff(a, b):
    diff_str = '\n'.join(diff_html(a, b))
    if diff_str.count("\n+ ") > diff_str.count("\n- ") + 1:
        return True

    minus = ''
    add = ''
    for x in list(diff_html(a, b)):
        if x.startswith('- '):
            minus += x
        elif x.startswith('+ '):
            add += x

    if len(add) != 0 and len(minus) != 0\
            and (len(add) / len(minus)) > 11:
        return True

    return False


def diff_html(a, b):
    # normalize all strings, remove all numbers
    a = regex_numsym.sub("", a)
    b = regex_numsym.sub("", b)

    # compare and remove commonalities on both
    a_soup = bs4.BeautifulSoup(a, "html.parser")
    b_soup = bs4.BeautifulSoup(b, "html.parser")

    a_pre = []
    for ap in a_soup.find_all("pre"):
        a_pre = a_pre + ap.text.split()

    b_pre = []
    for bp in b_soup.find_all("pre"):
        b_pre = b_pre + bp.text.split()

    d = Differ()
    # diff = d.compare(list(a_soup.stripped_strings), list(b_soup.stripped_strings))
    diff = d.compare(list(a_soup.stripped_strings) + a_pre,
                     list(b_soup.stripped_strings) + b_pre)
    return diff


# start = time.time()
# i = Injector("sample_p2.json")
i = Injector(p2_file_path)
i.start_inject()
i.end_inject()
# print "Elapsed Time: %s" % (time.time() - start)