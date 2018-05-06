#!/usr/bin/env python

# Author: Saurabh Gulati
# Script to compare different machine learning models for pollen project.

# Importing libraries
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.svm import NuSVR
from sklearn.ensemble import RandomForestRegressor

# Reading in the input file
data = pd.read_csv('/home/saurabhg59/biostats/mergedDataInterpolatedReformatted.tsv',sep="\t")

# Columns that will be used for prediction
X=data.drop(['totalCountsNoNa'],axis=1)

# Column which will be predicted
Y=data['totalCountsNoNa']

# Making default models
model1 = RandomForestRegressor(max_depth=10, random_state=0)
model2 = MLPRegressor(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(10,10), random_state=1)
model3 = NuSVR(C=1.0, nu=0.1)

# Chosing ranges of paramters to be tested for each model
param_grid1 = {
    "n_estimators": range(5, 30, 5),
    "max_depth": range(4, 10)
    "criterion":["mse","mae"]
}

param_grid2 = {
    "C": [50,100],
    "kernel":["rbf","linear"]
}

param_grid2 = {
    "hidden_layer_sizes": [(10,10),(12,12),(10,10,10),(10)],
}

# Performing GridSearch for RandomForrestRegressor
gridSearch = GridSearchCV(model1, param_grid=param_grid1, cv=10)
gridSearch.fit(X, Y)
print("RandomForestRegressor\n")
print(gridSearch.best_params_)
print(gridSearch.best_score_)

# Performing GridSearch for Support Vector Regressor
gridSearch = GridSearchCV(model2, param_grid=param_grid2, cv=10)
gridSearch.fit(X, Y)
print("NuSVR\n")
print(gridSearch.best_params_)
print(gridSearch.best_score_)

# Performing GridSearch for Neural Network
gridSearch = GridSearchCV(model3, param_grid=param_grid3, cv=10)
gridSearch.fit(X, Y)
print("MLPRegressor\n")
print(gridSearch.best_params_)
print(gridSearch.best_score_)