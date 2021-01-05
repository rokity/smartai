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
		print(stat)
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
	def status(stat, name, symb):			#rimuovere alleati e nemici
		if stat[2:4]== "OK":
			allies = []
			enemies = []
			i = stat.find("state=")        
			stat = stat[i+6:]
			i = stat.find(" ")
			stato = stat[:i]		#return stato match
			
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
					state = stat[:i-1] 	#return stato giovatore
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
		if ris[2:4] != "OK":
			return "ERROR"
		else:
			return "OK"
	def meaning(message, allies, enemies, mappa, size, sizex):
		message = str(message)
		hit = message.find("hit")
		if hit != -1:
			print('##########')
			print(message)
			print('##########')
			print(allies)
			print(enemies)
			i = message.find(" ")
			player_kill = message[:i]
			player_killed = message[hit+4:]
			if player_kill in allies:
				if player_killed in allies:
					t =  allies[player_kill]
					t2 = allies[player_killed]
					del allies[player_killed]
					if controllo(mappa,t, t2, size, sizex, enemies):
						del allies[player_kill]
						enemies[player_kill] = t
						print('777777777777777777777777777777777777')
						return True, player_kill, allies, enemies
				elif player_killed in enemies:
					del enemies[player_killed]
					return False, player_killed, allies, enemies
			else:
				if player_killed in allies:
					del allies[player_killed]
				elif player_killed in enemies:
					t = enemies[player_kill]
					t2 = enemies[player_killed]
					del enemies[player_killed]
					if controllo(mappa, t, t2, size, sizex, allies):
						del enemies[player_kill]
						allies[player_kill] = t
						print('66666666666666666666666666666666666666')

			return False, player_kill, allies, enemies
		else:
			return False, "", allies, enemies		



	def finished(message):
		if message[0:13] == "Game finished":
			print('##########')
			print(message)
			print('##########')
			return True
		return False
def controllo(mappa, t, t2, size, sizex, team):
	trovati = 0
	avversario = []
	for i in team.keys():
		avversario.append(team[i])
	for i in range(0, size):
		for j in range(0, sizex):
			if mappa[i][j] == t:
				x = j
				y = i
				trovati = trovati+1
			if mappa[i][j] == t2:
				x2 = j
				y2 = i	
				trovati = trovati + 1 
			if trovati == 2:
				break
		if trovati == 2:
			break
	if trovati != 2:
		return False
	if abs(x - x2) <= abs(y - y2):
		if x <= x2:
			if y <= y2:
				for i in range(x, sizex):
					for j in range(y, y2+1):
						if mappa[j][i] in avversario:
							return False
				return True
			else:
				for i in range(x, sizex):
					for j in range(y2, y+1):
						if mappa[j][i] in avversario:
							return False
				return True
		else:
			if y <= y2:
				for i in range(x, -1, -1):
					for j in range(y, y2+1):
						if mappa[j][i] in avversario:
							return False
				return True
			else:
				for i in range(x, -1, -1):
					for j in range(y2, y+1):
						if mappa[j][i] in avversario:
							return False
				return True
	else:
		if y <= y2:
			if x <= x2:
				for i in range(y, size):
					for j in range(x, x2+1):
						if mappa[i][j] in avversario:
							return False
				return True
			else:
				for i in range(y, size):
					for j in range(x2, x+1):
						if mappa[i][j] in avversario:
							return False
				return True
		else:
			if x <= x2:
				for i in range(y, -1, -1):
					for j in range(x, x2+1):
						if mappa[i][j] in avversario:
							return False
				return True
			else:
				for i in range(y, -1, -1):
					for j in range(x2, x+1):
						if mappa[i][j] in avversario:
							return False
				return True	





#AI-4-7 shot Wai4-1 @GameServer AI-4-7 hit AI-4-9
