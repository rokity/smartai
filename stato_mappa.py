import numpy as np
def stato_mappa(mapp, symbol, size, sizex):
	stato = np.zeros((size, sizex))
	for i in range(0, size):
		for j in range(0, sizex):
			if mapp[i][j] == '#' or mapp[i][j] == '@' or mapp[i][j] == '&':
				stato[i][j] = 1
			if (mapp[i][j] == 'X' and symbol == 0) or (mapp[i][j] == 'x' and symbol == 1):
				stato[i][j] = 400
				posx=j
				posy=i
	
	stato = f(posx, posy, size, sizex, stato)
	return stato

def f(x, y, size, sizex, stato):
	s = np.zeros((size, sizex))
	s[y][x] = 400
	for i in range(x, sizex-1):
		for j in range(y+1, size):
			s[j][i] = s[j-1][i] - 1
		for j in range(y-1, -1, -1):
			s[j][i] = s[j+1][i] - 1
		s[y][i+1] = s[y][i]-1
	s[y][x-1] = 399
	for i in range(x-1, 0, -1):
		for j in range(y+1, size):
			s[j][i] = s[j-1][i] - 1
		for j in range(y-1, -1, -1):
			s[j][i] = s[j+1][i] - 1
		s[y][i-1] = s[y][i] -1	
	for i in range(0, size):
		for j in range(0, sizex):
			if stato[i][j] == 1:
				s[i][j] =1
	for i in range(1, size-1):
		for j in range(1, sizex-1):		
			if s[i][j] != 1:
				if s[i][j+1] == 1:
					s[i][j] = max(s[i][j-1], s[i-1][j]) - 1
				if s[i+1][j] == 1:
					s[i][j] = max(s[i][j+1], s[i-1][j]) - 1
	for i in range(0, sizex):
		s[0][i] = s[1][i] - 1
		s[size-1][i] = s[size-2][i]- 1
	for i in range(0, size):
		s[i][0] = s[i][1] - 1
		s[i][sizex-1] = s[i][sizex-2] - 1
	return s
		

def fi():
	stallo = True
	while stallo:
		print('provo')
		stallo = False
		for i in range(1, size-1):
			for j in range(1, sizex-1):
				if stato [i][j] != 1 and stato[i][j] != 400:
					t = stato[i][j]
					stato[i][j] = max(stato[i+1][j], stato[i-1][j], stato[i][j+1], stato[i][j-1]) - 1 
					if stato[i][j] == -1 or stato[i][j] == t:
						stato[i][j] = t
					else:
						stallo = True
	for i in range(0, sizex):
		if stato[0][i] == 0:
			stato[0][i] = stato[1][i] - 1
		if stato[size-1][i] == 0:
			stato[size-1][i] = stato[size-2][i]- 1
	for i in range(0, size):
		if stato[i][0] == 0 or stato[i][0] == -1:
			stato[i][0] = stato[i][1] - 1
		if stato[i][size-1] == 0 or stato[i][size-1] == -1:
			stato[i][sizex-1] = stato[i][sizex-2] - 1
	return stato
