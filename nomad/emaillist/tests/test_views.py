from django.test import TestCase

# Create your tests here.

from ..models import Manager, Subscription
from django.urls import reverse

from django.contrib.auth.models import User  # Необходимо для представления User


class ManagerListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create 13 managers for pagination tests
        number_of_managers = 13
        for manager_num in range(number_of_managers):
            Manager.objects.create(first_name='Иван' + 'я' * manager_num, last_name='Петров' + 'я' * manager_num, )

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/emaillist/managers/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('managers'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('managers'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'emaillist/manager_list.html')

    def test_pagination_is_10(self):
        resp = self.client.get(reverse('managers'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['manager_list']) == 10)

    def test_lists_all_managers(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        resp = self.client.get(reverse('managers') + '?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['manager_list']) == 3)


class ByUserListViewTest(TestCase):

    def setUp(self):
        # Создание двух пользователей
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user1.save()
        test_user2 = User.objects.create_user(username='testuser2', password='12345')
        test_user2.save()

        # Создание рассылок
        test_subscription = Subscription.objects.create(name='Test', status='+', frequency='D', created_by=test_user1)
        test_subscription.save()

        number_of_subscriptions = 5
        for subscription_num in range(number_of_subscriptions):
            test_subscription = Subscription.objects.create(name='Test ' + str(subscription_num),
                                                            status='+', frequency='D', created_by=test_user2)
            test_subscription.save()

    def tearDown(self):
        Subscription.objects.all().delete()
        User.objects.filter(username='testuser1').delete()
        User.objects.filter(username='testuser2').delete()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('subscriptions'))
        self.assertRedirects(resp, '/accounts/login/?next=/emaillist/subscriptions/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('subscriptions'))

        # Проверка что пользователь залогинился
        self.assertEqual(str(resp.context['user']), 'testuser1')
        # Проверка ответа на запрос
        self.assertEqual(resp.status_code, 200)

        # Проверка того, что мы используем правильный шаблон
        self.assertTemplateUsed(resp, 'emaillist/subscription_list.html')

    def test_only_needed_subscription_in_list_testuser2(self):
        login = self.client.login(username='testuser2', password='12345')
        resp = self.client.get(reverse('subscriptions'))

        # Проверка, что пользователь залогинился
        self.assertEqual(str(resp.context['user']), 'testuser2')
        # Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)

        # Проверка, что изначально у нас нет рассылок в списке
        self.assertTrue('subscription_list' in resp.context)
        self.assertEqual(len(resp.context['subscription_list']), 5)

        # Подтверждение, что все рассылки принадлежат testuser1
        for subscriptionitem in resp.context['subscription_list']:
            self.assertEqual(resp.context['user'], subscriptionitem.created_by)
            self.assertEqual('+', subscriptionitem.status)

    def test_only_needed_subscription_in_list_testuser1(self):
        login = self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('subscriptions'))

        # Проверка, что пользователь залогинился
        self.assertEqual(str(resp.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)

        # Проверка, что изначально у нас нет рассылок в списке
        self.assertTrue('subscription_list' in resp.context)
        self.assertEqual(len(resp.context['subscription_list']), 1)

        # Подтверждение, что все рассылки принадлежат testuser1
        for subscriptionitem in resp.context['subscription_list']:
            self.assertEqual(resp.context['user'], subscriptionitem.created_by)
            self.assertEqual('+', subscriptionitem.status)

    def test_pages_ordered_by_id(self):

        login = self.client.login(username='testuser2', password='12345')
        resp = self.client.get(reverse('subscriptions'))

        # Пользователь залогинился
        self.assertEqual(str(resp.context['user']), 'testuser2')
        # Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)

        # Подтверждение, что из всего списка показывается только 5 экземпляров
        self.assertEqual(len(resp.context['subscription_list']), 5)

        # Подтверждение, что сортировка по id
        sub_test_id = 0
        for copy in resp.context['subscription_list']:
            if sub_test_id == 0:
                sub_test_id = copy.id
            else:
                self.assertTrue(sub_test_id <= copy.id)
