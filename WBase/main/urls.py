from django.urls import path
from django.conf.urls import url
from .import views


urlpatterns = [ 
    
url(r'^$', views.index, name='index'),
url(r'^batchview$', views.Batch_view.as_view(), name='ww'),
url(r'^(?P<batch>\d{1,4}\D{1}\d{1})/$', views.Varka_view.as_view(), name='ww'),
]