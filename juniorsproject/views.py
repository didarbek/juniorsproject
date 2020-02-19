from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def groups(request):
    return render(request,'groups.html')

def group_detail(request):
    return render(request,'group_page.html')

def post(request):
    return render(request, 'create_post.html')