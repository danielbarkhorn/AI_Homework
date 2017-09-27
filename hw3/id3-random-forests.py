import copy
import dataset
import numpy as np

class DTree:
  'Represents a decision tree created with the ID3 algorithm'

  def __init__(self, classifier, training_data, attributes):
    self.classifier = classifier
    self.temp_data = training_data
    self.attributes = attributes
    self.masterList = []

    count = 0
    N = self.temp_data.__len__()
    # can set this yourself
    for i in range(50):
        rand = np.random.randint(0,N,N*4/float(5))
        training_data = dataset.DataSet(); testing_data = dataset.DataSet()
        for i in range(N):
            if i in rand:
                training_data.append(self.temp_data.all_examples[i])

        self.masterList.append(self.iteration(training_data, self.attributes))
        self.dump()


    #print(self.path)
    return

  def test(self, classifier, testing_data):
    correct = 0
    for i in testing_data:
        for j in self.masterList:
            correct += self.testStep(i, j, classifier)/float(50)
    return correct

  def dump(self):
    #self.dumpHelp(self.path, 0)
    return ""

  def dumpHelp(self, ls, count):
    if(not isinstance(ls[0], str)):
        for i in ls:
            self.dumpHelp(i, count+1)
    elif(isinstance(ls, str)):
        print(' '*count + ls)
    else:
        print(' '*count + ls[0]+':'+ls[1])
        self.dumpHelp(ls[2], count+1)

  def iteration(self, data, tempAttr):
      # The case where everything is the same
      if(data.entropy(self.classifier) == 0):
          return '<'+data.all_examples[0].get_value(self.classifier)+'>'

      # Compute the most common classifier values
      classVals = dict((key,0) for key in self.classifier.values)
      #{key:0 for (key) in self.classifier.values}
      for i in data:
          classVals[i.get_value(self.classifier)] += 1
      maxClass = ''; maxClassNum = -1
      for i in classVals.keys():
          if(classVals[i] > maxClassNum):
              maxClass = i
      # Done computing the most common classifier value

      #Check to make sure we have more attributes to split on, if not we will return most common
      currAttrs = copy.copy(tempAttr)
      if(currAttrs.__len__() == 0):
          return '<'+maxClass+'>'

      # Now we need to find out what to split on
      maxEnt = float('inf'); splitter = ''; N = data.__len__()
      for i in currAttrs:
          currEnt = 0
          # the different possible values of this attribute
          for j in i.values:
              jData = dataset.DataSet()
              for k in data:
                  if(k.get_value(i) == j):
                      jData.append(k)
              # now we have jData, which holds one value's entropy contribution
              currEnt += jData.entropy(self.classifier)*jData.__len__()/float(N)
              # and we just added to currEnt to describe this attr's ent.

          if(currEnt<maxEnt):
              maxEnt = currEnt
              splitter = i.name
          if(currEnt == maxEnt and i.name < splitter):
              maxEnt = currEnt
              splitter = i.name
      # found what to split on

      splitterAttr = currAttrs.__getitem__(splitter)
      currAttrs.remove(splitterAttr)
      # now we have the attr we would like to split with regard to...
      levelSplit = []
      # loop through all the different value possibilities of the chosen attribute
      for i in splitterAttr.values:
          # Everything in this dataset will have the same value for the splitting attr
          iExs = dataset.DataSet()
          for j in data:
              # if we find a piece of data that has splitter attr == current i possibility
              if(j.get_value(splitterAttr) == i):
                  iExs.append(j)
          # now we have a section of the data that share the chosen attr
          # Making sure we actually have some data
          if(iExs.__len__() != 0):
              levelSplit.append([splitterAttr.name, i, self.iteration(iExs, currAttrs)])
          elif(iExs.__len__() == 0):
              levelSplit.append([splitterAttr.name, i, '<'+maxClass+'>'])
      return levelSplit

  def testStep(self, example, ls, classifier):
      if(isinstance(ls, str)):
          return(ls[1:-1] == example.get_value(classifier))
      else:
          attr = ls[0][0]
          for i in ls:
              #print(i)
              if(i[1] == example.get_value(attr)):
                  return self.testStep(example, i[2], classifier)
