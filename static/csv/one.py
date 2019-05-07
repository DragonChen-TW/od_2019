import os, csv
import pandas as pd
import matplotlib.pyplot as plt

data_dir = './'
csv_name = '107_12_people.csv'
f_csv = os.path.join(data_dir, csv_name)
csv_data = pd.read_csv(f_csv, header=0, skiprows=1)

print(csv_data.head())
# print(csv_data['老化指數'].value_counts())
print(csv_data['老化指數'].describe())

old_point = csv_data['老化指數']
plt.hist(old_point)
