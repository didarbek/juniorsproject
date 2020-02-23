from django.shortcuts import render,get_object_or_404,redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from communities.models import Community
from posts.models import Post

# Create your views here.

def search(request,community_slug=None):
    if 'query' in request.GET:
        q = request.GET.get('query',None)
        if not community_slug:
            posts_list = Post.search_posts(q)
            bv = False
            community = False
        else:
            community = get_object_or_404(Community,slug=community_slug)
            posts_list = Post.search_posts(q,community)
            bv = True
        paginator = Paginator(posts_list,15)
        page = request.GET.get('page')
        if paginator.num_pages > 1:
            p = True
        else:
            p = False
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        p_obj = posts
        return render(request,'search/search_results.html',{
            'page':page,
            'posts':posts,
            'p':p,
            'bv':bv,
            'community':community,
            'q':q,
            'p_obj':p_obj
        })
    else:
        return redirect('home')
        