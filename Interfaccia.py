import getpass
import telnetlib
from Ese import Interface
import time


HOST = "margot.di.unipi.it"
PORT = 8421


inter = Interface()
r = inter.newgame("PROVA1")
time.sleep(1)
r = inter.join_game("a", "U", "no")
time.sleep(1)
r = inter.start_game()
time.sleep(1)
r = inter.look()

