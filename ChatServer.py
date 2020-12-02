from telnetlib import Telnet
import time
import multiprocessing
import threading


TIME = 0.3

class ChatServer:
  channels = ["#GLOBAL","#CHAT","#LEAGUE","#LOGS","#DATA","#STREAM"]
  channels_joined=[]
  messages=[]
  def __init__(self, _host, _port,_name):
    self.host = _host
    self.port = _port
    self.name= _name
    self.tn = Telnet(self.host, self.port)
    self.bootstrap_connection()


  def bootstrap_connection(self):
    self.tn.write(("NAME "+self.name).encode('ascii') + b"\n")
    threading.Thread(target=self.listen, args=()).start()
    self.join_existing_channel("#LEAGUE")

  def join_existing_channel(self,channel):
    self.tn.write(("JOIN " + channel).encode('ascii') + b"\n")
    self.channels_joined.append(channel)


  def leave_existing_channel(self,channel):
    self.tn.write(("LEAVE " + channel ).encode('ascii') + b"\n")

  def send_message_on_channel(self,channel,message):
    self.tn.write(("POST " + channel + " " + message).encode('ascii') + b"\n")

  def get_channels(self):
    return self.channels

  def is_connected(self):
      return False if self.tn.get_socket().fileno() == -1 else True

  def is_new_tournament(self,message):
      if(message["channel"]=="#LEAGUE" and message['user']=="@LeagueManager"):
        self.send_message_on_channel(message['message'],f"join")

  def listen(self):
    while(True):
      message=self.tn.read_very_eager().decode("utf-8") 
      if(len(message)>0):
        message=message.split(" ")
        if(message[0] in self.channels_joined):
          message_text=" ".join(message[2:len(message)]).replace("\n", "")
          message={"channel":message[0],"user":message[1],"message":message_text}
          self.messages.append(message)
          self.check_message(message)
          
  def check_message(self,message):
    self.is_new_tournament(message)
    return


  

      


