from django.conf.urls import url

from customer import views

urlpatterns = [
    url(r'^register_customer$', views.register_customer, name='register_customer'),
    url(r'^register_account/(?P<national_id>\w+)$', views.register_account, name='register_account'),
    url(r'^disbale_account$', views.disable_account, name='disable_account'),
]
