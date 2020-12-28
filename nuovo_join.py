from tensorforce.environments import Environment
import getpass
import telnetlib
from Interface import Interface
from DataManager import Data_Manager
from posBandiera import pos_bandiera
from stato_mappa import stato_mappa
from variabili import var	
import time
import numpy as np
import random
import re
import pickle
from ChatServer import ChatServer


#variabili globali e funzioni
host = "margot.di.unipi.it"
port = 8421
TIME = var.TIME  #150 ms per training


def get_state(mapp, bx, by, x, y, size, sizex, allies, enemies, t, l):     #0-1-2-3 posizione rispetto alla bandiera 4-5-6-7 se ci sono muri vicini 8-9-10-11 se ci sono nemici in linea 12 se siamo impostori
	stato = np.zeros(13)
	if t != l:
		stato[12] = 1
	if y > by:
		stato[0] = 1
	else:	
		stato[0] = 0
	if y < by:
		stato[1] = 1
	else:	
		stato[1] = 0
	if x < bx:
		stato[2] = 1
	else:
		stato[2] = 0
	if x > bx:
		stato[3] = 1
	else:
		stato[3] = 0
	if y == 0 or (mapp[y-1][x] == '#' or mapp[y-1][x] == '@' or mapp[y-1][x] == '!'):
		stato[4] = 0
	else: 
		stato[4] = 1
	if y == size - 1 or (mapp[y+1][x] == '#' or mapp[y+1][x] == '@' or mapp[y+1][x] == '!'):
		stato[5] = 0
	else: 
		stato[5] = 1
	if x == sizex - 1 or (mapp[y][x+1] == '#' or mapp[y][x+1] == '@' or mapp[y][x+1] == '!'):
		stato[6] = 0
	else: 
		stato[6] = 1
	if x == 0 or (mapp[y][x-1] == '#' or mapp[y][x-1] == '@' or mapp[y][x-1] == '!'):
		stato[7] = 0
	else: 
		stato[7] = 1

	stato[8] = 1
	stato[9] = 1
	stato[10] = 1
	stato[11] = 1
	if y != 0:
		for i in range(y-1, -1, -1):
			if mapp[i][x] == '#':
				break
			elif mapp[i][x] in allies:
				if stato[12] == 1:
					stato[8] = 0
				break
			elif mapp[i][x] in enemies:
				if stato[12] == 0:
					stato[8] = 0
				break
	if y != size-1:
		for i in range(y+1, size):
			if mapp[i][x] == '#':
				break
			elif mapp[i][x] in allies:
				if stato[12] == 1:
					stato[9] = 0
				break
			elif mapp[i][x] in enemies:
				if stato[12] == 0:
					stato[9] = 0
				break
	if x != size-1:
		for i in range(x+1, sizex):
			if mapp[y][i] == '#':
				break
			elif mapp[y][i] in allies:
				if stato[12] == 1:
					stato[10] = 0
				break
			elif mapp[y][i] in enemies:
				if stato[12] == 0:
					stato[10] = 0
				break
	if x != 0:
		for i in range(x-1, -1, -1):
			if mapp[y][i] == '#':
				break
			elif mapp[y][i] in allies:
				if stato[12] == 1:
					stato[11] = 0
				break
			elif mapp[y][i] in enemies:
				if stato[12] == 0:
					stato[11] = 0
				break
	
	return stato



class Env(Environment):
	def __init__(self, match, n, numero):
		self.inter = Interface(nome = match)
		self.n = n
		self.match = match
		self.numero = numero
		super().__init__()
		self.win = False
	def reset(self):
		self._timestep = 1000
		n = str(self.n)
		self.inter.nome = self.match + str(self.n)
		self.chat= ChatServer(_name="AI-4-" + str(numero))
		self.chat.send_message_on_channel(channel=var.torneo,message="join")
		ris = self.inter.join_game("AI-4-" + str(self.numero), "AI", "nn")
		while str(ris)[2:7] == "ERROR":
			time.sleep(0.3)
			ris = self.inter.join_game("AI-4-" + str(self.numero), "AI", "nn")
			print(ris)
		ris = self.inter.status()
		while Data_Manager.check(str(ris)) == "ERROR":
			print(str(ris))
			time.sleep(0.4)
			ris = self.inter.nop()
			ris = self.inter.status()
		self.stato, self.size, self.sizex, self.symbol, self.name, self.team, self.loyalty, self.x, self.y = Data_Manager.status_iniziale(str(ris))		#name è superfluo, lo sappiamo già
		self.x = int(self.x)
		self.y = int(self.y)		
		self.morto = False
		while self.stato != "ACTIVE":
			if self.stato == "ERROR":
				time.sleep(0.4)
				ris = self.inter.nop()
			ris = self.inter.status()
			time.sleep(0.3)
			self.stato = Data_Manager.status_wait(str(ris))
			print(self.stato)

		self.stato, self.energy, self.score, self.st, self.allies, self.enemies = Data_Manager.status(str(ris), self.name, self.symbol)
		ris = self.inter.look()
		while Data_Manager.check(str(ris)) == "ERROR":
			print(str(ris))
			time.sleep(0.4)
			ris = self.inter.nop()
			#time.sleep(1)
			ris = self.inter.look()
		self.mapp = Data_Manager.mappa(str(ris), self.size) 
		self.bx, self.by = pos_bandiera(self.mapp, self.symbol, int(self.size), self.sizex)
		self.state = get_state(self.mapp, self.bx, self.by, self.x, self.y, self.size, self.sizex, self.allies, self.enemies, self.team, self.loyalty)
		self.mappa_stato = stato_mappa(self.mapp, self.symbol, int(self.size), self.sizex)

		self.kill = 0
		self.ciclo = True	
		return self.state


	def states(self):
		return dict(type = 'float', shape = (13,), min_value=0.0, max_value=1.0)
	def actions(self):
		return dict(type = 'int', num_values = 10)
	
	def mossa_giusta(self):
		self.mappa_stato = stato_mappa(self.mapp, self.symbol, int(self.size), self.sizex)
		self.pos = self.mappa_stato[self.y][self.x]
		self.pos = int(self.pos)
		if self.energy > 50:
			self.state = get_state(self.mapp, self.bx, self.by, self.x, self.y, self.size, self.sizex, self.allies, self.enemies, self.team, self.loyalty)
			if self.state[8] == 0:
				return 5
			if self.state[9] == 0:
				return 6
			if self.state[10] == 0:
				return 7 
			if self.state[11] == 0:
				return 8
		if self.ciclo:
			self.ciclo = False
			if self.y != 0 and self.pos < int(self.mappa_stato[self.y-1][self.x]):
				print(self.mappa_stato[self.y-1][self.x])
				return 0
			elif self.y != self.size - 1 and self.pos < int(self.mappa_stato[self.y+1][self.x]):
				print(self.mappa_stato[self.y+1][self.x])			
				return 1
			elif self.x != self.sizex - 1 and self.pos < int(self.mappa_stato[self.y][self.x+1]):
				print(self.mappa_stato[self.y][self.x+1])
				return 2
			else: 
				print(self.mappa_stato[self.y][self.x-1])
				return 3
		else:
			self.ciclo = True
			if self.x != self.sizex - 1 and self.pos < int(self.mappa_stato[self.y][self.x+1]):
				print(self.mappa_stato[self.y][self.x+1])
				return 2
			elif self.x != 0 and self.pos < int(self.mappa_stato[self.y][self.x-1]):
				print(self.mappa_stato[self.y][self.x-1])
				return 3
			elif self.y != 0 and self.pos < int(self.mappa_stato[self.y-1][self.x]):
				print(self.mappa_stato[self.y-1][self.x])
				return 0
			else:
				print(self.mappa_stato[self.y+1][self.x])			
				return 1

	def execute(self, actions):
		if actions == 0:
			print("mi muovo a nord")
			ris = self.inter.move("N")
			#print(ris)
			ris = Data_Manager.movimento(str(ris))
			print(ris)
			if ris == 'OK':
				self.y = self.y-1
				self.state = get_state(self.mapp, self.bx, self.by, self.x, self.y, self.size, self.sizex, self.allies, self.enemies, self.team, self.loyalty)
				if self.state[0] == 1:
					return self.state, 5, False
				else:
					return self.state, -10, False

			if ris == 'BLOCKED':
				if self.y!= 0 and self.mappa_stato[self.y-1][self.x] == 300 and self.state[12] == 0:	
					self.win = True
					return self.state, 500, True
				else:
					return self.state, -100, False

			if ris == 'ERROR':
				time.sleep(0.4)
				ris = self.inter.nop()
				#time.sleep(1) #qua crasha alla mossa dopo
				return self.state,-1, False
			#recharge

			#move object
		if actions == 1:	
			print("mi muovo a sud")
			ris = self.inter.move("S")
			#print(ris)
			ris = Data_Manager.movimento(str(ris)) 
			print(ris)
			if ris == 'OK':
				self.y = self.y+1	
				self.state = get_state(self.mapp, self.bx, self.by, self.x, self.y, self.size, self.sizex, self.allies, self.enemies, self.team, self.loyalty)
				if self.state[1] == 1 and self.state[12] == 0:
					return self.state, 5, False
				elif self.state[12] == 0:
					return self.state, -10, False
				else:
					return self.state, 0, False

			if ris == 'BLOCKED':
				if self.y != self.size - 1 and self.mappa_stato[self.y+1][self.x] == 300 and self.state[12] == 0:
					self.win = True
					return self.state, 500, True
				else:
					return self.state, -100, False

			if ris == 'ERROR':
				time.sleep(0.4)
				ris = self.inter.nop()
				print(ris)
				#time.sleep(1)
				return self.state,-1, False

		if actions == 2:
			print("mi muovo a est")
			ris = self.inter.move("E")
			#print(ris)
			ris = Data_Manager.movimento(str(ris))
			print(ris)
			if ris == 'OK':
				self.x = self.x+1
				self.state = get_state(self.mapp, self.bx, self.by, self.x, self.y, self.size, self.sizex, self.allies, self.enemies, self.team, self.loyalty)
				if self.state[2] == 1 and self.state[12] == 0:
					return self.state, 5, False
				elif self.state[12] == 0:
					return self.state, -10, False
				else:
					return self.state, 0, False

			if ris == 'BLOCKED':
				if self.x != self.sizex - 1 and self.mappa_stato[self.y][self.x+1] == 300 and self.state[12] == 0:
					self.win = True
					return self.state, 500, True
				else:
					return self.state, -100, False

			if ris == 'ERROR':
				time.sleep(0.4)
				ris = self.inter.nop()		
				#time.sleep(1)
				print(ris)
				return self.state,-1, False

		if actions == 3:
			print("mi muovo a ovest")
			ris = self.inter.move("W")
			#print(ris)
			ris = Data_Manager.movimento(str(ris))
			print(ris)
			if ris == 'OK':
				self.x = self.x-1
				self.state = get_state(self.mapp, self.bx, self.by, self.x, self.y, self.size, self.sizex, self.allies, self.enemies, self.team, self.loyalty)
				if self.state[2] == 1 and self.state[12] == 0:
					return self.state, 5, False
				elif self.state[12] == 0:
					return self.state, -10, False
				else:
					return self.state, 0, False


			if ris == 'BLOCKED':
				if self.x != 0 and self.mappa_stato[self.y][self.x-1] == 300 and self.state[12] == 0:
					self.win = True
					return self.state, 500, True
				else:
					return self.state, -100, False

			if ris == 'ERROR':
				time.sleep(0.4)
				ris = self.inter.nop()
				print(ris)
				#time.sleep(1)
				return self.state,-1, False

		if actions == 4:
			print("guardo")    #da rifare
			ris = self.inter.look()
			while Data_Manager.check(str(ris)) == "ERROR":
				print(str(ris))	
				time.sleep(0.4)
				ris = self.inter.nop()
				print(ris)
				#time.sleep(1)			
				ris = self.inter.look()
			self.mapp = Data_Manager.mappa(str(ris), self.size)

			self.state = get_state(self.mapp, self.bx, self.by, self.x, self.y, self.size, self.sizex, self.allies, self.enemies, self.team, self.loyalty)
			return self.state, -5, False

		if actions == 5:
			if self.energy > 0:
				print("sparo a nord")
				ris = self.inter.shoot("N")
				ris = Data_Manager.colpito(str(ris))
				print(ris)
				if ris == '#':
					return self.state, -20, False
				if ris == '&':
					return self.state, -20, False
				if ris == 'x' or ris == 'X':
					return self.state, -20, False
				if ris in self.allies:
					self.allies.remove(ris)
					if self.state[12] == 0:
						return self.state, -50, False
					else:
						self.kill = self.kill + 1
						return self.state, 100, False
				if ris in self.enemies:
					self.enemies.remove(ris) 
					if self.state[12] == 0:
						self.kill = self.kill + 1
						return self.state, 100, False
					else:
						return self.state, -50, False
				if ris == '?':
					 return self.state, -20, False
				if ris == '.':
					 return self.state, -20, False
				if ris == '@':
					 return self.state, -20, False
				if ris == '~':
					 return self.state, -20, False
				if ris == '!':
					 return self.state, -20, False
				if ris == '$' or ris == 'x' or ris == 'X':
					 return self.state, -20, False
				if ris == "not shoot":
					return self.state, -20, False
				if ris == 'ERROR':
					time.sleep(0.4)
					ris = self.inter.nop()
					print(ris)
					#time.sleep(1)
					return self.state,-1, False
			else:
				return self.state, -20, False

		if actions == 6:
			if self.energy > 0: 
				print("sparo a sud")
				ris = self.inter.shoot("S")
				ris = Data_Manager.colpito(str(ris))
				print(ris)
				if ris == '#':
					return self.state, -20, False
				if ris == '&':
					return self.state, -20, False
				if ris == 'x' or ris == 'X':
					return self.state, -20, False
				if ris in self.allies:
					self.allies.remove(ris)
					if self.state[12] == 0:
						return self.state, -50, False
					else:
						self.kill = self.kill + 1
						return self.state, 100, False
				if ris in self.enemies:
					self.enemies.remove(ris) 
					if self.state[12] == 0:
						self.kill = self.kill + 1
						return self.state, 100, False
					else:
						return self.state, -50, False
				if ris == '?':
					 return self.state, -20, False
				if ris == '.':
					 return self.state, -20, False
				if ris == '@':
					 return self.state, -20, False
				if ris == '~':
					 return self.state, -20, False
				if ris == '!':
					 return self.state, -20, False
				if ris == '$' or ris == 'x' or ris == 'X':
					 return self.state, -20, False
				if ris == "not shoot":
					return self.state, -20, False
				if ris == 'ERROR':
					time.sleep(0.4)
					ris = self.inter.nop()
					print(ris)
					#time.sleep(1)
					return self.state,-1, False
			else:
				return self.state, -20, False

		if actions == 7:
			if self.energy > 0:
				print("sparo a est")
				ris = self.inter.shoot("E")
				ris = Data_Manager.colpito(str(ris))
				print(ris)
				if ris == '#':
					return self.state, -20, False
				if ris == '&':
					return self.state, -20, False
				if ris == 'x' or ris == 'X':
					return self.state, -20, False
				if ris in self.allies:
					self.allies.remove(ris)
					if self.state[12] == 0:
						return self.state, -50, False
					else:
						self.kill = self.kill + 1
						return self.state, 100, False
				if ris in self.enemies:
					self.enemies.remove(ris) 
					if self.state[12] == 0:
						self.kill = self.kill + 1
						return self.state, 100, False
					else:
						return self.state, -50, False
				if ris == '?':
					 return self.state, -20, False
				if ris == '.':
					 return self.state, -20, False
				if ris == '@':
					 return self.state, -20, False
				if ris == '~':
					 return self.state, -20, False
				if ris == '!':
					 return self.state, -20, False
				if ris == '$' or ris == 'x' or ris == 'X':
					 return self.state, -20, False
				if ris == "not shoot":
					return self.state, -20, False
				if ris == 'ERROR':
					time.sleep(0.4)
					ris = self.inter.nop()
					print(ris)
					#time.sleep(1)
					return self.state,-1, False
			else:
				return self.state, -20, False

		if actions == 8:
			if self.energy > 0:
				print("sparo a ovest")
				ris = self.inter.shoot("W")
				ris = Data_Manager.colpito(str(ris))
				print(ris)
				if ris == '#':
					return self.state, -20, False
				if ris == '&':
					return self.state, -20, False
				if ris == 'x' or ris == 'X':
					return self.state, -20, False
				if ris in self.allies:
					self.allies.remove(ris)
					if self.state[12] == 0:
						return self.state, -50, False
					else:
						self.kill = self.kill + 1
						return self.state, 100, False
				if ris in self.enemies:
					self.enemies.remove(ris) 
					if self.state[12] == 0:
						self.kill = self.kill + 1
						return self.state, 100, False
					else:
						return self.state, -50, False
					return self.state, 100, False
				if ris == '?':
					 return self.state, -20, False
				if ris == '.':
					 return self.state, -20, False
				if ris == '@':
					 return self.state, -20, False
				if ris == '~':
					 return self.state, -20, False
				if ris == '!':
					 return self.state, -20, False
				if ris == '$' or ris == 'x' or ris == 'X':
					 return self.state, -20, False
				if ris == "not shoot":
					return self.state, -20, False
				if ris == 'ERROR':
					time.sleep(0.4)
					ris = self.inter.nop()
					print(ris)
					#time.sleep(1)
					return self.state,-1, False
			else:
				return self.state, -20, False
			

		if actions == 9:
			print("stato")     #valutare
			ris = self.inter.status()
			while Data_Manager.check(str(ris)) == "ERROR":
				print(str(ris))
				time.sleep(0.4)
				ris = self.inter.nop()
				print(ris)				
				ris = self.inter.status()

			self.stato, self.energy, self.score, self.st, self.allies, self.enemies = Data_Manager.status(str(ris), self.name, self.symbol)
			print(self.stato)
			print(self.energy)
			print(self.score)
			print(self.st)
			print(self.allies)
			print(self.enemies)
			if self.stato == "FINISHED":
				if self.st == "ACTIVE":
					return self.state, 100, True
				else:
					return self.state, 0, True
			if self.st == "ACTIVE":
				return self.state, -5, False		
			else:
				self.morto = True
				return self.state, -50, False
	def close(self):
		super().close()

