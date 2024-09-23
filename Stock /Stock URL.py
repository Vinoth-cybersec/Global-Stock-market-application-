from django.urls import path
from . import views

urlpatterns = [
    path('portfolio/', views.portfolio_view, name='portfolio'),
    path('add/', views.add_stock_to_portfolio, name='add_stock'),
]
