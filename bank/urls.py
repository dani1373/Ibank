from django.conf.urls import url

from bank import views

urlpatterns = [
    url(r'^define_annual_profit$', views.define_annual_profit, name='define_annual_profit'),
    url(r'^create_branch$', views.create_branch, name='create_branch'),
    url(r'^assign_admin$', views.assign_admin, name='assign_admin'),
    url(r'^assign_admin/(?P<branch_id>\w+)$', views.assign_admin_branch, name='assign_admin'),
    url(r'^assign_admin/(?P<branch_id>\w+)/(?P<national_id>\w+)$', views.assign_admin_branch_national,
        name='assign_admin'),
]
