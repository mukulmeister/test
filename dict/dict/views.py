from django.shortcuts import render
import requests
from .forms import InputForm



weather_url = "https://api.weatherapi.com/v1/current.json?"






Direction = {"N": "North","S": "South","W": "West","E": "East"}

def weather(request):

    weather_details = ''
    if request.method == "POST":
        city = InputForm(request.POST)


        if city.is_valid():
            city_details= city.cleaned_data['City']



            endpoint = weather_url

            url = endpoint + city_details

            headers = {"Accept": "application/json"}
            response = requests.get(url, headers=headers)

            json_str = response.json()

            weather_details = json_str


    return render(request, 'index.html', {"form": InputForm,"weather": weather_details, "wind_dir": Direction})




















#def home(request):

  #  form = InputForm()


   # return render(request,'index.html', context={'form': form,'weather':weather()})



#def submit(request):
   # pass

    #data = form.Shift.data

    #if request.method=='POST':
    #    send_email(data,rec)
#
 #       return render('shift.html', t2=rec, priority=Pri,state=STATES, maji=mi, shiftsum=data)