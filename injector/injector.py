import bs4
import errno
import json
import os
import requests
from difflib import Differ
from result_models import SQLInjectionModel, SSCInjectionModel,\
    DirectoryTraversalModel, OpenRedirectModel, CommandInjectionModel
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Disable the HTTPS warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

p1_file_path = "../crawler/p1.json"
p2_file_path = "../generater/p2.json"

results_dir = "../results/"
results_sql = results_dir + "sql_results.json"
results_ssc = results_dir + "ssc_results.json"
results_dtr = results_dir + "dtr_results.json"
results_ore = results_dtr + "ore_results.json"
results_cmi = results_dtr + "cmi_results.json"

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
        with open(payload_file) as pf:
            j = json.load(pf)
            self.payloads = j
        pf.close()

        # read for header info
        with open(p1_file_path) as hf:
            d = json.load(hf)
            self.crawler_info = {}
            for v in d:
                header = None
                if "headers" in v:
                    header = v["headers"]

                param = None
                if "param" in v:
                    param = v["param"]

                self.crawler_info[v["url"]] = {
                    "headers": header,
                    "params": param
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

        if not self.sqli_results.results\
                and not self.ssci_results.results\
                and not self.dtra_results.results\
                and not self.opre_results.results\
                and not self.cmdi_results.results:
            print("==== NO RESULTS ====")

        # end and output
        # self.end_inject()

    def start_inject(self):
        """
        Start injecting payloads
        :return:
        """

        for p in self.payloads:
            url = p["url"]
            o_params = {}
            headers = default_header
            if url in self.crawler_info:
                vals = self.crawler_info.get(url)
                if "param" in vals:
                    o_params = vals["param"]
                if "headers" in vals:
                    headers = vals["headers"]

            res = self.do_inject(url,
                                 p["type"].upper(),
                                 p["param"],
                                 o_params,
                                 headers)
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
                print(str.format("[ERR]: Unable to identify payload for {} ({})"), p["url"], p["class"])
                continue
            print(str.format("[VUL]: {} ({})", p["url"], p["type"]))

    def do_inject(self, url, method, atk_params, o_params, headers):
        if method.upper() == "GET":
            return self.do_get(url, atk_params, o_params, headers)
        return self.do_post(url, atk_params, o_params, headers)

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

    def do_get(self, url, atk_params, o_params, headers):
        """
        GET requests
        :return:
        """
        # use original params
        o_req = requests.get(url, params=o_params, headers=headers, verify=False)
        # replace away original param
        o_req_content = o_req.content
        for k, v in o_params.iteritems():
            o_req_content = o_req_content.replace(k, "")
            o_req_content = o_req_content.replace(v, "")

        atk_req = requests.get(url, params=atk_params, headers=headers, verify=False)
        atk_req_content = atk_req.content
        for k, v in atk_params.iteritems():
            atk_req_content = atk_req_content.replace(k, "")
            atk_req_content = atk_req_content.replace(v, "")

        return is_html_diff(o_req_content, atk_req_content)

    def do_post(self, url, atk_params, o_params, headers):
        """
        POST requests
        :return:
        """
        # use original data
        o_req = requests.post(url, data=o_params, headers=headers, verify=False)
        o_req_content = o_req.content
        for k, v in o_params.iteritems():
            o_req_content = o_req_content.replace(k, "")
            o_req_content = o_req_content.replace(v, "")

        atk_req = requests.post(url, data=atk_params, headers=headers, verify=False)
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
    a_soup = bs4.BeautifulSoup(a, "lxml")
    b_soup = bs4.BeautifulSoup(b, "lxml")

    d = Differ()
    diff = d.compare(list(a_soup.stripped_strings), list(b_soup.stripped_strings))
    return '\n'.join(diff)


# i = Injector("sample_p2.json")
i = Injector(p2_file_path)
i.start_inject()
# i.end_inject()
