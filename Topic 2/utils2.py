#===================================================================================================================
#                                                  유틸기능 모듈 주제2
#===================================================================================================================

import csv
from collections import OrderedDict
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class Utils2():
    
    #-------------------------
    # 1. 대륙별 데이터 프레임 생성함수 
    #-------------------------
    @staticmethod
    def getContinentalDataFrameFromCSV(fileName) :
        '''
        instruction : 
            info   : CSV파일을 가져온뒤 월단위 필터링을 하여 데이터 프레임을 생성\n 
            param  : 원본 대륙별 CSV파일 (ex : './asia_data_kor.csv')\n
            return : 선택한 대륙의 데이터프레임 을 필터링하여 리턴 
        '''   
        newDataFrame =  pd.read_csv(fileName,encoding='utf-8-sig')
        newDataFrame = newDataFrame.iloc[0:233]
        return newDataFrame
    
    #-------------------------
    # 2. 국가별 데이터 프레임 생성함수 
    #-------------------------
    @staticmethod
    def getCountryDataFrame(continentalDataFrame,countryNameKor) :
        '''
        instruction : 
            info   : 대륙별 데이터프레임에서 특정국가를 선택 하여 데이터 프레임을 생성\n 
            param  : 대륙 데이터 프레임,선택국가명(한글)\n
            return : 선택한 국가의 데이터를 리턴 
        '''   
        if f'{countryNameKor}_명수' in continentalDataFrame.columns:
            numVisitors = continentalDataFrame[f'{countryNameKor}_명수'] / 10000
            numVisitors.fillna(0, inplace=True)
            annualGrowthRate = continentalDataFrame[f'{countryNameKor}_전년대비']
            annualGrowthRate.fillna(0, inplace=True)
            
            visitYear  = continentalDataFrame.Year
            visitYear.fillna(method='ffill', inplace=True)

            visitMonth  = continentalDataFrame.month
            visitMonth.fillna(method='ffill', inplace=True)            

            newDataFrame = pd.DataFrame({
                                            'Year': visitYear,
                                            'Month': visitMonth,
                                            'NumVisitors': numVisitors,
                                            'annualGrowthRate': annualGrowthRate,
                                         })

        else:
            print(f"There is no '{countryNameKor}_명수' \n해당 컬럼이 존재하지 않습니다.")
            
        return newDataFrame    
    
    
    
    #-------------------------
    # 3-1-1. 날짜 데이터타입 변환함수
    #-------------------------
    @staticmethod
    def changeYearAndMonthDtypeToInt(countryDataFrame) :    
        
        # 'Year' 컬럼에서 숫자만 추출하여 정수형으로 변환
        countryDataFrame['Year'] = countryDataFrame['Year'].str.replace('년', '').astype(int)

        # 'Month' 컬럼에서 숫자만 추출하여 정수형으로 변환
        countryDataFrame['Month'] = countryDataFrame['Month'].str.replace('월', '').astype(int)

        # Year와 Month 컬럼을 결합하여 새로운 datetime 형식의 컬럼 생성
        countryDataFrame['Date'] = pd.to_datetime(countryDataFrame[['Year', 'Month']].assign(DAY=1))    

        # DataFrame의 인덱스를 초기화 (기존 인덱스는 삭제)
        countryDataFrame.reset_index(drop=True, inplace=True)

        return countryDataFrame   
    
    #-------------------------
    # 3-1-1. 날짜 데이터타입 변환함수
    #-------------------------
    @staticmethod
    def changeYearAndMonthDtypeToObject(countryDataFrame) :    
        
        # 'Year' 컬럼에서 숫자를 문자열로 변환하고, 뒤에 '년' 문자열 추가
        countryDataFrame['Year'] = countryDataFrame['Year'].astype(str) + '년'

        # 'Month' 컬럼에서 숫자를 문자열로 변환하고, 뒤에 '월' 문자열 추가
        countryDataFrame['Month'] = countryDataFrame['Month'].astype(str) + '월'


        return countryDataFrame   
        

    
    #-------------------------
    # 3-2. 데이터 날짜 필터링 하여 추출하는 함수
    #-------------------------
    @staticmethod
    def extractDataByDateFilter(countryDataFrame,startDate,endDate) :    
        '''
        instruction : 
            info   : \n 
            param  : 국가데이터프레임 ,시작날짜('yyyy-MM-dd') , 종료날짜('yyyy-MM-dd')\n
            return : 선택한 국가데이터프레임에서 사용자가 입력한 날짜 데이터만을 필터링후 추출하여 리턴 
        '''   
        # pandas의 to_datetime 함수를 사용해 문자열 형태의 날짜를 datetime 객체로 변환
        startDate = pd.to_datetime(startDate)
        endDate = pd.to_datetime(endDate)

        # 'Date' 컬럼이 시작 날짜와 종료 날짜 사이에 있는지 확인하는 조건으로 데이터 필터링
        selectedData = countryDataFrame[(countryDataFrame['Date'] >= startDate) & (countryDataFrame['Date'] <= endDate)]
         
        return selectedData
        
    #-------------------------
    # 3-3. 국가 데이터프레임의 컬럼을 재정렬 하는 함수
    #-------------------------
    @staticmethod
    def arrangeDataFrameColumns(countryDataFrame) :    
        '''
        instruction : 
            info   : \n 
            param  : 국가데이터프레임 ,시작날짜('yyyy-MM-dd') , 종료날짜('yyyy-MM-dd')\n
            return : 선택한 국가데이터프레임에서 사용자가 입력한 날짜 데이터만을 필터링후 추출하여 리턴 
        '''   
        orderedData = countryDataFrame[
                                        ['Year','Month','Date','NumVisitors','annualGrowthRate']
                                      ]
         
        return orderedData
    
    #-------------------------
    # 3-3. 데이터프레임에서 시작과 끝 년월을 문자열로 추출하는 함수
    #-------------------------
    @staticmethod
    def getStrYearAndMonth(countryDataFrame) :    
        '''
        instruction : 
            info   : \n 
            param  : 국가데이터프레임\n
            return : 날짜 필터링된 국가데이터프레임에서 시작과 끝 날짜의 문자열을 리턴 
        '''   
        startYear = countryDataFrame.iloc[0]['Year']
        startMonth = countryDataFrame.iloc[0]['Month']

        endYear = countryDataFrame.iloc[-1]['Year']
        endMonth = countryDataFrame.iloc[-1]['Month']
    
         
        return startYear , startMonth , endYear, endMonth
        
    
    


    
    #-------------------------
    # 2 데이터 프레임에 인덱스 초기화 함수(T)
    #-------------------------
    @staticmethod
    def resetIndexForDataFrame(df):
        '''
        instruction : 
            True  : 기존 인덱스는 삭제, 기존의 인덱스 정보는 완전히 사라짐
            False  : 기존의 인덱스가 새로운 열로 추가
        '''
        resetedIndexData =  df.reset_index(drop=True)
        return resetedIndexData
    


#===================================================================================================================
#                                                  현재 사용안함
#===================================================================================================================  

#   #-----------------
    
#   # 1-1 CSV파일에서 특정 컬럼의 값들만 추출하는 함수
#   @staticmethod
#   def extract_column_from_csv(file_path, column_name):
#       with open(file_path, 'r',encoding='utf-8-sig') as csvfile:
#           reader = csv.DictReader(csvfile)
#           return [row[column_name] for row in reader]

#   #-----------------
  
#   # 1-2 csv파일에서 추출한 국가정보 리스트에서 국가를 추출하는 함수(위 코드와 중복됨 삭제예정)
#   @staticmethod
#   def get_country_list_from_csv(country_info):
#       country_list = [ country for country in country_info]
#       return country_list
  
#   #-----------------
  
#   # 1-3 문자열을 받아온뒤 쪼개서 리스트로 반환하는 함수
#           # notice : 문자열을 입력받아 
#           # 공백으로 쪼갠뒤, 리스트로 리턴한다.
#   @staticmethod
#   def get_splited_string_list(string) :
#       splited_string_list = string.split()
#       return splited_string_list
  
#   #-----------------
  
#   # 1-5 두 개의 리스트를 비교하여 
#   #     중복되는 문자열을 반환하는 함수
#   @staticmethod
#   def get_one_duplicate_string_from_two_lists(source_list, filter_list):
#     set2 = set(filter_list)
#     duplicates = set()
    
#     for item in source_list:
#         if item in set2:
#             duplicates.add(item)
#         elif duplicates:
#             return next(iter(duplicates))
#     return None
  
#   #-----------------
  
# #   # 1-5 두 개의 리스트를 비교하여 
# #   #     중복되는 문자열리스트를 반환하는 함수
# #   @staticmethod
# #   def get_duplicate_string_from_two_list(source_list, filter_list):
# #       # 이중리스트 제거
# #       flat_filter_list = Utils.get_flatten_list(filter_list)
      
# #       # 중복 문자열 제거
# #       duplicate_list = [
# #           source_item 
# #           for source_item in source_list 
# #           if source_item in flat_filter_list
# #       ]
      
# #       return duplicate_list
  
# #   #-----------------
  
#   # 1-6 리스트 요소의 중복제거 함수
#   @staticmethod
#   def get_unique_values(lst):
#       return list(OrderedDict.fromkeys(lst))

#   #-----------------
  
#   # 1-7 이중 리스트 해제(평탄화) 함수
#   @staticmethod
#   def get_flatten_list(lst):
#       return [item for sublist in lst for item in sublist]

#   #-----------------
  
#   # 1-8 두 개의 리스트를 비교하여 
#   #     문자열 중복시 True 값을 반환하는 함수
#   @staticmethod
#   def get_boolean_list_of_duplicates(source_list, filter_list):
#       # 이중리스트 제거
#       flat_filter_list = Utils.get_flatten_list(filter_list)
      
#       # 중복 여부 확인
#       boolean_duplicate_list = [
#           True if source_item in flat_filter_list else False 
#           for source_item in source_list 
#       ]
      
#       return boolean_duplicate_list
  
#   #-----------------  
  
  
# #-----------------
  
#   # 1-9 단일 요소를 리스트로 만드는 함수
#   @staticmethod
#   def formatStringToList(str):
#         resultList = [str]
#         return resultList
  
# #-----------------  





# # 아이템에서 비디오 데이터와 비디오 ID를 추출
# def extract_video_data(item):
#     videoDataFrame = pd.DataFrame(item['snippet'])
#     videoId = item['id']['videoId']

#     return videoDataFrame, videoId





# def make_df(dictData) : 
#     '''
#     instruction : 
#         텅빈 데이터생성후,
#         원본 딕셔너리 데이터에서, 스니펫(딕셔너리)과 비디오아이디(문자열) 추출,
#         concat으로 텅빈 videos 데이터프레임 에 새로 생성한 스니펫(딕셔너리)을 넣은 데이터프레임을 합치고
#         ignore_index으로 서로다른 데이터프레임의 인덱스 중복을 방지함,
#         videoDataFrame에서 불필요한 컬럼 삭제후
#         비디오 아이디 컬럼 추가       
#     '''
    
#     # 빈 데이터프레임과 리스트 생성
#     videoDataFrame = pd.DataFrame()
#     videoIds = []  
    
#     # 원본 딕셔너리 데이터에서 스니펫(딕셔너리)과 비디오아이디(문자열) 추출
#     # 각 아이템에 대해 비디오 정보와 ID를 추출
#     for item in dictData['items']:
#         video_data, video_id = extract_video_data(item)
        
#         # 비디오 정보 추가
#         videos = pd.concat([videos, video_data])
        
#         # 비디오 ID 추가
#         videoIds.append(video_id)
 
#     # 비디오 ID 리스트를 시리즈로 변환하고 이름 설정
#     videoIdsSeries = pd.Series(videoIds, name='videoId')
    
#     # 불필요한 컬럼 삭제    
#     videosCleaned = videos.drop(['high', 'medium']).reset_index(drop=True)
    
#     # 비디오 정보와 ID 결합
#     final_videos_df = pd.concat([videosCleaned, videoIdsSeries], axis=1)
    
#     return final_videos_df
        
#     # videoDataFrame.drop(['high', 'medium'], axis=1, inplace=True)  
#     # 비디오 아이디 컬럼 추가
#     videoDataFrame['videoId'] = videoIds  
#     return videoDataFrame 



    # #----------------------
    # # 데이터 프레임 생성함수 테스트
    # #----------------------    
    # def make_df(dictData) : 
    #     '''
    #     instruction : 
    #           텅빈 데이터생성후,
    #           원본 딕셔너리 데이터에서, 스니펫(딕셔너리)과 비디오아이디(문자열) 추출,
    #           concat으로 텅빈 videos 데이터프레임 에 새로 생성한 스니펫(딕셔너리)을 넣은 데이터프레임을 합치고
    #           ignore_index으로 서로다른 데이터프레임의 인덱스 중복을 방지함,
    #           videoDataFrame에서 불필요한 컬럼 삭제후
    #           비디오 아이디 컬럼 추가       
    #     '''
        
    #     # 텅빈 데이터생성
    #     videoDataFrame = pd.DataFrame()
    #     videoIds = []  
        
    #     # 원본 딕셔너리 데이터에서 스니펫(딕셔너리)과 비디오아이디(문자열) 추출
    #     for item in dictData['items']:  
    #         snippet = item['snippet'] 
    #         videoId = item['id']['videoId'] 

    #         # 데이터프레임 조합
    #         videoDataFrame = pd.concat([videoDataFrame, pd.DataFrame(snippet)], ignore_index=True)           
    #         # 리스트에 요소 추가
    #         videoIds.append(videoId) 
            
    #     # 불필요한 컬럼 삭제    
    #     videoDataFrame.drop(['high', 'medium'], axis=1, inplace=True)  
    #     # 비디오 아이디 컬럼 추가
    #     videoDataFrame['videoId'] = videoIds  

    #     return videoDataFrame  
    
    
    # # 비디오 조회수, 좋아요 수 등을 가져옴
    # def get_video_detail(df) : 
    #     counts = pd.DataFrame()

    #     for i in df['videoId'] :
    #         videoQuery = f"videos?part=statistics&maxResults=1&key={apiKey}&id={parse.quote(i)}"

    #         res = requests.get(url +  videoQuery)
    #         data = json.loads(res.text)
    #         data = data['items'][0]['statistics']
    #         data = pd.DataFrame.from_dict([data])

    #         counts = pd.concat([counts, data])

    #     return counts