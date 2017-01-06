from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.decorators import login_required

from client.views import client_form
from customer.models import Account
from handlers import ValidateRole
from service.models import BillType


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
                data['message'] = _('There is no account with account number %s' % account_number)
                return client_form(request, data=data)

            account = Account.objects.get(account_number=account_number)
            if account.state not in 'A':
                data['error'] = True
                data['message'] = _('Account %s is not active' % account_number)
                return client_form(request, data=data)

            bill_type = BillType.objects.create(destination_account=account, name=name)
            data['success'] = True
            data['message'] = _('Bill %s created with id %s and account number %s' % (name, bill_type.id, account_number))
            return client_form(request, data=data)
        except:
            data['error'] = True
            return client_form(request, data=data)
