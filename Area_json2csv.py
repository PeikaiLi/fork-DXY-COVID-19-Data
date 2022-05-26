# -*- coding: utf-8 -*-
"""
Created on Thu May 26 18:39:00 2022

@author: Peikai_Li
"""
import os
import json
import datetime
import pandas as pd
from tqdm import tqdm

# from save2jc import Listener
# dict_parser = Listener().dict_parser


def dict_parser(document: dict, city_dict: dict = None) -> dict:
       result = dict()

       try:
           result['continentName'] = document['continentName']
           result['continentEnglishName'] = document['continentEnglishName']
       except KeyError:
           result['continentName'] = None
           result['continentEnglishName'] = None

       result['countryName'] = document['countryName']

       try:
           result['countryEnglishName'] = document['countryEnglishName']
       except KeyError:
           result['countryEnglishName'] = None

       result['provinceName'] = document['provinceName']
       result['provinceEnglishName'] = document.get('provinceEnglishName')
       result['province_zipCode'] = document.get('locationId')
       result['province_currentConfirmedCount'] = document.get('currentConfirmedCount')
       result['province_confirmedCount'] = document['confirmedCount']
       result['province_suspectedCount'] = document['suspectedCount']
       result['province_curedCount'] = document['curedCount']
       result['province_deadCount'] = document['deadCount']

       result['province_comment'] = document.get('comment')
       result['province_highDangerCount'] = document.get('highDangerCount')      
       result['province_midDangerCount'] = document.get('midDangerCount')
       result['province_detectOrgCount'] = document.get('detectOrgCount')               
       result['province_vaccinationOrgCount'] = document.get('vaccinationOrgCount')          


       if city_dict:
           result['cityName'] = city_dict['cityName']
           result['cityEnglishName'] = city_dict.get('cityEnglishName')
           result['city_zipCode'] = city_dict.get('locationId')
           result['city_currentConfirmedCount'] = city_dict.get('currentConfirmedCount')
           result['city_confirmedCount'] = city_dict['confirmedCount']
           result['city_suspectedCount'] = city_dict['suspectedCount']
           result['city_curedCount'] = city_dict['curedCount']
           result['city_deadCount'] = city_dict['deadCount']
           result['city_highDangerCount'] = city_dict.get('highDangerCount') 
           result['city_midDangerCount'] = city_dict.get('midDangerCount')
           
           
       result['updateTime'] = datetime.datetime.fromtimestamp(int(document['updateTime']/1000))

       return result


if __name__ == "__main__":
    
    with open("datas/DXYArea.json",'r',encoding = "utf-8") as load_f:
        history_dict = json.load(load_f)
        
    print(type(history_dict))
    
 
    structured_results = list()
    for document in tqdm(history_dict):
        if document.get('cities', None):
            for city_counter in range(len(document['cities'])):
                city_dict = document['cities'][city_counter]
                structured_results.append(dict_parser(document=document, city_dict=city_dict))
        else:
            structured_results.append(dict_parser(document=document))

    df = pd.DataFrame(structured_results)
    df.to_csv(
        path_or_buf=os.path.join(
            os.path.split(os.path.realpath(__file__))[0], 'history_dict' + '.csv'),
        # os.path.split(os.path.realpath(__file__))[0] 当前文件夹 == pwd
        index=False, encoding='utf_8_sig', float_format="%i"
        )