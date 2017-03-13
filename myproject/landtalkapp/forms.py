from django import forms

from .models import Submission

class SubmissionForm(forms.ModelForm):

    class Meta:
        model = Submission
        exclude = ('pub', 'privkey', 'time_submitted', 'time_posted',)