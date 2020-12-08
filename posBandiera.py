import numpy as np
def pos_bandiera(mapp, symbol, size, sizex):
	for i in range(0, size):
		for j in range(0, sizex):
			if (mapp[i][j] == 'X' and symbol == 0) or (mapp[i][j] == 'x' and symbol == 1):
				return i, j

