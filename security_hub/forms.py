from django import forms
from security_hub.models import Worker


class AddWorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['name', 'surname', 'card']
