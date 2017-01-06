from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from bank.models import Branch
from employee.models import Employee
from handlers import ValidateRole
from profile.models import Profile


def employee_home_page(user):
    employee = user.profile.employee

    return HttpResponse(employee.get_type_display())


@login_required
@ValidateRole(['Branch Admin'])
def register_employee(request):
    if request.method == 'GET':
        return HttpResponse('client page')
    if request.method == 'POST':
        profile = Profile.register(request.POST)

        branch_admin = request.user.profile.branchadmin
        if not hasattr(branch_admin, 'branch'):
            return HttpResponse('You are not assigned to any branch')

        if Employee.objects.filter(profile=profile).exists():
            return HttpResponse('Previously created')

        employee = Employee.objects.create(profile=profile, branch=branch_admin.branch, type=request.POST['type'])

        return HttpResponse('employee with national id %s and type %s is created for branch with id %s'
                            % (employee.profile.national_id, employee.get_type_display(), branch_admin.branch.id))
