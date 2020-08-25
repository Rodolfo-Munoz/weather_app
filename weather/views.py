from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=ab27c6408d2bf2ab57f572629eef037a'

    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            # in this variable we hold the city entered by the user
            new_city = form.cleaned_data['name']
            # if the existing_city_count is 0, then the city is not duplicated
            existing_city_count = City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                # using the API to check if the city exists
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City does not exist'
            else:
                err_msg = 'City already exists in the database'

        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added successfully!'
            message_class = 'is-success'

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

    context = {
        'weather_data': weather_data,
        'form': form,
        'message': message,
        'message_class': message_class,
    }

    return render(request, 'weather/weather.html', context)


def delete_city(request, city_name):
    # here we query for the city and delete it and then redirects the user to home page
    City.objects.get(name=city_name).delete()
    return redirect('home')
