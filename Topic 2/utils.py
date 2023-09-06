#===================================================================================================================
#                                                  유틸기능 모듈
#===================================================================================================================

import csv
from collections import OrderedDict
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class Utils():

    #-------------------------
    # 1.1 데이터 프레임1 생성함수 
    #-------------------------
    @staticmethod
    def make_df(dictData): 
        """
        instruction : 

        YouTube API 응답에서 DataFrame을 생성

        1. 빈 DataFrame과 리스트를 생성
        2. 원본 딕셔너리 데이터의 각 항목에서 스니펫(딕셔너리)과 비디오ID(문자열)을 추출
           빈 DataFrame과 스니펫으로부터 생성된 새 DataFrame을 concat 함수로 결합하고
           ignore_index=True를 사용하여 서로 다른 DataFrame들 사이의 인덱스 중복을 방지
        3. 최종 DataFrame에서 불필요한 열들을 삭제
        4. 최종 DataFrame에 비디오 ID들의 열을 추가

           param : dictData: YouTube API 응답이 포함된 딕셔너리
           return : 처리된 YouTube 데이터가 포함된 pandas dataframe
         """

        # 빈 DataFrame과 리스트를 초기화
        videosDataFrame = pd.DataFrame()
        videoIds = []  

        # 원본 딕셔너리 데이터의 각 항목에서 스니펫(딕셔너리)과 비디오ID(문자열) 추출
        for item in dictData['items']:
            snippetDataFrame = pd.DataFrame([item['snippet']])
            videoId = item['id']['videoId']

            # videosDataFrame에  'snippetDataFrame' 결합
            videosDataFrame = pd.concat([videosDataFrame, snippetDataFrame], ignore_index=True)

            # 'videoId'를 'videoIds' 리스트에 추가 
            videoIds.append(videoId)
            
        # 필요 없는 컬럼 삭제 (해당하는 경우에만)
        if {'high', 'medium'}.issubset(videosDataFrame.columns) :
           videosDataFrame.drop(['high', 'medium'], axis=1, inplace=True)
        # 비디오ID 컬럼 추가 
        videosDataFrame['videoId'] = pd.Series(videoIds)
        
        # 인덱스 초기화
        videosDataFrame = Utils.resetIndexForDataFrame(videosDataFrame)
        
        return videosDataFrame 

    #-------------------------
    # 1.2 데이터 프레임2 생성함수 
    #-------------------------
    @staticmethod
    def makeDataFromStatistics(dictData) :
        countsData = pd.DataFrame()
        statisticsDataFrame = pd.DataFrame.from_dict([dictData])
        countsData = pd.concat([countsData, statisticsDataFrame])
        countsData = Utils.resetIndexForDataFrame(countsData) # 인덱스 초기화
        
        return countsData
    
    #-------------------------
    # 1.3 데이터 프레임에 인덱스 초기화 함수(T)
    #-------------------------
    @staticmethod
    def resetIndexForDataFrame(df):
        '''
        instruction : 
            True  : 기존 인덱스는 삭제, 기존의 인덱스 정보는 완전히 사라짐
            False  : 기존의 인덱스가 새로운 열로 추가
        '''
        return df.reset_index(drop=True)
    
    #-------------------------
    # 1.4 데이터 프레임에서 필요 없는 columns drop 및 재정렬
    #-------------------------
    @staticmethod
    def dropAndReorganizeColumns(df):
        df = df[['videoId', 'title', 'description', 'viewCount', 'likeCount', 'favoriteCount', 'commentCount', 
                 'publishedAt', 'channelId', 'channelTitle', 'country']]
        return df

    #-------------------------
    # 1.5 publishedAt 날짜 type으로 변환
    #-------------------------
    @staticmethod
    def changeTypeToDatetime(data):
        pubdate = pd.to_datetime(data)
        year = pubdate.dt.year.values[0]
        month = pubdate.dt.month.values[0]
        date = str(year) +'년' + str(month) + '월'
        return year, month, date
    
    #-------------------------    
    # 1.6 published 날짜의 visitor row 추출
    #-------------------------    
    @staticmethod
    def extractIndexOfVisitorRow(data, year, month):
        if (year > 2023) or (year >= 2023 and month > 6) :
            return -24
        bool_mask = (data['Year'] == (str(year) + '년')) & (data['month'] == (str(month) + '월'))
        published_idx = data[bool_mask].index.values[0]
        return published_idx
    


    #------------------------- 
    # 2.3 문자열을 받아온뒤 쪼개서 리스트로 반환하는 함수
    #------------------------- 
    @staticmethod
    def get_splited_string_list(string) :
        '''        
          instruction :  문자열을 입력받아 공백으로 쪼갠뒤, 리스트로 리턴한다.
        '''
        splited_string_list = string.split()
        return splited_string_list
    #-------------------------   
    # 2.5 두 리스트를 비교하여 중복문자열을 반환함수
    #-------------------------   
    @staticmethod
    def get_one_duplicate_string_from_two_lists(source_list, filter_list):
        '''
        info : 중복되는 문자열을 반환하는 함수
        '''
        set2 = set(filter_list)
        duplicates = set()

        for item in source_list:
            if item in set2:
                duplicates.add(item)
            elif duplicates:
                return next(iter(duplicates))
        return None
    
    #-----------------

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