import numpy as np
import re

class Data_Manager:
	#def __init__()
	def movimento(move):
		if move[5] == 'm':
			return "OK"
		elif move[5] == 'b':
			return "BLOCKED"
		elif move[8:11] == "501":
			return "WIN"
		else:
			print(move)
			return "ERROR"
	def mappa(mapp, size):
		if mapp[2:4] == "OK":
			i = mapp.find("n")
			mapp = mapp[i+1:]
			i = mapp.find("n")
			a = np.array(list(mapp[:i-1]))
			a = np.asmatrix(a)
			a = np.array(a)
			mapp = mapp[i+1:]
			for j in range(1, size):
				b = np.array(list(mapp[:i-1]))
				b = np.asmatrix(b)
				b = np.array(b)
				a = np.concatenate((a, b), axis=0)
				mapp = mapp[i+1:]
			return a	
		else:
			#return mapp
			return "ERROR"
	def colpito(m):
		if m[8:11] == "406":
			return "not shoot"
		elif m[2:4] == "OK":
			return m[5]
		else:
			return "ERROR"
	def status_iniziale(stat):
		stat = str(stat)
		if stat[2:4]== "OK":
			i = stat.find("state=")
			stat = stat[i+6:]
			i = stat.find(" ")
			stato = stat[:i]	#return stato match
			stat = stat[i+1:]
			i = stat.find(" ")
			size = int(stat[5:i])	#return dimensioni mappa
			stat = stat[i+1:]
			i = stat.find("n")			
			q = stat[6:i-1]
			if q == "Q":
				sizex = size
			else:
				sizex = size*2
			stat = stat[i+1:]
			i = stat.find("symbol=")
			stat = stat[i+7:]
			symbol = stat[0]	#return team symbol
			if bool(re.search('[a-z]', symbol)):	
				symbol = 0	#0 per team lettere piccole
			else:
				symbol = 1	#1 per team lettere grandi
			stat = stat[2:]
			i = stat.find(" ")
			name = stat[5:i] 	#return name 
			team = int(stat[i+6]) 	#return team  non serve
			loyalty = int(stat[i+16])	#return loyalty
			stat = stat[i+25:]
			i = stat.find(" ")
			energy = int(stat[:i])	#return energy forse superflua
			stat = stat[i+1:]
			i = stat.find("n")
			score = int(stat[6:i-1])	#return score forse superflua
			i = stat.find("name=" + name)
			stat = stat[i+5:]
			i = stat.find("x=")
			stat = stat[i+2:]
			i = stat.find(" ")
			x = int(stat[:i])		#coordinata x iniziale
			stat = stat[i+3:]
			i = stat.find(" ")
			y = int(stat[:i])		#coordinata y iniziale
						#c'e' anche la parte state ma e' superflua
			return stato, size, sizex, symbol, name, team, loyalty, x, y
		else:
			print(stat)
			return "ERROR"
	def status(stat, name, symb):
		if stat[2:4]== "OK":
			allies = []
			enemies = []
			i = stat.find("state=")
			stat = stat[i+6:]
			i = stat.find(" ")
			stato = stat[:i]
			
			i = stat.find("energy=")
			stat = stat[i+7:]
			i = stat.find(" ")
			energy = int(stat[:i])		#return energy
			stat = stat[i+1:]
			i = stat.find("n")
			score = int(stat[6:i-1])	#return score
			i = stat.find("symbol=")
			while i!=-1:
				stat = stat[i+7:]
				symbol = stat[0]
				i = stat.find("name=")
				stat = stat[i+5:]
				if stat[0:len(name)] == name:
					i = stat.find("state=")
					stat = stat[i+6:]
					i = stat.find("n")
					state = stat[:i-1] 	#return state
				else:
					i = stat.find("state=")
					stat = stat[i+6:]
					i = stat.find("n")
					if str(stat[:i-1]) == "ACTIVE":
						if symb == 0:
							if bool(re.search('[A-Z]', symbol)):
								enemies.append(str(symbol))
							else:
								allies.append(str(symbol))
						else:	
							if bool(re.search('[A-Z]', symbol)):
								allies.append(str(symbol))
							else:
								enemies.append(str(symbol))
				i = stat.find("symbol=")				

			return stato, energy, score, state, allies, enemies
		else:
			print(stat)
			return "ERROR"
	def status_wait(stat):
		if stat[2:4] == "OK":
			i = stat.find("state=")
			stat = stat[i+6:]
			i = stat.find(" ")
			stato = stat[:i]
			return stato
		else:
			return "ERROR"
	def check(ris):
		#print(ris)
		if ris[2:4] != "OK":
			return "ERROR"
		else:
			return "OK"
