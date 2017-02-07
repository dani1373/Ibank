from django.utils.translation import ugettext as _

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from client.views import client_login, client_index


def home_page(request, user):
    home_page_data = [
        {'role': 'Bank Admin', 'name': _('Annual profit'), 'href': '/bank/define_annual_profit'},
        {'role': 'Bank Admin', 'name': _('Create branch admin'), 'href': '/modir/register_branch_admin'},
        {'role': 'Bank Admin', 'name': _('Create branch'), 'href': '/bank/create_branch'},
        {'role': 'Bank Admin', 'name': _('Assign admin to branch'), 'href': '/bank/assign_admin'},
        {'role': 'Bank Admin', 'name': _('Get admin report'), 'href': '/'},
        {'role': 'Bank Admin', 'name': _('Create bill'), 'href': '/service/define_bill'},
        {'role': 'Bank Admin', 'name': _('Transaction commission'), 'href': '/bank/transaction_commission'},
        {'role': 'Bank Admin', 'name': _('Loan report'), 'href': '/'},

        {'role': 'Branch Admin', 'name': _('Create employee account'), 'href': '/employee/register_employee'},
        {'role': 'Branch Admin', 'name': _('Assign role'), 'href': '/employee/assign_role'},
        {'role': 'Branch Admin', 'name': _('Define money'), 'href': '/atm/define_money'},
        {'role': 'Branch Admin', 'name': _('Define atm'), 'href': '/atm/define_atm'},
        {'role': 'Branch Admin', 'name': _('Define minimum amount for atm'), 'href': '/atm/define_minimum'},
        {'role': 'Branch Admin', 'name': _('Loan report'), 'href': '/'},

        {'role': 'Lawyer', 'name': _('Disable account'), 'href': '/customer/disable_account'},
        {'role': 'Lawyer', 'name': _('Verify customer information'), 'href': '/customer/verify_customer'},
        {'role': 'Lawyer', 'name': _('Verify cheque'), 'href': '/service/verify_lawyer_cheque'},
        {'role': 'Lawyer', 'name': _('Verify loan'), 'href': '/service/verify_lawyer_loan'},

        {'role': 'Cashier', 'name': _('Create account'), 'href': '/customer/register_customer'},
        {'role': 'Cashier', 'name': _('Create transaction'), 'href': '/transaction/create_transaction'},
        {'role': 'Cashier', 'name': _('Cheque creation request'), 'href': '/service/create_cheque_book'},
        {'role': 'Cashier', 'name': _('Cheque transaction'), 'href': '/service/cheque_transaction'},
        {'role': 'Cashier', 'name': _('Bill transaction'), 'href': '/service/pay_bill'},
        {'role': 'Cashier', 'name': _('Profile transaction report'), 'href': '/'},
        {'role': 'Cashier', 'name': _('Periodic order creation'), 'href': '/service/create_perodic_order'},
        {'role': 'Cashier', 'name': _('Loan request'), 'href': '/service/loan_request'},
        {'role': 'Cashier', 'name': _('Create card'), 'href': '/atm/create_card'},

        {'role': 'Auditor', 'name': _('Verify cheque'), 'href': '/service/verify_auditor_cheque'},
        {'role': 'Auditor', 'name': _('Verify loan'), 'href': '/service/verify_auditor_loan'},
        {'role': 'Auditor', 'name': _('Auditor report'), 'href': '/'},

        {'role': 'ATM Master', 'name': _('Put money in atm'), 'href': '/atm/assign_money'},

        {'role': 'Customer', 'name': _('ATM transaction'), 'href': '/atm/atm_transaction'},
    ]

    if hasattr(user.profile, 'bankadmin'):
        return client_index(request, role='Bank Admin', usecases=home_page_data)
    elif hasattr(user.profile, 'branchadmin'):
        return client_index(request, role='Branch Admin', usecases=home_page_data)
    elif hasattr(user.profile, 'employee'):
        return client_index(request, role=user.profile.employee.get_type_display(), usecases=home_page_data)
    else:
        return client_index(request, role='Customer', usecases=home_page_data)


def login(request):
    if request.method == 'GET':
        if not request.user.is_authenticated():
            return client_login(request)
        else:
            return HttpResponseRedirect('/')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponse('failed')


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/profile/login')
    else:
        return home_page(request, request.user)
