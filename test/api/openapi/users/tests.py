import datetime
import random

from django.test import Client, TestCase
from faker import Faker
from faker.providers import internet, person, address

from users.models import User, Address

client = Client()

fake = Faker()
fake.add_provider(address)
fake.add_provider(internet)
fake.add_provider(person)


class UsersTest(TestCase):
    count = 5

    def setUp(self):
        for i in range(self.count):
            User.objects.create(
                first_name=fake.first_name(),
                middle_name=fake.last_name(),
                last_name=fake.last_name(),
                date_of_birth=datetime.date.today(),
                email=fake.unique.safe_email(),
                phone=random.randint(1000000000, 9999999999),
                address=Address.objects.create(
                    number=random.randint(1, 9999),
                    street=fake.street_name(),
                    city=fake.city(),
                    state=fake.state_abbr(),
                    zip=fake.zipcode()
                )
            )

        fake.unique.clear()

    def test_create_user(self):
        first_name = fake.first_name()
        middle_name = fake.last_name()
        last_name = fake.last_name()
        date_of_birth = datetime.date.today()
        email = fake.email()
        phone = random.randint(1000000000, 9999999999)

        address_number = random.randint(1, 9999)
        address_street = fake.street_name()
        address_city = fake.city()
        address_state = fake.state_abbr()
        address_zip = fake.zipcode()

        user_data = {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'date_of_birth': str(date_of_birth),
            'email': email,
            'phone': phone,
            'address': {
                'number': address_number,
                'street': address_street,
                'city': address_city,
                'state': address_state,
                'zip': address_zip
            }
        }

        response_body = client.post('/users', user_data, content_type='application/json').json()

        self.assertTrue(response_body.pop('id'))

        response_address = response_body['address']
        self.assertTrue(response_address.pop('id'))
        response_body['address'] = response_address

        self.assertEqual(user_data, response_body)

    def test_get_all_users(self):
        response = client.get('/users')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json(), list))
        self.assertEqual(len(response.json()), self.count)
        self.assertTrue(response.json()[0].get('id', None))

    def test_get_user_by_id(self):
        random_id = random.randint(1, self.count)
        response = client.get(f'/users/{random_id}')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json(), dict))
        self.assertEqual(response.json().get('id', None), random_id)
