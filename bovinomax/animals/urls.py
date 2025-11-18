from django.urls import path # type: ignore
from .views import AnimalListView, AnimalDetailView, AnimalCreateView
from . import views


app_name = 'animals'

urlpatterns = [
    path('', AnimalListView.as_view(), name='animal_list'),
    path('<int:pk>/', AnimalDetailView.as_view(), name='animal_detail'),
    path('new/', AnimalCreateView.as_view(), name='animal_create'),
    path('<int:pk>/apply-vaccine/', views.apply_vaccine, name='apply_vaccine'),
]
