##############################################################
#     _     _       _           _      _         _   
#    | |_  | |__   (_)  _ __   | | __ / |  ___  | |_ 
#    | __| | '_ \  | | | '_ \  | |/ / | | / __| | __|
#    | |_  | | | | | | | | | | |   <  | | \__ \ | |_ 
#     \__| |_| |_| |_| |_| |_| |_|\_\ |_| |___/  \__|
#                                       my@think1st.app
#
##############################################################
from http.server import BaseHTTPRequestHandler

class Think1stBaseWebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))