import sys

import numpy as np
import pandas as pd

df = pd.read_csv(sys.argv[1], names=[i for i in range(0, 4)])

# get columns in order
# $ sed -e 's/^"",*//' -e 's/,"",""/,""/' tabula-Water_Fountain_Testing_Final_Results.csv

# blank col, name col, value col, blank col
rows = df.loc[df[0].isnull() & df[3].isnull()].index.values
df.iloc[rows, 0] = df.iloc[rows][1]
df.iloc[rows, 1] = df.iloc[rows][2]

# blank col, name col, blank col, value col
rows = df.loc[df[0].isnull() & df[2].isnull()].index.values
df.iloc[rows, 0] = df.iloc[rows][1]
df.iloc[rows, 1] = df.iloc[rows][3]

# blank col, blank col, name col, value col
rows = df.loc[df[0].isnull() & df[1].isnull()].index.values
df.iloc[rows, 0] = df.iloc[rows][2]
df.iloc[rows, 1] = df.iloc[rows][3]

# name col, blank col, blank col, value col
df.loc[df[1].isnull() & df[2].isnull(), 1] = df.loc[df[1].isnull() & df[2].isnull()][3]

# name col, blank col, value col, blank col
df.loc[df[0].notnull() & df[1].isnull() & df[2].notnull(), 1] = df.loc[df[0].notnull() & df[1].isnull() & df[2].notnull()][2]

# remove dummy cols
df.drop([2], axis=1, inplace=True)
df.rename(columns={0: 'fixture_location', 1: 'result_value', 2: 'park_name'}, inplace=True)


# remove indoor/outdoor rows
df['fixture_location'] = df['fixture_location'].str.rstrip()
df.drop(list(df.loc[df['fixture_location'].isin(['Indoor', 'Outdoor', 'Oudoor'])].index.values), inplace=True)


# move park names from headers to row attrs
header_rows = df.loc[df.result_value.isnull()].index
park_names = df.loc[df.result_value.isnull()]['fixture_location']
park_objects = list(zip(header_rows, park_names))

for ind, park_obj in enumerate(park_objects):
    start, park = park_obj
    try:
        end = park_objects[ind+1][0] - 1
    except IndexError:
        end = len(df)
    df.loc[start:end, 'park_name'] = park
    
df.drop(list(header_rows), inplace=True)


# spot cleaning
df['result_flag'] = df['result_value'].apply(lambda x: x.split(' ')[-1] if len(x.split(' ')) > 1 else '')
df['result_value'] = df['result_value'].apply(lambda x: x.split(' ')[0]).str.replace('˂', '<')

df.loc[1002, 'result_value'] = '3.09'
df.loc[1002, 'result_flag'] = 'J'

df.loc[2020, 'result_value'] = '0.243'
df.loc[2020, 'result_flag'] = 'J'

df.loc[df['park_name'].str.contains('Logan').index.values, 'park_name'] = 'Logan Square Skate Park'

for string in ('Follow Up', 'Follow-Up', 'repair', 'Test 2'):
	retest_rows = df.loc[df['fixture_location'].str.contains(string)].index.values
	df.drop(retest_rows, inplace=True)

df = df.ix[:, [2, 0, 1, 3]]


with sys.stdout as f:
    f.write(df)