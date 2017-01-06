from django.contrib import auth
from django.http import HttpResponse

from client.views import client_login
from employee.views import employee_home_page
from modir.views import branch_admin_home_page, bank_admin_home_page


def home_page(user):
    try:
        if hasattr(user.profile, 'bankadmin'):
            return bank_admin_home_page(user)
        elif hasattr(user.profile, 'branchadmin'):
            return branch_admin_home_page(user)
        elif hasattr(user.profile, 'employee'):
            return employee_home_page(user)
        else:
            return HttpResponse(':|')
    except:
        return HttpResponse('what do you want?')


def login(request):
    if request.method == 'GET':
        return client_login(request)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return home_page(user)
        else:
            return HttpResponse('failed')
