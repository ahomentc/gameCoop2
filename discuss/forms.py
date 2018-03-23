from django import forms
from .models import Post,Reply

# form for creating a new post
class newPost(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content','discussionType')

    CHOICES=[('General','General'),('Idea','Idea'),('Voting','Voting')]

    title = forms.CharField(label='Title', max_length=100)
    content = forms.Textarea()
    discussionType = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(),required=False)

# form for textbox for a reply on the above post
class newMainReply(forms.ModelForm):

    class Meta:
        model = Reply
        fields = ('content',)

    content = forms.CharField(widget=forms.Textarea, label='',required=False)
