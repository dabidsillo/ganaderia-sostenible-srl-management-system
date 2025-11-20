from django.urls import path # type: ignore
from . import views
from .views import AnimalListView,manage_vaccines

app_name = 'animals'

urlpatterns = [
    path('', AnimalListView.as_view(), name='animal_list'),
    path('generate-feed/', views.generate_daily_feed, name='generate_feed'),
    path('daily-feed/', views.daily_feed, name='daily_feed'),
    path('complete-feed/<int:feed_id>/', views.complete_feed, name='complete_feed'),
    path('<int:animal_id>/vaccines/', manage_vaccines, name='manage_vaccines'),
]
