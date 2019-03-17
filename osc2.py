import json
from requests_wrapper import RequestsWrapper

class Osc2:
    # Uses Version 2 of OpenSphericalCamera API to get a live video stream.
    # https://developers.google.com/streetview/open-spherical-camera/

    def __init__(self, mode="local", host=None, port=None, theta_id=None, password=None):
        self.response = None
        self.requests_wrapper = RequestsWrapper(mode, host, port, theta_id, password)
        self.ip = host
        self.port = port

    def get_live_preview(self):
        url = self.get_url("commands/execute")
        body = json.dumps({"name": "camera.getLivePreview"})

        response = self.requests_wrapper.post(url, body, stream=True)
        if response is None:
            return False

        if response.status_code == 200:
            self.response = response
            return True
        else:
            osc_error(response)
            return False

    def get_url(self, url_request):
        osc_request = str("/osc/" + url_request)
        url_base = "http://%s:%s" % (self.ip, self.port)
        url = url_base + osc_request
        return url

    def info(self):
        url = self.get_url("info")
        req = self.requests_wrapper.get(url)
        if req is None:
            return None

        if req.status_code == 200:
            response = req.json()
        else:
            osc_error(req)
            response = None
        return response

    def state(self):
        return self.do_post("state")["state"]

    def get_option(self, option_name):
        body = json.dumps({"name": "camera.getOptions",
                           "parameters": {
                               "optionNames": [
                                   option_name]
                           }
                           })
        response = self.do_post("commands/execute", data=body)
        if response is not None:
            value = response["results"]["options"][option_name]
        else:
            value = None
        return value

    def set_option(self, option_name, option_value):
        body = json.dumps({"name": "camera.setOptions",
                           "parameters": {
                               "options": {
                                   option_name: option_value
                               }
                           }
                           })
        response = self.do_post("commands/execute", data=body)
        if response is not None:
            value = response["state"]
        else:
            value = None
        return value

    def do_post(self, command, data=None):
        url = self.get_url(command)
        req = self.requests_wrapper.post(url, data)
        if req is None:
            return None

        if req.status_code == 200:
            response = req.json()
            return response
        else:
            osc_error(req)
            return None

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
