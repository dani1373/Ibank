from django.shortcuts import render


def client_login(request, error=False):
    return render(request, 'login.html', {'error': error})


def client_index(request, role, usecases):
    return render(request, 'index.html', {'role': role, 'usecases': usecases})


def client_listh(request, data=None):
    if data is None:
        data = {
            'title': 'Branches',
            'columns': ['Name', 'Age', 'Action'],
            'entities': [
                [{'label': 'Hamed'}, {'label': '13'}, {'label': 'Edit', 'href': 'https://google.com'}],
                [{'label': 'Hamed'}, {'label': '13'}, {'label': 'Edit', 'href': 'https://google.com'}],
                [{'label': 'Hamed'}, {'label': '13'}, {'label': 'Edit', 'href': 'https://google.com'}],
                [{'label': 'Hamed'}, {'label': '13'}, {'label': 'Edit', 'href': 'https://google.com'}],
            ]
        }
    return render(request, 'list.html', data)


def client_form(request, data=None):
    if data is None:
        data = {
            'title': 'Edit User',
            'fields': [
                {'id': 'name', 'label': 'Name', 'value': 'Hamed', 'type': 'text'},
                {'id': 'name', 'label': 'Name', 'value': 'Hamed', 'type': 'text'},
                {'id': 'name', 'label': 'Name', 'value': 'Hamed', 'type': 'text'},
            ]
        }
    return render(request, 'form.html', data)
