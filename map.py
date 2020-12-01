import numpy as np
def mappa(mapp):
	if mapp[2:4] == "OK":
		i = mapp.find("n")
		mapp = mapp[i+1:]
		i = mapp.find("n")
		a = np.array(list(mapp[:i-1]))
		a = np.asmatrix(a)
		a = np.array(a)
		mapp = mapp[i+1:]
		for j in range(1, i-1):
			b = np.array(list(mapp[:i-1]))
			b = np.asmatrix(b)
			b = np.array(b)
			a = np.concatenate((a, b), axis=0)
			mapp = mapp[i+1:]
		return a	
	else:
		return "ERROR"
