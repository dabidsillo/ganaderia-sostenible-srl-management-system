from django.urls import path
from . import views
from .views import manage_resources, ResourceLogListView

app_name = 'resources'

urlpatterns = [
    path('manage/', manage_resources, name='manage_resources'),
    path('history/', ResourceLogListView.as_view(), name='resource_log'),
]
