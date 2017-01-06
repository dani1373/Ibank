from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.decorators import login_required

from client.views import client_form
from handlers import ValidateRole
from modir.models import BranchAdmin
from profile.models import Profile


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
        ]
    }

    if request.method == 'GET':
        return client_form(request, data=data)
    if request.method == 'POST':
        profile = Profile.register(request.POST)

        if not profile:
            data['error'] = True
            return client_form(request, data=data)

        if BranchAdmin.objects.filter(profile=profile).exists():
            data['error'] = True
            data['message'] = _('We have same admin branch with id %s and password %s' % (profile.national_id,
                                                                                          profile.password))
            return client_form(request, data=data)

        branch_admin = BranchAdmin.objects.create(profile=profile)
        data['success'] = True
        data['message'] = _('profile with national id %s and password %s is upgraded to branch admin profile'
                            % (branch_admin.profile.national_id, branch_admin.profile.password))
        return client_form(request, data=data)
