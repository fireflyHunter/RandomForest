# -*- coding: utf-8 -*-
from __future__ import division  

global DataDict
global tempfeatures
tempfeatures = []
DataDict = {}

import math
import operator

import csv
def generateData():
  csvfile = file('tennis.csv', 'rb') 
  reader = csv.reader(csvfile)
  alldata = []
  for line in reader:
    alldata.append(line)

  csvfile.close()
  # print(len(alldata) "data in total") 
  features = []

  for feature in alldata[0]:
    features.append(feature) # generate featureset
  features = features[:-1] # get rid of the class value from featureset
  featurestemp = features

  for j in range(len(alldata[0])):
    valueSet = []
    for i in range(len(alldata)):
      valueSet.append(alldata[i][j])
      DataDict[alldata[0][j]] = valueSet
  dataset = []
  for i in range(1,len(alldata)):
    dataset.append(alldata[i]) #generate dataset 
  return dataset,features


def calculateEntropy(dataset):  
  #calculate the entropy of given data set
    numEntries = len(dataset)  
    labelCounts = {}  
    for featVec in dataset:  
        currentLabel = featVec[-1]  
        if currentLabel not in labelCounts.keys():  
            labelCounts[currentLabel] = 0  
        labelCounts[currentLabel] += 1  

    entropy = 0.0
    #in case it automaticlly converted to int
  
    for key in labelCounts:  
        prob = float(labelCounts[key])/numEntries  
        if prob != 0:  
            entropy -= prob*math.log(prob,2)  
    return entropy

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
    numFeatures = len(dataSet[0]) - 1   #number of features
    originalEntropy = calculateEntropy(dataSet) #calculate the original entropy
    bestInfoGain = 0.0; bestFeature = -1
    for i in range(numFeatures):   
        featureSet = set([item[i] for item in dataSet])   #
        newEntropy= 0.0
        for value in featureSet:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calculateEntropy(subDataSet)   #the entropy of selected feature
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
    sortedClassCount = sorted(classCount.iteritems(), key = operator.itemgetter(1), reverse = True)
    # print("bingo!",repr(sortedClassCount[0][0]))
     #generate result by majority voting
    return sortedClassCount[0][0]



def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet






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





def ID3classifier(split):
  if split >= 1 or split <= 0:
    print("must input a valid split number!!!")
  dataSet,featureSet = generateData()
  trainingSet = []
  testSet = []
  splitNum = int(split*len(dataSet))
  trainingSet = dataSet[splitNum:]
  print("trainingSet size is: " + repr(len(trainingSet)))
  testSet = dataSet[:splitNum]
  print("testSet size is: " + repr(len(testSet)))
  # print(featureSet)
  ID3tree = makeDecisionTree(trainingSet,featureSet)
  # print(featureSet)
  # dataSet,featureSet = generateData()
  NumOfAccurateInstance = 0
  accuracy = 0
  for i in range(len(testSet)):
    if generateClassResult(ID3tree,featureSet,testSet[i]) == DataDict['class'][i+1]:
      NumOfAccurateInstance += 1

  # for i in range(len(testSet)):
  #   data = {}

  accuracy = NumOfAccurateInstance/len(testSet)
  print("Accuracy of decision tree when split=" + repr(split) + " is: " + repr(accuracy))
  print("\n"*3 +"Here is the stucture of ID3 decision tree:" )
  print ID3tree
# ID3classifier(0.4)
# def test():
#   dataSet,featureSet = generateData()
#   ID3tree = makeDecisionTree(dataSet,featureSet)
#   dataSet,featureSet = generateData()
#   result = []
#   num = 0
#   for i in range(len(dataSet)):
#     if generateClassResult(ID3tree,featureSet,dataSet[i]) == '':
#       result.append("error")
#       num += 1
#     else:
#       result.append(generateClassResult(ID3tree,featureSet,dataSet[i]))
#   print(result,num)
    




ID3classifier(0.6)
# a,b = generateData()
# for i in range (len(a)):
#   print a[i]
#   del(a[i][3])


# print("-----------")
# for i in range (len(a)):
#   print a[i]
# print(b[3])
# # test()
    # print makePrection(tree,data)



    # print data

    




def entropyCal(a):
  NumYes = 5
  NumNo = 3
  p = NumYes/(NumNo+NumYes)
  q = 1-p
  print q,p
  entropy = -p*math.log(p,2)-q*math.log(q,2)
  return entropy