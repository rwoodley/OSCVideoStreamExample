from flask import Flask, render_template, Response, send_from_directory
from osc2 import Osc2
import logging
# see line 398 of connectionpool.py:
logging.basicConfig(level=logging.DEBUG)

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
    thetav = Osc2()
    thetav.get_live_preview()
    return Response(gen(thetav),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
