from flask import Flask, render_template, Response, send_from_directory, jsonify, make_response
from json import dumps
from osc2 import Osc2

import logging
# see line 398 of connectionpool.py:
logging.basicConfig(level=logging.DEBUG)

thetav = None

app = Flask(__name__, static_url_path='/public', static_folder='static')

def gen(thetav):
    bytes = ''
    a = -1
    # Video streaming generator function.
    # Handles MJPEG stream.
    for block in thetav.response.iter_content(16384):
        print("Read Block ")
        if bytes == '':
            bytes = block
        else:
            bytes += block

        # Search the current block of bytes for the jpq start and end
        if a == -1:
            a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')

        if a != - 1 and b != -1:
            print("Writing frame %04d - Byte range : %d to %d" % (0, a, b))
            # Found a jpg, write to disk
            frame = bytes[a:b + 2]
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            # Reset the buffer to point to the next set of bytes
            bytes = bytes[b + 2:]
            print("Wrote frame.")
            a = -1



@app.route('/video_feed')
def video_feed():
    thetav.get_live_preview()
    return Response(gen(thetav),
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

def pretty_json(json):
    response = make_response(dumps(json, indent=4, sort_keys=True))
    response.headers['Content-Type'] = 'application/json;'
    response.headers['mimetype'] = 'application/json'
    return response

if __name__ == '__main__':
    thetav = Osc2()
    app.run(host='0.0.0.0', threaded=True)
