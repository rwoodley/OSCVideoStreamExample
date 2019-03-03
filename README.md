# OSCVideoStreamExample
A simple example of how to stream live video over HTTP from a camera implementing the OSC 2.0 API (like the Ricoh Theta V).

This is python 3, using the flask web server.

The main interest here (for me) is *wireless* streaming from the Theta V.

Steps:
1. Plug the Theta V into your laptop, turn it on, let it boot up. 
(The blue light will flash several times as it is booting, when boot is complete the blue light will stay one).
2. Unplug the theta. The wireless icon will start to flash on the theta.
3. Connect to the theta's network. Once connected the wireless icon will stop flashing and will remain on.
4. Then you can run this app to start streaming:

    python3 app.py
