def status_wait(stat):
	if stat[2:4] == "OK":
		i = stat.find("state=")
		stat = stat[i+6:]
		i = stat.find(" ")
		stato = stat[:i]
		return stato
	else:
		return "ERROR"
