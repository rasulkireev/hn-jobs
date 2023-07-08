from django import forms
from django.forms import Form, ModelForm

from users.models import Subscriber


class SupportForm(Form):
    # user = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, current_user=None, *args, **kwargs):
        self.current_user = current_user
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["current_user"] = self.current_user
        return cleaned_data


class CreateAlertForm(ModelForm):
    class Meta:
        model = Subscriber
        fields = [
            "email",
            "technology_selected",
        ]


class UpdateAlertForm(ModelForm):
    class Meta:
        model = Subscriber
        fields = ["confirmed"]
