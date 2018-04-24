import json
import requests


default_header = {
    "Referrer": "http://google.com",
    "User-Agent": "Scrapy/1.5.0 (+https://scrapy.org)"
}
post_template = """import requests\r\n
\r\nreq = requests.post(\"**URL**\", data=**DATA**, headers=**HEADERS**, verify=False)\r\n
\r\nprint(req.content)\r\n"""
get_template = """import requests\r\n
\r\nreq = requests.get(\"**URL**\", params=**PARAMS**, headers=**HEADERS**, verify=False)\r\n
\r\nprint(req.content)\r\n"""

token_URL = "**URL**"
token_GET_PARAMS = "**PARAMS**"
token_POST_PARAMS = "**DATA**"
token_headers = "**HEADERS**"


def get_json(file_name):
    with open(file_name) as f:
        return json.load(f)


def gen_cmi():
    data = get_json('cmi_results.json')
    if "results" not in data or len(data["results"]) < 1:
        print("No results for Command Injection")

    count = 1
    for k, v in data["results"].iteritems():
        for i in xrange(len(v)):
            headers = default_header
            params = {}
            if "headers" in v[i]:
                headers = v[i]["headers"]
            if "params" in v[i]:
                params = v[i]["params"]

            with open(str.format("cmi_({}).py", count), "w") as f:
                if v[i]["method"].upper() == "GET":
                    template = get_template
                    template = template.replace(token_URL, "http://" + k + v[i]["endpoint"])
                    template = template.replace(token_GET_PARAMS, json.dumps(params))
                    template = template.replace(token_headers, json.dumps(headers))
                else:
                    template = post_template
                    template = template.replace(token_URL, "http://" + k + v[i]["endpoint"])
                    template = template.replace(token_POST_PARAMS, json.dumps(params))
                    template = template.replace(token_headers, json.dumps(headers))
                f.write(template)
            f.close()
            count += 1


def gen_dtr():
    data = get_json('dtr_results.json')
    if "results" not in data or len(data["results"]) < 1:
        print("No results for Directory Traversal")

    count = 1
    for k, v in data["results"].iteritems():
        for i in xrange(len(v)):
            headers = default_header
            params = {}
            if "headers" in v[i]:
                headers = v[i]["headers"]
            if "params" in v[i]:
                params = v[i]["params"]

            with open(str.format("dtr_({}).py", count), "w") as f:
                if v[i]["method"].upper() == "GET":
                    template = get_template
                    template = template.replace(token_URL, "http://" + k + v[i]["endpoint"])
                    template = template.replace(token_GET_PARAMS, json.dumps(params))
                    template = template.replace(token_headers, json.dumps(headers))
                else:
                    template = post_template
                    template = template.replace(token_URL, "http://" + k + v[i]["endpoint"])
                    template = template.replace(token_POST_PARAMS, json.dumps(params))
                    template = template.replace(token_headers, json.dumps(headers))
                f.write(template)
            f.close()
            count += 1


def gen_ore():
    data = get_json('ore_results.json')
    if "results" not in data or len(data["results"]) < 1:
        print("No results for Open Redirect")

    count = 1
    for k, v in data["results"].iteritems():
        for i in xrange(len(v)):
            headers = default_header
            params = {}
            if "headers" in v[i]:
                headers = v[i]["headers"]
            if "params" in v[i]:
                params = v[i]["params"]

            with open(str.format("ore_({}).py", count), "w") as f:
                if v[i]["method"].upper() == "GET":
                    template = get_template
                    template = template.replace(token_URL, "http://" + k + v[i]["endpoint"])
                    template = template.replace(token_GET_PARAMS, json.dumps(params))
                    template = template.replace(token_headers, json.dumps(headers))
                else:
                    template = post_template
                    template = template.replace(token_URL, "http://" + k + v[i]["endpoint"])
                    template = template.replace(token_POST_PARAMS, json.dumps(params))
                    template = template.replace(token_headers, json.dumps(headers))
                f.write(template)
            f.close()
            count += 1


def gen_ssc():
    data = get_json('ssc_results.json')
    if "results" not in data or len(data["results"]) < 1:
        print("No results for Server Side Code Injection")

    count = 1
    for k, v in data["results"].iteritems():
        for i in xrange(len(v)):
            headers = default_header
            params = {}
            if "headers" in v[i]:
                headers = v[i]["headers"]
            if "params" in v[i]:
                params = v[i]["params"]

            with open(str.format("ssc_({}).py", count), "w") as f:
                if v[i]["method"].upper() == "GET":
                    template = get_template
                    template = template.replace(token_URL, "http://" + k + v[i]["endpoint"])
                    template = template.replace(token_GET_PARAMS, json.dumps(params))
                    template = template.replace(token_headers, json.dumps(headers))
                else:
                    template = post_template
                    template = template.replace(token_URL, "http://" + k + v[i]["endpoint"])
                    template = template.replace(token_POST_PARAMS, json.dumps(params))
                    template = template.replace(token_headers, json.dumps(headers))
                f.write(template)
            f.close()
            count += 1


def gen_sql():
    data = get_json('sql_results.json')
    if "results" not in data or len(data["results"]) < 1:
        print("No results for SQL Injection")

    count = 1
    for k, v in data["results"].iteritems():
        # print(k,v)
        for i in xrange(len(v)):
            # for each endpoint
            headers = default_header
            params = {}
            if "headers" in v[i]:
                headers = v[i]["headers"]
            if "params" in v[i]:
                params = v[i]["params"]

            with open(str.format("sql_({}).py", count), "w") as f:
                if v[i]["method"].upper() == "GET":
                    template = get_template
                    template = template.replace(token_URL, "http://" + k + v[i]["endpoint"])
                    template = template.replace(token_GET_PARAMS, json.dumps(params))
                    template = template.replace(token_headers, json.dumps(headers))
                else:
                    template = post_template
                    template = template.replace(token_URL, "http://" + k + v[i]["endpoint"])
                    template = template.replace(token_POST_PARAMS, json.dumps(params))
                    template = template.replace(token_headers, json.dumps(headers))
                f.write(template)
            f.close()
            count+=1
            # if v[i]["method"].upper() == "POST":
            #     req = requests.post("http://" + k + v[i]["endpoint"], data=params, headers=headers, verify=False)
            # else:
            #     req = requests.get("http://" + k + v[i]["endpoint"], params=params, headers=headers, verify=False)
            #
            # with open(str.format("sql_{}({}).html", k, i+1), "w") as f:
            #     f.write(req.content)
            # f.close()


gen_cmi()
gen_dtr()
gen_ore()
gen_ssc()
gen_sql()
