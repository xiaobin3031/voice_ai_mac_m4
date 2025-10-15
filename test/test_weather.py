from src.module.weather import Weather

m_weather = Weather()

"""
loc = m_weather.location()
print('location', loc)
"""

"""
weather_info = {"place": '鄞州区'}
citycode = m_weather.get_city_code('鄞州区')
if citycode is None:
    print('没有找到该城市')
    exit()
weather_info['adcode'] = citycode
weather = m_weather.query_weather(weather_info)
print('weather', weather)
"""