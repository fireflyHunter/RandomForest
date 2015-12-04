ID3.py(question1)
Randombootstrap.py(question2)
FeatureSelection.py(question3)
CombinationRandomForest.py(question4)

The 4 python file can run directly(has no import connection between 4 files).

The python file are all commented, email me(hao.wu.2@ucdconnect.ie) if require any further explanation.

For any python file in those 4, Find and change the following code in the function “def generateData()” if you want to test specified csv file:
csvfile = file('banks.csv', 'rb') 
If you want to test tennis.csv, just directly change it to: 
csvfile = file(‘politics.csv', 'rb') 

(The default csv file is politics.csv)

