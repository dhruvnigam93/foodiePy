import json as json
import pandas as pd
import requests as requests
zipCodes = pd.read_csv('zipcodesMumbai.csv')

class ZomatoAPI:
    baseurl = 'https://developers.zomato.com/api/v2.1'
    headers = {'Accept': 'application/json', 'user-key': '7e6aa3545186fe321e5af45fa705646c'}

    proxyDict = {
        "http": "http://bloombecg:Dnpd1234@hkproxy01.int.clsa.com:8080/",
        "https": "https://bloombecg:Dnpd1234@hkproxy01.int.clsa.com:8080/",
    }

    def searchquery(self, search_str,start ):
        retval = requests.get(self.baseurl +'/search?entity_id=3&entity_type=city&q=' + search_str + '&start=' + start.__str__(), headers=self.headers , proxies = self.proxyDict , verify = False).content
        print(self.baseurl +'/search?q=' + search_str)
        retvaljson = json.loads(retval)
        return retvaljson

    def jsonTodf(self, jsonObj):
        df = pd.DataFrame()
        for i in range(1,jsonObj['restaurants'].__len__()):
            #General info
            id = jsonObj['restaurants'][i]['restaurant']['id']
            name = jsonObj['restaurants'][i]['restaurant']['name']
            cuisines = jsonObj['restaurants'][i]['restaurant']['cuisines']
            average_cost_for_two = jsonObj['restaurants'][i]['restaurant']['average_cost_for_two']
            
            #Location info
            locality = jsonObj['restaurants'][i]['restaurant']['location']['locality']
            locality_verbose = jsonObj['restaurants'][i]['restaurant']['location']['locality_verbose']
            address = jsonObj['restaurants'][i]['restaurant']['location']['address']
            
            #Rating Info
            aggregate_rating = jsonObj['restaurants'][i]['restaurant']['price_range']
            votes = jsonObj['restaurants'][i]['restaurant']['price_range']
            price_range = jsonObj['restaurants'][i]['restaurant']['price_range']
            price_range = jsonObj['restaurants'][i]['restaurant']['price_range']
            price_range = jsonObj['restaurants'][i]['restaurant']['price_range']

            restData = pd.DataFrame({  })

