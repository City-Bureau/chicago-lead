import sys

import numpy as np
import pandas as pd

df1 = pd.read_csv(sys.argv[1], header=0)
df2 = pd.read_csv(sys.argv[2], header=0)

df = pd.concat([df1, df2])

# count expected zero values (below threshold/none str values)
counts = dict(df.result.value_counts())
zero_keys = [key for key in counts.keys() if '<' in key] + ['None Detected', 'ND']
zero_counts = [v for k, v in counts.items() if k in zero_keys]
effective_zero_values = sum(list(zero_counts))

# convert, coercing str values to NaN
df['result'] = pd.to_numeric(df['result'], errors='coerce')
df['result'].fillna(0, inplace=True)

# check actual zero values against converted
if effective_zero_values == df['result'].value_counts()[0]:

    # generate id from sample serial num
    df['location_id'] = df['sample'].apply(lambda x: '-'.join(x.split('-')[:-1]))
    # binary var encode scores
    df['exceeds_epa'] = df['result'].apply(lambda x: 0 if x < 15 else 1)

    # generate df with mean of trial scores for each fixture
    location_id = pd.DataFrame(
        {'score': df.groupby(['school', 'location_id', 'filename'])['exceeds_epa'].mean()}
    ).reset_index()

    # generate df with mean fixture score for each school
    test_schools = pd.DataFrame(
        {'score': location_id.groupby(['school', 'filename'])['score'].mean(),
         'num_fixtures': location_id.groupby(['school', 'filename'])['location_id'].count()}
    ).reset_index()

    test_schools.to_csv(sys.stdout, index=False)

else:

    with sys.stdout as f:
        f.write('u\'ve got sum cleanin to do')