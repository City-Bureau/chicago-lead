# -*- coding: UTF-8 -*-

import sys

import numpy as np
import pandas as pd

df = pd.read_csv(sys.stdin)

for string in ('Follow Up', 'Follow-Up', 'repair', 'Test 2'):
	retest_rows = df.loc[df['fixture_location'].str.contains(string)].index.values
	df.drop(retest_rows, inplace=True)

df = df.ix[:, [2, 0, 1, 3]]

df.to_csv(sys.stdout, index=False)