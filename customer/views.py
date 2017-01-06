import random

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from customer.models import Customer, Account
from handlers import ValidateRole
from profile.models import Profile


@login_required
@ValidateRole(['Cashier'])
def register_customer(request):
    if request.method == 'GET':
        return HttpResponse('client page')
    if request.method == 'POST':
        profile = Profile.register(request.POST)

        if Customer.objects.filter(profile=profile).exists():
            return HttpResponseRedirect('customer/register_account/%s' % profile.national_id)

        customer = Customer.objects.create(profile=profile)
        return HttpResponseRedirect('customer/register_account/%s' % profile.national_id)


@login_required
@ValidateRole(['Cashier'])
def register_account(request, national_id):
    if request.method == 'GET':
        if not Customer.objects.filter(profile__national_id=national_id).exists():
            return HttpResponse('customer not exists')
        else:
            customer = Customer.objects.get(profile__national_id=national_id)
            if customer.state == 'W':
                return HttpResponse('Waiting to be verified')
            if customer.state == 'D':
                return HttpResponse('Customer is disabled')
            if customer.state == 'A':
                return HttpResponse('client page')

    if request.method == 'POST':
        amount = request.POST['amount']
        customer = Customer.objects.get(profile__national_id=national_id)
        employee = request.user.profile.employee

        if amount < 10 * 1000 or customer.state not in 'A':
            return HttpResponse('Invalid request')

        account = Account.objects.create(customer=customer, employee=employee, branch=employee.branch,
                                         account_number=random.randrange(int(1e9), int(1e10)), credit=amount)

        return HttpResponse('an account for customer %s created with credit %s by employee %s'
                            % (customer.profile.national_id, account.amount, employee.profile.national_id))


@login_required
@ValidateRole(['Lawyer'])
def disable_account(request):
    if request.method == 'GET':
        return HttpResponse('client view')
    if request.method == 'POST':
        account_number = request.POST['account_number']

        if not Account.objects.filter(account_number=account_number).exists():
            return HttpResponse('There is no account with account number %s' % account_number)

        account = Account.objects.get(account_number=account_number)
        account.state = 'D'
        account.save()

        return HttpResponse('Account with number %s is disabled' % account.account_number)
