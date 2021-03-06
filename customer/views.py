from django.utils.translation import ugettext_lazy as _

import random

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from client.views import client_form, client_listh
from customer.models import Customer, Account
from handlers import ValidateRole
from profile.models import Profile


@login_required
@ValidateRole(['Cashier'])
def register_customer(request):
    data = {
        'title': _('Register Account'),
        'fields': [
            {'id': 'first_name', 'label': _('first name'), 'value': '', 'type': 'text'},
            {'id': 'last_name', 'label': _('last name'), 'value': '', 'type': 'text'},
            {'id': 'national_id', 'label': _('national id'), 'value': '', 'type': 'text'},
            {'id': 'phone_number', 'label': _('phone number'), 'value': '', 'type': 'text'},
            {'id': 'address', 'label': _('address'), 'value': '', 'type': 'text'},
            {'id': 'email', 'label': _('Email'), 'value': '', 'type': 'text'},
        ]
    }

    if request.method == 'GET':
        return client_form(request, data=data)
    if request.method == 'POST':
        try:
            profile = Profile.register(request.POST)

            if Customer.objects.filter(profile=profile).exists():
                return HttpResponseRedirect('/customer/register_account/%s' % profile.national_id)

            customer = Customer.objects.create(profile=profile)
            return HttpResponseRedirect('/customer/register_account/%s' % customer.profile.national_id)
        except:
            data['error'] = True
            return client_form(request, data=data)


@login_required
@ValidateRole(['Cashier'])
def register_account(request, national_id):
    data = {
        'title': _('Register Account'),
        'fields': []
    }

    if request.method == 'GET':
        if not Customer.objects.filter(profile__national_id=national_id).exists():
            data['error'] = True
            data['message'] = _('customer not exists')
            return client_form(request, data=data)
        else:
            customer = Customer.objects.get(profile__national_id=national_id)
            if customer.state == 'W':
                data['error'] = True
                data['message'] = _('customer is waiting to be verified')
                return client_form(request, data=data)
            if customer.state == 'D':
                data['error'] = True
                data['message'] = _('customer is disabled')
                return client_form(request, data=data)
            if customer.state == 'A':
                data['fields'] = [{'id': 'amount', 'label': _('Amount'), 'value': 0, 'type': 'text'}]
                return client_form(request, data)

    if request.method == 'POST':
        data['fields'] = [{'id': 'amount', 'label': _('Amount'), 'value': 0, 'type': 'text'}]
        try:
            customer = Customer.objects.get(profile__national_id=national_id)
            amount = int(request.POST['amount'])
            employee = request.user.profile.employee

            if customer.state not in 'A':
                return HttpResponseRedirect('/customer/register_account/%s' % national_id)

            if amount < 10 * 1000:
                data['error'] = True
                data['message'] = _('Amount should not be less than 10,000')
                return client_form(request, data=data)

            account = Account.objects.create(customer=customer, creator=employee, branch=employee.branch,
                                             account_number=random.randrange(int(1e9), int(1e10)), credit=amount)

            data['success'] = True
            data['message'] = _('an account with number {} for customer {} created with credit {} by employee {}'
                                ).format(account.account_number, customer.profile.national_id, account.credit,
                                         employee.profile.national_id)
            return client_form(request, data=data)
        except:
            return HttpResponseRedirect('/customer/register_account/%s' % national_id)


@login_required
@ValidateRole(['Lawyer'])
def disable_account(request):
    data = {
        'title': _('Disable Account'),
        'fields': [
            {'id': 'account_number', 'label': _('Account Number'), 'value': '', 'type': 'text'},
        ]
    }

    if request.method == 'GET':
        return client_form(request, data=data)
    if request.method == 'POST':
        try:
            account_number = request.POST['account_number']

            if not Account.objects.filter(account_number=account_number).exists():
                data['error'] = True
                data['message'] = _('There is no account with account number {}').format(account_number)
                return client_form(request, data=data)

            account = Account.objects.get(account_number=account_number)
            account.state = 'D'
            account.save()

            data['success'] = True
            data['message'] = _('Account with number {} is disabled').format(account.account_number)
            return client_form(request, data=data)
        except:
            data['error'] = True
            return client_form(request, data=data)


@login_required
@ValidateRole(['Lawyer'])
def verify_customer(request):
    data = {
        'title': _('Verify Customer'),
        'columns': [_('Id'), _('Name'), _('Phone number'), _('Address')],
        'entities': []
    }

    if request.method == 'GET':
        for customer in Customer.objects.filter(state='W'):
            data['entities'].append([{'label': customer.profile.national_id},
                                     {'label': '%s %s' % (customer.profile.user.first_name,
                                                          customer.profile.user.last_name)},
                                     {'label': customer.profile.phone_number},
                                     {'label': customer.profile.address},
                                     {'label': _('Accept'), 'href': '/customer/verify_customer/%s/accept'
                                                                    % customer.profile.national_id},
                                     {'label': _('Reject'), 'href': '/customer/verify_customer/%s/reject'
                                                                    % customer.profile.national_id}])
        return client_listh(request, data=data)


@login_required
@ValidateRole(['Lawyer'])
def verify_customer_state(request, national_id, state):
    data = {
        'title': _('Verify Customer'),
        'fields': []
    }

    if request.method == 'GET':
        states = ['accept', 'reject']

        if state not in states:
            data['error'] = True
            data['message'] = _('Invalid state')
            return client_form(request, data)

        if not Customer.objects.filter(profile__national_id=national_id).exists():
            data['error'] = True
            data['message'] = _('No customer with {} national id').format(national_id)
            return client_form(request, data=data)

        customer = Customer.objects.get(profile__national_id=national_id)

        if state == 'accept':
            customer.state = 'A'
        else:
            customer.state = 'D'
        customer.save()

        data['success'] = True
        data['message'] = _('Customer with national id {} state updated').format(national_id)
        return client_form(request, data)
    if request.method == 'POST':
        return HttpResponseRedirect('/customer/verify_customer')
