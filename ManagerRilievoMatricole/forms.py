from django import forms


class TemplateForm(forms.Form):

    file = forms.FileField()  # for creating file input


class RilievoForm(forms.Form):

    file = forms.FileField()  # for creating file input

class CronologiaForm(forms.Form):

    file = forms.FileField()  # for creating file input