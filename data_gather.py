#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 11:38:52 2019

@author: dhruv
"""

import pandas as pd
from zmtAPI import *

def getRestaurantDetails(zmt_api , locality):
    retDf = pd.DataFrame()
    for i in range(0,100,20):
        ret= zmt.searchquery(locality,i)
        if len(ret['restaurants'])==0 :
        temp =zmt.jsonTodf(ret)
        retDf = retDf.append(temp)
    return retDf
        

def getSubLocalities(address_list , locality , n_most_common):
    import re
    step1 = [re.sub(', | ,', ',', x, flags=re.IGNORECASE) for x in address_list] # remove spaces between commas
    step2 = [re.sub(',' + locality.lower() + '(.*)', '', x, flags=re.IGNORECASE) for x in step1] # remove everything after sub locality
    step3 = [re.sub('(.*),', '', x, flags=re.IGNORECASE) for x in step2] # remove everything afer sub locality
    from collections import Counter
    c = Counter(step3)
    most_common = c.most_common(n_most_common)
    sub_locality = [most_common[i][0] for i in range(len(most_common))]
    return sub_locality

mumbai_localitiy = pd.read_csv('zipCodesMumbai.csv')
zmt = ZomatoAPI()
#totalRestaurantes = zmt.searchquery('mumbai',0)
#totalRestaurantes = totalRestaurantes['results_found']
all_restaurants = pd.DataFrame()

for locality in mumbai_localitiy['Location']:
    print('started for locality' ,locality )
    retDf_locality = getRestaurantDetails(zmt , locality)
    if len(retDf_locality)==0 :
        continue
    all_restaurants = pd.concat([all_restaurants,retDf_locality]).drop_duplicates().reset_index(drop=True)
    sub_localities = getSubLocalities(retDf_locality['address'] , locality , 10)
    for sub_locality in sub_localities :
        print('in locality ' ,locality , ' searching for ' ,  sub_locality )
        retDf_sub_locality = getRestaurantDetails(zmt , locality)
        all_restaurants = pd.concat([all_restaurants,retDf_sub_locality]).drop_duplicates().reset_index(drop=True)


