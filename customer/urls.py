from django.conf.urls import url

from customer import views

urlpatterns = [
    url(r'^register_customer$', views.register_customer, name='register_customer'),
    url(r'^register_account/(?P<national_id>\w+)$', views.register_account, name='register_account'),
    url(r'^disable_account$', views.disable_account, name='disable_account'),
    url(r'^verify_customer$', views.verify_customer, name='verify_customer'),
    url(r'^verify_customer/(?P<national_id>\w+)/(?P<state>.*)$', views.verify_customer_state, name='verify_customer'),
]
