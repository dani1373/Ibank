from datetime import datetime, timedelta

import tablib
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _

from bank.models import Bank
from client.views import client_form, client_listh
from customer.models import Account
from employee.models import Employee
from handlers import ValidateRole
from transaction.models import Transaction


@login_required
@ValidateRole(['Cashier'])
def create_transaction(request):
    data = {
        'title': _('Create Transaction'),
        'fields': [
            {'id': 'source', 'label': _('source account'), 'value': '', 'type': 'text'},
            {'id': 'destination', 'label': _('destination account'), 'value': '', 'type': 'text'},
            {'id': 'amount', 'label': _('amount'), 'value': '0', 'type': 'text'},
        ]
    }

    if request.method == 'GET':
        return client_form(request, data=data)
    if request.method == 'POST':
        try:
            source_account_number = request.POST['source']
            destination_account_number = request.POST['destination']

            if not source_account_number and not destination_account_number:
                data['error'] = True
                data['message'] = _('Source and destination could not be empty together')
                return client_form(request, data=data)

            if source_account_number and not Account.objects.filter(account_number=source_account_number).exists():
                data['error'] = True
                data['message'] = _('There is no account with number {}').format(source_account_number)
                return client_form(request, data=data)

            if destination_account_number and not Account.objects.filter(account_number=destination_account_number).exists():
                data['error'] = True
                data['message'] = _('There is no account with number {}').format(destination_account_number)
                return client_form(request, data=data)

            try:
                amount = int(request.POST['amount'])
                if amount < 0:
                    data['error'] = True
                    data['message'] = _('Amount should be greater than 0')
                    return client_form(request, data=data)
            except ValueError:
                data['error'] = True
                data['message'] = _('Invalid amount')
                return client_form(request, data=data)

            destination_account = None
            source_account = None

            transaction_commission = 0
            if destination_account_number and source_account_number:
                transaction_commission = Bank.objects.all()[0].transfer_commission

            if destination_account_number:
                destination_account = Account.objects.get(account_number=destination_account_number)
                if destination_account.state == 'D':
                    data['error'] = True
                    data['message'] = _('Account with number {} is disabled').format(destination_account_number)
                    return client_form(request, data=data)

                destination_account.credit += amount
                destination_account.save()

            if source_account_number:
                source_account = Account.objects.get(account_number=source_account_number)
                if source_account.state == 'D':
                    data['error'] = True
                    data['message'] = _('Account with number {} is disabled').format(source_account_number)
                    return client_form(request, data=data)
                if amount + transaction_commission > source_account.credit:
                    data['error'] = True
                    data['message'] = _('Your account has not enough credit')
                    return client_form(request, data=data)

                source_account.credit -= amount + transaction_commission
                source_account.save()

            transaction_type = 'T'
            if not source_account_number:
                transaction_type = 'D'
            if not destination_account_number:
                transaction_type = 'W'

            transaction = Transaction(source_account=source_account, destination_account=destination_account,
                                      amount=amount, type=transaction_type, method='H',
                                      employee=request.user.profile.employee)
            transaction.save()

            if transaction.type == 'T':
                bank_account = Account.objects.get(account_number=1)
                Transaction.objects.create(amount=transaction_commission, destination_account=bank_account, method='H',
                                           type='D', source_account=source_account)
                bank_account.credit += transaction_commission
                bank_account.save()
            data['success'] = True
            return client_form(request, data=data)
        except:
            data['error'] = True
            return client_form(request, data=data)


@login_required
@ValidateRole(['Auditor'])
def auditor_report(request):
    data = {
        'title': _('Auditor Report'),
        'fields': [
            {'id': 'from_date', 'label': _('From Date'), 'value': '2017/1/1', 'type': 'text'},
            {'id': 'to_date', 'label': _('To Date'), 'value': '', 'type': 'text'},
            {'id': 'cashier', 'label': _('Cashier National Id'), 'value': '', 'type': 'text'},
        ]
    }

    if request.method == 'GET':
        return client_form(request, data=data)
    if request.method == 'POST':
        try:
            from_date = datetime(*[int(x) for x in request.POST['from_date'].split('/')])
            if request.POST['to_date']:
                to_date = datetime(*[int(x) for x in request.POST['to_date'].split('/')])
            else:
                to_date = from_date + timedelta(days=1)
            if request.POST['cashier']:
                if not Employee.objects.filter(type='C', profile__national_id=request.POST['cashier']).exists():
                    data['error'] = True
                    data['message'] = _('There is no cashier with national id {}').format(request.POST['cashier'])
                    return client_form(request, data=data)
                cashier = request.POST['cashier']
            else:
                cashier = 0

            return HttpResponseRedirect('/transaction/auditor_report_result/%s/%s/%s' % (str(from_date), str(to_date),
                                                                                         cashier))
        except:
            data['error'] = True
            return client_form(request, data=data)


@login_required
@ValidateRole(['Auditor'])
def auditor_report_result(request, from_date, to_date, cashier):
    data = {
        'title': _('Auditor Transaction Report'),
        'columns': [_('Cashier'), _('Source Account'), _('Destination Account'), _('Amount')],
        'entities': []
    }

    if request.method == 'GET':
        begin = datetime.strptime(from_date, "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(to_date, "%Y-%m-%d %H:%M:%S")
        print begin, end
        if cashier == '0':
            transactions = Transaction.objects.filter(create_time__gte=begin, create_time__lt=end, type__in=['D', 'W'],
                                                      employee__isnull=False)
        else:
            cashier_employee = Employee.objects.get(profile__national_id=cashier)
            transactions = Transaction.objects.filter(create_time__gte=begin, create_time__lt=end,
                                                      employee=cashier_employee, type__in=['D', 'W'])
        for transaction in transactions:
            data['entities'].append([{'label': transaction.employee.profile.national_id},
                                     {'label': transaction.source_account.account_number
                                     if transaction.source_account else ''},
                                     {'label': transaction.destination_account.account_number
                                     if transaction.destination_account else ''},
                                     {'label': transaction.amount}])
        return client_listh(request, data=data)


@login_required
@ValidateRole(['Cashier'])
def profile_report(request):
    data = {
        'title': _('Auditor Report'),
        'fields': [
            {'id': 'from_date', 'label': _('From Date'), 'value': '2017/1/1', 'type': 'text'},
            {'id': 'to_date', 'label': _('To Date'), 'value': '2017/1/1', 'type': 'text'},
            {'id': 'count', 'label': _('Count'), 'value': '', 'type': 'text'},
            {'id': 'type', 'label': _('Type'), 'value': 'PDF or XLS', 'type': 'text'},
            {'id': 'account', 'label': _('Account Number'), 'value': '', 'type': 'text'},
        ]
    }

    if request.method == 'GET':
        return client_form(request, data=data)
    if request.method == 'POST':
        try:
            try:
                account = Account.objects.get(account_number=request.POST['account'])
            except:
                data['error'] = True
                data['message'] = _('There is no account with number {}').format(request.POST['account'])
                return client_form(request, data=data)
            if request.POST['from_date']:
                from_date = datetime(*[int(x) for x in request.POST['from_date'].split('/')])
                to_date = datetime(*[int(x) for x in request.POST['to_date'].split('/')])
                transactions = []
                for transaction in Transaction.objects.filter(create_time__gte=from_date, create_time__lt=to_date):
                    if transaction.source_account == account or transaction.destination_account == account:
                        transactions.append(transaction)
            else:
                transactions = []
                for transaction in Transaction.objects.all().order_by('-create_time'):
                    if transaction.source_account == account or transaction.destination_account == account:
                        transactions.append(transaction)
                transactions = transactions[:int(request.POST['count'])]

            view_transactions = []
            for transaction in transactions:
                view_transactions.append((str(transaction.create_time), transaction.source_account.account_number if
                transaction.source_account else '', transaction.destination_account.account_number if
                transaction.destination_account else '', transaction.amount))

            if request.POST['type'] == 'XLS':
                data = tablib.Dataset(*view_transactions, headers=['Create Time', 'Source Account Number',
                                                                   'Destination Account Number', 'Amount'])

                response = HttpResponse(data.xls, content_type="application/ms-excel")
                response['Content-Disposition'] = 'attachment; filename=%s.xls' % account.account_number
                return response
            if request.POST['type'] == 'PDF':
                data = tablib.Dataset(*view_transactions, headers=['Create Time', 'Source Account Number',
                                                                   'Destination Account Number', 'Amount'])
                
                response = HttpResponse(data.xls, content_type="application/ms-excel")
                response['Content-Disposition'] = 'attachment; filename=%s.xls' % account.account_number
                return response

            data['error'] = True
            data['message'] = _('You should choose a valid type')
            return client_form(request, data=data)
        except:
            data['error'] = True
            return client_form(request, data=data)
