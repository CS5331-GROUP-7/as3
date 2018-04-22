
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
        self.payloads = {}
        pass

    def check_login(self):
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
        pass

    def do_get(self):
        """
        GET without login
        :return:
        """

    def do_get_login(self):
        """
        GET with login
        :return:
        """

    def do_post(self):
        """
        POST without login
        :return:
        """

    def do_post_login(self):
        """
        POST with login
        :return:
        """