from django import forms


class PromptFillForm(forms.Form):
    business_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "e.g. The Potting Place"}),
    )
    business_type = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "e.g. Florist, Restaurant, Gym etc"}
        ),
    )
    business_location = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "e.g. Bristol BS1, Manchester, Shoreditch"}
        ),
    )
    target_audience = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "e.g. Families, young professionals, local foodies"}
        ),
    )
    additional_info = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "placeholder": "e.g. Award-winning yoga studio, Open Until 11pm, Limited parking",
                "rows": 2,
            }
        ),
    )
