#!/usr/bin/env python

# Author: Saurabh Gulati
# Script for predicitng misisng pollen levels which will be used to predict future pollen levels.

# Importing the libraries needed
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV

# Reading in the data
data = pd.read_csv('/home/saurabhg59/biostats/mergeddataCategorical.tsv',sep="\t")

# Creating LabelEncoder model to encode Events
le = LabelEncoder()
le.fit(data['Events'])
data['Events']=le.transform(data['Events'])

data["Events"] = data["Events"].astype('category')

# Removing totalCounts column
data=data.drop(['totalCounts'],axis=1)

# Keeping only lines that have pollen levels
data1=data.dropna(axis=0,how='any')

# Keeping only lines that do not have pollen levels
data2=data[pd.isnull(data['weedLevel'])]


# Creating training data, i.e. all lines that have pollen levels available
XweedTrain=data1.drop(['weedLevel','treeLevel','grassLevel'],axis=1)
YweedTrain=data1['weedLevel']

XtreeTrain=data1.drop(['treeLevel','weedLevel','grassLevel'],axis=1)
YtreeTrain=data1['treeLevel']

XgrassTrain=data1.drop(['grassLevel','treeLevel','weedLevel'],axis=1)
YgrassTrain=data1['grassLevel']

# Creating Test data, i.e. lines which did not have pollen levels available (This will be predicted)
XweedTest=data2.drop(['weedLevel','treeLevel','grassLevel'],axis=1)
YweedTest=data2['weedLevel']

XtreeTest=data2.drop(['treeLevel','weedLevel','grassLevel'],axis=1)
YtreeTest=data2['treeLevel']

XgrassTest=data2.drop(['grassLevel','treeLevel','weedLevel'],axis=1)
YgrassTest=data2['grassLevel']

# Dropping the individual levels from data that will be used to fit the model
data2=data2.drop(['grassLevel','treeLevel','weedLevel'],axis=1)
data1temp=data1[['grassLevel','treeLevel','weedLevel']].copy()
data1=data1.drop(['grassLevel','treeLevel','weedLevel'],axis=1)

# Building customized models for level prediction, these parameters were found using GridSearchCV.
modelWeed = RandomForestClassifier(n_estimators=20,max_depth=6,n_jobs=-1)
modelTree = RandomForestClassifier(n_estimators=20,max_depth=10,n_jobs=-1)
modelGrass = RandomForestClassifier(n_estimators=20,max_depth=12,n_jobs=-1)

# Fitting the models
modelWeed.fit(XweedTrain, YweedTrain)
modelTree.fit(XtreeTrain, YtreeTrain)
modelGrass.fit(XgrassTrain, YgrassTrain)

# Making predictions using the fitted models
predictionsWeed = modelWeed.predict(XweedTest)
predictionsTree = modelTree.predict(XtreeTest)
predictionsGrass = modelGrass.predict(XgrassTest)

# Unencoding the events column
data1['Events']=le.inverse_transform(data1['Events'])
data2['Events']=le.inverse_transform(data2['Events'])

# Printing the predicted weed levels to a new file
data2['weedLevel']=predictionsWeed
data1['weedLevel']=data1temp['weedLevel']

weedValues=pd.concat([data1,data2],axis=0,join='outer')
weedValues.to_csv("/home/saurabhg59/biostats/weedValues.csv",sep=",")
### the file has to manually sorted before using in next script, also history columns have to be added manually
data1=data1.drop(['weedLevel'],axis=1)
data2=data2.drop(['weedLevel'],axis=1)


# Printing the predicted grass levels to a new file
data2['grassLevel']=predictionsGrass
data1['grassLevel']=data1temp['grassLevel']
grassValues=pd.concat([data1,data2],axis=0,join='outer')
grassValues.to_csv("/home/saurabhg59/biostats/grassValues.csv",sep=",")
### the file has to manually sorted before using in next script, also history columns have to be added manually
data1=data1.drop(['grassLevel'],axis=1)
data2=data2.drop(['grassLevel'],axis=1)


# Printing the predicted tree levels to a new file
data2['treeLevel']=predictionsTree
data1['treeLevel']=data1temp['treeLevel']
treeValues=pd.concat([data1,data2],axis=0,join='outer')
treeValues.to_csv("/home/saurabhg59/biostats/treeValues.csv",sep=",")
### the file has to manually sorted before using in next script, also history columns have to be added manually
data1=data1.drop(['treeLevel'],axis=1)
data2=data2.drop(['treeLevel'],axis=1)