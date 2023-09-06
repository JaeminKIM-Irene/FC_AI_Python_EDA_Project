import seaborn as sns

# 영한사전 (대륙용)
def getContinentDictForEngToKor() :
    '''
    info : 영문 - > 한글 (대륙용)
    '''
    dictForContinent =  {
                            'asia'     : '아시아',
                            'europe'   : '유럽',
                            'africa'   : '아프리카',
                            'america'  : '아메리카',
                            'oceania'  : '오세아니아',                        
                        }
    return dictForContinent

# 한영사전 (대륙용)
def getContinentDictForKorToEng() :
    '''
    info : 한글 - > 영문 (대륙용)
    '''
    dictForContinent =  {
                            '아시아'     : 'asia',
                            '유럽'       : 'europe',
                            '아프리카'   : 'africa',
                            '아메리카'   : 'america',
                            '오세아니아'  : 'oceania',                             
                        }
    return dictForContinent

# 영한사전 (아시아국가용)
def getAsiaDictForEngToKor() :
    '''
    info : 영문 - > 한글 (국가용)
    '''
    dictForCountryInAsia = {
                            'japan'         : '일본',
                            'china'         : '중국',
                            'hongkong'      : '홍콩',
                            'taiwan'        : '대만',
                            'vietnam'       : '베트남',
                            'thailand'      : '태국',
                            'malaysia'      : '말레이시아',
                            'philippines'   : '필리핀',
                            'indonesia'     : '인도네시아',
                            'laos'          : '라오스', 
                            'cambodia'      : '캄보디아', 
                            'macau'         : '마카오', 
                            'singapore'     : '싱가폴', 
                            'turkey'        : '튀르키예', 
                            'india'         : '인도',  
                            'myanmar'       : '미얀마',  
                            'mongolia'      : '몽골',  
                            'maldives'      : '몰디브',
                            'israel'        : '이스라엘',
                            'nepal'         : '네팔',
                            'jordan'        : '요르단',
                            'srilanka'      : '스리랑카',
                            'bhutan'        : '부탄',
                            'yemen'         : '예멘',      
                            'cyprus'        : '사이프러스'                          
                        }
    return dictForCountryInAsia

# 한영사전 (국가용)
def getAsiaDictForKorToEng() :
    '''
    info : 한글 - > 영문 (국가용)
    '''
    dictForCountryInAsia = {
                            '일본'          : 'japan',
                            '중국'          : 'china',
                            '홍콩'          : 'hongkong',
                            '대만'          : 'taiwan',
                            '베트남'        : 'vietnam',
                            '태국'          : "thailand",
                            '말레이시아'    : "malaysia",
                            '필리핀'        : "philippines",
                            '인도네시아'    : "indonesia",
                            '라오스'        : "laos", 
                            '캄보디아'      : "cambodia", 
                            '마카오'        : "macau", 
                            '싱가폴'        : "singapore", 
                            '튀르키예'      : "turkey", 
                            '인도'          : "india",  
                            '미얀마'        : "myanmar",  
                            '몽골'          : "mongolia",  
                            '몰디브'        : "maldives",
                            '이스라엘'      : 'israel', 
                            '네팔'          : 'nepal',  
                            '요르단'        : 'jordan',   
                            '스리랑카'      : 'srilanka',   
                            '부탄'          : 'bhutan',   
                            '예멘'          : 'yemen',      
                            '사이프러스'    : 'cyprus'                       
                        }
    return dictForCountryInAsia

# seaborn 팔레트
def getSeabornPaletteDict() :
    '''
    팔레트 종류 : viridis,spring,Reds,Greens.Blues,Set1,Set2,RdPu ...
    사용법 : 함수 불러온뒤 팔레트 괄호에 이름을 입력해서 사용\n ex:) palette['viridis']
    '''
    palette = {
                'Reds' : sns.color_palette("Reds"),
                'Greens' : sns.color_palette("Greens"),
                'Blues' : sns.color_palette("Blues"),
                'deep' : sns.color_palette("deep"),
                'muted' : sns.color_palette("muted"),
                'colorblind' : sns.color_palette("colorblind"),
                'BuGn_r':sns.color_palette('BuGn_r'),
                'GnBu_d':sns.color_palette('GnBu_d'),
                
                'bright' : sns.color_palette("bright"),
                'spring' : sns.color_palette("spring"),
                'pastel' : sns.color_palette("pastel"),
                'viridis' : sns.color_palette("viridis"),
                'Accent_r':sns.color_palette('Accent_r'),
                'Paired':sns.color_palette('Paired'),
                'Pastel1':sns.color_palette('Pastel1'),
                'Pastel2':sns.color_palette('Pastel2'),
                'Set1':sns.color_palette('Set1'),
                'Set2':sns.color_palette('Set2'),
                'Set3':sns.color_palette('Set3'),
              }
    return palette







#0.xx) 옵션(선택사항) 주제2의 inpynb 파일 실행용
#-------------------------
# selectedCountryEng = 'japan'    # 국가명선택(영문)
# selectedContinentKor = '아시아' # 대륙명선택(한글)
# selectedContinentEng = 'asia'   # 대륙명선택(영문)
# startDate = '2018-06-01'        # 시작일선택
# endDate = '2019-05-01'          # 종료일 선택

# selectedCountryKor   = input("국가명을 입력하세요.  \n(ex : 일본)")    # 사용자입력  : 국가명선택(한글)
# selectedCountryEng   = input("국가명을 입력하세요.  \n(ex : japan)")   # 사용자입력  : 국가명선택(영문)
# selectedContinentKor = input("대륙명을 입력하세요.  \n(ex : 아시아)")  # 사용자입력  : 대륙명선택(한글)
# selectedContinentEng = input("대륙명을 입력하세요.  \n(ex : asia)")    # 사용자입력  : 대륙명선택(영문)