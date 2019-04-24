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
            restData = pd.DataFrame({  })
