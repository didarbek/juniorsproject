from django import forms
from .models import Group

class GroupForm(forms.ModelForm):
    title = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    description = forms.CharField(label='',widget=forms.Textarea(attrs={'rows': 5,'placeholder':'Text'}))
    cover = forms.ImageField(label='Add Group Cover (optional)',widget=forms.FileInput(),help_text="Image dimensions should be <b>900 &#10005; 300</b>",required=False)
    class Meta:
        model = Group
        fields = ('title', 'description', 'cover')
        
class GroupCoverForm(forms.ModelForm):
    cover = forms.ImageField(widget=forms.FileInput(),help_text="Image dimensions should be <b>1200x250</b>",required=False)
    class Meta:
        model = Group
        fields = ('cover',)
        