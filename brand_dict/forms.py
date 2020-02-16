from django import forms
from django.forms.models import inlineformset_factory
from brands.models import BrandsDict, BrandDictSup


class BrandForm(forms.ModelForm):
    class Meta:
        model = BrandsDict
        fields = ['brand']


class BrandFormSetFactory(forms.ModelForm):

    class Meta:
        model = BrandDictSup
        exclude = ()


# Uploading csv file brnds angara list

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50, label='Название', required=False)
    file = forms.FileField(label='Файл')
