from src.module.weather import Weather
import requests

m_weathre = Weather()

result = m_weathre.first('今天天气怎么样')
print(result)

"""
resp = requests.get("https://ipapi.co/json/")
data = resp.json()
print(data["city"], data["region"], data["country_name"])
"""