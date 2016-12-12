import sys

import pandas as pd

df = pd.read_csv(sys.stdin)

df['processed_result'] = pd.to_numeric(df['result_value'], errors='coerce')
df.fillna(0, inplace=True)

df['exceeds_epa'] = df['processed_result'].apply(lambda x: 0 if x < 15 else 1)

scored_df = pd.DataFrame(
    {'score': df.groupby(['park_name'])['exceeds_epa'].mean(),
     'num_fixtures': df.groupby(['park_name'])['fixture_location'].count()}
).reset_index()

with sys.stdout as f:
    f.write(scored_df)
