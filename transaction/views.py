from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _

from client.views import client_form
from customer.models import Account
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
                if amount > source_account.credit:
                    data['error'] = True
                    data['message'] = _('Your account has not enough credit')
                    return client_form(request, data=data)

                source_account.credit -= amount
                source_account.save()

            transaction_type = 'T'
            if not source_account_number:
                transaction_type = 'D'
            if not destination_account_number:
                transaction_type = 'W'

            transaction = Transaction(source_account=source_account, destination_account=destination_account,
                                      amount=amount, type=transaction_type, method='H')
            transaction.save()
            data['success'] = True
            return client_form(request, data=data)
        except:
            data['error'] = True
            return client_form(request, data=data)
