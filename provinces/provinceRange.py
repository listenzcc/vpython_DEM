'''
FileName: provinceRange.py
Author: Chuncheng
Version: V0.0
Purpose: Fetch the range of provinces.
'''

# %%
import pandas as pd

# %%
url = r'https://blog.csdn.net/esa72ya/article/details/114642127'

# %%

table = pd.read_html(url)[0]
table

# %%
table['lonMin'] = table['经度范围'].map(lambda x: x.split('~')[0])
table['lonMax'] = table['经度范围'].map(lambda x: x.split('~')[1])

table['latMin'] = table['纬度范围'].map(lambda x: x.split('~')[0])
table['latMax'] = table['纬度范围'].map(lambda x: x.split('~')[1])

table
# %%
table['cmd'] = 'eio clip -o ' + table['省名'] + '-30m-DEM.tif --bounds ' + \
    table['lonMin'] + ' ' + table['latMin'] + ' ' + \
    table['lonMax'] + ' ' + table['latMax']

table.to_csv('provinceRange.csv', encoding='gbk')

table
# %%
