from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Group
from posts.models import Post
from .decorators import user_is_group_admin,user_is_not_banned_from_group
from django.http import HttpResponse
from .forms import GroupForm
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from users.models import CustomUser
from django.contrib.auth import get_user_model

# Create your views here.

User = settings.AUTH_USER_MODEL
 
class GroupsPage(ListView):
    model = Group
    queryset = Group.objects.all()
    paginate_by = 15
    template_name = 'groups/all_groups.html'
    context_object_name = 'groups'

class GroupPage(ListView):
    model = Post
    paginate_by = 20
    template_name = 'groups/group.html'
    context_object_name = 'posts'

    def get_queryset(self,**kwargs):
        self.group = get_object_or_404(Group,slug=self.kwargs['group'])
        return self.group.submitted_posts.filter(active=True)
    
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['admins'] = self.group.admins.all()
        context['group'] = self.group
        return context
    
class UserSubscriptionList(LoginRequiredMixin,ListView):
    model = Group
    paginate_by = 10
    template_name = 'groups/user_subscription_list.html'
    context_object_name = 'subscriptions'

    def get_queryset(self,**kwargs):
        user = get_object_or_404(User,username=self.request.user)
        return user.subscribed_groups.all()

@login_required
@user_is_not_banned_from_group
def subscribe(request,group):
    group = get_object_or_404(Group,slug=group)
    user = request.user
    if group in user.subscribed_groups.all():
        group.subscribers.remove(user)
    else:
        group.subscribers.add(user)
    return HttpResponse(group.subscribers.count())

class UserCreatedGroupsPage(LoginRequiredMixin,ListView):
    model = Group
    paginate_by = 20
    template_name = 'groups/user_created_groups.html'
    context_object_name = 'user_groups'

    def get_queryset(self,**kwargs):
        user = get_object_or_404(User,username=self.request.user)
        return user.inspected_groups.all()

@login_required
def create_group(request):
    group_form = GroupForm()
    if request.method == 'POST':
        group_form = GroupForm(request.POST,request.FILES)
        if group_form.is_valid():
            new_group = group_form.save()
            new_group.admins.add(request.user)
            new_group.subscribers.add(request.user)
            return redirect(new_group.get_absolute_url())
    else:
        group_form = GroupForm()
    return render(request,'groups/create_group.html',{'group_form':group_form})

@login_required
@user_is_group_admin
def edit_group_cover(request,group):
    group = get_object_or_404(Group,slug=group)
    if request.method == 'POST':
        group_cover = request.FILES.get('cover')
        if check_image_extension(group_cover.name):
            group.cover = group_cover
            group.save()
            return redirect('group',group=group.slug)
        else:
            return HttpResponse('Filetype not supported. Supported filetypes are .jpg, .png etc.')
    else:
        return render(request,'groups/edit_group_cover.html',{'group':group})

@login_required
@user_is_group_admin
def banned_users(request,group):
    group = get_object_or_404(Group,slug=group)
    users = group.banned_users.all()
    paginator = Paginator(users,20)
    page = request.GET.get('page')
    if paginator.num_pages > 1:
        p = True
    else:
        p = False
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    p_obj = users
    return render(request,'groups/banned_users.html',{'group':group,'page':page,'p_obj':p_obj,'p':p,'users':users})

@login_required
@user_is_group_admin
def ban_user(request,group,user_id):
    group = get_object_or_404(Group,slug=group)
    user = get_object_or_404(User,id=user_id)
    if group in user.subscribed_groups.all():
        group.subscribers.remove(user)
        group.banned_users.add(user)
    else:
        group.banned_users.remove(user)
        return redirect('banned_users',group=group.slug)
        