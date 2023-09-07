import csv
from collections import OrderedDict
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

class Utils():

    # 1.1 데이터 프레임1 생성함수 
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
        4. 최종 DataFrame에 비디오 ID들의 열을 추가합니다.

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


    # 1.2 데이터 프레임2 생성함수 
    @staticmethod
    def makeDataFromStatistics(dictData) :
        countsData = pd.DataFrame()
        statisticsDataFrame = pd.DataFrame.from_dict([dictData])
        countsData = pd.concat([countsData, statisticsDataFrame])
        countsData = Utils.resetIndexForDataFrame(countsData) # 인덱스 초기화
        
        return countsData
    
    # 1.3 데이터 프레임에 인덱스 초기화 함수(T)
    @staticmethod
    def resetIndexForDataFrame(df):
        '''
        instruction : 
            True  : 기존 인덱스는 삭제, 기존의 인덱스 정보는 완전히 사라짐
            False  : 기존의 인덱스가 새로운 열로 추가
        '''
        return df.reset_index(drop=True)
    

    # 1.4 데이터 프레임에서 필요 없는 columns drop 및 재정렬
    @staticmethod
    def dropAndReorganizeColumns(df):
        df = df[['videoId', 'title', 'description', 'viewCount', 'likeCount', 'favoriteCount', 'commentCount', 
                 'publishedAt', 'channelId', 'channelTitle', 'country']]
        return df


    # 1.5 publishedAt 날짜 type으로 변환
    @staticmethod
    def changeTypeToDatetime(data):
        pubdate = pd.to_datetime(data)
        year = pubdate.dt.year.values[0]
        month = pubdate.dt.month.values[0]
        date = str(year) +'년' + str(month) + '월'
        return year, month, date
    
    
    # 1.6 published 날짜의 visitor row 추출
    @staticmethod
    def extractIndexOfVisitorRow(data, year, month):
        # 누계 이전까지의 인덱스 반환
        if (year > 2023) or (year >= 2023 and month > 6) :
            return -24
        bool_mask = (data['Year'] == (str(year) + '년')) & (data['month'] == (str(month) + '월'))
        published_idx = data[bool_mask].index.values[0]
        return published_idx

    # 1.7 각 나라의 10년치 누적 방문객 수 추출
    @staticmethod
    def get_cum_data(data) :  
        cum = data.iloc[-11:-1, 4::2]
        cum = cum.fillna(0).astype('float').astype('int')
        total = cum.sum(axis=0)
        
        return total
    
    # 1.8 유튜브 채널 정보 리스트로 만들기
    @staticmethod
    def extractYoutubeStatistics(count_list) :  
        subs = []
        view = []
        video = []
        search = []

        for i in count_list :
            a, b, c = i.text.split()
            s_v_split = re.split(r'^(\d{1,3}[만])', a)
            subs.append(int(s_v_split[1].split('만')[0]))
            view.append(int(''.join(s_v_split[2][:-1].split('억'))))
            video.append(int(b.replace(',', '')))
            search.append(int(c.replace(',', '')))
        
        return subs, view, video, search
    
    # 1.8 유튜브 채널 정보 리스트로 만들기 (채널 직접 검색 시)
    @staticmethod
    def extractYoutubeStatistics2(soup) :  
        channel_list = soup.select('table .subject h1 a')[0]
        channel_name = channel_list.text.strip().split('\n')[1]

        count = soup.select('table .subject h3')[0]

        subs, view, video = count.text.split()

        subs = int(subs.split('만')[0])
        view = int(''.join(view[:-1].split('억')))
        video = int(video.replace(',', ''))
        category = soup.select('table .subject h1 a span')[0].text

        category = re.sub('\[|\]', '', category)
        
        return channel_name, subs, view, video, category
    
    # 2.3 문자열을 받아온뒤 쪼개서 리스트로 반환하는 함수
    @staticmethod
    def get_splited_string_list(string) :
        '''        
          instruction :  문자열을 입력받아 공백으로 쪼갠뒤, 리스트로 리턴한다.
        '''
        splited_string_list = string.split()
        return splited_string_list

    # 2.5 두 리스트를 비교하여 중복문자열을 반환함수
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
    