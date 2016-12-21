# coding: utf-8

import sys

import pandas as pd

df = pd.read_csv(sys.argv[1], header=0)

# drop all-null rows, rows with no result value
df.drop(df.loc[(df.school.isnull()) | (df.result.isnull())].index.values, inplace=True)

# remove incomplete data (replaced in hand scrape data) 
for s in ('Tanner', 'Powell'):
    df.drop(df[df.school == s].index.values, inplace=True)

# move sample columns to the correct place where misread
df.loc[~df['sample'].str.contains('-'), 'sample'] = df.loc[~df['sample'].str.contains('-')]['location']

# spot cleaning
df = df.append(pd.DataFrame([
    ['Zapata', '1-E-CS02-51', 'Room 105 - North', '6/3/16 6:50 AM', '27.6', 
     'http://www.cps.edu/SiteCollectionDocuments/LeadTesting/Individualschool_Zapata_609973.pdf']
    ], columns=[c for c in df.columns]))

df = df.append(pd.DataFrame([
    ['Orr', '51558-1-HAL-F05', 'Main- Next to Room 118, Fountain', '10/12/16 6:00 AM', '530', 
     'http://www.cps.edu/SiteCollectionDocuments/LeadTesting/IndividualSchool_Orr_610389.pdf']
    ], columns=[c for c in df.columns]))

df.loc[(df.school == 'Zapata') & (df.result.isnull()), 'result'] = 'None Detected'
df.loc[(df.school == 'Camras') & (df['sample'] == '3-N-F03-30'), 'result'] = 'None Detected'
df.loc[(df.school == 'Cvca') & (df['sample'] == '51625-1-113-S01-04'), 'result'] = 'None Detected'

# remove collins (added back in manual rescrape)
collins = df.loc[df.school.str.lower() == 'collinshs'].index.values
df.drop(collins, inplace=True)

# grab filename from source url and drop source url
df['filename'] = df['pdf'].apply(lambda x: x.split('/')[-1])
df.drop('pdf', axis=1, inplace=True)

df.to_csv(sys.stdout, index=False)
