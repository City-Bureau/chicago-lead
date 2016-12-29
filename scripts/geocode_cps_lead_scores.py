import sys

import numpy as np
import pandas as pd

df = pd.read_csv(sys.stdin)

# import fusion table from cps portal
fusion = pd.read_csv('raw/cps_lead_fusion_table.csv')
fusion.columns = [c.lower() for c in fusion.columns]

# fix one filename (missing .pdf), remove incorrect filename (williams hs dupe)
fusion.loc[fusion.schoolname == 'FALCONER', 'filename'] = 'Individualschool_Falconer_609910.pdf'
fusion.loc[fusion.schoolname == 'BRONZEVILLE HS', 'filename'] = np.nan

fusion['schoolname'] = fusion['schoolname'].str.title()

# join results with lat/long from fusion table
geo = pd.merge(df, fusion[['filename', 'lat', 'long', 'schoolname']], on='filename', how='left')
geo = geo[['schoolname', 'score', 'num_fixtures', 'lat', 'long']]

geo.to_csv(sys.stdout, index=False)