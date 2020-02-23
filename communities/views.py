from django.shortcuts import render,get_object_or_404,redirect
from .models import Community
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.utils.decorators import method_decorator
import requests
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required
from utils import check_image_extension
from .decorators import user_is_community_admin, user_is_not_banned_from_community
from .forms import CommunityForm
from django.conf import settings
# Create your views here.
User = settings.AUTH_USER_MODEL
class CommunitiesPageView(ListView):
    model = Community
    queryset = Community.objects.all()
    pagiante_by = 20
    template_name = 'communities/communities_list.html'
    context_object_name = 'communities'

class CommunityPageView(ListView):
    model = Post
    paginate_by = 20
    template_name = 'communities/community_detail.html'
    context_object_name = 'posts'

    def get_queryset(self,**kwargs):
        self.community = get_object_or_404(Community,slug=self.kwargs['community'])
        return self.community.submitted_subjects.filter(active=True)

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['bv'] = True
        context['admins'] = self.community.admins.all()
        context['community'] = self.community
        return context

class UserSubscriptionListPage(LoginRequiredMixin,ListView):
    model = Community
    paginate_by = 10
    template_name = 'communities/user_subscription_list.html'
    context_object_name = 'subscriptions'

    def get_quryset(self,**kwargs):
        user = get_object_or_404(User,username=self.request.user)
        return user.subscribed_boards.all()

@login_required
@user_is_not_banned_from_community
def subscribe(request,community):
    community = get_object_or_404(Community,slug=community)
    user = request.user
    if community in user.subscribed_communities.all():
        community.subscribers.remove(user)
    else:
        community.subscribers.add(user)
    return HttpResponse(community.subscribers.count())

class UserCreatedCommunitiesPageView(LoginRequiredMixin,ListView):
    model = Community
    paginate_by = 20
    template_name = 'communities/user_created_communities.html'
    context_object_name = 'user_communities'

    def get_queryset(self,**kwargs):
        user = get_object_or_404(User,username=self.request.user)
        return user.inspected_communities.all()

@login_required
def new_community(request):
    community_form = CommunityForm()
    if request.method == 'POST':
        community_form = CommunityForm(request.POST,request.FILES)
        if community_form.is_valid():
            new_community = community_form.save()
            new_community.admins.add(request.user)
            new_community.subscribers.add(request.user)
            return redirect(new_community.get_absolute_url())
    form_filling = True
    return render(request,'communities/new_community.html',{
        'community_form':community_form,'form_filling':form_filling
    })

@login_required
@user_is_community_admin
def edit_community_cover(request,community):
    community = get_object_or_404(Community,slug=community)
    if request.method == 'POST':
        community_cover = request.FILES.get('cover')
        if check_image_extension(community_cover.name):
            community.cover = community_cover
            community.save()
            return redirect('community',community=community.slug)
        else:
            return HttpResponse('Filetype not supported.Supported filetypes are .jpg .png etc.')
    else:
        form_filling = True
        return render(request,'communities/edit_community_cover.html',{
            'community':community,'form_filling':form_filling
        })

@login_required
@user_is_community_admin
def banned_users(request,community):
    community = get_object_or_404(Community,slug=community)
    users = community.bannned_users.all()
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
    bv = True

    return render(request,'communities/banned_users.html',{
        'community':community,
        'bv':bv,
        'page':page,
        'p_obj':p_obj,
        'p':p,
        'users':users
    })

@login_required
@user_is_community_admin
def ban_user(request,community,user_id):
    community = get_object_or_404(Community,slug=community)
    user = get_object_or_404(User,id=user_id)
    if community in user.subscribed_communities.all():
        community.subscribers.remove(user)
        community.bannned_users.add(user)
        return redirect('banned_users',community=community.slug)
    else:
        community.banned_users.remove(user)
        return redirect('banned_users',community=community.slug)
        