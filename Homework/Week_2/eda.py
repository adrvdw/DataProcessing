#!/usr/bin/env python
# Name: Ad Ruigrok van der Werve
# Student number: 11323760
# """
# This script visualizes data obtained from a .csv file
# """

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

INPUT_CSV = "input.csv"
input = pd.read_csv(INPUT_CSV)
list_gdp = []


country = "Country"
region = "Region"
pop_density = "Pop. Density (per sq. mi.)"
infant_mortality = "Infant mortality (per 1000 births)"
gdp = "GDP ($ per capita) dollars"


input[gdp] = input[gdp].str.strip("dollars")
input = input.replace("unknown", np.NaN)
input[region] = input[region].str.strip()



input[gdp] = input[gdp].astype(float)
input[infant_mortality] = input[infant_mortality].str.replace(',', '.').astype(float)
list_gdp = input[gdp].tolist()
list_gdp.remove(max(list_gdp))

input = input[[country,region,pop_density,infant_mortality,gdp]]


# mean = input[gdp].mean()
# print(mean)
# median = input[gdp].median()
# print(median)
# mode = input[gdp].mode()
# print(mode)
# standard_dev = input[gdp].std()
# print(standard_dev)


# cleaned_gdp_list = [x for x in list_gdp if str(x) != 'nan']
#
# plt.hist(cleaned_gdp_list, bins=50)
# plt.xlabel('x')
# plt.ylabel('y')
# plt.show()

# five_number_summary = input[infant_mortality].describe()
# plt.boxplot(five_number_summary)
# plt.xlabel('x')
# plt.ylabel('y')
# plt.show()


# d = input.set_index('Country').to_dict('index')
# print(d)

j = input.set_index('Country').to_json("input.json", orient='index')
print(j)

# out = input.to_json("input.json", orient='rev')
