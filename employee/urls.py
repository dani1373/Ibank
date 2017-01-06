from django.conf.urls import url

from employee import views

urlpatterns = [
    url(r'^register_employee$', views.register_employee, name='register_employee'),
]
