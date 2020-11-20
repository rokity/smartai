def status_iniziale(stat)
	if stat[0:2]== "OK":
		i = stat.find("state=")
		stat = stat[i+6:]
		i = stat.find(" ")
		stato = stat[:i]	#return stato match
		stat = stat[i+1:]
		i = stat.find("\n")
		size = stat[5:i]	#return dimensioni mappa
		stat = stat[i+1:]
		i = stat.find("symbol=")
		stat = stat[i+7:]
		symbol = stat[0]	#return team symbol
		if symbol == "a":	
			symbol = 0	#0 per team lettere piccole
		else:
			symbol = 1	#1 per team lettere grandi
		stat = stat[2:]
		i = stat.find(" ")
		name = stat[5:i] 	#return name 
		team = stat[i+6] 	#return team
		loyalty = stat[i+16]	#return loyalty
		stat = stat[i+25:]
		i = stat.find(" ")
		energy = stat[:i]	#return energy forse superflua
		stat = stat[i+1:]
		i = stat.find("\n")
		score = stat[6:i]	#return score forse superflua
		i = stat.find("name=" + name)
		stat = stat[i+5:]
		i = stat.find("x=")
		stat = stat[i+2:]
		i = stat.find(" ")
		x = stat[:i]		#coordinata x iniziale
		stat = stat[i+3:]
		i = stat.find(" ")
		y = stat[:i]		#coordinata y iniziale
					#c'e' anche la parte state ma e' superflua
		return stato, size, symbol, name, team, loyalty, x, y
	else:
		return "ERROR"
