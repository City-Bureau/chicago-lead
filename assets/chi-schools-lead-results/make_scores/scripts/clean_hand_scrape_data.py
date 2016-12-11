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

files = os.listdir('csv')

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

# garvey
gar = pd.read_csv('csv/%s' % files[2])
gar['filename'] = get_filename(files[2])
gar['school'] = get_name(files[2])
gar = gar.ix[:, [6, 0, 1, 2, 3, 4, 5]]
gar.columns = [i for i in range(0, 7)]

# juarez
jua = pd.read_csv('csv/%s' % files[3])
jua['filename'] = get_filename(files[3])
jua.drop('Facility ID', axis=1, inplace=True)
jua.columns = [i for i in range(0, 7)]
jua[0] = get_name(files[3])

# lasalle
las = pd.read_csv('csv/%s' % files[4])
las['filename'] = get_filename(files[4])
las['school'] = get_name(files[4])
las = las.ix[:, [6, 0, 1, 2, 3, 4, 5]]
las.columns = [i for i in range(0, 7)]

# sabin
sab = pd.read_csv('csv/%s' % files[5])
sab['filename'] = get_filename(files[5])
sab['school'] = get_name(files[5])
sab = sab.ix[:, [6, 0, 1, 2, 3, 4, 5]]
sab.columns = [i for i in range(0, 7)]

# skinner north
ski = pd.read_csv('csv/%s' % files[6])
ski['filename'] = get_filename(files[6])
ski['school'] = get_name(files[6])
ski = ski.ix[:, [6, 0, 1, 2, 3, 4, 5]]
ski.columns = [i for i in range(0, 7)]

# young
you = pd.read_csv('csv/%s' % files[7])
you['filename'] = get_filename(files[7])
you.drop(['Facility ID'], axis=1, inplace=True)
you.columns = [i for i in range(0, 8)]
you.loc[you[4].isnull(), 4] = you.loc[you[4].isnull()][5]
you.drop(5, axis=1, inplace=True)
you.columns = [i for i in range(0, 7)]
you[0] = get_name(files[7])
you.loc[you[2] == 'Hall outside West Dining Area Right\rFountain', 2] = 'Hall outside West Dining Area Right Fountain'

df = pd.concat([cas, col, gar, jua, las, sab, ski, you]).reset_index(drop=True)
df.drop(5, axis=1, inplace=True)
df.columns = ['school', 'sample', 'location', 'date', 'result', 'filename']

# remove carriage returns
df['location'] = df.location.str.replace('\r', ' ')

# spot clean collins
amend(116, 117, '51569-B-HAL-F08-002', '7.1')
amend(165, 166, '51569-1-HAL-F02-001')
amend(214, 213, '59651-1-POOL-WC04-005')

# spot clean juarez
amend(336, 335, '51570-1-KIT-KS05-02')
amend(364, 363, '51570-1-HAL-F04-05')
amend(392, 391, '51570-3-HAL-F05-03')
amend(420, 421, '51570-3-CUL-S01-01')
amend(434, 433, '51570-3-HAL-F01-05')
amend(435, 436, '50751-1-HAL-F01-01')
amend(464, 463, '50751-2-HAL-F02-05')
amend(465, 466, '50551-1-011-F01-01')

df.drop(df.loc[df.result.isnull()].index.values, inplace=True)

df.to_csv(sys.stdout, index=False)
