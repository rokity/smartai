import getpass
import telnetlib
from Interface import Interface
from DataManager import Data_Manager
from posBandiera import pos_bandiera
from stato_mappa import stato_mappa	
import time
import numpy as np
import random
import re
import pickle

host = "margot.di.unipi.it"
port = 8421
TIME = 0.6    #150 ms per training

class env:
	def __init__(self, match):
		self.inter = Interface(nome = match)

	def reset(self, match, n, numero):  
		n = str(n)
		ris = self.inter.new_game(match + n)
		#time.sleep(TIME)
		print(str(ris))
		ris = self.inter.join_game("AI-4-" + str(numero), "AI", "nn")
		print(str(ris))
		#time.sleep(TIME)
		ris = self.inter.status()
		self.stato, self.size, self.symbol, self.name, self.team, self.loyalty, self.x, self.y = Data_Manager.status_iniziale(str(ris))			#name è superfluo, lo sappiamo già
		self.x = int(self.x)
		self.y = int(self.y)		
		self.morto = False
		time.sleep(5)
		ris = self.inter.start_game()
		print(str(ris))
		#time.sleep(TIME)
		ris = self.inter.status()
		self.stato, self.energy, self.score, self.st, self.allies, self.enemies = Data_Manager.status(str(ris), self.name, self.symbol)
		ris = self.inter.look()
		#time.sleep(TIME)
		self.mapp = Data_Manager.mappa(str(ris))
		#print(self.mapp)
		#print(self.x)
		#print(self.y)
		#print(self.mapp[self.y][self.x])
		self.bx, self.by = pos_bandiera(self.mapp, self.symbol, int(self.size))
		self.state = get_state(self.mapp, self.bx, self.by, self.x, self.y, self.size, self.allies, self.enemies)
		self.mappa_stato = stato_mappa(self.mapp, self.symbol, int(self.size))
		#print(self.mappa_stato)
		self.ciclo = True
		self.kill = 0		
		return self.state
		# coordinate iniziali date da status?
		# stato iniziale
		#state = # direi la visuale della mappa da look()

	def reset_join(self, match, n, numero):
		n = str(n)
		self.inter.nome = match + n
		ris = self.inter.join_game("AI-4-" + str(numero), "AI", "nn")
		while str(ris)[2:7] == "ERROR":
			print(str(ris)[2:7])
			time.sleep(TIME)
			ris = self.inter.join_game("AI-4-" + str(numero), "AI", "nn")
			print(ris)
		#time.sleep(TIME)
		ris = self.inter.status()
		self.stato, self.size, self.symbol, self.name, self.team, self.loyalty, self.x, self.y = Data_Manager.status_iniziale(str(ris))		#name è superfluo, lo sappiamo già
		#self.state = int(y)*32 + int(x)
		self.x = int(self.x)
		self.y = int(self.y)		
		self.morto = False
		while self.stato != "ACTIVE":
			time.sleep(TIME)
			ris = self.inter.status()
			self.stato = Data_Manager.status_wait(str(ris))
			print(self.stato)
		#time.sleep(TIME)
		self.stato, self.energy, self.score, self.st, self.allies, self.enemies = Data_Manager.status(str(ris), self.name, self.symbol)
		ris = self.inter.look()
		self.mapp = Data_Manager.mappa(str(ris)) 
		#print(self.mapp)
		#print(self.x)
		#print(self.y)
		#print(self.mapp[self.y][self.x])
		self.bx, self.by = pos_bandiera(self.mapp, self.symbol, int(self.size))
		self.state = get_state(self.mapp, self.bx, self.by, self.x, self.y, self.size, self.allies, self.enemies)
		self.mappa_stato = stato_mappa(self.mapp, self.symbol, int(self.size))
		#print(self.mappa_stato)
		self.kill = 0
		self.ciclo = True		
		return self.state


	action_space = range(0, 10)
	observation_space = range(0, 4095) #dobbiamo decidere il possibile set da stati
	
	def mossa_giusta(self):
		self.mappa_stato = stato_mappa(self.mapp, self.symbol, int(self.size))
		self.pos = self.mappa_stato[self.y][self.x]
		self.pos = int(self.pos)
		if self.energy > 50:
			self.state = get_state(self.mapp, self.bx, self.by, self.x, self.y, self.size, self.allies, self.enemies)
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
				#print(self.mappa_stato[self.y-1][self.x])
				return 0
			elif self.y != 31 and self.pos < int(self.mappa_stato[self.y+1][self.x]):
				#print(self.mappa_stato[self.y+1][self.x])			
				return 1
			elif self.x != 31 and self.pos < int(self.mappa_stato[self.y][self.x+1]):
				#print(self.mappa_stato[self.y][self.x+1])
				return 2
			else: 
				#print(self.mappa_stato[self.y][self.x-1])
				return 3
		else:
			self.ciclo = True
			if self.x != 31 and self.pos < int(self.mappa_stato[self.y][self.x+1]):
				#print(self.mappa_stato[self.y][self.x+1])
				return 2
			elif self.x != 0 and self.pos < int(self.mappa_stato[self.y][self.x-1]):
				#print(self.mappa_stato[self.y][self.x-1])
				return 3
			elif self.y != 0 and self.pos < int(self.mappa_stato[self.y-1][self.x]):
				#print(self.mappa_stato[self.y-1][self.x])
				return 0
			else:
				#print(self.mappa_stato[self.y+1][self.x])			
				return 1

	def step(self, action):
		if action == 0:
			print("mi muovo a nord")
			ris = self.inter.move("N")
			#print(ris)
			ris = Data_Manager.movimento(str(ris))
			print(ris)
			if ris == 'OK':
				self.y = self.y-1
				self.state = get_state(self.mapp, self.bx, self.by, self.x, self.y, self.size, self.allies, self.enemies)
				if self.state[0] == 1:
					return self.state, 5, False
				else:
					return self.state, -10, False

			if ris == 'BLOCKED':
				if self.y!= 0 and self.mappa_stato[self.y-1][self.x] == 100:
					return self.state, 1000, True
				else:
					return self.state, -100, False

			#if ris == 'TRAP':
				#state[x, y-1] = 'ai'
				#state[x, y] = '.'
				#return state, -100, false

			if ris == 'WIN':
				self.y = self.y-1
				self.state = get_state(self.mapp, self.bx, self.by, self.x, self.y, self.size, self.allies, self.enemies)
				return self.state, 10000, True
			if ris == 'ERROR':
				#time.sleep(1) #qua crasha alla mossa dopo
				return self.state,-1, False
			#recharge

			#move object
		if action == 1:	
			print("mi muovo a sud")
			ris = self.inter.move("S")
			#print(ris)
			ris = Data_Manager.movimento(str(ris)) 
			print(ris)
			if ris == 'OK':
				self.y = self.y+1	
				self.state = get_state(self.mapp, self.bx, self.by, self.x, self.y, self.size, self.allies, self.enemies)
				if self.state[1] == 1 and self.state[12] == 0:
					return self.state, 5, False
				elif self.state[12] == 0:
					return self.state, -10, False
				else:
					return self.state, 0, False

			if ris == 'BLOCKED':
				if self.y != 31 and self.mappa_stato[self.y+1][self.x] == 100 and self.state[12] == 0:
					return self.state, 1000, True
				else:
					return self.state, -100, False

			#if ris == 'TRAP':
			#	state[x, y+1] = 'ai'
			#	state[x, y] = '.'
			#	return state, -100, false

			if ris == 'WIN':	#non esiste
				self.y = self.y+1	
				self.state = get_state(self.mapp, self.bx, self.by, self.x, self.y, self.size, self.allies, self.enemies)
				return self.state, 1000, True
			if ris == 'ERROR':
				#time.sleep(1)
				return self.state,-1, False

		if action == 2:
			print("mi muovo a est")
			ris = self.inter.move("E")
			#print(ris)
			ris = Data_Manager.movimento(str(ris))
			print(ris)
			if ris == 'OK':
				self.x = self.x+1
				self.state = get_state(self.mapp, self.bx, self.by, self.x, self.y, self.size, self.allies, self.enemies)
				if self.state[2] == 1 and self.state[12] == 0:
					return self.state, 5, False
				elif self.state[12] == 0:
					return self.state, -10, False
				else:
					return self.state, 0, False

			if ris == 'BLOCKED':
				if self.x != 31 and self.mappa_stato[self.y][self.x+1] == 100 and self.state[12] == 0:
					return self.state, 1000, True
				else:
					return self.state, -100, False

			#if ris == 'TRAP':
			#	state[x+1, y] = 'ai'
			#	state[x, y] = '.'
			#	return state, -100, false

			if ris == 'WIN':
				self.x = self.x+1
				self.state = get_state(self.mapp, self.bx, self.by, self.x, self.y, self.size, self.allies, self.enemies)
				return self.state, 1000, True
			if ris == 'ERROR':
				#time.sleep(1)
				return self.state,-1, False

		if action == 3:
			print("mi muovo a ovest")
			ris = self.inter.move("W")
			#print(ris)
			ris = Data_Manager.movimento(str(ris))
			print(ris)
			if ris == 'OK':
				self.x = self.x-1
				self.state = get_state(self.mapp, self.bx, self.by, self.x, self.y, self.size, self.allies, self.enemies)
				if self.state[2] == 1 and self.state[12] == 0:
					return self.state, 5, False
				elif self.state[12] == 0:
					return self.state, -10, False
				else:
					return self.state, 0, False


			if ris == 'BLOCKED':
				if self.x != 0 and self.mappa_stato[self.y][self.x-1] == 100 and self.state[12] == 0:
					return self.state, 1000, True
				else:
					return self.state, -100, False

			#if ris == 'TRAP':
			#	state[x-1, y] = 'ai'
			#	state[x, y] = '.'
			#	return state, -100, false

			if ris == 'WIN':
				self.x = self.x-1
				self.state = get_state(self.mapp, self.bx, self.by, self.x, self.y, self.size, self.allies, self.enemies)
				return self.state, 1000, True
			if ris == 'ERROR':
				#time.sleep(1)
				return self.state,-1, False

		if action == 4:
			print("guardo")    #da rifare
			ris = self.inter.look()
			self.mapp = Data_Manager.mappa(str(ris))
			print(self.mapp)
			self.state = get_state(self.mapp, self.bx, self.by, self.x, self.y, self.size, self.allies, self.enemies)
			return self.state, -5, False

		if action == 5:
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
				#time.sleep(TIME)
				return self.state,-1, False

		if action == 6:
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
				#time.sleep(TIME)
				return self.state,-1, False

		if action == 7:
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
				#time.sleep(TIME)
				return self.state,-1, False

		if action == 8:
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
				#time.sleep(TIME)
				return self.state,-1, False
			

		if action == 9:
			print("stato")     #valutare
			ris = self.inter.status()
			#print(ris)
			self.stato, self.energy, self.score, self.st, self.allies, self.enemies = Data_Manager.status(str(ris), self.name, self.symbol)
			print(self.stato)
			print(self.energy)
			print(self.score)
			print(self.st)
			print(self.allies)
			print(self.enemies)
			if self.stato == "FINISHED":
				if self.st == "ACTIVE":
					return self.state, 30, True
				else:
					return self.state, 0, True
			if self.st == "ACTIVE":
				return self.state, -5, False		
			else:
				self.morto = True
				return self.state, -50, False

	def get_state(mapp, bx, by, x, y, size, allies, enemies):
		stato = np.zeros(13)
		if self.team != self.loyalty:
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
		if y == 0 or (mapp[y-1][x] == '#' or mapp[y-1][x] == '@'):
			stato[4] = 0
		else: 
			stato[4] = 1
		if y == size - 1 or (mapp[y+1][x] == '#' or mapp[y+1][x] == '@'):
			stato[5] = 0
		else: 
			stato[5] = 1
		if x == size - 1 or (mapp[y][x+1] == '#' or mapp[y][x+1] == '@'):
			stato[6] = 0
		else: 
			stato[6] = 1
		if x == 0 or (mapp[y][x-1] == '#' or mapp[y][x-1] == '@'):
			stato[7] = 0
		else: 
			stato[7] = 1

		stato[8] = 1
		stato[9] = 1
		stato[10] = 1
		stato[11] = 1
		if y != 0:
			for i in range(y-1, -1, -1):
				if mapp[i][x] == '#' or mapp[i][x] in allies:
					break
				if mapp[i][x] in enemies:
					stato[8] = 0
					break
		if y != size-1:
			for i in range(y+1, size):
				if mapp[i][x] == '#' or mapp[i][x] in allies:
					break
				if mapp[i][x] in enemies:
					stato[9] = 0
					break
		if x != size-1:
			for i in range(x+1, size):
				if mapp[y][i] == '#' or mapp[y][i] in allies:
					break
				if mapp[y][i] in enemies:
					stato[10] = 0
					break
		if x != 0:
			for i in range(x-1, -1, -1):
				if mapp[y][i] == '#' or mapp[y][i] in allies:
					break
				if mapp[y][i] in enemies:
					stato[11] = 0
					break
	
		return stato

