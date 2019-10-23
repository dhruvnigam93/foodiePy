

import pandas as pd
from zmtAPI import *

def getRestaurantDetails(zmt_api , locality):
    """
    API call with locality string to fetch 100 restaurants
    """
    retDf = pd.DataFrame()
    for i in range(0,100,20):
        ret= zmt.searchquery(locality,i)
        if len(ret['restaurants'])!=0 : # non empty serch result
            temp =zmt.jsonTodf(ret)
            retDf = retDf.append(temp)
    return retDf
        

def getSubLocalities(address_list , locality , n_most_common):
    """
    From an address list of iven locality - returns n_most_common sub localities
    """
    import re
    step1 = [re.sub(', | ,', ',', x, flags=re.IGNORECASE) for x in address_list] # remove spaces between commas
    step2 = [re.sub(',' + locality.lower() + '(.*)', '', x, flags=re.IGNORECASE) for x in step1] # remove everything after sub locality
    step3 = [re.sub('(.*),', '', x, flags=re.IGNORECASE) for x in step2] # remove everything afer sub locality
    from collections import Counter
    c = Counter(step3)
    most_common = c.most_common(n_most_common)
    sub_locality = [most_common[i][0] for i in range(len(most_common))]
    return sub_locality

mumbai_localitiy = pd.read_csv('zipCodesMumbai.csv') # read list of mumbai localities
zmt = ZomatoAPI() # zomato API object
nRest = 0
all_restaurants = pd.DataFrame() # intialise restautants df with 0 obs

for locality in mumbai_localitiy['Location']:
    print('started for locality' ,locality )
    retDf_locality = getRestaurantDetails(zmt , locality)
    
    if len(retDf_locality)==0 :
        continue
    
    all_restaurants = pd.concat([all_restaurants,retDf_locality]).drop_duplicates().reset_index(drop=True) # add non duplicate values to all resaurants 

    sub_localities = getSubLocalities(retDf_locality['address'] , locality , 10)
    for sub_locality in sub_localities :
        print('in locality ' ,locality , ' searching for ' ,  sub_locality )
        retDf_sub_locality = getRestaurantDetails(zmt , locality)
        all_restaurants = pd.concat([all_restaurants,retDf_sub_locality]).drop_duplicates().reset_index(drop=True)
    print( all_restaurants.shape[0] - nRest , " restaurants added for locality ", locality )
    nRest = all_restaurants.shape[0]

pd.to_pickle(all_restaurants , path='restaurant_data1')

