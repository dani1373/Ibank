from django.conf.urls import url

from atm import views

urlpatterns = [
    url(r'^define_atm$', views.define_atm, name='define_atm'),
    url(r'^define_money$', views.define_money, name='define_money'),
    url(r'^define_minimum$', views.define_minimum, name='define_minimum'),
    url(r'^assign_money$', views.assign_money, name='assign_money'),
    url(r'^create_card$', views.create_card, name='create_card'),
    url(r'^atm_transaction$', views.atm_transaction, name='atm_transaction'),
]
