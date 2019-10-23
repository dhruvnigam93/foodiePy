import json as json
import pandas as pd
import requests as requests

class ZomatoAPI:
    baseurl = 'https://developers.zomato.com/api/v2.1'
    headers = {'Accept': 'application/json', 'user-key': '7e6aa3545186fe321e5af45fa705646c'}

    proxyDict = {
        "http": "http://bloombecg:Dnpd1234@hkproxy01.int.clsa.com:8080/",
        "https": "https://bloombecg:Dnpd1234@hkproxy01.int.clsa.com:8080/",
    }

    nCalls = 0
    
    def searchquery(self,search_str,start, proxy=False):
        """
        queries the zomato API with search_str and returns meta data and at max 20 resluts
        
        Parameters:
        search_str (string)
        start (int)
        proxy (boolean) if connectin to internet through proxy 
        Returns:
        json
        """ 
        
        self.nCalls += 1
        
        assert self.nCalls < 950 , "Halted at current search due to hitting API threshold" + search_str # adhearing to API limits for zomato
            
        if(proxy):
            retval = (requests.get(
                self.baseurl + '/search?entity_id=3&entity_type=city&q=' + search_str + '&start=' + start.__str__(),
                                  headers=self.headers, proxies=self.proxyDict, verify=False).content).decode('utf-8')
        else:
            retval = (requests.get(
                self.baseurl + '/search?entity_id=3&entity_type=city&q=' + search_str + '&start=' + start.__str__(),
                headers=self.headers, verify=False).content).decode('utf-8')

        #print(self.baseurl +'/search?q=' + search_str)
        retvaljson = json.loads(retval)
        return retvaljson

    def jsonTodf(self, jsonObj):
        """ 
        Converts the json from Zomato to a pd df - 1 pbservation per restaurant
        
        Parameters:
        search_str (string)
        start (int)
        proxy (boolean) if connectin to internet through proxy 
        Returns:
        dataframe
        """
        df = pd.DataFrame()
        for i in range(0,jsonObj['restaurants'].__len__()):
            rest_object = jsonObj['restaurants'][i]['restaurant']

            #General info
            id = rest_object['id']
            name = rest_object['name']
            cuisines = rest_object['cuisines']
            average_cost_for_two = rest_object['average_cost_for_two']
            price_range = rest_object['price_range']
            establishment_type = ','.join(rest_object['establishment'])
            timings = rest_object['timings']

            #Location info
            locality = rest_object['location']['locality']
            locality_verbose = rest_object['location']['locality_verbose']
            address = rest_object['location']['address']
            latitude = rest_object['location']['longitude']
            longitude = rest_object['location']['latitude']

            #Rating Info
            aggregate_rating = rest_object['user_rating']['aggregate_rating']
            votes = rest_object['user_rating']['votes']

            df = df.append(pd.DataFrame({'id' : id , 'name' : name , 'cuisines' : cuisines , 'average_cost_for_two' :average_cost_for_two ,
                                      'price_range': price_range , 'extamblishment_type' : establishment_type , 'timings' : timings ,
                                      'locality' : locality , 'locality_verbose' : locality_verbose,
                                      'address' : address , 'latitude' : latitude , 'longitude' : longitude ,
                                      'aggregate_rating' : aggregate_rating,
                                      'votes' : votes} , index = [0]),ignore_index = True)

        return df



