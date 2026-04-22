from django import forms

class GenreForm(forms.Form):
    name = forms.CharField(max_length=512)
    slug = forms.CharField(max_length=512, required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)
    parent_id = forms.CharField(max_length=64, required=False)
    color = forms.CharField(max_length=32, required=False)
    icon = forms.CharField(max_length=128, required=False)