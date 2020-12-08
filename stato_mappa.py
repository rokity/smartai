import numpy as np
def stato_mappa(mapp, symbol, size, sizex):
	stato = np.zeros((size, sizex))
	for i in range(0, size):
		for j in range(0, sizex):
			if mapp[i][j] == '#' or mapp[i][j] == '@' or mapp[i][j] == '&':
				stato[i][j] = 1
			if (mapp[i][j] == 'X' and symbol == 0) or (mapp[i][j] == 'x' and symbol == 1):
				stato[i][j] = 100
	stallo = True
	while stallo:
		stallo = False
		for i in range(1, size-1):
			for j in range(1, sizex-1):
				if stato [i][j] != 1 and stato[i][j] != 100:
					t = stato[i][j]
					stato[i][j] = max(stato[i+1][j], stato[i-1][j], stato[i][j+1], stato[i][j-1]) - 1 
					if stato[i][j] == -1 or stato[i][j] == t:
						stato[i][j] = t
					else:
						stallo = True
	for i in range(0, size):
		stato[0][i] = 1
		stato[size-1][i] = 1
		stato[i][0] = 1
		stato[i][sizex-1] = 1
	return stato
