import inspect
import SimpleHTTPServer
import SocketServer
PORT = 4000
import pickle

def findKeyValue(filename, key):
  fileobject = open(filename, "r")
  extracted_value = "Key not found"
  for line in fileobject:
     values = line.split("=")
     extracted_key = values[0]
     value = values[1]
     if key == extracted_key:
        extracted_value = value
  fileobject.close()
  return extracted_value

def init_dicts(filename):
    pkl_file = open(filename, 'wb')
    my_dict = {3:2}
    pickle.dump(my_dict, pkl_file)
    pkl_file.close()

def writeFileName(filename, key, value):
  fileobject = open(filename, "a")
  line = key + "=" + value + "\n"
  fileobject.write(line)
  fileobject.close()

def writeFileName2(filename, key, value):
  pkl_file = open(filename, 'rb')
  my_dict = pickle.load(pkl_file)
  my_dict[key] = value
  pkl_file.close()
  pkl_file = open(filename, 'wb')
  print "my dict is", my_dict
  pickle.dump(my_dict, pkl_file)
  pkl_file.close()
 
def findKeyValue2(filename, key):
  pkl_file = open(filename, 'rb')
  my_dict = pickle.load(pkl_file)
  print key, my_dict
  if key in my_dict:
    return my_dict[key]
  else:
    return "Key not found"
  pkl_file.close()

class Server_Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text")
        self.end_headers()
        path = self.path
        if path.startswith("/set?"):
            values = path[5:].split("=")
            key = values[0]
            value = values[1]
            writeFileName2("tester.pkl", key, value)
        if path.startswith("/get?key="):
            key = path[9:]
            value = findKeyValue2("tester.pkl", key)
            self.wfile.write(value)
init_dicts("tester.pkl")
handler = Server_Handler
httpd = SocketServer.TCPServer(("", PORT), handler)

print "serving at port", PORT
httpd.serve_forever()
