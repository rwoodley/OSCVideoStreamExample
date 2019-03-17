import time


def stream_handler(thetav):
    # Video streaming generator function.
    # Handles MJPEG stream.

    bytes = ''
    a = -1
    frame_count = 0
    start_time = time.time()
    for block in thetav.response.iter_content(16384):
        # print("Read Block ")
        if bytes == '':
            bytes = block
        else:
            bytes += block

        # Search the current block of bytes for the jpq start and end
        if a == -1:
            a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')

        if a != - 1 and b != -1:
            # print("Writing frame %04d - Byte range : %d to %d" % (0, a, b))
            # Found a jpg, write to disk
            frame = bytes[a:b + 2]
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            # Reset the buffer to point to the next set of bytes
            bytes = bytes[b + 2:]
            frame_count += 1
            elapsed_time = time.time() - start_time
            print("Wrote frame: {}, fps={}".format(frame_count, 1 / elapsed_time))
            start_time = time.time()
            a = -1
