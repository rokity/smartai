from telnetlib import Telnet
import time
import multiprocessing
import threading
from pathlib import Path
from datetime import date
from datetime import datetime
import pandas as pd
from DataManager import Data_Manager
host = "margot.di.unipi.it"
port = 8422
name= "AI-4"
match = "test"
TIME = 0.3

class ChatServer:
  channels = ["#GLOBAL","#CHAT","#LEAGUE","#LOGS","#DATA","#STREAM"]
  channels_joined=[]
  messages=[]
  log_file=""
  def __init__(self, _host=host , _port=port,_name=name, _match=match, _inter = ""):
    self.host = _host
    self.port = _port
    self.name= _name
    self.match = _match
    self.inter = _inter
    self.tn = Telnet(self.host, self.port)
    self.bootstrap_connection()


  def bootstrap_connection(self):
    self.tn.write(("NAME "+self.name).encode('ascii') + b"\n")
    self.join_all_channels()
    self.join_existing_channel(self.match)
    self.init_file_logs()
    threading.Thread(target=self.listen, args=()).start()
    

  def join_existing_channel(self,channel):
    self.tn.write(("JOIN " + channel).encode('ascii') + b"\n")
    self.channels_joined.append(channel)


  def leave_existing_channel(self,channel):
    self.tn.write(("LEAVE " + channel ).encode('ascii') + b"\n")

  def send_message_on_channel(self,channel,message):
    self.tn.write(("POST " + channel + " " + message).encode('ascii') + b"\n")

  def join_all_channels(self):
      for channel in self.channels:
        self.join_existing_channel(channel)

  def get_channels(self):
    return self.channels

  def is_connected(self):
      return False if self.tn.get_socket().fileno() == -1 else True

  def is_new_tournament(self,message):
      if(message["channel"]=="#LEAGUE" and message['user']=="@LeagueManager"):
        self.send_message_on_channel(message['message'],"join")
  
  def get_time_now(self):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

  def init_file_logs(self):
    today = date.today()
    current_time = self.get_time_now()
    self.log_file="data/logs/{}:{}:{}:{}.csv".format(today,current_time, self.name, self.match)
    df=pd.DataFrame(columns = ['channel', 'user','message','time'])
    df.to_csv(self.log_file,index=False)

  def save_message_to_file(self,message):
    df=pd.read_csv(self.log_file).to_dict('records')
    message['time']=self.get_time_now()    
    df.append(message)
    df=pd.DataFrame(df,columns=['channel', 'user','message','time'])
    df.to_csv(self.log_file,index=False)

  def listen(self):
    while(True):
      message=self.tn.read_very_eager().decode("utf-8") 
      if(len(message)>0):
        message=message.split(" ")
        message_text=" ".join(message[2:len(message)]).replace("\n", "")
        message={"channel":message[0],"user":message[1],"message":message_text}
        self.save_message_to_file(message)
        if Data_Manager.meaning(message_text):
          break
        if(message['channel'] in self.channels_joined):        
          self.check_message(message)        
        
        
          
  def check_message(self,message):
    self.is_new_tournament(message)
    return


