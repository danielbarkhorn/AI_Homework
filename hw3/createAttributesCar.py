import pandas as pd
import numpy as np

# column headers
attNames = ['buying', 'maint', 'doors', 'persons', 'lug_boot',
'safety', 'acceptability']

path = '/Users/danielbarkhorn/Desktop/SCU_2016-2017/Spring/COEN_266/'

# our data in a numpy ndarray
data = np.genfromtxt(path+'car.csv', delimiter = ',', dtype=str).astype(str)
np.random.shuffle(data)
n = data.shape[0]
train = data[int(n/5):]
test = data[:int(n/5)]

np.savetxt(path+'carTrainDataset.txt', train, fmt='%s', delimiter=',')
np.savetxt(path+'carTestDataset.txt', test, fmt='%s', delimiter=',')

attributes = []
for i in range(len(attNames)):
    atts = ','.join(np.unique(data[:,i]).astype(str))
    attributes.append(''.join([attNames[i], ':', atts]))

np.savetxt(path+'carAttributes.txt', attributes, fmt='%s', delimiter=',')
