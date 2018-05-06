#!/usr/bin/env python

# Author: Saurabh Gulati
# Script for predicting future pollen levels based on past pollen levels and weather data.

# Importing the libraries needed
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV

# Reading in the data
grassData = pd.read_csv('/home/saurabhg59/biostats/grassValues.csv',sep=",")
treeData = pd.read_csv('/home/saurabhg59/biostats/treeValues.csv',sep=",")
weedData = pd.read_csv('/home/saurabhg59/biostats/weedValues.csv',sep=",")

# Creating LabelEncoder model to encode Events
eventLe = LabelEncoder()
eventLe.fit(treeData['Events'])
grassData['Events']=eventLe.transform(grassData['Events'])
treeData['Events']=eventLe.transform(treeData['Events'])
weedData['Events']=eventLe.transform(weedData['Events'])

# Creating LabelEncoder model to encode past pollen levels
dayLe = LabelEncoder()
dayLe.fit(treeData['Day-1'])
treeData['Day-1']=dayLe.transform(treeData['Day-1'])
treeData['Day-2']=dayLe.transform(treeData['Day-2'])
treeData['Day-3']=dayLe.transform(treeData['Day-3'])
treeData['Day-4']=dayLe.transform(treeData['Day-4'])

grassData['Day-1']=dayLe.transform(grassData['Day-1'])
grassData['Day-2']=dayLe.transform(grassData['Day-2'])
grassData['Day-3']=dayLe.transform(grassData['Day-3'])
grassData['Day-4']=dayLe.transform(grassData['Day-4'])

weedData['Day-1']=dayLe.transform(weedData['Day-1'])
weedData['Day-2']=dayLe.transform(weedData['Day-2'])
weedData['Day-3']=dayLe.transform(weedData['Day-3'])
weedData['Day-4']=dayLe.transform(weedData['Day-4'])

# Making the X and Y variables, i.e. columns that will be used to predict and column that will be predicted
weedX=weedData.drop(['weedLevel'],axis=1)
weedY=weedData['weedLevel']

treeX=treeData.drop(['treeLevel'],axis=1)
treeY=treeData['treeLevel']

grassX=grassData.drop(['grassLevel'],axis=1)
grassY=grassData['grassLevel']

# Building default models
modelWeed = RandomForestClassifier(n_estimators=20,n_jobs=-1)
modelTree = RandomForestClassifier(n_estimators=20,n_jobs=-1)
modelGrass = RandomForestClassifier(n_estimators=20,n_jobs=-1)

# Creating a parameter grid to test different tree depths
param_grid = {
    "max_depth": range(1, 7)
}

# Predicting pollen levels using the parameter grid, i.e. using different models of varying tree depth and finding the best model
gridSearchWeed = GridSearchCV(modelWeed, param_grid=param_grid, cv=10)
gridSearchWeed.fit(weedX, weedY)
print("WEED\n")
print(gridSearchWeed.best_params_)
print(gridSearchWeed.best_score_)

gridSearchTree = GridSearchCV(modelTree, param_grid=param_grid, cv=10)
gridSearchTree.fit(treeX, treeY)
print("\nTREE\n")
print(gridSearchTree.best_params_)
print(gridSearchTree.best_score_)

gridSearchGrass = GridSearchCV(modelGrass, param_grid=param_grid, cv=10)
gridSearchGrass.fit(grassX, grassY)
print("\nGRASS\n")
print(gridSearchGrass.best_params_)
print(gridSearchGrass.best_score_)