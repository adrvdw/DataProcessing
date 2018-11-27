#!/usr/bin/env python
# Name: Ad Ruigrok van der Werve
# Student number: 11323760

import json
import csv
import pandas as pd

input = pd.read_csv('index.csv', usecols=[0,5,6])

location = input["LOCATION"]
time = input["TIME"]
value = input["Value"]


data = input.take(range(116,173))

with open ('index.json', 'w') as f:
    json = data.to_json(orient = "records")
    f.write(json)
