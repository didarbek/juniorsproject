<<<<<<< HEAD
from django import forms
from groups.models import Group
from .models import Post

class PostForm(forms.ModelForm):
    def get_subscribed_groups(self):
        return self.user.subscribed_groups

    title = forms.CharField(help_text="You can mention other members in your post i.e <b>u/username</b>")
    body = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    group = forms.ModelChoiceField(queryset=Group.objects.all())

    def __init__(self,*args,**kwargs):
        user = kwargs.pop('user', None)
        super(PostForm, self).__init__(*args, **kwargs)
        if user is not None:
            subscribed_groups = user.subscribed_groups.all()
            self.fields['group'].queryset = subscribed_groups
            if not subscribed_groups:
                self.fields['group'].help_text = "You need to <b>subscribe</b> a group to post in it."

    class Meta:
        model = Post
        fields = ('title','body','image','group')
        