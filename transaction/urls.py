from django.conf.urls import url

from transaction import views

urlpatterns = [
    url(r'^create_transaction$', views.create_transaction, name='create_transaction'),
    url(r'^auditor_report$', views.auditor_report, name='auditor_report'),
    url(r'^auditor_report_result/(?P<from_date>.*)/(?P<to_date>.*)/(?P<cashier>.*)$', views.auditor_report_result,
        name='auditor_report_result'),
    url(r'^profile_report$', views.profile_report, name='profile_report'),
]
