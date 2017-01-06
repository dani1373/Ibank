"""ibank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include


urlpatterns = [
    url(r'^bank/', include('bank.urls', namespace='bank')),
    url(r'^profile/', include('profile.urls', namespace='profile')),
    url(r'^customer/', include('customer.urls', namespace='customer')),
    # url(r'^atm/', include('atm.urls', namespace='atm')),
    url(r'^employee/', include('employee.urls', namespace='employee')),
    url(r'^modir/', include('modir.urls', namespace='modir')),
    url(r'^service/', include('service.urls', namespace='service')),
    # url(r'^transaction/', include('transaction.urls', namespace='transaction')),
]
