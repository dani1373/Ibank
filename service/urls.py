from django.conf.urls import url

from service import views

urlpatterns = [
    url(r'^define_bill$', views.define_bill, name='define_bill'),
    url(r'^create_cheque_book$', views.create_cheque_book, name='create_cheque_book'),
    url(r'^cheque_transaction$', views.cheque_transaction, name='cheque_transaction'),
    url(r'^verify_lawyer_cheque$', views.verify_lawyer_cheque, name='verify_lawyer_cheque'),
    url(r'^lawyer_cheque/(?P<cheque_id>\w+)/(?P<state>.*)$', views.lawyer_cheque, name='lawyer_cheque'),
    url(r'^verify_auditor_cheque$', views.verify_auditor_cheque, name='verify_auditor_cheque'),
    url(r'^auditor_cheque/(?P<cheque_id>\w+)/(?P<state>.*)$', views.auditor_cheque, name='auditor_cheque'),
    url(r'^pay_bill$', views.pay_bill, name='pay_bill'),
    url(r'^create_perodic_order$', views.create_perodic_order, name='create_perodic_order'),
    url(r'^loan_request$', views.loan_request, name='loan_request'),
    url(r'^verify_lawyer_loan$', views.verify_lawyer_loan, name='verify_lawyer_loan'),
    url(r'^lawyer_loan/(?P<loan_id>\w+)/(?P<state>.*)$', views.lawyer_loan, name='lawyer_loan'),
    url(r'^verify_auditor_loan$', views.verify_auditor_loan, name='verify_auditor_loan'),
    url(r'^auditor_loan/(?P<loan_id>\w+)/(?P<state>.*)$', views.auditor_loan, name='auditor_loan'),
]
