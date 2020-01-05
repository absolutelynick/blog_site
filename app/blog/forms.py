from django import forms

from .models import Comment, BlogPost


class PostForm(forms.ModelForm):
    title = forms.CharField(
        max_length=BlogPost._meta.get_field("title").max_length,
        widget=forms.Textarea(
            attrs={
                "name": "title",
                "rows": 1,
                "type": "text",
                "class": "form-control",
                "id": "validationTooltip01",
                "placeholder": "Title",
                "required": True,
            }
        ),
        help_text="Please make a title for this post",
    )

    content = forms.CharField(
        max_length=200,
        widget=forms.Textarea(
            attrs={
                "name": "content",
                "class": "form-control",
                "id": "exampleFormControlTextarea1",
                "placeholder": "Content",
                "rows": 3,
                "required": True,
            }
        ),
        help_text="Write your post content here",
    )

    class Meta:
        model = BlogPost
        fields = ("title", "content")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("comment", "comment_by")
