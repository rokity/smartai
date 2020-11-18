from telnetlib import Telnet
import time
import multiprocessing


TIME = 0.3

class ChatServer:
  channels = ["#GLOBAL","#CHAT","#LEAGUE","#LOGS","#DATA","#STREAM"]
  def __init__(self, _host, _port,_name):
    self.host = _host
    self.port = _port
    self.name= _name
    self.tn = Telnet(self.host, self.port)
    self.bootstrap_connection()
    n_threads = multiprocessing.cpu_count()
    print(n_threads)
    self.pool = multiprocessing.Pool(processes=n_threads)
    self.pool_results = multiprocessing.Manager().list()

  def bootstrap_connection(self):
    self.tn.write(("NAME "+self.name).encode('ascii') + b"\n")

  def join_existing_channel(self,channel):
    self.tn.write(("JOIN " + channel).encode('ascii') + b"\n")
    self.pool.apply_async(func=run,args=(self,channel))

  def leave_existing_channel(self,channel):
    self.tn.write(("LEAVE " + channel ).encode('ascii') + b"\n")

  def send_message_on_channel(self,channel,message):
    self.tn.write(("POST " + channel + " " + message).encode('ascii') + b"\n")

  def get_channels(self):
    return self.channels

  def is_connected(self):
      return False if self.tn.get_socket().fileno() == -1 else True
  
  def listen(self,channel):
    while(True):
      msg=self.tn.read_all()
      print(msg)
      


