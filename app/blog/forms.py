from django import forms

from .models import BlogPost


class BlogPostForm(forms.Form):
    title = forms.CharField(
        max_length=40,
        widget=forms.Textarea(
            attrs={
                "name": "title",
                "type": "text",
                "class": "form-control",
                "id": "validationTooltip01",
                "placeholder": "Title",
                "required": True,
            }
        ),
        help_text="Please make a title for this post",
    )
    slug = forms.SlugField(
        max_length=50,
        widget=forms.Textarea(
            attrs={
                "name": "slug",
                "type": "text",
                "class": "form-control",
                "id": "validationTooltip01",
                "placeholder": "Slug",
                "required": True,
            }
        ),
        help_text="Please make a path for this post",
    )
    content = forms.CharField(
        max_length=200,
        widget=forms.Textarea(
            attrs={
                "name": "content",
                "class": "form-control",
                "id": "exampleFormControlTextarea1",
                "placeholder": "Content",
                "rows": "3",
                "required": True,
            }
        ),
        help_text="Write your post content here",
    )

    def clean(self):
        cleaned_data = super(BlogPostForm, self).clean()
        title = cleaned_data.get("name")
        slug = cleaned_data.get("slug")
        content = cleaned_data.get("content")
        if not title and not slug and not content:
            raise forms.ValidationError("Please correct the issues!")


class BlogPostModelForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title", "slug", "content"]
