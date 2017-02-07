from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.decorators import login_required

from client.views import client_form, client_listh
from employee.models import Employee
from handlers import ValidateRole
from profile.models import Profile


@login_required
@ValidateRole(['Branch Admin'])
def register_employee(request):
    data = {
        'title': _('Define Employee'),
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

            branch_admin = request.user.profile.branchadmin
            if not hasattr(branch_admin, 'branch'):
                data['error'] = True
                data['message'] = _('You are not assigned to any branch')
                return client_form(request, data=data)

            if Employee.objects.filter(profile=profile).exists():
                data['error'] = True
                data['message'] = _('This employee has been created previously')
                return client_form(request, data=data)

            employee = Employee.objects.create(profile=profile, branch=branch_admin.branch)

            data['success'] = True
            data['message'] = _('employee with national id {} and password {} is created for branch with id {}'
                                ).format(employee.profile.national_id, employee.profile.password,
                                         branch_admin.branch.id)
            return client_form(request, data=data)
        except:
            data['error'] = True
            return client_form(request, data=data)


@login_required
@ValidateRole(['Branch Admin'])
def assign_role(request):
    data = {
        'title': _('Assign Role'),
        'columns': [_('Id'), _('Role')],
        'entities': []
    }

    if request.method == 'GET':
        for employee in Employee.objects.all():
            if employee.branch.admin == request.user.profile.branchadmin:
                current_role = _(employee.get_type_display())
                data['entities'].append([{'label': employee.profile.national_id}, {'label': current_role},
                                         {'label': _('Edit'), 'href': '/employee/assign_role/%s'
                                                                      % employee.profile.national_id}])
        return client_listh(request, data=data)


@login_required
@ValidateRole(['Branch Admin'])
def assign_role_employee(request, national_id):
    data = {
        'title': _('Assign Role to Employee {}').format(national_id),
        'columns': [_('Role')],
        'entities': []
    }

    translated_roles = [_('Lawyer'), _('Cashier'), _('Auditor'), _('ATM Master')]
    roles = ['Lawyer', 'Cashier', 'Auditor', 'ATM_Master']
    if request.method == 'GET':
        for id, role in enumerate(roles):
            data['entities'].append([{'label': translated_roles[id]}, {'label': _('Assign'),
                                                                       'href': '/employee/assign_role/%s/%s'
                                                                               % (national_id, role)}])
        return client_listh(request, data=data)


@login_required
@ValidateRole(['Branch Admin'])
def assign_role_employee_national(request, national_id, role):
    data = {
        'title': _('Assign Role'),
        'fields': []
    }

    if request.method == 'GET':
        roles = ['Lawyer', 'Cashier', 'Auditor', 'ATM_Master']
        types = {
            'Lawyer': 'L',
            'Cashier': 'C',
            'Auditor': 'A',
            'ATM_Master': 'T',
        }

        if role not in roles:
            data['error'] = True
            data['message'] = _('Invalid role')
            return client_form(request, data)

        if not Employee.objects.filter(profile__national_id=national_id).exists():
            data['error'] = True
            data['message'] = _('No employee with {} national id').format(national_id)
            return client_form(request, data=data)

        employee = Employee.objects.get(profile__national_id=national_id)
        employee.type = types[role]
        employee.save()

        data['success'] = True
        data['message'] = _('role updated for employee with national id {} ').format(national_id)
        return client_form(request, data)
    if request.method == 'POST':
        return HttpResponseRedirect('/employee/assign_role')
