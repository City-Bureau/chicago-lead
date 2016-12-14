# -*- coding: UTF-8 -*-

import sys

import numpy as np
import pandas as pd

df = pd.read_csv(sys.stdin)

# move park names from headers to row attrs
header_rows = df.loc[df.result.isnull()].index
park_names = df.loc[df.result.isnull()]['fixture_location']
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
df['result_flag'] = df['result'].apply(lambda x: x.split(' ')[-1] if len(x.split(' ')) > 1 else '')
df['result'] = df['result'].apply(lambda x: x.split(' ')[0]).str.replace('˂', '<')

df.loc[1002, 'result'] = '3.09'
df.loc[1002, 'result_flag'] = 'J'

df.loc[2020, 'result'] = '0.243'
df.loc[2020, 'result_flag'] = 'J'

for string in ('Follow Up', 'Follow-Up', 'repair', 'Test 2'):
	retest_rows = df.loc[df['fixture_location'].str.contains(string)].index.values
	df.drop(retest_rows, inplace=True)

df = df.ix[:, [2, 0, 1, 3]]

df.to_csv(sys.stdout, index=False)