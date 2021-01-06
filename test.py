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
from nuovo_join import Env
from variabili import var
from tensorforce.agents import Agent
from tensorforce.environments import Environment
from tensorforce.execution import Runner

np.set_printoptions(threshold=np.inf)

match = var.nome
num = var.numero
mossa = 0

host = "margot.di.unipi.it"
port = 8421
TIME = var.TIME



s = 0
k = 0
v = 0
team = 0
ked = 0
for i in range(1, num):
	env = Env.create(environment = Env(match, i, 10))	
	#agent = Agent.create(agent = 'ppo', environment = env, max_episode_timesteps = 1000, batch_size = 1)
	agent = Agent.load(directory='model-complete-2', format='checkpoint', environment=env)

	states = env.reset()
	terminal = False
	while not terminal:
		if env.morto == False:
			for mos in range(0, 3-mossa):

				if env.morto == True:
					#actions = agent.act(states = states)
					actions = 4
					states, reward, terminal = env.execute(actions = actions)
				else:
					actions = agent.act(states = states)
					states, reward, terminal = env.execute(actions = actions)
					agent.observe(terminal = terminal, reward = reward)	

				if terminal:
					if env.win == True:
						print('vinto 10')
						v = v+1
					break
		if env.morto == False and terminal == False:
			for mos in range(0, mossa):
				#actions = agent.act(states = states)
				actions = env.mossa_giusta()
				states, reward, terminal = env.execute(actions = actions)
				#agent.observe(terminal = terminal, reward = reward)
				if terminal:
					if env.win == True:
						print('vinto 10')
						v = v + 1
					break
		if not terminal:
			#actions = agent.act(states = states)
			actions = 4				
			states, reward, terminal = env.execute(actions = actions)
			#agent.observe(terminal = terminal, reward = reward)
			#actions = agent.act(states = states)
			actions = 9
			states, reward, terminal = env.execute(actions = actions)
			#agent.observe(terminal = terminal, reward = reward)


	if env.morto:
		ked = ked + 1
	s = s + env.score
	k = k + env.kill
	team = team + env.chat.vittoria
	print("Fine partita")
	agent.save(directory='model-complete-2', format='checkpoint')
print(v)
print(team)
print(s)
print(k)
print(ked)


