'''
python3 manage.py test nomad.tests   # Run the specified module
python3 manage.py test nomad.tests.test_models  # Run the specified module
python3 manage.py test nomad.tests.test_models.YourTestClass # Run the specified class
python3 manage.py test nomad.tests.test_models.YourTestClass.test_one_plus_one_equals_two  # Run the specified method
'''

from django.test import TestCase

from ..models import Manager, Department

# Create your tests here.


MANAGER_ID = 1


class ManagerModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Department.objects.create(name='Гусятник', short_name='ГУС')
        Manager.objects.create(first_name='Александр', last_name='Ильин', department=Department.objects.get(id=1))

    def test_first_name_label(self):
        manager = Manager.objects.get(id=MANAGER_ID)
        field_label = manager._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'Имя')

    def test_department_label(self):
        manager = Manager.objects.get(id=MANAGER_ID)
        field_label = manager._meta.get_field('department').verbose_name
        self.assertEquals(field_label, 'Отдел')

    def test_first_name_max_length(self):
        manager = Manager.objects.get(id=MANAGER_ID)
        max_length = manager._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 50)

    def test_last_name_max_length(self):
        manager = Manager.objects.get(id=MANAGER_ID)
        max_length = manager._meta.get_field('last_name').max_length
        self.assertEquals(max_length, 50)

    def test_object_name_is_last_name_comma_first_name(self):
        manager = Manager.objects.get(id=MANAGER_ID)
        expected_object_name = " ".join(
            (manager.first_name, manager.middle_name, manager.last_name, f"({manager.status})"))
        self.assertEquals(expected_object_name, str(manager))

    def test_get_absolute_url(self):
        manager = Manager.objects.get(id=MANAGER_ID)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(manager.get_absolute_url(), '/emaillist/manager/' + str(MANAGER_ID))
