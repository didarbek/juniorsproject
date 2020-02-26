from django import forms
# from communities.models import Community
from .models import Post

class PostForm(forms.ModelForm):
    def get_subscribed_communities(self):
        return self.user.subscribed_communities

    title = forms.CharField(help_text="You can mention other members in your post i.e <b>u/username</b>")
    body = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    # board = forms.ModelChoiceField(queryset=Community.objects.all())

    def __init__(self,*args,**kwargs):
        user = kwargs.pop('user', None)
        super(PostForm, self).__init__(*args, **kwargs)
        if user is not None:
            subscribed_communities = user.subscribed_communities.all()
            self.fields['community'].queryset = subscribed_communities
            if not subscribed_communities:
                self.fields['community'].help_text = "You need to <b>subscribe</b> a community to post in it."

    class Meta:
        model = Post
        fields = ('title','body','image','community')
        