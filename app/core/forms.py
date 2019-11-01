from django import forms


class ContactForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    content = forms.CharField(widget=forms.Textarea)

    def clean_email(self, *args, **kwargs):
        self.cleaned_data.get("first_name")
        self.cleaned_data.get("last_name")
        self.cleaned_data.get("email")
        self.cleaned_data.get("content")
