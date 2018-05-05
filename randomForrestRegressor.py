#!/usr/bin/env python

# Author: Saurabh Gulati
# Script using RandomForrestRegressor to predict pollen counts.

# Importing Libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import export_graphviz
import os

# Reading in the data
data = pd.read_csv('/home/saurabhg59/biostats/mergedDataInterpolatedReformatted.tsv',sep="\t")

# Dropping History columns to change number of days into future, drop just Day-1 to go 2 days into future. (Commented out)
# Drop nothing to predict 1 day in future.
# Currently all days are dropped to test the predictions based on just weather data.
data = data.drop(['Day-1','Day-2','Day-3','Day-4','Day-5'],axis=1)

# Columns based on which predictions will be made
X=data.drop(['totalCountsNoNa'],axis=1)

# Column which will be predicted
Y=data['totalCountsNoNa']

# Splitting data into training data and testing data
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.10)

# Builind model for RandomForrestRegressor, change this part to use other machine learning models.
model = RandomForestRegressor(max_depth=4, criterion="mse", num_estimators=25)

# Fitting the model
model.fit(X_train, Y_train)

# Making predictions based on fitted model
predictions = model.predict(X_test)

# Printing tree 1 to a file, remove this part if using other Machine learning models
export_graphviz(model.estimators_[0],
			   feature_names=X_train.columns,
			   filled=True,
			   rounded=True)

os.system('dot -Tpng tree.dot -o tree.png')

# Printing the R2 score
print("r2_score for RandomForestRegressor\n")
print(r2_score(Y_test,predictions))