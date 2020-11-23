import getpass
import telnetlib
from Interface import Interface
from colpito import colpito
from map import mappa
from move import movimento
from status_iniziale import status_iniziale
from status import status
from status_wait import status_wait
import time
import numpy as np
import random

host = "margot.di.unipi.it"
port = 8421
TIME = 0.5

class env:
	def __init__(self, match):
		self.inter = Interface(nome = match)

	def reset(self, match, n):
		n = str(n)
		ris = self.inter.new_game(match + n)
		time.sleep(TIME)
		print(str(ris))
		ris = self.inter.join_game("AI-4", "AI", "nn")
		print(str(ris))
		time.sleep(TIME)
		ris = self.inter.status()
		self.stato, self.size, self.symbol, self.name, self.team, self.loyalty, x, y = status_iniziale(ris)		#name è superfluo, lo sappiamo già
		self.state = int(y)*32 + int(x)
		time.sleep(10)
		ris = self.inter.start_game()
		print(str(ris))
		time.sleep(TIME)
		ris = self.inter.look()
		time.sleep(TIME)
		self.mapp = mappa(str(ris))
		# coordinate iniziali date da status?
		# stato iniziale
		#state = # direi la visuale della mappa da look()

	def reset_join(self, match, n):
		n = str(n)
		self.inter.nome = match + n
		ris = self.inter.join_game("AI-4", "AI", "nn")
		print(ris)
		time.sleep(TIME)
		ris = self.inter.status()
		self.stato, self.size, self.symbol, self.name, self.team, self.loyalty, x, y = status_iniziale(str(ris))		#name è superfluo, lo sappiamo già
		self.state = int(y)*32 + int(x)

		while self.stato != "ACTIVE":
			time.sleep(TIME)
			ris = self.inter.status()
			self.stato = status_wait(str(ris))
			print(self.stato)
		time.sleep(TIME)
		ris = self.inter.look()
		self.mapp = mappa(str(ris)) 
		print(self.mapp)


	action_space = range(0, 10)
	observation_space = range(0, 1024) #dobbiamo decidere il possibile set da stati
	
	def step(self, action):
		if action == 0:
			print("mi muovo a nord")
			ris = self.inter.move("N")
			ris = str(ris)
			print(ris)
			ris = movimento(ris)
			print(ris)
			if ris == 'OK':
				self.state = self.state-32
				#state[x, y-1] = 'ai'
				#state[x, y] = '.'
				return self.state, -1, False

			if ris == 'BLOCKED':
				return self.state, -100, False

			#if ris == 'TRAP':
				#state[x, y-1] = 'ai'
				#state[x, y] = '.'
				#return state, -100, false

			if ris == 'WIN':
				self.state = self.state-32 
				return self.state, 1000, True
			if ris == 'ERRORE':
				return self.state,-1, False
			#recharge

			#move object
		if action == 1:	
			print("mi muovo a sud")
			ris = self.inter.move("S")
			ris = movimento(str(ris)) 
			print(ris)
			if ris == 'OK':
				self.state = self.state+32
				#state[x, y+1] = 'ai'
				#state[x, y] = '.'
				return self.state, -1, False

			if ris == 'BLOCKED':
				return self.state, -100, False

			#if ris == 'TRAP':
			#	state[x, y+1] = 'ai'
			#	state[x, y] = '.'
			#	return state, -100, false

			if ris == 'WIN':
				self.state = self.state+32
				return self.state, 1000, True
			if ris == 'ERRORE':
				return self.state,-1, False

		if action == 2:
			print("mi muovo a est")
			ris = self.inter.move("E")
			ris = movimento(str(ris))
			print(ris)
			if ris == 'OK':
				self.state = self.state+1
				#state[x+1, y] = 'ai'
				#state[x, y] = '.'
				return self.state, -1, False

			if ris == 'BLOCKED':
				return self.state, -100, False

			#if ris == 'TRAP':
			#	state[x+1, y] = 'ai'
			#	state[x, y] = '.'
			#	return state, -100, false

			if ris == 'WIN':
				self.state = self.state+1
				return self.state, 1000, True
			if ris == 'ERRORE':
				return self.state,-1, False

		if action == 3:
			print("mi muovo a ovest")
			ris = self.inter.move("W")
			ris = movimento(str(ris))
			print(ris)
			if ris == 'OK':
				self.state = self.state-1
				#state[x-1, y] = 'ai'
				#state[x, y] = '.'
				return self.state, -1, False

			if ris == 'BLOCKED':
				return self.state, -100, False

			#if ris == 'TRAP':
			#	state[x-1, y] = 'ai'
			#	state[x, y] = '.'
			#	return state, -100, false

			if ris == 'WIN':
				self.state = self.state-1
				return self.state, 1000, True
			if ris == 'ERRORE':
				return self.state,-1, False

		if action == 4:
			print("guardo")
			ris = self.inter.look()
			self.mapp = mappa(str(ris))
			print(self.mapp)
			return self.state, -5, False

		if action == 5:
			print("sparo a nord")
			ris = self.inter.shoot("N")
			ris = colpito(str(ris))
			print(ris)
			if ris == '#':
				return self.state, -10, False
			if ris == '&':
				return self.state, -10, False
			if ris == 'a' and self.symbol == 0:
				return self.state, -50, False
			if ris == 'a' and self.symbol == 1:
				return self.state, 100, False
			if ris == 'A' and self.symbol == 1:
				return self.state, -50, False
			if ris == 'A' and self.symbol == 0:
				return self.state, 100, False 
			if ris == "not shoot":
				return self.state, -10, False

		if action == 6:
			print("sparo a sud")
			ris = self.inter.shoot("S")
			ris = colpito(str(ris))
			print(ris)
			if ris == '#':
				return self.state, -10, False
			if ris == '&':
				return self.state, -10, False
			if ris == 'a' and self.symbol == 0:
				return self.state, -50, False
			if ris == 'a' and self.symbol == 1:
				return self.state, 100, False
			if ris == 'A' and self.symbol == 1:
				return self.state, -50, False
			if ris == 'A' and self.symbol == 0:
				return self.state, 100, False 
			if ris == "not shoot":
				return self.state, -10, False

		if action == 7:
			print("sparo a est")
			ris = self.inter.shoot("E")
			ris = colpito(str(ris))
			print(ris)
			if ris == '#':
				return self.state, -10, False
			if ris == '&':
				return self.state, -10, False
			if ris == 'a' and self.symbol == 0:
				return self.state, -50, False
			if ris == 'a' and self.symbol == 1:
				return self.state, 100, False
			if ris == 'A' and self.symbol == 1:
				return self.state, -50, False
			if ris == 'A' and self.symbol == 0:
				return self.state, 100, False 
			if ris == "not shoot":
				return self.state, -10, False

		if action == 8:
			print("sparo a ovest")
			ris = self.inter.shoot("W")
			ris = colpito(str(ris))
			print(ris)
			if ris == '#':
				return self.state, -10, False
			if ris == '&':
				return self.state, -10, False
			if ris == 'a' and self.symbol == 0:
				return self.state, -50, False
			if ris == 'a' and self.symbol == 1:
				return self.state, 100, False
			if ris == 'A' and self.symbol == 1:
				return self.state, -50, False
			if ris == 'A' and self.symbol == 0:
				return self.state, 100, False 
			if ris == "not shoot":
				return self.state, -10, False

		if action == 9:
			print("stato")
			ris = self.inter.status()
			self.energy, self.score, self.st = status(str(ris), self.name)
			print(self.energy)
			print(self.score)
			print(self.st)
			return self.state, -1, False

#inter = Interface()

#azioni convertite in numeri
# 0: nord
# 1: sud
# 2: est
# 3: ovest
# 4: look
# 5, 6, 7, 8: shoot N, S, E, W
# 9: status

match = "A1"
env = env(match)
q_table = np.zeros([len(env.observation_space),len(env.action_space)])
alpha = 0.1
gamma = 0.6
epsilon = 0.1

all_epochs = []
all_penalties = []


for i in range(1, 3):
	p = i
	state = env.reset_join(match, p) #qua devo creare la partita e fare look
	
	epochs, penalties, reward, = 0, 0, 0
	done = False

	while not done:
		if random.uniform(0, 1) < epsilon:
			action = random.randint(0, 9) #esplorazione delle azioni
		else:
			action = np.argmax(q_table[state]) #selezione mossa migliore
		time.sleep(TIME)

		next_state, reward, done = env.step(action)


		old_value = q_table[state, action]
		next_max = np.max(q_table[next_state])

		new_value = (1 - alpha) * old_value + alpha * ( reward + gamma * next_max)
		q_table[state, action] = new_value

		if reward == -10: #determinare reward
			penalties += 1

		state = next_state
		epochs += 1

	print("Fine partita")

#env ha una sezione azioni possibili  env.action_space
#env.step(action) aggiorna lo stato = stato, reward, done, info
#env.observation_space


