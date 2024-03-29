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
from nuovo import Env
from variabili import var
from tensorforce.agents import Agent
from tensorforce.environments import Environment
from tensorforce.execution import Runner

np.set_printoptions(threshold=np.inf)


match = var.nome
form = var.form
size = var.size
typ = var.typ
num = var.numero
mossa = 0

host = "margot.di.unipi.it"
port = 8421
TIME = var.TIME
#numero = 0


#agent = Agent.create(agent = 'tensorforce', environment = Env(match), update = 64, optimizer = dict(optimizer = 'adam', learning_rate = 1e-3), objective = 'policy_gradient')


#agent = Agent.create(agent = 'tensorforce', environment = env, update = 64, optimizer = dict(optimizer = 'adam', learning_rate = 1e-3), objective = 'policy_gradient')

s = 0
k = 0
v = 0
team = 0
ked = 0
for i in range(1, num):
	print("*******************")
	print("partita")
	print(i)
	print("*******************")
	env = Env.create(environment = Env(match, i, 0, form, size, typ))	
	#agent = Agent.create(agent = 'ppo', environment = env, max_episode_timesteps = 1000, batch_size = 1)
	agent = Agent.load(directory='model-complete-1', format='checkpoint', environment=env)

	states = env.reset()
	terminal = False
	while not terminal:
		print("***********")
		print(i)
		print("***********")
		if env.morto == False:
			for mos in range(0, 3-mossa):

				if env.morto == True:
					actions = 4
					states, reward, terminal = env.execute(actions = actions)
				else:
					actions = agent.act(states = states) #, independent = True, deterministic = True
					states, reward, terminal = env.execute(actions = actions)
					agent.observe(terminal = terminal, reward = reward) #da silenziare per validation
	
				if terminal:
					if env.win == True:
						print('vinto 0')
						v = v+1
					break
		if env.morto == False and terminal == False:
			for mos in range(0, mossa):
				actions = env.mossa_giusta()
				states, reward, terminal = env.execute(actions = actions)
				if terminal:
					if env.win == True:
						print('vinto 0')
						v = v + 1
					break
		if not terminal:
			actions = 4				
			states, reward, terminal = env.execute(actions = actions)
			actions = 9
			states, reward, terminal = env.execute(actions = actions)


	if env.morto:
		ked = ked + 1
	s = s + env.score
	k = k + env.kill
	team = team + env.chat.vittoria
	print("Fine partita")
	#agent.save(directory='model-complete-1', format='checkpoint')
print(v)
print(team)
print(s)
print(k)
print(ked)


