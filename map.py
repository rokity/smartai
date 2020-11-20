import numpy as np
def mappa(mapp):
	if mapp[0:2] == "OK":
		i = mapp.find("\n")
		mapp = mapp[i+1:]
		i = mapp.find("\n")
		a = np.array(list(mapp[:i]))
		a = np.asmatrix(a)
		a = np.array(a)
		mapp = mapp[i+1:]
		for j in range(1, i):
			b = np.array(list(mapp[:i]))
			b = np.asmatrix(b)
			b = np.array(b)
			a = np.concatenate((a, b), axis=0)
			mapp = mapp[i+1:]
		return a	
	else:
		return "ERROR"
