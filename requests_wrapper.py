import requests
from requests.auth import HTTPDigestAuth


class RequestsWrapper:
    def __init__(self, mode, ip_base, http_port, id, password):
        self.mode = mode
        self.theta_id = id
        self.theta_password = password
        self.ip = ip_base
        self.port = http_port

    def get(self, url):
        try:
            if self.mode == "local":
                return requests.get(url)
            else:
                return requests.get(
                    url,
                    auth=(HTTPDigestAuth(self.theta_id,
                                         self.theta_password)))
        except Exception as e:
            print("HTTP Error: {}".format(repr(e)))
            return None

    def post(self, url, body, stream=False):
        try:
            if self.mode == "local":
                return requests.post(
                    url,
                    stream=stream,
                    data=body,
                    headers={'Content-Type': 'application/json'})
            else:
                return requests.post(
                    url,
                    stream=stream,
                    data=body,
                    headers={'Content-Type': 'application/json'},
                    auth=(HTTPDigestAuth(self.theta_id,
                                         self.theta_password)))

        except Exception as e:
            print("HTTP Error: {}".format(repr(e)))
            return None
