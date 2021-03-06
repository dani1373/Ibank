from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.decorators import login_required

from client.views import client_form, client_listh
from handlers import ValidateRole
from modir.models import BranchAdmin
from profile.models import Profile
from service.models import Loan


@login_required
@ValidateRole(['Bank Admin'])
def register_branch_admin(request):
    data = {
        'title': _('Register branch admin'),
        'fields': [
            {'id': 'first_name', 'label': _('first name'), 'value': '', 'type': 'text'},
            {'id': 'last_name', 'label': _('last name'), 'value': '', 'type': 'text'},
            {'id': 'national_id', 'label': _('national id'), 'value': '', 'type': 'text'},
            {'id': 'phone_number', 'label': _('phone number'), 'value': '', 'type': 'text'},
            {'id': 'address', 'label': _('address'), 'value': '', 'type': 'text'},
            {'id': 'email', 'label': _('email'), 'value': '', 'type': 'text'},
        ]
    }

    if request.method == 'GET':
        return client_form(request, data=data)
    if request.method == 'POST':
        try:
            profile = Profile.register(request.POST)

            if BranchAdmin.objects.filter(profile=profile).exists():
                data['error'] = True
                data['message'] = _('We have same admin branch with id {} and password {}').format(profile.national_id,
                                                                                                   profile.password)
                return client_form(request, data=data)

            branch_admin = BranchAdmin.objects.create(profile=profile)
            data['success'] = True
            data['message'] = _('profile with national id {} and password {} is upgraded to branch admin profile'
                                ).format(branch_admin.profile.national_id, branch_admin.profile.password)
            return client_form(request, data=data)
        except:
            data['error'] = True
            return client_form(request, data=data)


@login_required
@ValidateRole(['Bank Admin', 'Branch Admin'])
def loan_report(request):
    data = {
        'title': _('Loan Report'),
        'columns': [_('Account'), _('Loan Amount'), _('Benfit Amount')],
        'entities': []
    }

    if request.method == 'GET':
        for loan in Loan.objects.all():
            data['entities'].append([{'label': loan.account.account_number},
                                     {'label': loan.amount},
                                     {'label': loan.periodicorder_set.all()[0].amount - loan.amount}])
        return client_listh(request, data=data)
