import json
import requests


class Osc2:
    # Uses Version 2 of OpenSphericalCamera API to get a live video stream.
    # https://developers.google.com/streetview/open-spherical-camera/

    def __init__(self, ip_base="192.168.1.1", http_port=80):
        self.response = None
        self._ip = ip_base
        self._http_port = http_port

    def get_live_preview(self):
        acquired = False

        url = self.get_url("commands/execute")
        body = json.dumps({"name": "camera.getLivePreview"})

        try:
            response = requests.post(url, data=body, headers={'Content-Type': 'application/json'}, stream=True)
        except Exception as e:
            print("HTTP Error: {}".format(repr(e)))
            return acquired

        if response.status_code == 200:
            self.response = response
            return True
        else:
            osc_error(response)
            return False

    def get_url(self, url_request):
        osc_request = str("/osc/" + url_request)
        url_base = "http://%s:%s" % (self._ip, self._http_port)
        url = url_base + osc_request
        return url


def osc_error(request):
    status = request.status_code

    try:
        error = request.json()

        print("OSC Error - HTTP Status : %s" % status)
        if 'error' in error:
            print("OSC Error - Code        : %s" % error['error']['code'])
            print("OSC Error - Message     : %s" % error['error']['message'])
        print("OSC Error - Name        : %s" % error['name'])
        print("OSC Error - State       : %s" % error['state'])
    except:
        print("OSC Error - HTTP Status : %s" % status)
