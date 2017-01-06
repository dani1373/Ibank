from django.conf.urls import url

from service import views

urlpatterns = [
    url(r'^define_bill$', views.define_bill, name='define_bill'),
]
