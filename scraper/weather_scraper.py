#!/usr/bin/env python3
# Author: Dongjo Ban
# Scraper: implementation by harrisonpim using Beautiful Soup
# This script scrapes weather data from https://www.wunderground.com/weather/us/ga/atlanta/30301
# from 1991 up until 2018

from src.scrape_weather import *

weatherData = get_weather(years=list(range(1991,2018)))

weatherData.to_csv('weather_data.csv')