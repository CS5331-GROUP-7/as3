import bs4
import itertools
import json
import re
import requests
import multiprocessing
from difflib import Differ
from result_models import SQLInjectionModel, SSCInjectionModel,\
    DirectoryTraversalModel, OpenRedirectModel, CommandInjectionModel
from requests.packages.urllib3.exceptions import InsecureRequestWarning
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

regex_nums = re.compile(r"[\d]")

sqli_results = SQLInjectionModel()
ssci_results = SSCInjectionModel()
dtra_results = DirectoryTraversalModel()
opre_results = OpenRedirectModel()
cmdi_results = CommandInjectionModel()

crawler_info = {}


def setup():
    # read p1
    with open(p1_file_path) as hf:
        d = json.load(hf)
        for v in d:
            header = None
            if "headers" in v:
                header = v["headers"]

            param = None
            if "param" in v:
                param = v["param"]

            crawler_info[v["type"] + v["url"]] = {
                "headers": header,
                "param": param
            }
    hf.close()

    # read p2
    payloads = []
    with open(p2_file_path) as pf:
        j = json.load(pf)
        # for t in j:
        #     if len(t) > 0:
        #         payloads[t[0]["class"]] = t
        payloads = list(itertools.chain.from_iterable(j))
    pf.close()
    return payloads


def do_attack(p):
    url = p["url"]
    key = p["type"] + url
    o_params = {}
    headers = default_header
    if key in crawler_info:
        vals = crawler_info.get(key)
        if "param" in vals:
            o_params = vals["param"]
        if "headers" in vals and vals["headers"] is not None:
            headers = vals["headers"]

    res = do_inject(url,
                    p["type"].upper(),
                    p["param"],
                    o_params,
                    headers)
    if res is False or res is None:
        return None

    # add to corresponding result
    # if p["class"] == "SQL Injection":
    #     sqli_results.add_payload(url, p)
    # elif p["class"] == "Server Side Code Injection":
    #     ssci_results.add_payload(url, p)
    # elif p["class"] == "Directory Traversal":
    #     dtra_results.add_payload(url, p)
    # elif p["class"] == "Open Redirect":
    #     opre_results.add_payload(url, p)
    # elif p["class"] == "Command Injection":
    #     cmdi_results.add_payload(url, p)
    # else:
    #     print(str.format("[ERR]: Unable to identify payload for {} ({})"), p["url"], p["class"])
    #     return None
    # print(str.format("[VUL]: {} ({})", p["url"], p["type"]))
    return p


def do_inject(url, method, atk_params, o_params, headers):
        if method.upper() == "GET":
            # use original params
            o_req = requests.get(url, params=o_params, headers=headers, verify=False)
            atk_req = requests.get(url, params=atk_params, headers=headers, verify=False)
        else:
            o_req = requests.post(url, data=o_params, headers=headers, verify=False)
            atk_req = requests.post(url, data=atk_params, headers=headers, verify=False)

        o_req_content = o_req.content
        # replace away original param
        for k, v in o_params.iteritems():
            o_req_content = o_req_content.replace(k, "")
            if type(v) is list or type(v) is tuple:
                for p in v:
                    o_req_content = o_req_content.replace(p, "")
            else:
                o_req_content = o_req_content.replace(v, "")

        atk_req_content = atk_req.content
        for k, v in atk_params.iteritems():
            atk_req_content = atk_req_content.replace(k, "")
            atk_req_content = atk_req_content.replace(v, "")

        return is_html_diff(o_req_content, atk_req_content)


def is_html_diff(a, b):
    diff_str = diff_html(a, b)
    if diff_str.count("\n+ ") > diff_str.count("\n- "):
        return True
    return False


def diff_html(a, b):
    # normalize all strings, remove all numbers
    a = regex_nums.sub("", a)
    b = regex_nums.sub("", b)

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
    return '\n'.join(diff)


def main():
    payloads = setup()

    pool = multiprocessing.Pool(25)
    results = pool.map(do_attack, payloads)
    for p in results:
        if p is None:
            continue
        if p["class"] == "SQL Injection":
            sqli_results.add_payload(p["url"], p)
        elif p["class"] == "Server Side Code Injection":
            ssci_results.add_payload(p["url"], p)
        elif p["class"] == "Directory Traversal":
            dtra_results.add_payload(p["url"], p)
        elif p["class"] == "Open Redirect":
            opre_results.add_payload(p["url"], p)
        elif p["class"] == "Command Injection":
            cmdi_results.add_payload(p["url"], p)
        else:
            print(str.format("[ERR]: Unable to identify payload for {} ({})"), p["url"], p["class"])
            continue
        print(str.format("[VUL]: {} ({})", p["url"], p["type"]))


start = time.time()
main()
print "Elapsed Time: %s" % (time.time() - start)
