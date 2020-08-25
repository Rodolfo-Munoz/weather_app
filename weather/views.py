from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm



def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=ab27c6408d2bf2ab57f572629eef037a'

    if request.method == 'POST':
        try:
            form = CityForm(request.POST)
            form.save()
        except KeyError:
            print('That City does not exist in our database')


    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon']
        }

        weather_data.append(city_weather)

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather/weather.html', context)
