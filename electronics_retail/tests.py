from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from electronics_retail.models import ElectronicsRetail, Product


class ElectronicsRetailViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user=self.user)

        self.product1 = Product.objects.create(name='Product 1', model="model 1", date_release="2022-08-15")
        self.product2 = Product.objects.create(name='Product 2', model="model 2", date_release="2020-07-20")

        self.electronics_retail = ElectronicsRetail.objects.create(
            level_name_retail='Завод',
            name='test',
            email="test@mail.ru",
            country="testcountry",
            city="testcity",
            street="teststreet",
            house_number=1,
            debt=50000
        )
        self.electronics_retail.products.set([self.product1, self.product2])

    def test_list_electronics_retail(self):
        """Тестируем получение списка объектов"""
        response = self.client.get(reverse('electronics_retail:retails-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['country'], 'testcountry')

    def test_create_electronics_retail(self):
        """Тестируем создание нового объекта"""
        data = {
            'level_name_retail': 'Розничная сеть',
            'name': "test_name_2",
            'email': "test_email@mail.com",
            'country': 'Canada',
            'city': 'test-city_2',
            'street': 'test_street_2',
            'house_number': '2',
            'debt': '10000'
        }
        response = self.client.post(reverse('electronics_retail:retails-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ElectronicsRetail.objects.count(), 2)

    def test_update_electronics_retail(self):
        """Тестируем обновление объекта"""
        url = reverse('electronics_retail:retails-detail', args=[self.electronics_retail.pk])
        data = {'country': 'Mexico'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.electronics_retail.refresh_from_db()
        self.assertEqual(self.electronics_retail.country, 'Mexico')

    def test_update_electronics_retail_with_debt(self):
        """Тестируем обновление объекта с полем debt"""
        url = reverse('electronics_retail:retails-detail', args=[self.electronics_retail.pk])
        data = {'country': 'Mexico', 'debt': 100}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_electronics_retail(self):
        """Тестируем удаление объекта"""
        url = reverse('electronics_retail:retails-detail', args=[self.electronics_retail.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ElectronicsRetail.objects.count(), 0)

    def test_search_electronics_retail(self):
        """Тестируем поиск объектов"""
        response = self.client.get(reverse('electronics_retail:retails-list'), {'search': 'testcountry'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
