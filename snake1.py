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
from AI4 import env
from variabili import var
from AI4 import conv

np.set_printoptions(threshold=np.inf)

match = var.nome
num = var.numero
mossa = 3

host = "margot.di.unipi.it"
port = 8421
TIME = var.TIME
#numero = 0
							


#azioni convertite in numeri
# 0: nord
# 1: sud
# 2: est
# 3: ovest
# 4: look
# 5, 6, 7, 8: shoot N, S, E, W
# 9: status

env = env(match)
#q_table = np.zeros([len(env.observation_space),len(env.action_space)])
f = open('store1.pckl', 'rb')
q_table = pickle.load(f)
f.close()
alpha = 0.1
gamma = 0.6
epsilon = -1

all_epochs = []
all_penalties = []

v = 0
s = 0
k = 0
ked = 0
for i in range(1, num):
	p = i
	state = env.reset_join(match, p, 0) #qua devo creare la partita e fare look
	state = conv(state)
	epochs, penalties, reward, = 0, 0, 0
	done = False

	while not done:   #implemetare fine game, turing game
		if env.morto == False:
			for mos in range(0, 3- mossa):
				if random.uniform(0, 1) < epsilon :
					action = random.randint(0, 9) #esplorazione delle azioni
				else:
					action = np.argmax(q_table[state]) #selezione mossa migliore
				#time.sleep(TIME)
				if env.morto == True: #continuo a guardare per turing game
					action = 4
					#done = True #esco per partita dopo

				next_state, reward, done = env.step(action)
				next_state = conv(next_state)

				old_value = q_table[state, action]
				next_max = np.max(q_table[next_state])

				new_value = (1 - alpha) * old_value + alpha * ( reward + gamma * next_max)
				q_table[state, action] = new_value

				if reward == -10: #determinare reward
					penalties += 1

				state = next_state
				epochs += 1
				if done:
					print("vinto 1")
					v = v+1
					break
		if env.morto == False and done == False:
			for mos in range (0, mossa):
				action = env.mossa_giusta()
				next_state, reward, done = env.step(action)
				next_state = conv(next_state)
				#time.sleep(TIME)
	
				old_value = q_table[state, action]
				next_max = np.max(q_table[next_state])
	
				new_value = (1 - alpha) * old_value + alpha * ( reward + gamma * next_max)
				q_table[state, action] = new_value
				if done:
					print("vinto 1")
					v = v+1
					break

		if not done:
			action = 4
			next_state, reward, done = env.step(action)
			next_state = conv(next_state)
			#time.sleep(TIME)
	
			old_value = q_table[state, action]
			next_max = np.max(q_table[next_state])
	
			new_value = (1 - alpha) * old_value + alpha * ( reward + gamma * next_max)
			q_table[state, action] = new_value

			action = 9
			next_state, reward, done = env.step(action)
			next_state = conv(next_state)
			#time.sleep(TIME)
	
			old_value = q_table[state, action]
			next_max = np.max(q_table[next_state])
	
			new_value = (1 - alpha) * old_value + alpha * ( reward + gamma * next_max)
			q_table[state, action] = new_value
		
	if env.morto:
		ked = ked + 1	
	s = s + env.score
	k = k + env.kill
	print("Fine partita")

print(v)
print(s)
print(k)
print(ked)
f = open('store1.pckl', 'wb')
pickle.dump(q_table, f)
f.close()
#env ha una sezione azioni possibili  env.action_space
#env.step(action) aggiorna lo stato = stato, reward, done, info
#env.observation_space
