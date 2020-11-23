def colpito(m):
	if m[8:11] == "406":
		return "not shoot"
	if m[2:4] == "OK":
		return m[5]
