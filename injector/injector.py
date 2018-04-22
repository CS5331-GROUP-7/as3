import json

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
            self.payloads = json.load(f)

        # get login info?

        pass

    def is_login_required(self, payload):
        """
        Checks if login is required
        :return:
        """
        pass

    def inject(self):
        """
        Start injecting payloads
        :return:
        """
        # store intermediates

        for p in self.payloads:
            # need to verify if successful
            if self.is_login_required(p):
                if p.type.upper() == "GET":
                    self.do_get_login()
                else:
                    self.do_post_login()
            else:
                if p.type.upper() == "GET":
                    self.do_get()
                else:
                    self.do_post()

        # process intermediates, convert to output format
        # write output

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

    def do_post(self):
        """
        POST without login
        :return:
        """
        pass

    def do_post_login(self):
        """
        POST with login
        :return:
        """
        pass
