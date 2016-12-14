import sys

import pandas as pd

df = pd.read_csv(sys.argv[1])

df['processed_result'] = pd.to_numeric(df['result'], errors='coerce')
df.fillna(0, inplace=True)

df['exceeds_epa'] = df['processed_result'].apply(lambda x: 0 if x < 15 else 1)

pd.DataFrame(
    {'score': df.groupby(['park_name'])['exceeds_epa'].mean(),
     'num_fixtures': df.groupby(['park_name'])['fixture_location'].count()}
).reset_index().to_csv(sys.stdout, index=False)