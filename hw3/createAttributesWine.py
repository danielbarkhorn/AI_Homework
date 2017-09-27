# Made by Dan Barkhorn

import pandas as pd
import numpy as np

# column headers
attNames = ['malic acid', 'ash', 'alcalinity of ash', 'magnesium', 'total phenols',
'flavanoids', 'nonflavanoid phenols', 'proanthocyanis', 'color intensity', 'hue', 'OD280',
'proline', 'alcohol']

path = '/Users/danielbarkhorn/Desktop/SCU_2016-2017/Spring/COEN_266/'

# our data in a numpy ndarray
data = np.genfromtxt(path+'wine.txt', delimiter = ',', defaultfmt = "%.8f")[:,1:]

np.random.shuffle(data)
n = data.shape[0]

np.savetxt(path+'wineTrainDataset.txt', data[:int(n/5)], fmt = '%s',delimiter=',')
np.savetxt(path+'wineTestDataset.txt', data[int(n/5):], fmt = '%s',delimiter=',')

attributes = []
for i in range(len(attNames)):
    atts = ','.join(np.unique(data[:,i]).astype(str))
    attributes.append(''.join([attNames[i], ':', atts]))

np.savetxt(path+'wineAttributes.txt', attributes, fmt = '%s')
