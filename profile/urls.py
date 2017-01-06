from django.conf.urls import url

from profile import views

urlpatterns = [
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^test$', views.home_page, name='test'),
]
