# WebServer
A simple web server using socket programming and HTTP protocols in Python3.
Initially, the webserver was made to handle one HTTP request at a time to implement HTTP status codes 200, 304, 400, 404 and 408.
Extended the webserver to a multithreaded version, capable of handling multiple requests simultaneously. Each TCP connection requested was handled in a separate thread.
