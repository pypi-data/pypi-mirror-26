from __future__ import unicode_literals, print_function
from unittest import TestCase
from authlib.client import OAuthClient
from authlib.client.apps import (
    twitter_fetch_user,
    dropbox_fetch_user,
    github_fetch_user,
)
from ..client_base import mock_json_response


class OAuthAppsTest(TestCase):

    def test_twitter_fetch_user(self):
        client = OAuthClient(
            'a', 'b',
            request_token_url='https://i.b',
            api_base_url='https://twitter.com/api'
        )
        client.set_token({'oauth_token': 'a', 'oauth_token_secret': 'b'})
        client.session.send = mock_json_response({
            'id': 1,
            'screen_name': 'lepture',
            'name': 'Hsiaoming',
            'email': 'a@b.c'
        })
        user = twitter_fetch_user(client)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.username, 'lepture')

    def test_dropbox_fetch_user(self):
        client = OAuthClient(
            'a', 'b',
            api_base_url='https://dropbox.com/api'
        )
        client.set_token({'access_token': 'a', 'token_type': 'bearer'})
        client.session.send = mock_json_response({
            'account_id': 1,
            'name': {'display_name': 'Hsiaoming'},
            'email': 'a@b.c'
        })
        user = dropbox_fetch_user(client)
        self.assertEqual(user.id, 1)
        self.assertIsNone(user.username)

    def test_github_fetch_user(self):
        client = OAuthClient(
            'a', 'b',
            api_base_url='https://github.com/api'
        )
        client.set_token({'access_token': 'a', 'token_type': 'bearer'})
        client.session.send = mock_json_response({
            'id': 1,
            'login': 'lepture',
            'name': 'Hsiaoming',
            'email': 'a@b.c'
        })
        user = github_fetch_user(client)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.username, 'lepture')
