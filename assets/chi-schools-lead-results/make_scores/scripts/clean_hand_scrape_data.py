# coding: utf-8

import os
import sys

import pandas as pd

def get_name(f):
    return f.split('_')[-2].title()

def get_filename(f):
    filename = f.split('-')[-1].split('.')[0]
    filename += '.pdf'
    return filename

def amend(wrong, right, sample, result=[]):
    df.loc[wrong] = df.loc[right]
    df.loc[wrong, 'sample'] = sample
    if bool(result):
        df.loc[wrong, 'result'] = result    

files = [f for f in os.listdir('csv') if f.split('.')[-1] == 'csv']

# cassell
cas = pd.read_csv('csv/%s' % files[0])
cas['filename'] = get_filename(files[0])
cas['school'] = get_name(files[0])
cas = cas.ix[:, [6, 0, 1, 2, 3, 4, 5]]
cas.columns = [i for i in range(0, 7)]

# collins
col = pd.read_csv('csv/%s' % files[1], skiprows=1)
col = col.ix[:, [1, 3, 4, 5, 6, 7]]
col['pdf'] = get_filename(files[1])
col.columns = [i for i in range(0, 7)]

# falconer
fal = pd.read_csv('csv/%s' % files[2])
fal['pdf'] = get_filename(files[2])
fal['school'] = get_name(files[2])
fal = fal.ix[:, [6, 0, 1, 2, 3, 4, 5]]
fal.columns = [i for i in range(0, 7)]

# garvey
gar = pd.read_csv('csv/%s' % files[3])
gar['filename'] = get_filename(files[3])
gar['school'] = get_name(files[3])
gar = gar.ix[:, [6, 0, 1, 2, 3, 4, 5]]
gar.columns = [i for i in range(0, 7)]

# juarez
jua = pd.read_csv('csv/%s' % files[4])
jua['filename'] = get_filename(files[4])
jua.drop('Facility ID', axis=1, inplace=True)
jua.columns = [i for i in range(0, 7)]
jua[0] = get_name(files[4])

# lasalle
las = pd.read_csv('csv/%s' % files[5])
las['filename'] = get_filename(files[5])
las['school'] = get_name(files[5])
las = las.ix[:, [6, 0, 1, 2, 3, 4, 5]]
las.columns = [i for i in range(0, 7)]

# sabin
sab = pd.read_csv('csv/%s' % files[6])
sab['filename'] = get_filename(files[6])
sab['school'] = get_name(files[6])
sab = sab.ix[:, [6, 0, 1, 2, 3, 4, 5]]
sab.columns = [i for i in range(0, 7)]

# skinner north
ski = pd.read_csv('csv/%s' % files[7])
ski['filename'] = get_filename(files[7])
ski['school'] = get_name(files[7])
ski = ski.ix[:, [6, 0, 1, 2, 3, 4, 5]]
ski.columns = [i for i in range(0, 7)]

# young
you = pd.read_csv('csv/%s' % files[8])
you['filename'] = get_filename(files[8])
you.drop(['Facility ID'], axis=1, inplace=True)
you.columns = [i for i in range(0, 8)]
you.loc[you[4].isnull(), 4] = you.loc[you[4].isnull()][5]
you.drop(5, axis=1, inplace=True)
you.columns = [i for i in range(0, 7)]
you[0] = get_name(files[8])

df = pd.concat([cas, col, fal, gar, jua, las, sab, ski, you]).reset_index(drop=True)
df.drop(5, axis=1, inplace=True)
df.columns = ['school', 'sample', 'location', 'date', 'result', 'filename']

# remove carriage returns
df['location'] = df.location.str.replace('\r', ' ')

# spot clean collins
amend(116, 117, '51569-B-HAL-F08-002', '7.1')
amend(165, 166, '51569-1-HAL-F02-001')
amend(214, 213, '59651-1-POOL-WC04-005')

# spot clean juarez
amend(482, 481, '51570-1-KIT-KS05-02')
amend(510, 509, '51570-1-HAL-F04-05')
amend(538, 537, '51570-3-HAL-F05-03')
amend(566, 567, '51570-3-CUL-S01-01')
amend(580, 579, '51570-3-HAL-F01-05')
amend(581, 582, '50751-1-HAL-F01-01')
amend(610, 609, '50751-2-HAL-F02-05')
amend(611, 612, '50551-1-011-F01-01')

df.drop(df.loc[df.result.isnull()].index.values, inplace=True)

df.to_csv(sys.stdout, index=False)
