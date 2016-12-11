# coding: utf-8

import sys

import pandas as pd

test = True if len(sys.argv) > 3 else False

df1 = pd.read_csv(sys.argv[1], header=0)
df2 = pd.read_csv(sys.argv[2], header=0)

df = pd.concat([df1, df2])

# check expected zero values against actual zero values after encoding
counts = dict(df.result.value_counts())
koi = [key for key in counts.keys() if '<' in key] + ['None Detected', 'ND']
coi = [v for k, v in counts.items() if k in koi]
effective_zero_values = sum(list(coi))

df['result'] = pd.to_numeric(df['result'], errors='coerce')
df['result'].fillna(0, inplace=True)

if effective_zero_values == df['result'].value_counts()[0]:

    if test:
        df.to_csv('school_reports.processed.csv', index=False)

    # generate id from sample serial num
    df['location_id'] = df['sample'].apply(lambda x: '-'.join(x.split('-')[:-1]))
    # binary var encode scores
    df['exceeds_epa'] = df['result'].apply(lambda x: 0 if x < 15 else 1)

    # generate df with mean of trial scores for each fixture
    location_id = pd.DataFrame({'score': df.groupby(['school', 'location_id', 'filename'])['exceeds_epa'].mean()}).reset_index()

    # generate df with mean fixture score for each school
    test_schools = pd.DataFrame(
        {'score': location_id.groupby(['school', 'filename'])['score'].mean(),
         'num_fixtures': location_id.groupby(['school', 'filename'])['location_id'].count()}
    ).reset_index()

    # import fusion table from cps portal
    fusion = pd.read_csv('cps_fusion_table.raw.csv')
    fusion.columns = [c.lower() for c in fusion.columns]

    # combine fusion table w lat/long
    geo = pd.merge(test_schools, fusion[['filename', 'lat', 'long', 'schoolname']], on='filename', how='left')
    geo['schoolname'] = geo['schoolname'].str.title()
    geo = geo[['schoolname', 'school', 'filename', 'score', 'num_fixtures', 'lat', 'long']]

    geo.to_csv(sys.stdout, index=False)

else:

    print('u got sum cleanin 2 do')