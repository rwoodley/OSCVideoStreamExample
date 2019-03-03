# OSCVideoStreamExample
A simple example of how to stream live video over HTTP from a camera implementing the OSC 2.0 API (like the Ricoh Theta V). OSC is Google's [Open Spherical Camera](https://developers.google.com/streetview/open-spherical-camera/) API.

The main interest here (for me) is *wireless* streaming from the Theta V. The OSC API implements streaming using the [Motion JPEG](https://en.wikipedia.org/wiki/Motion_JPEG) video format.

This is python 3, using the flask web server. 

Steps:
1. Turn on the Theta V. Do not have it plugged in via USB to a computer, otherwise the wireless icon won't come on.
The blue light will flash several times as it is booting, when boot is complete the blue light will stay one.  The wireless icon will start to flash on the theta.
2. Connect your laptop to the theta's network wirelessly. Once connected the wireless icon will stop flashing and will remain on.
3. Then you can run this app to start streaming:
````
    python3 app.py
````
4. You can embed the video feed in a web page like this:
````
    <img src="/video_feed">
````

