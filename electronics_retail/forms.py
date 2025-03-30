from django import forms
from .models import ElectronicsRetail


class ElectronicsRetailForm(forms.ModelForm):
    """Форма в админ-панели, исключающая поле уровня иерархии, при создании"""
    class Meta:
        model = ElectronicsRetail
        exclude = ('_level_retail',)
