import inspect
import SimpleHTTPServer
import SocketServer
PORT = 4000
import pickle


class Server_Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    filenames = [
        "tester1.pkl", "tester2.pkl", "tester3.pkl", "tester4.pkl",
        "tester5.pkl"
    ]

    @classmethod
    def init_dicts(cls):
        for filename in Server_Handler.filenames:
            pkl_file = open(filename, 'wb')
            my_dict = {}
            pickle.dump(my_dict, pkl_file)
            pkl_file.close()

    def writeFileName(self, filename, key, value):
        pkl_file = open(filename, 'r+')
        my_dict = pickle.load(pkl_file)
        my_dict[key] = value
        pkl_file.close()
        pkl_file = open(filename, 'wb')
        print "my dict is", my_dict
        pickle.dump(my_dict, pkl_file)
        pkl_file.close()

    def findKeyValue(self, filename, key):
        pkl_file = open(filename, 'rb')
        my_dict = pickle.load(pkl_file)
        print key, my_dict
        if key in my_dict:
            return my_dict[key]
        else:
            return "Key not found"
        pkl_file.close()

    def get_file_name(self, key):
        return Server_Handler.filenames[hash(key) %
                                        len(Server_Handler.filenames)]

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text")
        self.end_headers()
        path = self.path
        if path.startswith("/set?"):
            values = path[5:].split("=")
            key = values[0]
            value = values[1]
            filename = self.get_file_name(key)
            self.writeFileName(filename, key, value)
        if path.startswith("/get?key="):
            key = path[9:]
            filename = self.get_file_name(key)
            value = self.findKeyValue(filename, key)
            self.wfile.write(value)


handler = Server_Handler
handler.init_dicts()
httpd = SocketServer.TCPServer(("", PORT), handler)

print "serving at port", PORT
httpd.serve_forever()
