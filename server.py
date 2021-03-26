from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

from recomendation import Recommendations


class HttpServer:

    def __init__(self, hostName, serverPort, delta, force_reread_flag):

        self.recommendation = Recommendations(delta, force_reread_flag)
        self.hostName = hostName
        self.serverPort = serverPort

        def handler(*args):
            MyHandler(self.recommendation, *args)

        self.server = HTTPServer((hostName, serverPort), handler)

    def run(self):
        print("Server started http://%s:%s" % (self.hostName, self.serverPort))
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            pass
        self.server.server_close()
        print("Server stopped.")

    def set_recommendations_delta(self, delta):
        self.recommendation.set_delta(delta)


class MyHandler(BaseHTTPRequestHandler):

    def __init__(self, recommendation, *args):
        self.recommendation = recommendation
        BaseHTTPRequestHandler.__init__(self, *args)

    def do_GET(self):
        parsed_url = urlparse(self.path)
        if parsed_url.path == '/recommend':
            query = parse_qs(parsed_url.query)
            if 'sku' in query:
                res = self.recommendation.get_recommendations(query['sku'][0])

                if res:
                    self.send_response(200)
                    self.send_header("Content-type", 'application/json')
                    self.end_headers()
                    self.wfile.write(bytes(json.dumps({'recommendation': res}), 'ascii', errors='xmlcharrefreplace'))
                else:
                    self.send_response(404)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
        else:
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
