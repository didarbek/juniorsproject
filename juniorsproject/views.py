from django.shortcuts import render
from users.models import CustomUser
from groups.models import Group

def error_400(request,exception):
        data = {}
        return render(request,'400.html', data)

def error_403(request,exception):
        data = {}
        return render(request,'403.html', data)

def error_404(request,exception):
        data = {}
        return render(request,'404.html', data)

def error_500(request,exception):
        data = {}
        return render(request,'500.html', data)
