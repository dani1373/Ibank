from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.decorators import login_required

from client.views import client_form
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
