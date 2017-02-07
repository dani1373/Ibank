from django.conf.urls import url

from employee import views

urlpatterns = [
    url(r'^register_employee$', views.register_employee, name='register_employee'),
    url(r'^assign_role$', views.assign_role, name='assign_role'),
    url(r'^assign_role/(?P<national_id>\w+)$', views.assign_role_employee, name='assign_role'),
    url(r'^assign_role/(?P<national_id>\w+)/(?P<role>.*)$', views.assign_role_employee_national, name='assign_role'),
]
