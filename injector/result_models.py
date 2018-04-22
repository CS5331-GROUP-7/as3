import json


def json_default(object):
    o = object.__dict__.copy()
    o['class'] = o['name']
    del o['name']
    return o


# classes below may need additional methods of adding and converting payloads/url
class BaseOutput(object):
    def __init__(self, name, url, payloads):
        """
        object to convert to JSON output format required
        :param url: of vulnerable
        :param payloads: endpoint to method to params
        """
        self.name = name
        self.results = {
            url: [payloads]
        }

    def add_payload(self, url, payload):
        if url in self.results:
            self.results.get(url).append(payload)
        else:
            self.results[url] = [payload]

    def get_json(self):
        return json.dumps(self, default=json_default)


# Formats
class SQLInjection(BaseOutput):
    def __init__(self, url, payloads):
        super(SQLInjection, self).__init__("SQL Injection", url, payloads)


class SSCInjection(BaseOutput):
    def __init__(self, url, payloads):
        super(SSCInjection, self).__init__("Server Side Code Injection", url, payloads)


class DirectoryTraversal(BaseOutput):
    def __init__(self, url, payloads):
        super(DirectoryTraversal, self).__init__("Directory Traversal", url, payloads)


class OpenRedirect(BaseOutput):
    def __init__(self, url, payloads):
        super(OpenRedirect, self).__init__("Open Redirect", url, payloads)
