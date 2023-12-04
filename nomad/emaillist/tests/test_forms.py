from django.test import TestCase

# Создайте ваши тесты здесь

import random
import string

from ..forms import RenewManagerForm


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


class RenewManagerFormTest(TestCase):
    str_temp = ''

    def setUp(self):
        self.str_temp = randomword(10)
        # print(self.str_temp)

    def test_renew_form_first_name_field_label(self):
        form = RenewManagerForm()
        self.assertTrue(form.fields['first_name'].label == 'Имя')

    def test_renew_form_first_name_field_help_text(self):
        form = RenewManagerForm()
        self.assertEqual(form.fields['first_name'].help_text, 'Только криллица')

    def test_renew_form_first_name_long(self):
        form_data = {'first_name': self.str_temp*6, 'last_name': 'Алекс', 'middle_name': 'Петрович'}
        form = RenewManagerForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_renew_form_first_name_latin_symbols(self):
        form_data = {'first_name': self.str_temp, 'last_name': 'Алекс', 'middle_name': 'Петрович'}
        form = RenewManagerForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_renew_form_true_data(self):
        form_data = {'first_name': 'Алекс', 'last_name': 'Алекс', 'middle_name': 'Петрович'}
        form = RenewManagerForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_renew_form_last_name_latin_symbols(self):
        form_data = {'first_name': 'Алекс', 'last_name': self.str_temp, 'middle_name': 'Петрович'}
        form = RenewManagerForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_renew_form_middle_name_latin_symbols(self):
        form_data = {'first_name': 'Алекс', 'last_name': 'Иванов', 'middle_name': self.str_temp}
        form = RenewManagerForm(data=form_data)
        self.assertFalse(form.is_valid())
