import json


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

    def add_payload(self, url, payload):
        if url in self.results:
            self.results.get(url).append(payload)
        else:
            self.results[url] = [payload]

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
