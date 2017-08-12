import web_server
import web_client
import os
import time
import signal

def test_web_client():
  new_pid = os.fork()
  if new_pid == 0:
    web_server.start()
  else:
    #waiting for the web server to start
    time.sleep(5)
    web_client.set_key_value("key3","a")
    value = web_client.get_key_value("key3")
    assert(value == "a") 
    web_client.set_key_value("key3","b")
    web_client.set_key_value("key2","a")
    value = web_client.get_key_value("key3")
    assert(value == "b") 
    value = web_client.get_key_value("key2")
    assert(value == "a") 
    os.kill(new_pid, signal.SIGKILL)
