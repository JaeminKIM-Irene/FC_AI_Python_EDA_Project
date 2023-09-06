#===================================================================================================================
#                                                  유튜브 API 세팅
#===================================================================================================================

import requests
import json
from urllib import parse

class YoutubeApi():
  
    # 초기화  
    def __init__(self, apiKey):
      self.apiKey = apiKey
      self.url = 'https://youtube.googleapis.com/youtube/v3/'

    #----------------------
    # 사용자검색
    #----------------------
    # 사용자 검색어로 Json 데이터 반환  
    def getJsonBySearchQuery(self, searchQuery,searchCount):
        search = f'search?part=snippet&maxResults={searchCount}&type=video&key={self.apiKey}&q={parse.quote(searchQuery)}'
        res = requests.get(self.url + search)
        jsonData = res.text

        return jsonData   
      
    # 사용자 검색어로 Dictionary 데이터 반환  
    def getDictBySearchQuery(self, searchQuery,searchCount):
        search = f'search?part=snippet&maxResults={searchCount}&type=video&key={self.apiKey}&q={parse.quote(searchQuery)}'
        res = requests.get(self.url + search)
        jsonData = res.text
        dictData = json.loads(jsonData)
        
        return dictData 

    
    #----------------------
    # 채널ID 검색
    #----------------------
    # 채널아이디로 해당채널의 Json 데이터 반환
    def getJsonByChannelId(self, searchQuery,channelId):
        search = f'search?part=snippet&maxResults=10&type=video&key={self.apiKey}&q={parse.quote(searchQuery)}&channelId={channelId}&maxResults=1'
        res = requests.get(self.url + search)
        jsonData = res.text

        return jsonData   
    
    # 채널아이디로 해당채널의 Dictionary 데이터 반환
    def getDictByChannelId(self, searchQuery,channelId):
        search = f'search?part=snippet&maxResults=10&type=video&key={self.apiKey}&q={parse.quote(searchQuery)}&channelId={channelId}&maxResults=1'
        res = requests.get(self.url + search)
        jsonData = res.text
        dictData = json.loads(jsonData)
        
        return dictData 
    
    #----------------------
    # 비디오ID 검색
    #----------------------
    # 비디오아이디로 Json 데이터 반환
    def getJsonByVideoId(self, videoId,searchCount):
        search = f"videos?part=statistics&maxResults={searchCount}&key={self.apiKey}&id={parse.quote(videoId)}"
        res = requests.get(self.url + search)
        jsonData = json.loads(res.text)
        
        return jsonData['items'][0]['statistics']
    
    # 비디오아이디로 Dictionary 데이터 반환
    def getDictByVideoId(self, videoId,searchCount):
        search = f"videos?part=statistics&maxResults={searchCount}&key={self.apiKey}&id={parse.quote(videoId)}"
        res = requests.get(self.url + search)
        jsonData = res.text
        dictData = json.loads(jsonData)
        
        return dictData['items'][0]['statistics'] 
    
    
    
    
    
#===================================================================================================================
#                                                  현재 사용한함
#===================================================================================================================  
    
    # # 비디오아이디로 해당채널의 Json데이터 반환
    # def getJsonByVideoId(self, videoId,searchCount):
    #     search = f"videos?part=statistics&maxResults={searchCount}&key={self.apiKey}&id={parse.quote(videoId)}"
    #     res = requests.get(self.url + search)
    #     jsonData = json.loads(res.text)
        
    #     return jsonData['items'][0]['statistics']
      
      
      
      
      
      
    # # 비디오아이디로 해당영상의 조회수 반환
    # def getViewCountByVideoId(self, videoId,searchCount):
    #     search = f"videos?part=statistics&maxResults={searchCount}&key={self.apiKey}&id={parse.quote(videoId)}"
    #     res = requests.get(self.url + search)
    #     jsonData = json.loads(res.text)
        
    #     return jsonData['items'][0]['statistics']['viewCount']
      
      
    # # 비디오아이디로 해당영상의 좋아요수 반환
    # def getLikeCountByVideoId(self, videoId,searchCount):
    #     search = f"videos?part=statistics&maxResults={searchCount}&key={self.apiKey}&id={parse.quote(videoId)}"
    #     res = requests.get(self.url + search)
    #     jsonData = json.loads(res.text)
        
        
    #     return jsonData['items'][0]['statistics']['likeCount']    
    
    
    
    # # 사용자 검색어로 Json데이터 반환  
    # def getJsonBySearchQuery(self, searchQuery,searchCount):
    #     search = f'search?part=snippet&maxResults={searchCount}&type=video&key={self.apiKey}&q={parse.quote(searchQuery)}'
    #     res = requests.get(self.url + search)
    #     jsonData = res.text

    #     return jsonData 
    
    # 사용자 검색어로 비디오 아이디 반환
    # def getVideoIdBySearchQuery(self, searchQuery,searchCount):
    #     search = f'search?part=snippet&maxResults={searchCount}&type=video&key={self.apiKey}&q={parse.quote(searchQuery)}'
    #     res = requests.get(self.url + search)
    #     jsonData = json.loads(res.text)

    #     return jsonData["items"][0]['id']['videoId']
    
    # 사용자 검색어로 타이틀제목 반환
    # def getVideoTitleBySearchQuery(self, searchQuery,searchCount):
    #     search = f'search?part=snippet&maxResults={searchCount}&type=video&key={self.apiKey}&q={parse.quote(searchQuery)}'
    #     res = requests.get(self.url + search)
    #     jsonData = json.loads(res.text)

    #     return jsonData["items"][0]['snippet']['title'] 
    

    
    # # 비디오리스트로 해당채널의 Json데이터 반환
    # def getJsonByVideoList(self, videoList,statisticType):
    #     search = f"videos?part=statistics&maxResults={len(videoIdList)}&key={self.apiKey}&id={parse.quote(videoId)}"
    #     res = requests.get(self.url + search)
    #     jsonData = res.text

    #     return jsonData 
    
    
    # # 채널아이디로 해당채널의 Json데이터 반환
    # def search_channel_id_by(self, names):
    #   query = f"search?part=id&key={self.apiKey}&type=channel&q={parse.quote(names)}"
    #   channel_id = requests.get(self.url + query).json()['items'][0]['id']['channelId']
    
    #   return channel_id

    # def get_statistics_by(self, channelId):
    #   query = f"channels?part=statistics&key={self.apiKey}&id={channelId}"
    #   stats = requests.get(self.url + query).json()['items'][0]['statistics']
    
    #   return stats
