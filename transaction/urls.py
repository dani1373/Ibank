from django.conf.urls import url

from transaction import views

urlpatterns = [
    url(r'^create_transaction$', views.create_transaction, name='create_transaction'),
]
