from django import forms

class TypingTestForm(forms.Form):
    user_test_text = forms.CharField(label="Begin typing below", widget=forms.widgets.Textarea())