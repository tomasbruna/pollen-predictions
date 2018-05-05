# Author: Saurabh Gulati
# Script for interpolating pollen counts and weather data for machine learning part of pollen project.

# Import required libraries for the analysis
library(imputeTS)

# Reading the input file
series = read.csv(file = "mergedData_2.csv", sep =",", header = TRUE)

# Impute missing values (linear by default) to handle NA entries
totalCountsNoNa = na.interpolation(series$totalCounts)
humidityAvgNoNa = na.interpolation(series$humidityAvg)
humidityHighNoNa = na.interpolation(series$humidityHigh)
humidityLowNoNa = na.interpolation(series$humidityLow)
precipitationNoNa = na.interpolation(series$precipitation)
temperatureAvgNoNa = na.interpolation(series$temperatureAvg)
temperatureHighNoNa = na.interpolation(series$temperatureHigh)
temperatureLowNoNa = na.interpolation(series$temperatureLow)
windAvgNoNa = na.interpolation(series$windAvg)
windHighNoNa = na.interpolation(series$windHigh)
windLowNoNa = na.interpolation(series$windLow)

output=data.frame(totalCountsNoNa,humidityAvgNoNa,humidityHighNoNa,humidityLowNoNa,precipitationNoNa,temperatureAvgNoNa,temperatureHighNoNa,temperatureLowNoNa,windAvgNoNa,windHighNoNa,windLowNoNa)

write.table(output,file="mergedDataInterpolated.tsv",sep="\t")

# After this there is a manual step to add Day of year, and past pollen counts to the file and create mergedDataInterpolatedReformatted.tsv