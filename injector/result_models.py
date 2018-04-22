import json


def json_default(obj):
    # to do conversion of obj and fields
    o = obj.__dict__.copy()
    o['class'] = o['name']
    del o['name']
    return o


# classes below may need additional methods of adding and converting payloads/url
class BaseOutput(object):
    def __init__(self, name):
        """
        object to convert to JSON output format required
        :param name: of exploit
        """
        self.name = name
        self.results = {}

    def add_payload(self, url, payload):
        if url in self.results:
            self.results.get(url).append(payload)
        else:
            self.results[url] = [payload]

    def get_json(self):
        # call to generate json output
        return json.dumps(self, default=json_default)


# Formats
class SQLInjection(BaseOutput):
    def __init__(self):
        super(SQLInjection, self).__init__("SQL Injection")


class SSCInjection(BaseOutput):
    def __init__(self):
        super(SSCInjection, self).__init__("Server Side Code Injection")


class DirectoryTraversal(BaseOutput):
    def __init__(self):
        super(DirectoryTraversal, self).__init__("Directory Traversal")


class OpenRedirect(BaseOutput):
    def __init__(self):
        super(OpenRedirect, self).__init__("Open Redirect")
