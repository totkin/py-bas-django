from django import forms

from django.forms import ModelForm

from .models import Manager, Subscription


def match(text):
    alphabet = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    return not alphabet.isdisjoint(text.lower())


class RenewManagerForm(ModelForm):
    first_name = forms.RegexField(label='Имя', regex=r'^[а-яА-ЯёЁ]+$',
                                  help_text='Только криллица',
                                  error_messages={'invalid': "Только символы русского алфавита."})
    middle_name = forms.RegexField(label='Отчество', regex=r'^[а-яА-ЯёЁ]+$',
                                   help_text='Только криллица',
                                   error_messages={'invalid': "Только символы русского алфавита."})
    last_name = forms.RegexField(label='Фамилия', regex=r'^[а-яА-ЯёЁ]+$',
                                 help_text='Только криллица',
                                 error_messages={'invalid': "Только символы русского алфавита."})


    class Meta:
        model = Manager

        fields = ['first_name',
                  'middle_name',
                  'last_name',
                  'subscriptions',
                  ]


class SubscriptionCreateForm(ModelForm):

    class Meta:
        model = Subscription

        fields = ['name',
                  'status',
                  'frequency',
                  'created_by',
                  ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['created_by'].disabled = True
