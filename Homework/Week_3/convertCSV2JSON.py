import csv
import json
import pandas as pd

INPUT_CSV = "knmi.tsv"

input = pd.read_csv(INPUT_CSV)

id = "STN"
datum = "YYYYMMDD"
max_temp = "TX"

input = input[[id, datum, max_temp]]

j = input.set_index('YYYYMMDD').to_json("data.json", orient='index')
