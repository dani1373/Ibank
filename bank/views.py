import json
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from bank.models import Bank, Branch
from client.views import client_form
from handlers import ValidateRole
from modir.models import BranchAdmin


@login_required
@ValidateRole(['Bank Admin'])
def define_annual_profit(request):
    data = {
        'title': _('Define annual profit'),
        'fields': [
            {'id': 'annual_profit', 'label': _('Profit'), 'value': Bank.objects.all()[0].annual_profit, 'type': 'text'},
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
    if request.method == 'GET':
        return HttpResponse('client view')
    if request.method == 'POST':
        address = request.POST['annual_profit']

        branch = Branch.create(address=address)

        return HttpResponse('A branch created with id %s' % branch.id)


@login_required
@ValidateRole(['Bank Admin'])
def create_branch(request):
    if request.method == 'GET':
        return HttpResponse('client view')
    if request.method == 'POST':
        address = request.POST['annual_profit']

        branch = Branch.create(address=address)

        return HttpResponse('A branch created with id %s' % branch.id)


@login_required
@ValidateRole(['Bank Admin'])
def assign_admin(request):
    if request.method == 'GET':
        branches = Branch.objects.all()
        result = []
        for branch in branches:
            result.append({
                'id': branch.id,
                'address': branch.address,
            })
        return HttpResponse(json.loads(result))
    if request.method == 'POST':
        branch_id = request.POST['id']
        national_id = request.POST['nationa_id']

        if not BranchAdmin.objects.filter(profile__national_id=national_id).exists():
            return HttpResponse('No branch admin with %s national id' % national_id)
        if not Branch.objects.filter(id=branch_id).exists():
            return HttpResponse('No branch with id %s' % branch_id)

        branch = Branch.objects.get(id=branch_id)
        admin = BranchAdmin.objects.get(profile__national_id=national_id)

        branch.admin = admin
        branch.save()

        return HttpResponse('branch %s admin updated to %s %s' % (branch_id, admin.profile.user.first_name,
                                                                  admin.profile.user.last_name))
