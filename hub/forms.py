from .choices import PROTOCOL_CHOICES


class SomeForm(forms.Form):
    protocol = forms.ChoiceField(choices=PROTOCOL_CHOICES, label='', initial='', widget=forms.Select(), required=True)
