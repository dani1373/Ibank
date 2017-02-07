from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.decorators import login_required

from bank.models import Bank
from client.views import client_form, client_listh
from customer.models import Account
from handlers import ValidateRole
from service.models import BillType, ChequeBook, Cheque, Bill, PeriodicOrder, Loan
from transaction.models import Transaction


@login_required
@ValidateRole(['Bank Admin'])
def define_bill(request):
    data = {
        'title': _('Define annual profit'),
        'fields': [
            {'id': 'account_number', 'label': _('Account Number'), 'value': '', 'type': 'text'},
            {'id': 'name', 'label': _('Bill Name'), 'value': '', 'type': 'text'},
        ]
    }

    if request.method == 'GET':
        return client_form(request, data=data)
    if request.method == 'POST':
        try:
            name = request.POST['name']
            account_number = request.POST['account_number']

            if not Account.objects.filter(account_number=account_number).exists():
                data['error'] = True
                data['message'] = _('There is no account with account number {}').format(account_number)
                return client_form(request, data=data)

            account = Account.objects.get(account_number=account_number)
            if account.state not in 'A':
                data['error'] = True
                data['message'] = _('Account {} is not active').format(account_number)
                return client_form(request, data=data)

            bill_type = BillType.objects.create(destination_account=account, name=name)
            data['success'] = True
            data['message'] = _('Bill {} created with id {} and account number {}').format(name, bill_type.id,
                                                                                           account_number)
            return client_form(request, data=data)
        except:
            data['error'] = True
            return client_form(request, data=data)


@login_required
@ValidateRole(['Cashier'])
def create_cheque_book(request):
    data = {
        'title': _('Create Cheque Book'),
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
            if account.state not in 'A':
                data['error'] = True
                data['message'] = _('Account {} is not active').format(account_number)
                return client_form(request, data=data)

            cheque_book = ChequeBook(account=account)
            cheque_book.save()

            cheque_list = []
            for i in range(10):
                cheque = Cheque(cheque_book=cheque_book)
                cheque.save()

                cheque_list.append(str(cheque.id))

            data['success'] = True
            data['message'] = _('Cheque book with id {} created for account number {}. Paper id\'s for this book are {}'
                                ).format(cheque_book.id, account_number, ', '.join(cheque_list))
            return client_form(request, data=data)
        except:
            data['error'] = True
            return client_form(request, data=data)


@login_required
@ValidateRole(['Cashier'])
def cheque_transaction(request):
    data = {
        'title': _('Cheque Transaction'),
        'fields': [
            {'id': 'cheque', 'label': _('cheque id'), 'value': '', 'type': 'text'},
            {'id': 'destination', 'label': _('destination account'), 'value': '', 'type': 'text'},
            {'id': 'amount', 'label': _('amount'), 'value': '0', 'type': 'text'},
        ]
    }

    if request.method == 'GET':
        return client_form(request, data=data)
    if request.method == 'POST':
        try:
            cheque_id = request.POST['cheque']
            destination_account_number = request.POST['destination']

            if not Cheque.objects.filter(id=cheque_id).exists():
                data['error'] = True
                data['message'] = _('There is no cheque with id {}').format(cheque_id)
                return client_form(request, data=data)

            cheque = Cheque.objects.get(id=cheque_id)
            if cheque.state not in 'N':
                data['error'] = True
                data['message'] = _('Cheque with id {} has been used previously').format(cheque_id)
                return client_form(request, data=data)

            source_account = cheque.cheque_book.account
            if source_account.state == 'D':
                data['error'] = True
                data['message'] = _('This cheque account is disabled')
                return client_form(request, data=data)

            if destination_account_number and not Account.objects.filter(account_number=destination_account_number).exists():
                data['error'] = True
                data['message'] = _('There is no account with number {}').format(destination_account_number)
                return client_form(request, data=data)

            try:
                amount = int(request.POST['amount'])
                if amount <= 0:
                    data['error'] = True
                    data['message'] = _('Amount should be greater than 0')
                    return client_form(request, data=data)
            except ValueError:
                data['error'] = True
                data['message'] = _('Invalid amount')
                return client_form(request, data=data)

            transaction_commission = 0
            if destination_account_number:
                transaction_commission = Bank.objects.all()[0].transfer_commission

            if amount + transaction_commission > source_account.credit:
                data['error'] = True
                data['message'] = _('Your account has not enough credit')
                # TODO notify
                return client_form(request, data=data)

            destination_account = None
            if destination_account_number:
                destination_account = Account.objects.get(account_number=destination_account_number)
                if destination_account.state == 'D':
                    data['error'] = True
                    data['message'] = _('Account with number {} is disabled').format(destination_account_number)
                    return client_form(request, data=data)

            cheque.amount = amount
            cheque.state = 'WL'
            cheque.save()

            transaction_type = 'T'
            if not destination_account_number:
                transaction_type = 'D'
            Transaction.objects.create(destination_account=destination_account, source_account=source_account,
                                       amount=cheque.amount, cheque=cheque, type=transaction_type, method='C')

            data['success'] = True
            return client_form(request, data=data)
        except:
            data['error'] = True
            return client_form(request, data=data)


@login_required
@ValidateRole(['Lawyer'])
def verify_lawyer_cheque(request):
    data = {
        'title': _('Verify Cheque'),
        'columns': [_('Id'), _('Source'), _('Destination'), _('Amount')],
        'entities': []
    }

    if request.method == 'GET':
        for transaction in Transaction.objects.filter(method='C', cheque__state='WL'):
            data['entities'].append([{'label': transaction.cheque.id},
                                     {'label': transaction.source_account.account_number},
                                     {'label': transaction.destination_account.account_number if
                                     transaction.destination_account else ''},
                                     {'label': transaction.amount},
                                     {'label': _('Accept'), 'href': '/service/lawyer_cheque/%s/accept'
                                                                    % transaction.cheque.id},
                                     {'label': _('Reject'), 'href': '/service/lawyer_cheque/%s/reject'
                                                                    % transaction.cheque.id}])
        return client_listh(request, data=data)


@login_required
@ValidateRole(['Lawyer'])
def lawyer_cheque(request, cheque_id, state):
    data = {
        'title': _('Verify Cheque'),
        'fields': []
    }

    if request.method == 'GET':
        states = ['accept', 'reject']

        if state not in states:
            data['error'] = True
            data['message'] = _('Invalid state')
            return client_form(request, data)

        if not Cheque.objects.filter(id=cheque_id).exists():
            data['error'] = True
            data['message'] = _('No cheque with id {}').format(cheque_id)
            return client_form(request, data=data)

        cheque = Cheque.objects.get(id=cheque_id)

        if state == 'accept':
            cheque.state = 'WA'
            # TODO NOTIFY
        else:
            cheque.state = 'DL'
        cheque.save()

        data['success'] = True
        data['message'] = _('Cheque with id {} state updated').format(cheque_id)
        return client_form(request, data)
    if request.method == 'POST':
        return HttpResponseRedirect('/service/verify_lawyer_cheque')


@login_required
@ValidateRole(['Auditor'])
def verify_auditor_cheque(request):
    data = {
        'title': _('Verify Cheque'),
        'columns': [_('Id'), _('Source'), _('Destination'), _('Amount')],
        'entities': []
    }

    if request.method == 'GET':
        for transaction in Transaction.objects.filter(method='C', cheque__state='WA'):
            data['entities'].append([{'label': transaction.cheque.id},
                                     {'label': transaction.source_account.account_number},
                                     {'label': transaction.destination_account.account_number
                                     if transaction.destination_account else ''},
                                     {'label': transaction.amount},
                                     {'label': _('Accept'), 'href': '/service/auditor_cheque/%s/accept'
                                                                    % transaction.cheque.id},
                                     {'label': _('Reject'), 'href': '/service/auditor_cheque/%s/reject'
                                                                    % transaction.cheque.id}])
        return client_listh(request, data=data)


@login_required
@ValidateRole(['Auditor'])
def auditor_cheque(request, cheque_id, state):
    data = {
        'title': _('Verify Cheque'),
        'fields': []
    }

    if request.method == 'GET':
        states = ['accept', 'reject']

        if state not in states:
            data['error'] = True
            data['message'] = _('Invalid state')
            return client_form(request, data)

        if not Cheque.objects.filter(id=cheque_id).exists():
            data['error'] = True
            data['message'] = _('No cheque with id {}').format(cheque_id)
            return client_form(request, data=data)

        cheque = Cheque.objects.get(id=cheque_id)

        if state == 'accept':
            cheque.state = 'V'
            # TODO NOTIFY
        else:
            cheque.state = 'DA'
        cheque.save()

        transaction = Transaction.objects.get(cheque__id=cheque_id)

        commission = 0
        if transaction.destination_account:
            commission = Bank.objects.all()[0].transfer_commission

        transaction.source_account.credit -= transaction.amount + commission
        transaction.source_account.save()
        if transaction.destination_account:
            transaction.destination_account.credit += transaction.amount
            transaction.destination_account.save()

        Transaction.objects.create(source_account=transaction.source_account,
                                   destination_account=Account.objects.get(account_number=1),
                                   amount=commission, method='C',
                                   type='T')

        data['success'] = True
        data['message'] = _('Cheque with id {} state updated').format(cheque_id)
        return client_form(request, data)
    if request.method == 'POST':
        return HttpResponseRedirect('/service/verify_auditor_cheque')


@login_required
@ValidateRole(['Cashier'])
def pay_bill(request):
    data = {
        'title': _('Pay Bill'),
        'fields': [
            {'id': 'name', 'label': _('bill name'), 'value': '', 'type': 'text'},
            {'id': 'source', 'label': _('source account'), 'value': '', 'type': 'text'},
            {'id': 'amount', 'label': _('amount'), 'value': '0', 'type': 'text'},
            {'id': 'owner', 'label': _('owner'), 'value': '', 'type': 'text'},
        ]
    }

    if request.method == 'GET':
        return client_form(request, data=data)
    if request.method == 'POST':
        try:
            bill_name = request.POST['name']
            source_account_number = request.POST['source']
            owner = request.POST['owner']

            if not BillType.objects.filter(name=bill_name).exists():
                data['error'] = True
                data['message'] = _('There is no bill with name {}').format(bill_name)
                return client_form(request, data=data)

            try:
                amount = int(request.POST['amount'])
                if amount <= 0:
                    data['error'] = True
                    data['message'] = _('Amount should be greater than 0')
                    return client_form(request, data=data)
            except ValueError:
                data['error'] = True
                data['message'] = _('Invalid amount')
                return client_form(request, data=data)

            if source_account_number and not Account.objects.filter(account_number=source_account_number).exists():
                data['error'] = True
                data['message'] = _('There is no account with number {}').format(source_account_number)
                return client_form(request, data=data)

            source_account = None
            if source_account_number:
                source_account = Account.objects.get(account_number=source_account_number)
                if source_account.state == 'D':
                    data['error'] = True
                    data['message'] = _('Account with number {} is disabled').format(source_account_number)
                    return client_form(request, data=data)
                if amount > source_account.credit:
                    data['error'] = True
                    data['message'] = _('Your account has not enough credit')
                    return client_form(request, data=data)

            bill_type = BillType.objects.get(name=bill_name)
            destination_account = bill_type.destination_account
            if destination_account.state == 'D':
                data['error'] = True
                data['message'] = _('Account with number {} is disabled').format(destination_account.account_number)
                return client_form(request, data=data)

            bill = Bill.objects.create(bill_type=bill_type, amount=amount, owner=owner)

            transaction_type = 'T'
            if not source_account_number:
                transaction_type = 'D'

            if source_account:
                source_account.credit -= amount
                source_account.save()

            destination_account.credit += amount
            destination_account.save()

            Transaction.objects.create(destination_account=destination_account, source_account=source_account,
                                       amount=amount, bill=bill, type=transaction_type, method='B')

            data['success'] = True
            return client_form(request, data=data)
        except:
            data['error'] = True
            return client_form(request, data=data)


@login_required
@ValidateRole(['Cashier'])
def create_perodic_order(request):
    data = {
        'title': _('Periodic Order'),
        'fields': [
            {'id': 'source', 'label': _('source account'), 'value': '', 'type': 'text'},
            {'id': 'destination', 'label': _('destination account'), 'value': '', 'type': 'text'},
            {'id': 'amount', 'label': _('amount'), 'value': '0', 'type': 'text'},
            {'id': 'count', 'label': _('count'), 'value': '0', 'type': 'text'},
            {'id': 'type', 'label': _('type'), 'value': _('Daily: 1 - Weekly: 2 - Monthly: 3 - Yearly: 4'),
             'type': 'text'},
        ]
    }

    if request.method == 'GET':
        return client_form(request, data=data)
    if request.method == 'POST':
        try:
            source_account_number = request.POST['source']
            destination_account_number = request.POST['destination']
            type_number = request.POST['type']

            try:
                amount = int(request.POST['amount'])
                if amount <= 0:
                    data['error'] = True
                    data['message'] = _('Amount should be greater than 0')
                    return client_form(request, data=data)
            except ValueError:
                data['error'] = True
                data['message'] = _('Invalid amount')
                return client_form(request, data=data)

            try:
                count = int(request.POST['count'])
                if count <= 0:
                    data['error'] = True
                    data['message'] = _('count should be greater than 0')
                    return client_form(request, data=data)
            except ValueError:
                data['error'] = True
                data['message'] = _('Invalid count')
                return client_form(request, data=data)

            if not source_account_number or not destination_account_number:
                data['error'] = True
                data['message'] = _('Please enter source and destination account number')
                return client_form(request, data=data)

            if not Account.objects.filter(account_number=source_account_number).exists():
                data['error'] = True
                data['message'] = _('There is no account with number {}').format(source_account_number)
                return client_form(request, data=data)

            if not Account.objects.filter(account_number=destination_account_number).exists():
                data['error'] = True
                data['message'] = _('There is no account with number {}').format(destination_account_number)
                return client_form(request, data=data)

            source_account = Account.objects.get(account_number=source_account_number)
            if source_account.state == 'D':
                data['error'] = True
                data['message'] = _('Account with number {} is disabled').format(source_account_number)
                return client_form(request, data=data)

            destination_account = Account.objects.get(account_number=destination_account_number)
            if destination_account.state == 'D':
                data['error'] = True
                data['message'] = _('Account with number {} is disabled').format(destination_account.account_number)
                return client_form(request, data=data)

            types_map = {
                '1': 'D',
                '2': 'W',
                '3': 'M',
                '4': 'Y',
            }
            if type_number not in types_map:
                data['error'] = True
                data['message'] = _('Please enter valid type')
                return client_form(request, data=data)

            periodic_order = PeriodicOrder(type=types_map[type_number], count=count, amount=amount,
                                           source_account=source_account, destination_account=destination_account)
            periodic_order.save()

            data['success'] = True
            return client_form(request, data=data)
        except:
            data['error'] = True
            return client_form(request, data=data)


@login_required
@ValidateRole(['Cashier'])
def loan_request(request):
    data = {
        'title': _('Loan Request'),
        'fields': [
            {'id': 'account', 'label': _('account number'), 'value': '', 'type': 'text'},
            {'id': 'amount', 'label': _('amount'), 'value': '0', 'type': 'text'},
            {'id': 'count', 'label': _('count'), 'value': '0', 'type': 'text'},
        ]
    }

    if request.method == 'GET':
        return client_form(request, data=data)
    if request.method == 'POST':
        try:
            source_account_number = request.POST['account']

            try:
                amount = int(request.POST['amount'])
                if amount <= 0:
                    data['error'] = True
                    data['message'] = _('Amount should be greater than 0')
                    return client_form(request, data=data)
            except ValueError:
                data['error'] = True
                data['message'] = _('Invalid amount')
                return client_form(request, data=data)

            try:
                count = int(request.POST['count'])
                if count <= 0:
                    data['error'] = True
                    data['message'] = _('count should be greater than 0')
                    return client_form(request, data=data)
            except ValueError:
                data['error'] = True
                data['message'] = _('Invalid count')
                return client_form(request, data=data)

            if not source_account_number:
                data['error'] = True
                data['message'] = _('Please enter source account number')
                return client_form(request, data=data)

            if not Account.objects.filter(account_number=source_account_number).exists():
                data['error'] = True
                data['message'] = _('There is no account with number {}').format(source_account_number)
                return client_form(request, data=data)

            source_account = Account.objects.get(account_number=source_account_number)
            if source_account.state == 'D':
                data['error'] = True
                data['message'] = _('Account with number {} is disabled').format(source_account_number)
                return client_form(request, data=data)

            bank_account = Account.objects.get(account_number=1)
            if amount > bank_account.credit:
                data['error'] = True
                data['message'] = _('Bank has not {} money').format(amount)
                return client_form(request, data=data)

            Loan.objects.create(account=source_account, amount=amount, count=count)

            data['success'] = True
            return client_form(request, data=data)
        except:
            data['error'] = True
            return client_form(request, data=data)


@login_required
@ValidateRole(['Lawyer'])
def verify_lawyer_loan(request):
    data = {
        'title': _('Verify Loan'),
        'columns': [_('Account Number'), _('Amount'), _('Count')],
        'entities': []
    }

    if request.method == 'GET':
        for loan in Loan.objects.filter(state='WL'):
            data['entities'].append([{'label': loan.account.account_number},
                                     {'label': loan.amount},
                                     {'label': loan.count},
                                     {'label': _('Accept'), 'href': '/service/lawyer_loan/%s/accept'
                                                                    % loan.id},
                                     {'label': _('Reject'), 'href': '/service/lawyer_loan/%s/reject'
                                                                    % loan.id}])
        return client_listh(request, data=data)


@login_required
@ValidateRole(['Lawyer'])
def lawyer_loan(request, loan_id, state):
    data = {
        'title': _('Verify Loan'),
        'fields': []
    }

    if request.method == 'GET':
        states = ['accept', 'reject']

        if state not in states:
            data['error'] = True
            data['message'] = _('Invalid state')
            return client_form(request, data)

        if not Loan.objects.filter(id=loan_id).exists():
            data['error'] = True
            data['message'] = _('No loan with id {}').format(loan_id)
            return client_form(request, data=data)

        loan = Loan.objects.get(id=loan_id)

        if state == 'accept':
            loan.state = 'WA'
            # TODO NOTIFY
        else:
            loan.state = 'DL'
        loan.save()

        data['success'] = True
        data['message'] = _('Loan with id {} state updated').format(loan_id)
        return client_form(request, data)
    if request.method == 'POST':
        return HttpResponseRedirect('/service/verify_lawyer_loan')


@login_required
@ValidateRole(['Auditor'])
def verify_auditor_loan(request):
    data = {
        'title': _('Verify Loan'),
        'columns': [_('Account Number'), _('Amount'), _('Count')],
        'entities': []
    }

    if request.method == 'GET':
        for loan in Loan.objects.filter(state='WA'):
            data['entities'].append([{'label': loan.account.account_number},
                                     {'label': loan.amount},
                                     {'label': loan.count},
                                     {'label': _('Accept'), 'href': '/service/auditor_loan/%s/accept'
                                                                    % loan.id},
                                     {'label': _('Reject'), 'href': '/service/auditor_loan/%s/reject'
                                                                    % loan.id}])
        return client_listh(request, data=data)


@login_required
@ValidateRole(['Auditor'])
def auditor_loan(request, loan_id, state):
    data = {
        'title': _('Verify Loan'),
        'fields': []
    }

    if request.method == 'GET':
        states = ['accept', 'reject']

        if state not in states:
            data['error'] = True
            data['message'] = _('Invalid state')
            return client_form(request, data)

        if not Loan.objects.filter(id=loan_id).exists():
            data['error'] = True
            data['message'] = _('No loan with id {}').format(loan_id)
            return client_form(request, data=data)

        loan = Loan.objects.get(id=loan_id)

        if state == 'accept':
            loan.state = 'V'
            # TODO NOTIFY
        else:
            loan.state = 'DA'
        loan.save()

        transaction = Transaction.objects.create(source_account=Account.objects.get(account_number=1),
                                                 destination_account=loan.account, amount=loan.amount, type='T',
                                                 method='H')

        transaction.source_account.credit -= transaction.amount
        transaction.source_account.save()

        transaction.destination_account.credit += transaction.amount
        transaction.destination_account.save()

        benefit = 0.0117 * loan.count * loan.amount
        PeriodicOrder.objects.create(amount=int(benefit)+loan.amount, count=loan.count, loan=loan, type='M',
                                     source_account=loan.account,
                                     destination_account=Account.objects.get(account_number=1))

        data['success'] = True
        data['message'] = _('Loan with id {} state updated').format(loan_id)
        return client_form(request, data)
    if request.method == 'POST':
        return HttpResponseRedirect('/service/verify_auditor_loan')
