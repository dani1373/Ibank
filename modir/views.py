from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from handlers import ValidateRole
from modir.models import BranchAdmin
from profile.models import Profile


def branch_admin_home_page(user):
    return HttpResponse('branch admin home')


def bank_admin_home_page(user):
    return HttpResponse('bank admin home')


@login_required
@ValidateRole(['Bank Admin'])
def register_branch_admin(request):
    if request.method == 'GET':
        return HttpResponse('client page')
    if request.method == 'POST':
        profile = Profile.register(request.POST)

        if BranchAdmin.objects.filter(profile=profile).exists():
            return HttpResponse('Previously upgraded')

        branch_admin = BranchAdmin.objects.create(profile=profile)
        return HttpResponse('profile with national id %s is upgraded to branch admin profile'
                            % branch_admin.profile.national_id)
