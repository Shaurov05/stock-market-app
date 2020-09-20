from django.shortcuts import render
import requests
import json
# Create your views here.

"""pk_73786c81d59f4cbf9b9fe4406e19e020 """


def index(request):

    if request.method == 'POST':
        quote_name = request.POST['quote_name']
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ quote_name +"/quote?token=pk_73786c81d59f4cbf9b9fe4406e19e020")

    else:
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/aapl/quote?token=pk_73786c81d59f4cbf9b9fe4406e19e020")
        quote_name = 'none'

    try:
        api = json.loads(api_request.content)
    except Exception as e:
        api = "Error page!"

    return render(request, 'index.html', {'api':api,
                                        'quote_name':quote_name})



def about(request):
    return render(request, 'about.html', {})











#
