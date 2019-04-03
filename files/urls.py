from django.urls import path, include
from django.conf.urls import include, url
from files import views
from rest_framework import routers

#
# router = routers.DefaultRouter()
# router.register('files', views.FileView.as_view(), name='file-upload')

urlpatterns = [
    url(r'^upload/$', views.FileView.as_view(), name='file-upload'),
    url(r'^preprocess/$', views.PreProcessView.as_view(), name='preprocess')
]

# urlpatterns += router.urls

