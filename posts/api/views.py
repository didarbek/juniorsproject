from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView,)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from posts.models import Post
from .pagination import PostPageNumberPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer

class PostListCreateAPIView(ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PostPageNumberPagination
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['title']

    def get_queryset(self,*args,**kwargs):
        queryset_list = Post.get_posts()
        user_query = self.request.GET.get('user','')
        group_query = self.request.GET.get('group','')
        trending_posts = self.request.GET.get('trending','')
        if user_query:
            queryset_list = queryset_list.filter(author__username__icontains=user_query)
        if group_query:
            queryset_list = queryset_list.filter(group__slug__icontains=group_query)
        if trending_subjects == "True":
            queryset_list = queryset_list.order_by('-rank_score')
        return queryset_list

    def perform_create(self,serializer):
        serializer.save(author=self.request.user)

class PostRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,IsAuthorOrReadOnly]
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def perform_update(self,serializer):
        serializer.save(author=self.request.user)

class StarPostView(APIView):
    def get(self,request,format=None):
        data = dict()
        post_slug = request.GET.get('post_slug')
        post = Post.objects.get(slug=post_slug)
        user = request.user
        if post in user.liked_posts.all():
            post.points.remove(user)
            data['is_starred'] = False
        else:
            post.points.add(user)
            data['is_starred'] = True
        data['total_points'] = post.points.count()
        return Response(data)

class ActiveThreadsList(APIView):
    def get(self, request, format=None):
        current_user = request.user
        active_threads = current_user.posted_posts.all()[:5]
        active_threads_list = [
            {'title': thread.title,
             'slug': thread.slug,
             'group_slug': thread.group.slug} for thread in active_threads
        ]
        return Response(active_threads_list)
        