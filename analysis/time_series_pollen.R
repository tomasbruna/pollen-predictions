# Author: Dongjo Ban
# Script for performing time series analysis part of the pollen project.

# Import required libraries for the analysis
library(imputeTS)
library(tseries)
library(forecast)

# Set local work directory
setwd("/Users/dban8/Desktop/")
series = read.csv(file = "mergedData_2.csv", sep =",", header = TRUE)

# Add a column at the end with merged dates in the format YYYY-MM-DD
series$Date <- as.Date(with(series, paste(Year, Month, Day,sep="-")), "%Y-%m-%d")

# Select dates ranging from January of 1992 to December of 2017 (Take only full years into account)
series = series[198:9687,]

# Create a time series object
pollen.counts<-ts(series$Total.Count, frequency = 365, start = c(1992,1,1))

# Impute missing values (linear by default) to handle NA entries
pollen.na = na.interpolation(pollen.counts)

# Plot the time series to examine its properties
plot(pollen.na)

# Draw a linear line to examine if deterministic trend can be observed
abline(reg = lm(pollen.na~time(pollen.na)))

# Plot ACF and PACF to further examine the time series
acf(pollen.na);
pacf(pollen.na);

# Decompose time series into seasonal, trend, and residual components
pollen.na.stl <- stl(pollen.na, s.window="periodic")

# 3 plots in single window
par(mfrow=c(3,1))
ts.plot(pollen.na.stl$time[,1]); title('Seasonal')
ts.plot(pollen.na.stl$time[,2]); title('Trend')
ts.plot(pollen.na.stl$time[,3]); title('Remainder')

# Check to see if there is a deterministic trend by fitting a linear line through the Trend
par(mfrow=c(1,1))
ts.plot(pollen.na.stl$time[,2]); title('Trend')
abline(reg = lm(pollen.na.stl$time[,2]~time(pollen.na.stl$time[,2])))

# Tests for determining stationarity
# Dickey Fuller test
adf.test(pollen.na, alternative="stationary")
# KPSS test
kpss.test(pollen.na, null="Trend")

# Fit best ARIMA model for the pollen dataset
fit <- auto.arima(pollen.na, D=1)
# Predict 1 year ahead
forecast <- forecast(fit, h=365)
# Plot to see how the predictions look like
plot(forecast)

# Predict 2 years ahead
forecast <- forecast(fit, h=730)
plot(forecast)


# Predict 5 years ahead
forecast <- forecast(fit, h=1825)
plot(forecast)