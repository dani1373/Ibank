import random

from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _

from atm.models import ATM, Money, ATMMoney, AddMoney, Card
from bank.models import Bank
from client.views import client_form
from customer.models import Account
from employee.models import Employee
from handlers import ValidateRole
from transaction.models import Transaction


@login_required
@ValidateRole(['Branch Admin'])
def define_atm(request):
    data = {
        'title': _('Define ATM'),
        'fields': [
            {'id': 'count', 'label': _('Count'), 'value': '1', 'type': 'text'},
        ]
    }

    if request.method == 'GET':
        return client_form(request, data=data)
    if request.method == 'POST':
        try:
            try:
                count = int(request.POST['count'])
                if count <= 0:
                    data['error'] = True
                    data['message'] = _('count must be greater than 0')
                    return client_form(request, data=data)
            except ValueError:
                data['error'] = True
                data['message'] = _('Please enter a valid integer')
                return client_form(request, data=data)

            try:
                branch = request.user.profile.branchadmin.branch
            except:
                data['error'] = True
                data['message'] = _('You are not assigned to any branch')
                return client_form(request, data=data)

            atm_ids = []
            for i in range(count):
                atm = ATM.objects.create(branch=branch)
                atm_ids.append(str(atm.id))

                for money in Money.objects.all():
                    ATMMoney.objects.create(atm=atm, money=money)

            data['success'] = True
            data['message'] = _('We created {} ATM for branch with id {}. ATM id\'s are {}'
                                ).format(count, branch.id, ', '.join(atm_ids))
            return client_form(request, data=data)
        except:
            data['error'] = True
            return client_form(request, data=data)


@login_required
@ValidateRole(['Branch Admin'])
def define_money(request):
    data = {
        'title': _('Define Money'),
        'fields': [
            {'id': 'amount', 'label': _('Amount'), 'value': '0', 'type': 'text'},
        ]
    }

    if request.method == 'GET':
        return client_form(request, data=data)
    if request.method == 'POST':
        try:
            amount = int(request.POST['amount'])

            if Money.objects.filter(amount=amount).exists():
                data['error'] = True
                data['message'] = _('There is money with amount {}').format(amount)
                return client_form(request, data=data)
            money = Money.objects.create(amount=amount)

            for atm in ATM.objects.all():
                ATMMoney.objects.create(atm=atm, money=money)

            data['success'] = True
            data['message'] = _('Money created with amount {}'
                                ).format(amount)
            return client_form(request, data=data)
        except:
            data['error'] = True
            return client_form(request, data=data)


@login_required
@ValidateRole(['Branch Admin'])
def define_minimum(request):
    data = {
        'title': _('Define Minimum Money for ATM'),
        'fields': [
            {'id': 'amount', 'label': _('Amount'), 'value': '0', 'type': 'text'},
            {'id': 'atm_id', 'label': _('ATM Id'), 'value': '0', 'type': 'text'},
        ]
    }

    if request.method == 'GET':
        return client_form(request, data=data)
    if request.method == 'POST':
        try:
            amount = int(request.POST['amount'])
            atm_id = int(request.POST['atm_id'])

            if amount <= 0:
                data['error'] = True
                data['message'] = _('amount should be greater that 0')
                return client_form(request, data=data)

            if not ATM.objects.filter(id=atm_id).exists():
                data['error'] = True
                data['message'] = _('There is no atm with id {}').format(atm_id)
                return client_form(request, data=data)

            atm = ATM.objects.get(id=atm_id)
            if atm.branch != request.user.profile.branchadmin.branch:
                data['error'] = True
                data['message'] = _('Your branch is different with atm branch')
                return client_form(request, data=data)

            atm.minimum = amount
            atm.save()

            data['success'] = True
            data['message'] = _('Minimum amount for atm with id {} is updated to {}'
                                ).format(atm_id, amount)
            return client_form(request, data=data)
        except:
            data['error'] = True
            return client_form(request, data=data)


@login_required
@ValidateRole(['ATM Master'])
def assign_money(request):
    data = {
        'title': _('Assign Money to ATM'),
        'fields': [
            {'id': 'atm_id', 'label': _('ATM Id'), 'value': '0', 'type': 'text'},
            {'id': 'amount', 'label': _('Amount'), 'value': '0', 'type': 'text'},
            {'id': 'count', 'label': _('Count'), 'value': '0', 'type': 'text'},
        ]
    }

    if request.method == 'GET':
        return client_form(request, data=data)
    if request.method == 'POST':
        try:
            amount = int(request.POST['amount'])
            atm_id = int(request.POST['atm_id'])
            count = int(request.POST['count'])

            if not Money.objects.filter(amount=amount).exists():
                data['error'] = True
                data['message'] = _('There is no money with amount {}').format(amount)
                return client_form(request, data=data)

            if not ATM.objects.filter(id=atm_id).exists():
                data['error'] = True
                data['message'] = _('There is no atm with id {}').format(atm_id)
                return client_form(request, data=data)

            atm = ATM.objects.get(id=atm_id)
            money = Money.objects.get(amount=amount)

            if atm.branch != request.user.profile.employee.branch:
                data['error'] = True
                data['message'] = _('Your branch is different with atm branch')
                return client_form(request, data=data)

            atm_money = ATMMoney.objects.get(atm=atm, money=money)
            atm_money.count += count
            atm_money.save()

            AddMoney.objects.create(atm=atm, employee=request.user.profile.employee, amount=amount, count=count)

            data['success'] = True
            data['message'] = _('Total {} money with amount {} is assigned to atm with id {}'
                                ).format(count, amount, atm_id)
            return client_form(request, data=data)
        except:
            data['error'] = True
            return client_form(request, data=data)


@login_required
@ValidateRole(['Cashier'])
def create_card(request):
    data = {
        'title': _('Create card for account'),
        'fields': [
            {'id': 'account', 'label': _('Account Number'), 'value': '0', 'type': 'text'},
        ]
    }

    if request.method == 'GET':
        return client_form(request, data=data)
    if request.method == 'POST':
        try:
            account_number = request.POST['account']

            if not Account.objects.filter(account_number=account_number).exists():
                data['error'] = True
                data['message'] = _('There is no account with number {}').format(account_number)
                return client_form(request, data=data)

            account = Account.objects.get(account_number=account_number)
            if account.state == 'D':
                data['error'] = True
                data['message'] = _('Account with number {} is disabled').format(account_number)
                return client_form(request, data=data)

            card_number = random.randrange(int(1e15), int(1e16))
            pin = random.randrange(int(1e3), int(1e4))

            card = Card.objects.create(card_number=str(card_number), account=account, pin=str(pin))

            data['success'] = True
            data['message'] = _('A card created for account number {} with card number {} and pin {}'
                                ).format(account_number, card.card_number, card.pin)
            return client_form(request, data=data)
        except:
            data['error'] = True
            return client_form(request, data=data)


def atm_transaction(request):
    data = {
        'title': _('ATM Transaction'),
        'fields': [
            {'id': 'atm_id', 'label': _('ATM Id'), 'value': '0', 'type': 'text'},
            {'id': 'card_number', 'label': _('Card Number'), 'value': '', 'type': 'text'},
            {'id': 'pin', 'label': _('PIN'), 'value': '', 'type': 'text'},
            {'id': 'amount', 'label': _('Amount'), 'value': '0', 'type': 'text'},
            {'id': 'destination', 'label': _('Destination Account'), 'value': '', 'type': 'text'},
        ]
    }

    if request.method == 'GET':
        return client_form(request, data=data)
    if request.method == 'POST':
        try:
            atm_id = request.POST['atm_id']
            card_number = request.POST['card_number']
            pin = request.POST['pin']
            destination_account_number = request.POST['destination']

            try:
                amount = int(request.POST['amount'])
                if amount <= 0:
                    data['error'] = True
                    data['message'] = _('Amount should be greater than 0')
                    return client_form(request, data=data)
            except ValueError:
                data['error'] = True
                data['message'] = _('Please enter a valid amount')
                return client_form(request, data=data)

            if destination_account_number and not Account.objects.filter(account_number=destination_account_number).exists():
                data['error'] = True
                data['message'] = _('There is no account with number {}').format(destination_account_number)
                return client_form(request, data=data)

            if not ATM.objects.filter(id=atm_id).exists():
                data['error'] = True
                data['message'] = _('There is no atm with id {}').format(atm_id)
                return client_form(request, data=data)

            if not Card.objects.filter(pin=pin, card_number=card_number).exists():
                data['error'] = True
                data['message'] = _('Invalid card or pin')
                return client_form(request, data=data)

            account = Card.objects.get(card_number=card_number, pin=pin).account
            if account.state == 'D':
                data['error'] = True
                data['message'] = _('Account with number {} is disabled').format(account.account_number)
                return client_form(request, data=data)

            if destination_account_number:
                destination_account = Account.objects.get(account_number=destination_account_number)
                if destination_account.state == 'D':
                    data['error'] = True
                    data['message'] = _('Account with number {} is disabled').format(destination_account_number)
                    return client_form(request, data=data)

                transaction_commission = Bank.objects.all()[0].transfer_commission

                if amount + transaction_commission > account.credit:
                    data['error'] = True
                    data['message'] = _('Your account has not enough credit')
                    return client_form(request, data=data)

                transaction = Transaction(source_account=account, destination_account=destination_account,
                                          amount=amount, type='T', method='A')
                transaction.save()

                transaction.destination_account.credit += transaction.amount
                transaction.source_account.credit -= transaction.amount + transaction_commission

                transaction.source_account.save()
                transaction.destination_account.save()

                if transaction.type == 'T':
                    bank_account = Account.objects.get(account_number=1)
                    Transaction.objects.create(amount=transaction_commission, destination_account=bank_account,
                                               method='A',
                                               type='D', source_account=account)
                    bank_account.credit += transaction_commission
                    bank_account.save()
            else:
                if account.credit < amount:
                    data['error'] = True
                    data['message'] = _('Your account has not enough credit')
                    return client_form(request, data=data)

                atm = ATM.objects.get(id=atm_id)
                can_satisfy, solution = atm.satisfy(amount)
                if not can_satisfy:
                    data['error'] = True
                    data['message'] = _('Atm with id {} can not give you {} money').format(atm_id, amount)
                    return client_form(request, data=data)

                transaction = Transaction(source_account=account, amount=amount, type='W', method='A')
                transaction.save()

                transaction.source_account.credit -= amount
                transaction.source_account.save()

                for money, count in solution:
                    atm_money = ATMMoney.objects.get(money__amount=money, atm__id=atm_id)
                    atm_money.count -= count
                    atm_money.save()

                atm_total_money = 0
                for atm_money in ATMMoney.objects.filter(atm__id=atm_id):
                    atm_total_money += atm_money.money.amount * atm_money.count
                if atm_total_money < atm.minimum:
                    try:
                        atm_master = Employee.objects.filter(branch=atm.branch, type='T')[0]
                        sendMail(title='Ibank atm less than minimum',
                                 message='Atm with id %s has less money than expected minimum amount' % atm.id,
                                 to=atm_master.profile.user.email)
                    except:
                        print 'We dont have atm master for branch %s!!!' % atm.branch.id

            data['success'] = True
            return client_form(request, data=data)
        except:
            data['error'] = True
            return client_form(request, data=data)
