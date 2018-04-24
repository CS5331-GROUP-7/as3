import json
from urlparse import urlparse

def json_default(obj):
    # to do conversion of obj and fields
    o = obj.__dict__.copy()
    o['class'] = o['name']
    del o['name']
    return o


# classes below may need additional methods of adding and converting payloads/url
class BaseOutputModel(object):
    def __init__(self, name):
        """
        object to convert to JSON output format required
        :param name: of exploit
        """
        self.name = name
        self.results = {}

    def add_payload(self, full_url, payload):
        url_comp = urlparse(full_url)
        url = url_comp.netloc
        endpoint = url_comp.path

        params = {}
        headers = {}
        if "header" in payload:
            for k in payload["header"]:
                if k.lower() == "referer" or k.lower() == "user-agent":
                    continue
                headers[k] = payload["header"][k]

        if "param" in payload:
            params = dict(payload["param"], **headers)
        else:
            params = headers
        # elif "param" in payload and "header" not in payload:
        #     params = payload["param"]
        # elif "param" not in payload and "header" in payload:
        #     params = payload["header"]

        out = {
            "endpoint": endpoint,
            "params": params,
            "method": payload["type"]
        }
        if url in self.results:
            self.results.get(url).append(out)
        else:
            self.results[url] = [out]

    def get_json(self):
        # call to generate json output
        return json.dumps(self, default=json_default, indent=4)


# Formats
class SQLInjectionModel(BaseOutputModel):
    def __init__(self):
        super(SQLInjectionModel, self).__init__("SQL Injection")


class SSCInjectionModel(BaseOutputModel):
    def __init__(self):
        super(SSCInjectionModel, self).__init__("Server Side Code Injection")


class DirectoryTraversalModel(BaseOutputModel):
    def __init__(self):
        super(DirectoryTraversalModel, self).__init__("Directory Traversal")


class OpenRedirectModel(BaseOutputModel):
    def __init__(self):
        super(OpenRedirectModel, self).__init__("Open Redirect")


class CommandInjectionModel(BaseOutputModel):
    def __init__(self):
        super(CommandInjectionModel, self).__init__("Command Injection")
