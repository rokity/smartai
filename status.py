def status(stat, name):
	if stat[2:4]== "OK":
		i = stat.find("energy=")
		stat = stat[i+7:]
		i = stat.find(" ")
		energy = stat[:i]	#return energy
		stat = stat[i+1:]
		i = stat.find("n")
		score = stat[6:i-1]	#return score
		i = stat.find("name=" + name)
		stat = stat[i:]
		i = stat.find("state=")
		stat = stat[i+6:]
		i = stat.find("n")
		state = stat[:i-1]	#return state
		return energy, score, state
	else:
		return "ERROR"
