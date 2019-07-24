from django.test import TestCase
from django.urls import reverse
from restaurants.models import Restaurant
from restaurants.forms import RestaurantForm

class RestaurantModelTestCase(TestCase):
    def test_create(self):
        Restaurant.objects.create(
            name="Hamza's Pizza",
            description="Pizza that tastes really good.",
            opening_time="00:01:00",
            closing_time="23:59:00"
            )

class RestaurantViewTestCase(TestCase):
    def setUp(self):
        self.data = {
            "name": "Hamza's Pizza",
            "description": "Pizza that tastes really good.",
            "opening_time": "00:01:00",
            "closing_time":"23:59:00"
        }
        self.restaurant_1 = Restaurant.objects.create(name="Restaurant 1", description="This is Restaurant 1", opening_time="00:01:00", closing_time="23:59:00")
        self.restaurant_2 = Restaurant.objects.create(name="Restaurant 2", description="This is Restaurant 2", opening_time="00:01:00", closing_time="23:59:00")
        self.restaurant_3 = Restaurant.objects.create(name="Restaurant 3", description="This is Restaurant 3", opening_time="00:01:00", closing_time="23:59:00")

    def test_welcome_view(self):
        url = reverse("hello-world")
        response = self.client.get(url)
        self.assertIn("Hello World!", response.context['msg'])
        self.assertContains(response, "Hello World!")
        self.assertEqual(response.status_code, 200)

    def test_list_view(self):
        list_url = reverse("restaurant-list")
        response = self.client.get(list_url)
        for restaurant in Restaurant.objects.all():
            self.assertIn(restaurant, response.context['restaurants'])
            self.assertContains(response, restaurant.name)
            self.assertContains(response, restaurant.description)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(response.status_code, 200)

    def test_detail_view(self):
        detail_url = reverse("restaurant-detail", kwargs={"restaurant_id":self.restaurant_1.id})
        response = self.client.get(detail_url)
        self.assertEqual(self.restaurant_1, response.context['restaurant'])
        self.assertContains(response, self.restaurant_1.name)
        self.assertContains(response, self.restaurant_1.description)
        self.assertTemplateUsed(response, 'detail.html')
        self.assertEqual(response.status_code, 200)

    def test_create_view(self):
        create_url = reverse("restaurant-create")
        response = self.client.get(create_url)
        self.assertEqual(response.status_code, 200)
        response2 = self.client.post(create_url, self.data)
        self.assertEqual(response2.status_code, 302)


class RestaurantFormTestCase(TestCase):
    def test_valid_form(self):
        name = "Some random restaurant"
        description = "Some random description"
        opening_time = "12:15"
        closing_time = "10:15"
        data = {
            'name':name,
            'description': description,
            'opening_time': opening_time,
            'closing_time': closing_time
        }
        form = RestaurantForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get('name'), name)
        self.assertEqual(form.cleaned_data.get('description'), description)

    def test_invalid_form(self):
        name = "Some restaurant"
        description = "Some random description"
        data = {
            'name':name,
            'description': description,
        }
        form = RestaurantForm(data=data)
        self.assertFalse(form.is_valid())
