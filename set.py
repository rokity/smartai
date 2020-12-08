import numpy as np
import pickle

np.set_printoptions(threshold=np.inf)

#action_space = range(0, 10)
#observation_space = range(0, 4095) #dobbiamo decidere il possibile set da stati
#q_table = np.zeros([len(observation_space),len(action_space)])

#f = open('store0.pckl', 'wb')
#pickle.dump(q_table, f)
#f.close()


#f = open('store0.pckl', 'rb')
#q_table = pickle.load(f)
#f.close()
#print(q_table)
c = np.zeros([8191, 10])
for i in range(0, 10):
#	f = open('store'+str(i)+'.pckl', 'wb')
#	pickle.dump(q_table, f)
#	f.close()	
		
	f = open('store'+str(i)+'.pckl', 'rb')
	q_table = pickle.load(f)
	f.close()
	#r = np.zeros([8191, 10])
	#r[0:4095] = q_table
	#c = c + r
	c = c + q_table
	#print(q_table)
	#m = np.zeros(4096)
	#for j in range(0, 4095):
#		m[j] = max(q_table[j])
	#print(m)
#print(c[0:4095])
#f = open('store0.pckl', 'rb')
#q_table = pickle.load(f)
#f.close()
#m = np.zeros(4095)
#for i in range(0, 4095):
	#m[i] = max(c[i])
#print(m)

for i in range(0, 10):
	f = open('store'+str(i)+'.pckl', 'wb')
	pickle.dump(c, f)
	f.close()	
		
