from django import forms


class PromptFillForm(forms.Form):
    business_name = forms.CharField(required=False)
    business_type = forms.CharField(required=False)
    business_location = forms.CharField(required=False)
    target_audience = forms.CharField(required=False)
