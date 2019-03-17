from flask import Flask, Response, make_response
from json import dumps
from osc2 import Osc2
from video_stream_handler import stream_handler
import logging

# see line 398 of connectionpool.py:
logging.basicConfig(level=logging.DEBUG)

thetav = None

app = Flask(__name__, static_url_path='/public', static_folder='static')


@app.route('/video_feed')
def video_feed():
    thetav.get_live_preview()
    return Response(stream_handler(thetav),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/state')
def state():
    return pretty_json(thetav.state())


@app.route('/info')
def info():
    return pretty_json(thetav.info())


@app.route('/getOption/<option_string>')
def get_option(option_string):
    return pretty_json(thetav.get_option(option_string))


@app.route('/setOption/<option_string>/<option_value>')
def set_option(option_string, option_value):
    if option_string == "previewFormat":
        if option_value == "320x640":
            option_value = {"width": 640, "height": 320, "framerate": 8}
        elif option_value == "512x1024":
            option_value = {"width": 1024, "height": 512, "framerate": 30}
    return pretty_json(thetav.set_option(option_string, option_value))


def pretty_json(json):
    response = make_response(dumps(json, indent=4, sort_keys=True))
    response.headers['Content-Type'] = 'application/json;'
    response.headers['mimetype'] = 'application/json'
    return response


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--router", help="connect via wireless router",
                        action="store_true")
    parser.add_argument("-o", "--host", action="store", dest="host",
                        help="Host name or ip of camera.")
    parser.add_argument("-p", "--port", action="store", dest="port",
                        help="port of camera.")
    parser.add_argument("-i", "--id", action="store", dest="id",
                        help="id of camera, eg: THETAYL00103139.")
    parser.add_argument("--pwd", action="store", dest="password",
                        help="password of camera, eg: 00103139")
    args = parser.parse_args()
    if args.router:
        print("Connecting via router/ip.")
        mode="router"
        host = args.host
        port = args.port
        theta_id = args.id
        password = args.password
    else:
        print("Connecting via local theta network.")
        if args.host is not None or args.port is not None or args.id is not None or args.password is not None:
            print("To run in local mode, do not specify any arguments.")
            exit(1)
        mode="local"
        host = "192.168.1.1"
        port = 80
        theta_id = None
        password = None

    print("host: {}".format(host))
    print("port: {}".format(port))
    print("id: {}".format(theta_id))
    print("pwd: {}".format(password))

    thetav = Osc2(mode=mode, host=host, port=port, theta_id=theta_id, password=password)
    app.run(host='0.0.0.0', threaded=True)
