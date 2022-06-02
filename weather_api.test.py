import weather_api

weather_data_dict = weather_api.get_today_weather()
print('weather_data_dict: ', weather_data_dict)
weather_data_key = list(weather_data_dict.keys())
weather_data_value = list(weather_data_dict.values())
weather_data_list = []
for i in range(len(weather_data_key)):
    weather_data_list.append(weather_data_key[i])
    weather_data_list.append(weather_data_value[i])

print('weather_data_list:', weather_data_list)
# connectionSocket.send(weather_data.encode("UTF-8"))