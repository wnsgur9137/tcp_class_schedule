import requests         # 날씨 공공데이터 api 사용하기 위한 라이브러리
import datetime
from socket import *
# import schedule
# import time
# import server


def get_today_weather():
    today = datetime.datetime.today()
    day_ = str(today.date()).replace('-', '')
    hour = str(today.hour - 1)
    if len(hour) == 1:
        hour = '0' + hour
    time_ = hour + '50'
    # 날씨 api
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'
    params = {'serviceKey' : 'LK5HxMQO7ScyFpgYc6+QgNRsqPfAKmnW1fczw8kHYE4BDXCaUX7uBUrZXK6wXoDnS5vivk2h0fYiboTWVjRjvQ==',
              'pageNo' : '1',       # 페이지 번호
              'numOfRows' : '100',  # 한 페이지의 결과 수(페이징)
              'dataType' : 'JSON',  # 요청 자료 형식(XML/JSON) Default: XML
              'base_date' : day_,   # 발표 일자
              'base_time' : time_,  # 발표 시간
              'nx' : '54',          # 에보 지점의 X 좌표값 (용현 1.4동)
              'ny' : '124'}         # 예보 지점의 Y 좌표값

    print('날씨 api 연결중...')
    response = requests.get(url, params=params)

    print(response.content)
    weather_data = dict()

    try:
        items = response.json().get('response').get('body').get('items')

        for item in items['item']:
            # 기온
            if item['category'] == 'T1H':
                weather_data['tmp'] = item['fcstValue']
            # 습도
            if item['category'] == 'REH':
                weather_data['hum'] = item['fcstValue']
            # 하늘상태: 맑음(1), 구름많음(3) 흐림(4)
            if item['category'] == 'SKY':
                weather_data['sky'] = item['fcstValue']
                if weather_data['sky'] == '0':
                    weather_data['sky'] = '없음'
                elif weather_data['sky'] == '1':
                    weather_data['sky'] = '맑음'
                elif weather_data['sky'] == '2':
                    weather_data['sky'] = '구름적음'
                elif weather_data['sky'] == '3':
                    weather_data['sky'] = '구름많음'
                elif weather_data['sky'] == '4':
                    weather_data['sky'] = '흐림'
            # 1시간 동안의 강수량
            if item['category'] == 'RN1':
                weather_data['rn1'] = item['fcstValue']
                if weather_data['rn1'] != '강수없음':
                    weather_data['rn1'] += ''
            # 강수 형태
            if item['category'] == 'PTY':
                weather_data['pty'] = item['fcstValue']
                if weather_data['pty'] == '0':
                    weather_data['pty'] = '없음'
                elif weather_data['pty'] == '1':
                    weather_data['pty'] = '비'
                elif weather_data['pty'] == '2':
                    weather_data['pty'] = '비/눈'
                elif weather_data['pty'] == '3':
                    weather_data['pty'] = '눈'
                elif weather_data['pty'] == '5':
                    weather_data['pty'] = '빗방울'
                elif weather_data['pty'] == '6':
                    weather_data['pty'] = '빗방울/눈 날림'
                elif weather_data['pty'] == '7':
                    weather_data['pty'] = '눈날림'

    except error as e:
        print('\n\nERROR:', e)

    print('\n\n[weather update]\n')
    print(weather_data)

    return weather_data

# get_today_weather()