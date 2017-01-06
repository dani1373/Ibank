from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from customer.models import Account
from handlers import ValidateRole
from service.models import BillType


@login_required
@ValidateRole(['Bank Admin'])
def define_bill(request):
    if request.method == 'GET':
        return HttpResponse('client view')
    if request.method == 'POST':
        name = request.POST['name']
        account_number = request.POST['account_number']

        if not Account.objects.filter(account_number=account_number).exists():
            return HttpResponse('There is no account with account number %s' % account_number)

        account = Account.objects.get(account_number=account_number)
        if account.state not in 'A':
            return HttpResponse('Account %s is not active' % account_number)

        bill_type = BillType.objects.create(account=account, name=name)
        return HttpResponse('Bill %s created with id %s and account number %s' % (name, bill_type.id, account_number))
