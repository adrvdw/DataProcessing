#!/usr/bin/env python
# Name: Ad Ruigrok van der Werve
# Student number: 11323760
"""
This script visualizes data obtained from a .csv file
"""

import csv
import matplotlib.pyplot as plt
import numpy

# Global constants for the input file, first and last year
INPUT_CSV = "movies.csv"
START_YEAR = 2008
END_YEAR = 2018

# Global dictionary for the data
data_dict = {str(key): [] for key in range(START_YEAR, END_YEAR)}

if __name__ == "__main__":

    with open(INPUT_CSV, newline='') as csvfile:
         movies = csv.reader(csvfile)
         year = int(START_YEAR)
         counter = 0
         for row in movies:
             rating = row[1]
             year = row[2]
             if counter > 1:
                 data_dict[year].append(rating)
             counter += 1
    average_list = []

    for key in range(START_YEAR, END_YEAR):
        string_list = data_dict[str(key)]
        float_list = []

        for value in string_list:
            value = float(value)
            float_list.append(value)

        length = float(len(float_list))
        summed = sum(float_list)
        average_list.append(summed / length)

plt.xticks(range(START_YEAR, END_YEAR))
plt.yticks([8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8, 8.9])
plt.plot(range(START_YEAR, END_YEAR), average_list)
plt.axis([START_YEAR -1 , END_YEAR, 8.1, 8.9])
plt.grid()
plt.show()
