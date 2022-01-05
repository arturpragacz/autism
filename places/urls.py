from django.urls import path
from django.views.generic import RedirectView

from .views import PlaceSearchView, PlaceView, RatingsView, RateView


app_name = 'places'

urlpatterns = [
	path('', RedirectView.as_view(url='search/')),
	path('search/', PlaceSearchView.as_view(), name='search'),
	path('<int:pk>/', PlaceView.as_view(), name='place'),
	path('<int:pk>/ratings/', RatingsView.as_view(), name='ratings'),
	path('<int:pk>/rate/', RateView.as_view(), name='rate'),
]