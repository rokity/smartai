# HOST = "margot.di.unipi.it"
# PORT=8421
# from telnetlib import Telnet
# tl=Telnet(host=HOST,port=PORT)
# tl.write("NEW ciccio".encode('ascii') + b"\n")
# print(tl.read_eager().decode('ascii'))


HOST = "margot.di.unipi.it"
PORT=8422


from ChatServer import ChatServer

cs=ChatServer(HOST,PORT,"test_riccardo")
_global=cs.get_channels()[0]
cs.join_existing_channel(_global)
cs.send_message_on_channel(_global,"test library")

received_message=[]