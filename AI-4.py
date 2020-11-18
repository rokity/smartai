import getpass
import telnetlib
from Interface import Interface
import time
import numpy as np
import random

host = "margot.di.unipi.it"
port = 8421
TIME = 0.3

inter = interface()

#azioni convertite in numeri
# 0: nord
# 1: sud
# 2: est
# 3: ovest
# 4: look
# 5, 6, 7, 8: shoot N, S, E, W

q_table = np.zeros([len(env.observation_space),len(env.action_space)])
alpha = 0.1
gamma = 0.6
epsilon = 0.1

all_epochs = []
all_penalties = []

for i in range(1, 100001):
	state = env.reset() #qua devo creare la partita e fare look
	
	epochs, penalties, reward, = 0, 0, 0
	done = false

	while not done
	if random.uniform(0, 1) < epsilon:
		action = env.action_space.sample() #esplorazione delle azioni
	else:
		action = np.argmax(q_table[state]) #selezione mossa migliore
	next_state, reward, done = env.step(action)

	old_value = q_state[state, action]
	next_max = np.max(q_table[next_state])

	new_value = (1 - alpha) * old_value + alpha * ( reward + gamma * next_max)
	q_table =[state, action] = new_value

	if reward == -10: #determinare reward
		penalties += 1

	state = next_state
	epochs += 1

print("Fine partita")

#env ha una sezione azioni possibili  env.action_space
#env.step(action) aggiorna lo stato = stato, reward, done, info
#env.observation_space

class env:
	def reset(self)
		inter = Interface()
		ris = inter.new_game("PROVA_AI-4")
		time.sleep(TIME)
		ris = inter.join_game("AI-4", "AI", "nn")
		time.sleep(TIME)
		ris = inter.status()
		#analisi status
		time.sleep(TIME)
		ris = inter.start_game()
		time.sleep(TIME)
		ris = inter.look()
		time.sleep(TIME)
		x, y, status = mappa(ris) 
		# coordinate iniziali date da status?
		# stato iniziale
		#state = # direi la visuale della mappa da look()

	action_space = range(0, 9)
	observation_space = range(0, 1024) #dobbiamo decidere il possibile set da stati
	
	def step(self, action)
		if action = 0:
			ris = inter.move("N")
			ris = movimento(ris)
			if ris == 'OK':
				state[x, y-1] = 'ai'
				state[x, y] = '.'
				return state, -1, false

			if ris == 'BLOCKED':
				return state, -100, false

			if ris == 'TRAP':
				state[x, y-1] = 'ai'
				state[x, y] = '.'
				return state, -100, false

			if ris == 'WIN':
				return state, 1000, true

			#recharge

			#move object
		if action = 1:	
			ris = inter.move("S")
			ris = movimento(ris) 
			if ris == 'OK':
				state[x, y+1] = 'ai'
				state[x, y] = '.'
				return state, -1, false

			if ris == 'BLOCKED':
				return state, -100, false

			if ris == 'TRAP':
				state[x, y+1] = 'ai'
				state[x, y] = '.'
				return state, -100, false

			if ris == 'WIN':
				return state, 1000, true


		if action = 2:
			ris = inter.move("E")
			ris = movimento(ris)
			if ris == 'OK':
				state[x+1, y] = 'ai'
				state[x, y] = '.'
				return state, -1, false

			if ris == 'BLOCKED':
				return state, -100, false

			if ris == 'TRAP':
				state[x+1, y] = 'ai'
				state[x, y] = '.'
				return state, -100, false

			if ris == 'WIN':
				return state, 1000, true

	if action = 3:
			ris = inter.move("W")
			ris = movimento(ris)
			if ris == 'OK':
				state[x-1, y] = 'ai'
				state[x, y] = '.'
				return state, -1, false

			if ris == 'BLOCKED':
				return state, -100, false

			if ris == 'TRAP':
				state[x-1, y] = 'ai'
				state[x, y] = '.'
				return state, -100, false

			if ris == 'WIN':
				return state, 1000, true

		if action = 4:
			ris = inter.look()
			x, y, status = mappa(ris)
			return state, 1, false

		if action = 5:
			ris = inter.shoot("N")
			ris = colpito(ris)
			if ris == '#'
				return status, -10, false
			if ris == '&'
				return status, -10, false
			if ris == 'KILL'
				return status, 100, false 
		if action = 6:
			ris = inter.shoot("S")
			ris = colpito(ris)
			if ris == '#'
				return status, -10, false
			if ris == '&'
				return status, -10, false
			if ris == 'KILL'
				return status, 100, false
		if action = 7:
			ris = inter.shoot("E")
			ris = colpito(ris)
			if ris == '#'
				return status, -10, false
			if ris == '&'
				return status, -10, false
			if ris == 'KILL'
				return status, 100, false
		if action = 8:
			ris = inter.shoot("W")
			ris = colpito(ris)
			if ris == '#'
				return status, -10, false
			if ris == '&'
				return status, -10, false
			if ris == 'KILL'
				return status, 100, false

