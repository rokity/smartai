# HOST = "margot.di.unipi.it"
# PORT=8421
# from telnetlib import Telnet
# tl=Telnet(host=HOST,port=PORT)
# tl.write("NEW ciccio".encode('ascii') + b"\n")
# print(tl.read_eager().decode('ascii'))


HOST = "margo.di.unipi.it"
PORT=8421


from Interface import Interface

tl=Interface(HOST,PORT)
print(tl)
