# OSCVideoStreamExample

A simple example of how to stream live video over HTTP from a camera implementing the OSC 2.0 API (like the Ricoh Theta V). OSC is Google's [Open Spherical Camera](https://developers.google.com/streetview/open-spherical-camera/) API.

The main interest here (for me) is *wireless* streaming from the Theta V. The OSC API implements streaming using the [Motion JPEG](https://en.wikipedia.org/wiki/Motion_JPEG) video format.  

Currently streaming uses the livePreview format, which is quite limited as to framerate. See here: https://developers.theta360.com/en/docs/v2.1/api_reference/options/preview_format.html

This is python 3, using the flask web server. 

#### Python packages required:
flask
requests

#### Connecting

Turn on the Theta V. Do not have it plugged in via USB to a computer, 
otherwise the wireless icon won't come on.
The blue light will flash several times as it is booting. When boot is complete 
the blue light will stay one.  The blue wireless icon will then start to flash on the theta.

You can connect wirelessly to the theta one of 2 ways:

Mode 1. By directly connecting your laptop to the Theta's own wireless network. Once connected the wireless icon will stop flashing and will remain on.

Mode 2. By having the theta connect to your wireless router. 
You will need the wireless plug-in to do this. 
See instructions here: https://gist.github.com/rwoodley/3715efa2d0ce8ed813b349f4f3745a1e

If you are in Mode 1, the wireless icon on the Theta will be blue. In Mode 2, it will be green.


#### To Run:

        workon cv           # or whatever command invokes your environment.
        python3 server.py <options (see below)>

Once it is up, you can navigate to http://localhost:5000/public/index.html to see some 
links for browsing camera state and viewing the stream.

The video feed is embedded in the web page via this tag:

        <img src="/video_feed">


So, what are the `<options>` mentioned above? It all depends on which of
the 2 possible ways you're connecting to the theta:

##### Mode 1: You are connecting to Theta's own network

If there are no command-line options, the program assumes that you
are connecting directly to the Theta's own network, in which case it needs no further 
information. It connects to the default ip: 192.168.1.1:80.
Example:

    python3 server.py 
    

##### Mode 2: The Theta is connected to your wireless router
In this case, more information is needed. You 
MUST specify all of the following options:
````
-r, --router          connect via wireless router
-o HOST, --host HOST  Host name or ip of camera.
-p PORT, --port PORT  port of camera.
-i ID, --id ID        id of camera, eg: THETAYL00103139.
--pwd PASSWORD        password of camera, eg: 00103139
````
    
Example:

    python3 server.py -r -o 192.168.0.101 -p 80 --id THETAYL00103139 --pwd 00103139
    
