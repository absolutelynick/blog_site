from django import forms


class Contact_Form(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={"placeholder": "Let us know what you are thinking", "rows": "4"}
        ),
    )
