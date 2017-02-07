from django.conf.urls import url

from modir import views

urlpatterns = [
    url(r'^register_branch_admin$', views.register_branch_admin, name='register_branch_admin'),
    url(r'^loan_report$', views.loan_report, name='loan_report'),
]
