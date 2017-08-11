import inspect
import SimpleHTTPServer
import SocketServer
PORT = 4000

class Server_Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    map = dict()
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text")
        self.end_headers()
        path = self.path
        if path.startswith("/set?"):
            values = path[5:].split("=")
            key = values[0]
            value = values[1]
            Server_Handler.map[key]=value
        if path.startswith("/get?key="):
            key = path[9:]
            value = Server_Handler.map[key]
            self.wfile.write(value)

handler = Server_Handler
httpd = SocketServer.TCPServer(("", PORT), handler)

print "serving at port", PORT
httpd.serve_forever()