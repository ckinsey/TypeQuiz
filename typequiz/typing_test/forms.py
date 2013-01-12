from django import forms

class TypingTestForm(forms.Form):
    user_test_text = forms.CharField(widget=forms.widgets.Textarea())