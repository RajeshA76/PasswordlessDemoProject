from django.urls import path
from .views import codeView, emailView,home


urlpatterns=[
    path('login/',emailView,name="login"),
    path('verify/<str:token>/',codeView,name="code"),
    path('home/<str:token>/',home,name="home"),
]