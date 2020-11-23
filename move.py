def movimento(move):
	if move[5] == 'm':
		return "OK"
	if move[5] == 'b':
		return "BLOCKED"
	if move[8:11] == "501":
		return "WIN"
	if move[2] == "E":
		return "ERROR"

