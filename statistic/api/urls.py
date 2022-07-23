from django.urls import path
from statistic.api.views import (
    general_statistics, 
)


urlpatterns = [
    path('general/', general_statistics, name='general_statistics'), 
] 