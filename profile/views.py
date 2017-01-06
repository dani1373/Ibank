from django.utils.translation import ugettext_lazy as _

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from client.views import client_login, client_index


def home_page(request, user):
    home_page_data = [
        {'role': _('Bank Admin'), 'name': _('Annual profit'), 'href': '/bank/define_annual_profit'},
        {'role': _('Bank Admin'), 'name': _('Create branch admin'), 'href': '/modir/register_branch_admin'},
        {'role': _('Bank Admin'), 'name': _('Create branch'), 'href': '/bank/create_branch'},
        {'role': _('Bank Admin'), 'name': _('Assign admin to branch'), 'href': '/bank/assign_admin'},
        {'role': _('Bank Admin'), 'name': _('Get admin report'), 'href': '/'},
        {'role': _('Bank Admin'), 'name': _('Create bill'), 'href': '/service/define_bill'},
        {'role': _('Bank Admin'), 'name': _('Transaction commission'), 'href': '/'},
        {'role': _('Bank Admin'), 'name': _('Loan report'), 'href': '/'},

        {'role': _('Branch Admin'), 'name': _('Create employee account'), 'href': '/employee/register_employee'},
        {'role': _('Branch Admin'), 'name': _('Assign role'), 'href': '/'},
        {'role': _('Branch Admin'), 'name': _('Define money'), 'href': '/'},
        {'role': _('Branch Admin'), 'name': _('Define atm'), 'href': '/'},
        {'role': _('Branch Admin'), 'name': _('Define minimum amount for atm'), 'href': '/'},
        {'role': _('Branch Admin'), 'name': _('Assign money to atm'), 'href': '/'},
        {'role': _('Branch Admin'), 'name': _('Loan report'), 'href': '/'},

        {'role': _('Lawyer'), 'name': _('Disable account'), 'href': '/customer/disable_account'},
        {'role': _('Lawyer'), 'name': _('Verify customer information'), 'href': '/'},
        {'role': _('Lawyer'), 'name': _('Verify cheque'), 'href': '/'},
        {'role': _('Lawyer'), 'name': _('Verify loan'), 'href': '/'},

        {'role': _('Cashier'), 'name': _('Create account'), 'href': '/customer/register_customer'},
        {'role': _('Cashier'), 'name': _('Create transaction'), 'href': '/'},
        {'role': _('Cashier'), 'name': _('Cheque creation request'), 'href': '/'},
        {'role': _('Cashier'), 'name': _('Cheque transaction'), 'href': '/'},
        {'role': _('Cashier'), 'name': _('Bill transaction'), 'href': '/'},
        {'role': _('Cashier'), 'name': _('Profile transaction report'), 'href': '/'},
        {'role': _('Cashier'), 'name': _('Periodic order creation'), 'href': '/'},
        {'role': _('Cashier'), 'name': _('Loan request'), 'href': '/'},

        {'role': _('Auditor'), 'name': _('Verify cheque'), 'href': '/'},
        {'role': _('Auditor'), 'name': _('Verify loan'), 'href': '/'},
        {'role': _('Auditor'), 'name': _('Auditor report'), 'href': '/'},

        {'role': _('ATM Master'), 'name': _('Put money in atm'), 'href': '/'},

        {'role': _('Customer'), 'name': _('ATM transaction'), 'href': '/'},
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
