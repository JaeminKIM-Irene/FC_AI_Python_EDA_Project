#===================================================================================================================
#                                                  국가코드정보 API 세팅
#===================================================================================================================
from urllib import parse
import requests
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import *

class CountryCodeApi():
  
  # 초기화  
  def __init__(self, apiKey):
    self.apiKey = apiKey
    self.url = 'https://api.odcloud.kr/api/15076566/v1/uddi:b003548e-3d28-42f4-8f82-e64766b055bc?'
    self.params = {
                    'page': '1',
                    'perPage': '250',
                    'returnType': 'JSON',
                    'serviceKey': apiKey,
                  }
    
  #  API로 부터 json데이터 받아오기
  def getJsonDataByCountryInfo(self):
      response = requests.get(self.url, params=self.params)
      jsonData = response.json()
      return jsonData

    
  # json데이터에서 미가공된 국가 리스트 추출(한글명)
  @staticmethod    
  def getKorCountryNameByList(jsonData):
      rawKorCoutryList = [item['국가명(국문)'] for item in jsonData['data']]
      return rawKorCoutryList
    
  @staticmethod    
  # json데이터에서 미가공된 국가 리스트 추출(영문명)
  def getEngCountryNameByList(jsonData):
      rawEngCoutryList = [item['국가명(영문)'] for item in jsonData['data']]
      return rawEngCoutryList
    
  #-------------------------
  # 국가정보 데이터 프레임 생성함수 
  #-------------------------
  @staticmethod
  def makeDataFromStatistics(Data) :
      countryDataFrame = pd.DataFrame()
      countryInfo = pd.DataFrame.from_dict([Data])
      countryDataFrame = pd.concat([countryDataFrame, countryInfo])
      countryDataFrame = Utils.resetIndexForDataFrame(countryDataFrame) # 인덱스 초기화
      
      return countryDataFrame
    