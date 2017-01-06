from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.decorators import login_required

from bank.models import Bank, Branch
from client.views import client_form, client_listh
from handlers import ValidateRole
from modir.models import BranchAdmin


@login_required
@ValidateRole(['Bank Admin'])
def define_annual_profit(request):
    data = {
        'title': _('Define annual profit'),
        'fields': [
            {'id': 'annual_profit', 'label': _('Annual profit'), 'value': Bank.objects.all()[0].annual_profit,
             'type': 'text'},
        ]
    }

    if request.method == 'GET':
        return client_form(request, data)
    if request.method == 'POST':
        try:
            annual_profit = request.POST['annual_profit']
            bank = Bank.objects.all()[0]

            bank.annual_profit = annual_profit
            bank.save()

            data['success'] = True
            data['fields'][0]['value'] = bank.annual_profit

            return client_form(request, data)
        except:
            data['error'] = True
            return client_form(request, data)


@login_required
@ValidateRole(['Bank Admin'])
def create_branch(request):
    data = {
        'title': _('Create branch'),
        'fields': [
            {'id': 'address', 'label': _('Address'), 'value': '', 'type': 'text'},
        ]
    }

    if request.method == 'GET':
        return client_form(request, data=data)
    if request.method == 'POST':
        try:
            address = request.POST['address']

            branch = Branch.objects.create(address=address)

            data['success'] = True
            data['message'] = _('A branch created with id {}').format(branch.id)
            return client_form(request, data=data)
        except:
            data['error'] = True
            return client_form(request, data=data)


@login_required
@ValidateRole(['Bank Admin'])
def assign_admin(request):
    data = {
        'title': _('Assign Admin'),
        'columns': [_('Id'), _('Address'), _('Current Admin'), _('Action')],
        'entities': []
    }

    if request.method == 'GET':
        for branch in Branch.objects.all():
            try:
                current_admin = '%s %s' % (branch.admin.profile.user.first_name, branch.admin.profile.user.last_name)
            except:
                current_admin = ''
            data['entities'].append([{'label': branch.id}, {'label': branch.address}, {'label': current_admin},
                                     {'label': _('Edit'), 'href': '/bank/assign_admin/%s' % branch.id}])
        return client_listh(request, data=data)


@login_required
@ValidateRole(['Bank Admin'])
def assign_admin_branch(request, branch_id):
    data = {
        'title': _('Assign Admin to Branch {}').format(branch_id),
        'columns': [_('Id'), _('Name')],
        'entities': []
    }

    if request.method == 'GET':
        try:
            if not Branch.objects.filter(id=branch_id).exists():
                return client_listh(request, data)
            branch = Branch.objects.get(id=branch_id)

            for branch_admin in BranchAdmin.objects.all():
                data['entities'].append([{'label': branch_admin.profile.national_id},
                                         {'label': '%s %s' % (branch_admin.profile.user.first_name,
                                                              branch_admin.profile.user.last_name)},
                                         {'label': _('Assign'),
                                          'href': '/bank/assign_admin/%s/%s'
                                                  % (branch.id, branch_admin.profile.national_id)}])
            return client_listh(request, data=data)
        except:
            return client_listh(request, data=data)


@login_required
@ValidateRole(['Bank Admin'])
def assign_admin_branch_national(request, branch_id, national_id):
    data = {
        'title': _('Assign Admin'),
        'fields': []
    }

    if request.method == 'GET':
        if not Branch.objects.filter(id=branch_id).exists():
            data['error'] = True
            data['message'] = _('No branch with id {}').format(branch_id)
            return client_form(request, data)
        branch = Branch.objects.get(id=branch_id)

        if not BranchAdmin.objects.filter(profile__national_id=national_id).exists():
            data['error'] = True
            data['message'] = _('No branch admin with {} national id').format(national_id)
            return client_form(request, data=data)

        admin = BranchAdmin.objects.get(profile__national_id=national_id)

        branch.admin = admin
        branch.save()

        data['success'] = True
        data['message'] = _('branch {} admin updated to {} {}').format(branch_id, admin.profile.user.first_name,
                                                                       admin.profile.user.last_name)
        return client_form(request, data)
    if request.method == 'POST':
        return HttpResponseRedirect('/bank/assign_admin')
