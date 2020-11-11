import getpass
import telnetlib


class Interface:
	def __init__(self, host = "margot.di.unipi.it", port = 8421):
		self.host = host
		self.port = port
		self.tn = telnetlib.Telnet(self.host, self.port)

	def new_game(self, nome):
		self.nome = nome
		self.tn.write(("NEW "+self.nome).encode('ascii') + b"\n")
		risp = self.tn.read_some()
		print(risp)
		return risp

	def join_game(self, player, nature, role, info=""):
		self.tn.write((self.nome + " JOIN "+player+" "+ nature + " "+ role + " "+info).encode('ascii') + b"\n")
		risp = self.tn.read_some()
		print(risp)
		return risp

	def start_game(self):
		self.tn.write((self.nome + " START").encode('ascii') + b"\n")
		risp = self.tn.read_some()
		print(risp)
		return risp

	def leave_game(self, reason):
		self.tn.write((self.nome + " LEAVE "+ reason).encode('ascii') + b"\n")
		risp = self.tn.readsome()
		print(risp)
		return risp

	def look(self):
		self.tn.write((self.nome + " LOOK").encode('ascii') + b"\n")
		risp = self.tn.read_some()
		print(risp)
		return risp

	def move(self, direction):
		self.tn.write((self.nome + " MOVE "+ direction).encode('ascii') + b"\n")
		risp = self.tn.read_some()
		print(risp)
		return risp

	def shoot(self, direction):
		self.tn.write((self.nome + " SHOOt "+ direction).encode('ascii') + b"\n")
		risp = self.tn.read_some()
		print(risp)
		return risp
	
	def status(self):
		self.tn.write((self.nome + " STATUS").encode('ascii') + b"\n")
		risp = self.tn.read_some()
		print(risp)
		return risp

	def accuse(self, player):
		self.tn.write((self.nome + " ACCUSE " + player).encode('ascii') + b"\n")
		risp = self.tn.read_some()
		print(risp)
		return risp

	def nop(self):
		self.tn.write((self.nome + " NOP").encode('ascii') + b"\n")
		risp = self.tn.read_some()
		print(risp)
		return risp



