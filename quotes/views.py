from django.shortcuts import render, redirect
import requests
import json
from django.contrib import messages
from django.urls import reverse

from . models import Stock
from . forms import StockForm
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


def add_stock(request):

    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            ticker = form.cleaned_data['ticker']
            messages.success(request, ("Stock("+ ticker +") has been added to list"))
            return redirect(reverse('add_stock'))
    else:
        api_info = []
        output = []
        tickers = Stock.objects.all()

        for quote_name in tickers:
            print("quote ",quote_name)
            url = "https://cloud.iexapis.com/stable/stock/"+ str(quote_name) +"/quote?token=pk_73786c81d59f4cbf9b9fe4406e19e020"
            print("url ",url)
            api_request = requests.get(url)
            try:
                api_response = json.loads(api_request.content)

            except Exception as e:
                api_info.append([quote_name.ticker, "--","--", "--",
                                            "--", "--","--", quote_name.id])
                messages.success(request, ("Couldn't find stock(" +str(quote_name)+ "), please try again with valid ticker!"))
                continue
            output.clear()
            company_name = api_response['companyName']
            latest_price = api_response['latestPrice']
            prev_close = api_response['previousClose']
            market_cap = api_response['marketCap']
            ytdChange = api_response['ytdChange']
            week52High = api_response['week52High']
            week52Low = api_response['week52Low']
            output.append(company_name)
            output.append(latest_price)
            output.append(prev_close)
            output.append(market_cap)
            output.append(ytdChange)
            output.append(week52High)
            output.append(week52Low)

            output.append(quote_name.id)
            # print("output " ,output)
            api_info.append(output[:])
            print("api info " ,api_info)
        # context = {'api_info':api_info, 'tickers':tickers}
        return render(request, 'stocks.html', {"api_info":api_info})



def delete_stock(request, stock_id):
    item = Stock.objects.get(id=stock_id)
    messages.success(request, "Stock query \'"+ item.ticker +"\' has been deleted")
    item.delete()
    return redirect('add_stock')








#
