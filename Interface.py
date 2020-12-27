import getpass
import telnetlib
import time
from variabili import var


TIME = var.TIME
class Interface:
	def __init__(self, host = "margot.di.unipi.it", port = 8421, nome=""):
		self.host = host
		self.port = port
		self.nome = nome
		self.tn = telnetlib.Telnet(self.host, self.port)
		time.sleep(0.6)

	def new_game(self, nome, form, size, typ = ""):
		self.nome = nome
		self.tn.write(("NEW "+self.nome + " " + form + size + typ).encode('ascii') + b"\n")
		time.sleep(0.6)
		risp = self.tn.read_some()
		return risp

	def join_game(self, player, nature, role): #info=""):
		#print(self.nome + " JOIN "+player+" "+ nature + " "+ role)
		self.tn.write((self.nome + " JOIN "+player+" "+ nature + " "+ role).encode('ascii') + b"\n") #+ " "+info
		time.sleep(0.6)
		risp = self.tn.read_some()
		return risp

	def start_game(self):
		self.tn.write((self.nome + " START").encode('ascii') + b"\n")
		time.sleep(TIME)
		risp = self.tn.read_some()
		return risp

	def leave_game(self, reason):
		self.tn.write((self.nome + " LEAVE "+ reason).encode('ascii') + b"\n")
		time.sleep(TIME)
		risp = self.tn.read_some()
		return risp

	def look(self):
		time.sleep(0.2)
		self.tn.write((self.nome + " LOOK").encode('ascii') + b"\n")
		time.sleep(TIME)
		risp = self.tn.read_until(("ENDOFMAP").encode('ascii'))
		c = str(risp)
		if c[2:4] == "OK":
			r = self.tn.read_until(("\n").encode('ascii'))
		#r = self.tn.read_until(("\n").encode('ascii'))
		return risp

	def move(self, direction):
		self.tn.write((self.nome + " MOVE "+ direction).encode('ascii') + b"\n")
		time.sleep(TIME)
		risp = self.tn.read_some()
		return risp

	def shoot(self, direction):
		self.tn.write((self.nome + " SHOOT "+ direction).encode('ascii') + b"\n")
		time.sleep(TIME)
		risp = self.tn.read_some()
		return risp
	
	def status(self):
		time.sleep(0.2)
		self.tn.write((self.nome + " STATUS").encode('ascii') + b"\n")
		time.sleep(TIME)
		risp = self.tn.read_until(("ENDOFSTATUS").encode('ascii'))
		#print(risp)
		c = str(risp)
		if c[2:4] == "OK":
			r = self.tn.read_until(("\n").encode('ascii'))
		#r = self.tn.read_until(("\n").encode('ascii'))
		return risp

	def accuse(self, player):
		self.tn.write((self.nome + " ACCUSE " + player).encode('ascii') + b"\n")
		time.sleep(TIME)
		risp = self.tn.read_some()
		return risp

	def nop(self):
		self.tn.write((self.nome + " NOP").encode('ascii') + b"\n")
		time.sleep(0.6)
		risp = self.tn.read_some()
		return risp



