from django.shortcuts import render


def index(request):
    return render(request, 'webex_admin/index.html')
