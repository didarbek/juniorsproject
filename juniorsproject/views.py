from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def groups(request):
    return render(request,'groups.html')