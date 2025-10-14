"""天气模块"""

from src.llm import LocalLLM
import json
from config import config
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.error import HTTPError
import logging
from src.tts import TTS
from src.module.base_module import BaseModule  # Add this import or adjust the path as needed
from datas import Datas

data = Datas('amap_city_code.json')

logger = logging.getLogger(__name__)

llm = LocalLLM()
llm_msg = """
    帮我提取一些信息，返回json格式，时间（startTime， endTime, yyyy-MM-dd HH:mm:ss格式），地点(place)，想要知道的天气（weather），其中weather是单独的字段，不用输出逻辑，直接给结果
    """

tts = TTS()
location_suffix = ['省', '区', '市', '县', '乡', '镇', '街', '村']

class Weather(BaseModule):

    def first(self, text):
        result = llm.ask(f"{text} {llm_msg}")
        weather_info = json.loads(result)
        if weather_info.get('place') is None:
            amap_location = self.__location()
            if amap_location['status'] == 1:
                weather_info['place'] = amap_location['city']
        
        if weather_info.get('place') is None:
            tts.speak("请告诉我你的位置")
            return
        
        ccs = data.load()
        citycode = ccs.get(weather_info['place']) 
        if citycode is None:
            for suffix in location_suffix:
                citycode = ccs.get(weather_info['place'] + suffix)
                if citycode is not None:
                    break
        if citycode is None:
            tts.speak("请告诉我你的位置")
            return

        weather_info['adcode'] = citycode
        weather = self.__query_weather(weather_info)
        print("weather result: ", weather)
        if weather['status'] == 0:
            tts.speak(weather.get('info', '天气查询失败'))
        else:
            lives = weather['lives']
            tts.speak(f"{lives['city']}{lives['weather']} {lives['temperature']}度")
    def again(self, text):
        pass

    def __query_weather(self, weather_info):
        params = {}
        params['key'] = config['amap']['key']
        params['city'] = weather_info['adcode']
        print('params', params)
        try:
            response = urlopen("https://restapi.amap.com/v3/weather/weatherInfo?" + urlencode(params))
            return json.load(response)
        except HTTPError as e:
            error = e.fp.read().decode()
            logger.exception(error)
            return {"status": 0, "info": error}

    def __location():
        params = {}
        params['key'] = config['amap']['key']
        try:
            response = urlopen("https://restapi.amap.com/v3/ip" + urlencode(params))
            return json.load(response)
        except HTTPError as e:
            error = e.fp.read().decode()
            logger.exception(error)
            return {"status": 0, "info": error}