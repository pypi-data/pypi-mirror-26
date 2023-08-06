Control Your Way Python Library
===============================

This project contains the library files Python V2.7 and V3. For examples on how to use this library please check out our other repositories on https://github.com/controlyourway.

The latest library uses WebSocket for communication. This means websocket client needs to be installed for it to work. Please use the following command to install websocket client:
pip install websocket-client

The library documentation can be found at:
https://www.controlyourway.com/Resources/PythonLibraryHelp

V1.0.0
- First release

V1.1.0
- If websocket times out and the websocket close command does not wake up the websocket thread then the program hangs. Add a timeout for restarting a new websocket thread.

V1.2.1
- Get package working properly to install correctly after uploading to PyPI