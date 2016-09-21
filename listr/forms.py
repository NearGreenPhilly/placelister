__author__ = 'kdenny'

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from listr.models import UserProfile, List

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class ListForm(forms.ModelForm):

    LIST_TYPE_CHOICES = (
    ('food', 'Restaurants'),
    ('drink', 'Bars'),
    ('music', 'Music Venues'),
    ('retail', 'Shopping'),
    ('poi', 'Points of Interest'),
    )

    type = forms.TypedChoiceField(choices=LIST_TYPE_CHOICES,
                                      widget=forms.Select)

    class Meta:
        model = List
        fields = ('name', 'location')
        exclude = ["created_by"]