from django import forms


class ParentNodeForm(forms.Form):
    name = forms.CharField(widget=forms.widgets.Input(attrs={'placeholder': 'новое слово'}), label='текст нового слова')
