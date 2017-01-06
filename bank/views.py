import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from bank.models import Bank, Branch
from handlers import ValidateRole
from modir.models import BranchAdmin


@login_required
@ValidateRole(['Bank Admin'])
def define_annual_profit(request):
    if request.method == 'GET':
        return HttpResponse('client view')
    if request.method == 'POST':
        annual_profit = request.POST['annual_profit']
        bank = Bank.objects.all()[0]

        bank.annual_profit = annual_profit
        bank.save()

        return HttpResponse('Successfully updated to %s percent profit per year' % bank.annual_profit)


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
