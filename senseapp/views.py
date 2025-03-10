from django.shortcuts import render
from django.http import JsonResponse
import requests
import math
from sense_emu import SenseHat
from .forms import weather_input

sense = SenseHat()


def abs_humidity(temperature, relative_humidity):
    P_sat = 6.112 * math.exp((17.67 * temperature) / (temperature + 243.5))
    RH_decimal = relative_humidity / 100.0
    AH = (RH_decimal * P_sat) / (0.622 + (1 - RH_decimal))
    return AH


def calculate_index(api_key, city_code):
    url = f"https://api.openweathermap.org/data/2.5/forecast?id={city_code}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Error while opening URL -> Response: {response.status_code}")

    try:
        all_data = []
        city = data["city"]["name"]
        for item in data["list"]:
            date = item["dt_txt"].split(" ")[0]
            time = item["dt_txt"].split(" ")[1][:2]
            temperature = int(item["main"]["temp"]-273.15)
            humidity = round(abs_humidity(temperature,item["main"]["humidity"]),1)
            rain = item.get("rain", {}).get("3h", 0)
            wind_speed = item["wind"]["speed"]
            if rain == 0 and humidity == 0:
                soil_humidity_index = 0
            else:
                soil_humidity_index = round((((rain*0.4)+(humidity*0.3))/((wind_speed*0.1)+(temperature*0.2))),1)
            
            all_data.append({
                    'city': city,
                    'date': date,
                    'time': time,
                    'soil_humidity_index': soil_humidity_index
            })
        return all_data
    except Exception as e:
        print(f"Error while fetching data and calculating: {e}")

def sense_func(request):
    form = weather_input(request.POST)
    all_data = []
    if request.method == 'POST':
        if form.is_valid():
            api_key = form.cleaned_data["api_key"]
            city_code = form.cleaned_data["city_code"]
            all_data = calculate_index(api_key, city_code)
        
            city_to_show = all_data[0]["city"]
            date_to_show = all_data[0]["date"][5:]
            time_to_show = all_data[0]["time"][:2]
            soil_humidity_index = float(all_data[0]["soil_humidity_index"])
            green = [0, 255, 0]
            red = [255, 0, 0]
            sense.set_rotation(0)
            try:
                sense.show_message(f"{city_to_show}-{date_to_show}-{time_to_show}h", scroll_speed=0.1,
                                    text_colour=green if soil_humidity_index < 3 else red)
            except Exception as e:
                print(f"Error while sensing: {e}")
                return JsonResponse({"status": "error", "message": str(e)})
        else:
            form = weather_input()

    return render(request, 'form.html', {'form':form, 'all_data':all_data})
