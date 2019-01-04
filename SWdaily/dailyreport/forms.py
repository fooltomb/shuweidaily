from django import forms
from django.contrib.admin import widgets

class WriteReportForm(forms.Form):
    pub_date=forms.DateField(required=True,label="日期",widget=widgets.AdminDateWidget())


