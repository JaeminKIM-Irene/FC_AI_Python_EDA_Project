#유틸기능 모듈 주제2

import csv
from collections import OrderedDict
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dictionary import * 
import plotly.graph_objects as go

class Utils2():

    # 1. 대륙별 데이터 프레임 생성함수 
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


    # 2. 국가별 데이터 프레임 생성함수 
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
    

    # 3-1-1. 날짜 데이터타입 변환함수
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
    

    # 3-1-1. 날짜 데이터타입 변환함수
    @staticmethod
    def changeYearAndMonthDtypeToObject(countryDataFrame) :    
        
        # 'Year' 컬럼에서 숫자를 문자열로 변환하고, 뒤에 '년' 문자열 추가
        countryDataFrame['Year'] = countryDataFrame['Year'].astype(str) + '년'

        # 'Month' 컬럼에서 숫자를 문자열로 변환하고, 뒤에 '월' 문자열 추가
        countryDataFrame['Month'] = countryDataFrame['Month'].astype(str) + '월'


        return countryDataFrame   
        

    # 3-2. 데이터 날짜 필터링 하여 추출하는 함수
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


    # 3-3. 국가 데이터프레임의 컬럼을 재정렬 하는 함수
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
    

    # 3-3. 데이터프레임에서 시작과 끝 년월을 문자열로 추출하는 함수
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
        

    # 4.1.1 한글 --> 영문 문자열 변환함수(대륙용)
    @staticmethod
    def translateKorToEngForContinent(continentName):
        '''
        instruction : 
            param   : 대륙명(한/영)\n
            return  : 키에 해당하는 값 리턴\n
            error   : 에러 메세지 리턴 
        '''
        
        try:
            # 입력받은 인자가 한글인지 영문인지 판단
            if is_korean(continentName): 
                continent_dict = getContinentDictForKorToEng()

            elif is_english(continentName):
                return continentName

            else: 
                raise ValueError('ERROR : 유효하지 않는 문자열 입니다!!')

            # 딕셔너리에 인풋된 문자열이 있는지 체크
            if continentName in continent_dict:
                translated_string = continent_dict[continentName]

            else:
                raise KeyError("존재하지 않는 대륙입니다")

        except (ValueError, KeyError) as e:
             return str(e)

        return translated_string
    

    # 4.1.2 한글 --> 영문 문자열 변환함수(국가용 only asia)
    @staticmethod
    def translateKorToEngForCountry(countryName):
        '''
        instruction : 
            info    : 현재는 아시아만 국가만 지원됩니다.\n
            param   : 국가명(한/영)\n
            return  : 키에 해당하는 값 리턴\n
            error   : 에러 메세지 리턴 
        '''
        
        try:
            # 입력받은 인자가 한글인지 영문인지 판단
            if is_korean(countryName): 
                country_dict = getAsiaDictForKorToEng()

            elif is_english(countryName):
                return countryName

            else: 
                raise ValueError('ERROR : 유효하지 않는 문자열 입니다!!')

            # 딕셔너리에 인풋된 문자열이 있는지 체크
            if countryName in country_dict:
                translated_string = country_dict[countryName]

            else:
                raise KeyError("존재하지 않는 국가입니다")

        except (ValueError, KeyError) as e:
             return str(e)

        return translated_string


    # 4.1.3 영문 --> 한글 문자열 변환함수(대륙용)
    @staticmethod
    def translateEngToKorForContinent(continentName):
        '''
        instruction : 
            param   : 대륙명(한/영)\n
            return  : 키에 해당하는 값 리턴\n
            error   : 에러 메세지 리턴 
        '''
        
        try:
            # 입력받은 인자가 한글인지 영문인지 판단
            if is_korean(continentName): 
                return continentName

            elif is_english(continentName):
                continent_dict = getContinentDictForEngToKor()

            else: 
                raise ValueError('ERROR : 유효하지 않는 문자열 입니다!!')

            # 딕셔너리에 인풋된 문자열이 있는지 체크
            if continentName in continent_dict:
                translated_string = continent_dict[continentName]

            else:
                raise KeyError("존재하지 않는 대륙입니다")

        except (ValueError, KeyError) as e:
             return str(e)

        return translated_string
    

    # 4.1.4 영문 --> 한글 문자열 변환함수(국가용 only asia)
    @staticmethod
    def translateEngToKorForCountry(countryName):
        '''
        instruction : 
            info    : 현재는 아시아만 국가만 지원됩니다.\n
            param   : 국가명(한/영)\n
            return  : 키에 해당하는 값 리턴\n
            error   : 에러 메세지 리턴 
        '''
        
        try:
            # 입력받은 인자가 한글인지 영문인지 판단
            if is_korean(countryName): 
                return countryName

            elif is_english(countryName):
                country_dict = getAsiaDictForEngToKor()

            else: 
                raise ValueError('ERROR : 유효하지 않는 문자열 입니다!!')

            # 딕셔너리에 인풋된 문자열이 있는지 체크
            if countryName in country_dict:
                translated_string = country_dict[countryName]

            else:
                raise KeyError("존재하지 않는 국가입니다")

        except (ValueError, KeyError) as e:
             return str(e)

        return translated_string
    

    # 5. 날짜 크기 지정
    @staticmethod
    def getPeriod(sizeOfYM):
        if sizeOfYM % 12 == 0 and (12 <= sizeOfYM <= 120):
            return f'{sizeOfYM // 12}년'
        else:
            return '유효하지 않은 기간'
        

    # 6. Moving average 계산
    @staticmethod
    def calculateMovingAverage(countryNameKor, period, countryDataFrame):
        countryDataFrame['MovingAverage'] = countryDataFrame['NumVisitors'].rolling(window=12).mean()

        # 원래 시계열 그리기 (파랑선)
        pre_covid = countryDataFrame.loc[(countryDataFrame['YM'] >= '2013-06-01') & (countryDataFrame['YM'] <= '2024-05-31')]
        trace1 = go.Scatter(x=pre_covid['YM'], y=pre_covid['NumVisitors'], mode='lines', name='원시계열', line=dict(color='blue', width=3))

        # Moving average 시계열 그리기 (초록선)
        post_covid = countryDataFrame.loc[(countryDataFrame['YM'] >= '2013-06-01') & (countryDataFrame['YM'] <= '2024-05-31')]
        trace2 = go.Scatter(x=post_covid['YM'], y=post_covid['MovingAverage'], mode='lines', name='Movingaverage', line=dict(color='green', width=3))

        data = [trace1, trace2]


        layout = go.Layout(
            title=f'{countryNameKor}_{period}치_Moving Average 방문자수 추이 비교_window12',
            xaxis=dict(
                title='날짜',
                tickangle=45 
            ),
            yaxis=dict(
                title='월별 방문자수 (만명)',
                dtick=5  
            ),
            showlegend=True
        )

        return data, layout


    # 2 데이터 프레임에 인덱스 초기화 함수(T)
    @staticmethod
    def resetIndexForDataFrame(df):
        '''
        instruction : 
            True  : 기존 인덱스는 삭제, 기존의 인덱스 정보는 완전히 사라짐
            False  : 기존의 인덱스가 새로운 열로 추가
        '''
        resetedIndexData =  df.reset_index(drop=True)
        return resetedIndexData
    
    

# xxx 문자열이 한글인지 판단

def is_korean(string):
    for char in string:
        unicode_value = ord(char)
        if 0xAC00 <= unicode_value <= 0xD7AF:
            return True
    return False

# xxx 문자열이 영문인지 판단
def is_english(string):
    for char in string:
        unicode_value = ord(char)
        if (0x0041 <= unicode_value <= 0x005A) or (0x0061 <= unicode_value <= 0x007A):
            return True
    return False
