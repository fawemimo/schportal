from django import forms


class CsvImportAdminForm(forms.Form):
    uploads = forms.FileField()
