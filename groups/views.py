from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Group
from posts.models import Post
from .decorators import user_is_group_admin,user_is_not_banned_from_group
from django.http import HttpResponse
from .forms import GroupForm,GroupCoverForm
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from users.models import CustomUser
from django.contrib.auth import get_user_model
from users.models import CustomUser
from django.http import JsonResponse
from django.db.models import Q
from groups.models import GroupCategory

# Create your views here.

User = settings.AUTH_USER_MODEL

class GroupsPage(ListView):
    model = Group
    queryset = Group.objects.all()
    paginate_by = 15
    template_name = 'groups/all_groups.html'
    context_object_name = 'groups'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = GroupCategory.objects.all()
        return context

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
        context["bv"] = True
        context['admins'] = self.group.admins.all()
        context['group'] = self.group
        return context
    
class UserSubscriptionList(LoginRequiredMixin,ListView):
    model = Group
    paginate_by = 10
    template_name = 'groups/user_subscription_list.html'
    context_object_name = 'subscriptions'

    def get_queryset(self, **kwargs ):
        user = get_object_or_404(CustomUser,username=self.request.user.username)
        return user.subscribed_groups.all()

   



class UserSubscriptionListAjax(LoginRequiredMixin,ListView):
    model = Group
    paginate_by = 10
    template_name = 'sub_show_group.html'
    context_object_name = 'subscriptions_ajax'

    def get_context_data(self, **kwargs):          
        context = super().get_context_data(**kwargs)                     
        data =  get_object_or_404(CustomUser,username=self.request.user.username).subscribed_groups.all()
        context["data"] = data

        return  context



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
        user = get_object_or_404(CustomUser,username=self.request.user.username)
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
        group_form = GroupCoverForm(instance=group,data=request.POST,files=request.FILES)
        if group_form.is_valid():
            group_form.save()
            return redirect(group.get_absolute_url())
        else:
            group_form = GroupCoverForm()
    else:
        group_form = GroupCoverForm()
    return render(request,'groups/edit_group_cover.html',{'group_form':group_form})

@login_required
@user_is_group_admin
def banned_users(request,group):
    group = get_object_or_404(Group, slug=group)
    users = group.banned_users.all()
    paginator = Paginator(users, 20)
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
    bv = True
    return render(request, 'groups/banned_users.html', {
        'group':group,
        'bv':bv,
        'page':page,
        'p_obj':p_obj,
        'p':p,
        'users':users
    })

@login_required
@user_is_group_admin
def ban_user(request,group,user_id):
    group = get_object_or_404(Group,slug=group)
    user = get_object_or_404(CustomUser,id=user_id)
    if group in user.subscribed_groups.all():
        group.subscribers.remove(user)
        group.banned_users.add(user)
        return redirect('groups:banned_users',group=group.slug)
    else:
        group.banned_users.remove(user)
        return redirect('groups:banned_users',group=group.slug)

class GroupSearch(ListView):
    model = Group 
    template_name = 'groups/group_search_result.html'

    def get_queryset(self):
        query = self.request.GET.get('group_search')
        object_list = Group.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        return object_list

def list_of_group_by_category(request,category_slug):
    categories = GroupCategory.objects.all()
    group = Group.objects.all()
    if category_slug:
        category = get_object_or_404(GroupCategory,slug=category_slug)
        group = group.filter(category=category)
    template = 'groups/list_of_group_by_category.html'
    context = {'categories':categories,'group':group,'category':category}
    return render(request,template,context)
    