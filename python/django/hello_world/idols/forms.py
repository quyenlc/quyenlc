# -*- coding: utf-8 -*-
from django import forms
class IdolSearchForm(forms.Form):
    name = forms.CharField(label='Họ tên', max_length=150, required=False, widget=forms.TextInput(attrs={"placeholder": "Họ tên", 'class': 'form-control',}))
    year_of_birth = forms.IntegerField(label='Năm sinh', max_value=2017, min_value=1900, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'type':'number', 'min':1900, 'max':2017, }))