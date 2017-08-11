import inspect
import SimpleHTTPServer
import SocketServer
PORT = 4000
import pickle


class Server_Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def init_dicts():
        for filename in filenames:
            pkl_file = open(filename, 'wb')
            my_dict = {}
            pickle.dump(my_dict, pkl_file)
            pkl_file.close()

    def writeFileName(filename, key, value):
        pkl_file = open(filename, 'r+')
        my_dict = pickle.load(pkl_file)
        my_dict[key] = value
        pkl_file.close()
        pkl_file = open(filename, 'wb')
        print "my dict is", my_dict
        pickle.dump(my_dict, pkl_file)
        pkl_file.close()

    def findKeyValue(filename, key):
        pkl_file = open(filename, 'rb')
        my_dict = pickle.load(pkl_file)
        print key, my_dict
        if key in my_dict:
            return my_dict[key]
        else:
            return "Key not found"
        pkl_file.close()

        def get_file_name(key):
            return filenames[hash(key) % len(filenames)]

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text")
        self.end_headers()
        path = self.path
        if path.startswith("/set?"):
            values = path[5:].split("=")
            key = values[0]
            value = values[1]
            filename = get_file_name(key)
            writeFileName(filename, key, value)
        if path.startswith("/get?key="):
            key = path[9:]
            filename = get_file_name(key)
            value = findKeyValue(filename, key)
            self.wfile.write(value)


filenames = [
    "tester1.pkl", "tester2.pkl", "tester3.pkl", "tester4.pkl", "tester5.pkl"
]
handler = Server_Handler
httpd = SocketServer.TCPServer(("", PORT), handler)

print "serving at port", PORT
httpd.serve_forever()
