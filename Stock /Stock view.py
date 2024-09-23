import yfinance as yf
from django.shortcuts import render, redirect
from .models import Stock, Portfolio
from .forms import StockSearchForm
from django.contrib.auth.decorators import login_required

def get_stock_data(symbol):
    stock_info = yf.Ticker(symbol)
    stock = stock_info.info

    # Extract relevant stock information
    data = {
        "name": stock.get("longName"),
        "symbol": stock.get("symbol"),
        "market": stock.get("exchange"),
        "price": stock.get("regularMarketPrice"),
        "market_cap": stock.get("marketCap"),
        "pe_ratio": stock.get("trailingPE"),
    }
    return data

@login_required
def add_stock_to_portfolio(request):
    if request.method == "POST":
        form = StockSearchForm(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data['symbol'].upper()

            # Get stock data
            stock_data = get_stock_data(symbol)

            if stock_data["price"] is not None:
                stock, created = Stock.objects.get_or_create(
                    symbol=symbol,
                    defaults={
                        "name": stock_data["name"],
                        "market": stock_data["market"],
                        "price": stock_data["price"],
                        "market_cap": stock_data["market_cap"],
                        "pe_ratio": stock_data["pe_ratio"]
                    }
                )
                portfolio, _ = Portfolio.objects.get_or_create(user=request.user)
                portfolio.stocks.add(stock)
                return redirect('portfolio')

    else:
        form = StockSearchForm()

    return render(request, 'stocks/add_stock.html', {'form': form})

@login_required
def portfolio_view(request):
    portfolio, _ = Portfolio.objects.get_or_create(user=request.user)
    return render(request, 'stocks/portfolio.html', {'portfolio': portfolio})
