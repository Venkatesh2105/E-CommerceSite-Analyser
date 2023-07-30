from django.urls import path
from . import views

urlpatterns =[
    # path('',views.ImageView,name='upload'),
    # path('img/',views.Display,name='display'),
    path('',views.Input,name='upload'),
    path('ranking/',views.ranking,name='rank')
    
]