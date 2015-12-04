# -*- coding: utf-8 -*-
from __future__ import division  

global DataDict
# global tempfeatures
# tempfeatures = []
DataDict = {}


import math
import operator
import random
import csv
import itertools


def makeDecisionTree(dataSet, features):
    resultList = [item[-1] for item in dataSet]
    # for i in resultList:
    #   print(i)
    if resultList.count(resultList[0]) == len(resultList):    
        return resultList[0]
    if len(dataSet[0]) == 1:    #if no feature remains
        return majorityVoting(resultList)       #return node that has the most vote
    bestFeatNo = findBestFeature(dataSet)
    bestFrature = features[bestFeatNo]
    # ID3tree = {bestFeatNo:{}} #generate root node of tree
    tree = {bestFrature:{}}

    # tempfeatures = features
    deletedFeature = features[bestFeatNo]
    # del(features[bestFeatNo]) #delete used node from featureSet
    featuresNew = []
    for i in range(len(features)):
      if not i == bestFeatNo:
        featuresNew.append(features[i])


    featValues = [item[bestFeatNo] for item in dataSet]    
    uniqueValues = set(featValues)
    for value in uniqueValues:

    #     for feature in features
        # subfeatures = features
      subfeatures = featuresNew[:]
      tree[bestFrature][value] = makeDecisionTree(splitDataSet(dataSet, bestFeatNo, value), subfeatures) #use recurse to generate next node
    return tree

def findBestFeature(dataSet):
    numFeatures = len(dataSet[0])-1   #number of features
    originalEntropy = calculateEntropy(dataSet) #calculate the original entropy
    bestInfoGain = 0.0; bestFeature = -1
    for i in range(numFeatures):   
        featureSet = set([item[i] for item in dataSet])   #
        newEntropy= 0.0
        for value in featureSet:
            subdataSet = splitDataSet(dataSet, i, value)
            prob = len(subdataSet)/float(len(dataSet))
            newEntropy += prob * calculateEntropy(subdataSet)   #the entropy of selected feature
        infoGain = originalEntropy - newEntropy
        if infoGain > bestInfoGain:
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

def majorityVoting(resultList):
    classCount = {}
    for vote in resultList:
        if vote not in classCount.keys():
            classCount[vote] = 0;
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key = operator.itemgetter(1), reverse = True)  #generate result by majority voting
    return sortedClassCount[0][0]



def splitDataSet(dataSet, axis, value):
    retdataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retdataSet.append(reducedFeatVec)
    return retdataSet


def calculateEntropy(dataSet):  
    numEntries = len(dataSet)  
    labelCounts = {}  
    for featVec in dataSet:  
        currentLabel = featVec[-1]  
        if currentLabel not in labelCounts.keys():  
            labelCounts[currentLabel] = 0  
        labelCounts[currentLabel] += 1  
    entropy = 0.0  
  
    for key in labelCounts:  
        prob = float(labelCounts[key])/numEntries  
        if prob != 0:  
            entropy -= prob*math.log(prob,2)  
    return entropy




def generateClassResult(tree, features, testVec):
    if isinstance(tree,dict):
      firstStr = tree.keys()[0]
    else:
      return tree
          # in case there is only one root node in the tree.
    
    secondDict = tree[firstStr]
    featIndex = features.index(firstStr)   
    classLabel = testVec[-1]
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = generateClassResult(secondDict[key], features, testVec)
            else: classLabel = secondDict[key]
    return classLabel
###
def generateData():
  csvfile = file('politics.csv', 'rb') 
  reader = csv.reader(csvfile)
  alldata = []
  for line in reader:
    alldata.append(line)
  csvfile.close()
  # print(len(alldata) "data in total") 
  features = []
  for feature in alldata[0]:
    features.append(feature) # generate featureSet
  features = features[:-1] # get rid of the class from featureSet
  subsetIndex = []
  featureSubSet = []
  loop = int(math.sqrt(len(features)))
  while(loop):
    index = int(random.uniform(0,len(features)))

    if index not in subsetIndex:
      subsetIndex.append(index)
      loop = loop -1
  subsetIndex.sort()
  # print("index of feature sub set is :" + repr(subsetIndex))
  for index in subsetIndex:
    featureSubSet.append(features[index])
  print(featureSubSet)
  print("*"*50)
  for j in range(len(alldata[0])):
    valueSet = []
    for i in range(len(alldata)):
      valueSet.append(alldata[i][j])
      DataDict[alldata[0][j]] = valueSet
  dataSet = []
  for i in range(1,len(alldata)):
    dataSet.append(alldata[i]) #generate dataSet
  # print(len(dataSet),len(features),len(dataSet[1]),dataSet[1][2])
  n = len(features)
  while(n):
  #using while loop to delete the data in the data set
    if features[n-1] not in featureSubSet:
      #ensure it goes to 0 because loop will cease when n = 0
      for q in range(len(dataSet)):
        del(dataSet[q][n-1])
    n = n - 1



  # for n in range(len(features)):
  #   if features[n] not in featureSubSet:
  #     for q in range(len(dataSet)):
  #       print(q,n,len(dataSet[q]))
  #       del(dataSet[q][n])
  #       n = n-1

      
        
        
  return dataSet,featureSubSet



def most_common(L):
  # get an iterable of (item, iterable) pairs
  SL = sorted((x, i) for i, x in enumerate(L))
  # print 'SL:', SL
  groups = itertools.groupby(SL, key=operator.itemgetter(0))
  # auxiliary function to get "quality" for an item
  def _auxfun(g):
    item, iterable = g
    count = 0
    min_index = len(L)
    for _, where in iterable:
      count += 1
      min_index = min(min_index, where)
    # print 'item %r, count %r, minind %r' % (item, count, min_index)
    return count, -min_index
  # pick the highest-count/earliest item
  return max(groups, key=_auxfun)[0]

def generateForest(split, sizeOfForest):
  if split >= 1 or split <= 0:
    print("must input a valid split number!!!")


  trees = []
  for i in range(sizeOfForest):
    print("The "+repr(i+1)+"th tree is generated, the features in that tree is:")

    dataSet,featureSubSet = generateData()
    splitNum = int(split*len(dataSet))
    trainingSet = dataSet[splitNum:]
    # print("trainingSet size is: " + repr(len(trainingSet)))
    testSet = dataSet[:splitNum]
    # print("testSet size is: " + repr(len(testSet)))  
    ID3= makeDecisionTree(trainingSet,featureSubSet)
    trees.append([ID3,featureSubSet,testSet,trainingSet])#generate trees

  

  accuracy = 0
  NumOfAccurateInstance = 0
  for i in range(len(trees[0][2])):
    resultsOfClass =[]
    for j in range(sizeOfForest):
      # print(trees[j][2],trees[j][1],trees[j][0][i],"here")
      resultsOfClass.append(generateClassResult(trees[j][0],trees[j][1],trees[j][2][i]))
    if most_common(resultsOfClass) == DataDict["class"][i+1]:
      NumOfAccurateInstance += 1
  accuracy = NumOfAccurateInstance/len(trees[0][2])
  print("There are " + repr(sizeOfForest) + " trees in the forest")
  print("Accuracy of decision tree when split=" + repr(split) + " is: " + repr(accuracy))



generateForest(0.6,5)
  # for i in range(len(alldata[0][2])):
  #   resultsOfClass = [] 
    
  #   for j in range(sizeOfForest):
  #     resultsOfClass.append(generateClassResult(alldata[j][0],alldata[j][1],alldata[j][2][i]))

  #   if most_common(resultsOfClass) == DataDict['class'][i+1]:
  #     NumOfAccurateInstance += 1
  # accuracy = NumOfAccurateInstance/len(alldata[0][2])
  # print("There are " + repr(sizeOfForest) + " trees in the forest")
  # print(accuracy)    





# def ID3classifier(split):
#   if split >= 1 or split <= 0:
#     print("must input a valid split number!!!")
#   dataSet,featureSet = generateData()
#   trainingSet = []
#   featureSubSet = random.sample(featureSet, int(math.sqrt(len(featureSet))))

#     # featureSubSet = featureSet[:2]

#   #generate feature set randomly without replacement, the length is the root value of the length of original feature set
#   # print dataSet
#   for i in range(len(featureSet)):
#     if featureSet[i] not in featureSubSet:
#       for j in range(len(dataSet)):
#         del(dataSet[j][i])

#   trainingSet = dataSet[int(split*len(dataSet)):]
#   testSet = dataSet[:int(split*len(dataSet))]


#   # # print len(trainingSet)
#   # for i in range(int(len(trainingSet)/2)):   #bag size = 50%
#   #   subTrainingSet.append(trainingSet[int(random.uniform(0,len(trainingSet)))]) #random generate sub training set with replacement
#   # print("sub training set size is: " + repr(len(subTrainingSet)))


#   # print("trainingSet size is: " + repr(len(trainingSet)))
#   # testSet = dataSet[:int(split*len(dataSet))]
#   # print("testSet size is: " + repr(len(testSet)))
#   ID3tree = makeDecisionTree(trainingSet,featureSubSet)

#   # dataSet,featureSet = generateData()
#   # NumOfAccurateInstance = 0
#   # accuracy = 0
#   # for i in range(len(testSet)):
#   #   if generateClassResult(ID3tree,featureSet,testSet[i]) == DataDict['class'][i+1]:
#   #     NumOfAccurateInstance += 1

#   # # for i in range(len(testSet)):
#   # #   data = {}

#   # accuracy = NumOfAccurateInstance/len(testSet)
#   # print("Accuracy of decision tree when split=" + repr(split) + " is: " + repr(accuracy))
#   # print("\n"*3 +"Here is the stucture of ID3 decision tree:" ) 

#   return ID3tree, featureSubSet, testSet

# # ID3classifier(0.4)


# def generateForest(split,sizeOfForest):
  
#   alldata = []
#   if not isinstance(sizeOfForest,int):
#     print("please input a valid number for size of forest(must input a int number)")
#   else:
#     for i in range(sizeOfForest):
#       alldata.append(ID3classifier(split))

#   NumOfAccurateInstance = 0
#   accuracy = 0
#   print alldata

#   # print alldata[0][1]
#   # print alldata[0][2]
#   # print("-----")
#   # print alldata[1][0]
#   # print alldata[1][1]
#   # print alldata[1][2]   
#   # print alldata[0][2][1]
#   for i in range(len(alldata[0][2])):
#     resultsOfClass = [] 
#     # resultsdict = {} 
#     for j in range(sizeOfForest):
#       resultsOfClass.append(generateClassResult(alldata[j][0],alldata[j][1],alldata[j][2][i]))

#     if most_common(resultsOfClass) == DataDict['class'][i+1]:
#       NumOfAccurateInstance += 1
#   accuracy = NumOfAccurateInstance/len(alldata[0][2])
#   print("There are " + repr(sizeOfForest) + " trees in the forest")
#   print(accuracy)

# generateForest(0.6,1)





#     # if generateClassResult(trees[i],featureSet,testSet[i]) == DataDict['class'][i+1]:
#     #   NumOfAccurateInstance += 1




#     # print data

# # ID3classifier(0.5)




