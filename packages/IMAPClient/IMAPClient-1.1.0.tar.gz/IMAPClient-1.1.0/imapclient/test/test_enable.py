# Copyright (c) 2017, Menno Smits
# Released subject to the New BSD License
# Please see http://en.wikipedia.org/wiki/BSD_licenses

from __future__ import unicode_literals

from mock import Mock

from imapclient import IMAPClient
from .imapclient_test import IMAPClientTest


class TestEnable(IMAPClientTest):

    def setUp(self):
        super(TestEnable, self).setUp()
        self.command = Mock()
        self.client._raw_command_untagged = self.command
        self.client._imap.state = 'AUTH'

    def test_success(self):
        self.command.return_value = b'CONDSTORE'

        resp = self.client.enable('CONDSTORE')

        self.command.assert_called_once_with(
            b'ENABLE', [b'CONDSTORE'],
            uid=False, response_name='ENABLED', unpack=True)
        self.assertEqual(resp, [b'CONDSTORE'])

    def test_failed1(self):
        # When server returns an empty ENABLED response
        self.command.return_value = b''

        resp = self.client.enable('FOO')

        self.command.assert_called_once_with(
            b'ENABLE', [b'FOO'],
            uid=False, response_name='ENABLED', unpack=True)
        self.assertEqual(resp, [])

    def test_failed2(self):
        # When server returns no ENABLED response
        self.command.return_value = None

        resp = self.client.enable('FOO')

        self.command.assert_called_once_with(
            b'ENABLE', [b'FOO'],
            uid=False, response_name='ENABLED', unpack=True)
        self.assertEqual(resp, [])

    def test_multiple(self):
        self.command.return_value = b'FOO BAR'

        resp = self.client.enable('FOO', 'BAR')

        self.command.assert_called_once_with(
            b'ENABLE', [b'FOO', b'BAR'],
            uid=False, response_name='ENABLED', unpack=True)
        self.assertEqual(resp, [b'FOO', b'BAR'])

    def test_wrong_state(self):
        self.client._imap.state = 'SELECTED'

        self.assertRaises(
            IMAPClient.Error,
            self.client.enable,
            'FOO',
        )
