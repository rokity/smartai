from telnetlib import Telnet
import time
import multiprocessing


TIME = 0.3

class ChatServer:
  channels = ["#GLOBAL","#CHAT","#LEAGUE","#LOGS","#DATA","#STREAM"]
  messages=[]
  def __init__(self, _host, _port,_name):
    self.host = _host
    self.port = _port
    self.name= _name
    self.tn = Telnet(self.host, self.port)
    self.bootstrap_connection()


  def bootstrap_connection(self):
    self.tn.write(("NAME "+self.name).encode('ascii') + b"\n")

  def join_existing_channel(self,channel):
    self.tn.write(("JOIN " + channel).encode('ascii') + b"\n")


  def leave_existing_channel(self,channel):
    self.tn.write(("LEAVE " + channel ).encode('ascii') + b"\n")

  def send_message_on_channel(self,channel,message):
    self.tn.write(("POST " + channel + " " + message).encode('ascii') + b"\n")

  def get_channels(self):
    return self.channels

  def is_connected(self):
      return False if self.tn.get_socket().fileno() == -1 else True
  

      


