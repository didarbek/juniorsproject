from django import forms
from .models import Community

class CommunityForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))
    cover = forms.ImageField(
        widget=forms.FileInput(),
        help_text="Image dimensions should be <b>900 &#10005; 300</b>.",
        required=False
    )

    class Meta:
        model = Community
        fields = ('title','description','cover')
        