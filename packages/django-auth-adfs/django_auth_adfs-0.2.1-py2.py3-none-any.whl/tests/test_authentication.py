from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied
from django.test import TestCase
from httmock import with_httmock, urlmatch
from mock import patch

from django_auth_adfs.backend import AdfsBackend
from .utils import get_base_claims, encode_jwt


@urlmatch(path=r"^/adfs/oauth2/token$")
def token_response(url, request):
    claims = get_base_claims()
    token = encode_jwt(claims)
    return {'status_code': 200, 'content': b'{"access_token":"' + token + b'"}'}


class AuthenticationTests(TestCase):
    def setUp(self):
        Group.objects.create(name='group1')
        Group.objects.create(name='group2')
        Group.objects.create(name='group3')

    @with_httmock(token_response)
    def test_with_auth_code(self):
        backend = AdfsBackend()
        user = backend.authenticate(authorization_code="dummycode")
        self.assertIsInstance(user, User)
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertEqual(len(user.groups.all()), 2)
        self.assertEqual(user.groups.all()[0].name, "group1")
        self.assertEqual(user.groups.all()[1].name, "group2")

    @with_httmock(token_response)
    def test_empty(self):
        backend = AdfsBackend()
        self.assertIsNone(backend.authenticate())

    @with_httmock(token_response)
    def test_group_claim(self):
        backend = AdfsBackend()
        with patch("django_auth_adfs.backend.settings.GROUP_CLAIM", "nonexisting"):
            user = backend.authenticate(authorization_code="dummycode")
            self.assertIsInstance(user, User)
            self.assertEqual(user.first_name, "John")
            self.assertEqual(user.last_name, "Doe")
            self.assertEqual(user.email, "john.doe@example.com")
            self.assertEqual(len(user.groups.all()), 0)

    @with_httmock(token_response)
    def test_empty_keys(self):
        backend = AdfsBackend()
        with patch("django_auth_adfs.backend.AdfsBackend._public_keys", []):
            self.assertRaises(PermissionDenied, backend.authenticate, authorization_code='testcode')

    @with_httmock(token_response)
    def test_group_removal(self):
        user, created = User.objects.get_or_create(**{
            User.USERNAME_FIELD: "testuser"
        })
        group = Group.objects.get(name="group3")
        user.groups.add(group)
        user.save()

        self.assertEqual(user.groups.all()[0].name, "group3")

        backend = AdfsBackend()

        user = backend.authenticate(authorization_code="dummycode")
        self.assertIsInstance(user, User)
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertEqual(len(user.groups.all()), 2)
        self.assertEqual(user.groups.all()[0].name, "group1")
        self.assertEqual(user.groups.all()[1].name, "group2")
