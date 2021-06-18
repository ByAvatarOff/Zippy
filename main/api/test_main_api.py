import io

from PIL import Image
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from main.models import Profile


class ProfileAPITestCase(APITestCase):
    """
    Tests of main app
    """

    def setUp(self):
        User.objects.create_user("TestUser", "TestUser@mail.ru", "TestUserPassword")
        token_url = reverse('accounts:login')
        data = {'username': 'TestUser', 'password': 'TestUserPassword'}
        response = self.client.post(token_url, data, format='json')
        self.token = response.data['token']

    def test_profile_is_created(self):
        profile = Profile.objects.all().count()
        self.assertEqual(profile, 1)

    def test_profiles_list_allow(self):
        user = User.objects.get(username='TestUser')
        url = reverse('profiles')
        self.client.force_authenticate(user=user)
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

    # def test_is_add_like(self):
    #     user = User.objects.get(username='TestUser')
    #     profile = Profile.objects.create()
    #     url = reverse('add_like')
    #     data = {'profile': 'TestUSer', 'like': True}
    #     self.client.force_authenticate(user=user)
    #     post_response = self.client.post(url, data, format='json')
    #     self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def test_add_content(self):
        user = User.objects.get(username='TestUser')
        url = reverse('add_content')
        self.client.force_authenticate(user=user)
        photo_file = self.generate_photo_file()
        data = {"image": photo_file, "description": "Test"}
        post_response = self.client.post(url, data)
        print(post_response)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

    # def test_update_is_confirm(self):
    #     user = User.objects.get(username='TestUser')
    #     url = reverse('update')
    #     self.client.force_authenticate(user=user)
    #     data = {
    #         'image': 'http://127.0.0.1:8000/media/image/Font_xVK6cYS.jpg',
    #         'phone': '111111111',
    #         'name': 'Vlad',
    #         'surname': 'Tes',
    #         'group': 'base',
    #         'geo_location': 'SRID=4326;POINT (53.901 27.5707)',
    #     }
    #     response = self.client.put(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
